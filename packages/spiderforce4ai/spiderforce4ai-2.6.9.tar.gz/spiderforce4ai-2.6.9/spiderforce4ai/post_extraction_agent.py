# post_extraction_agent.py

from dataclasses import dataclass, asdict
from typing import Any, Callable, Dict, List, Optional, Union
import json
import asyncio
import time
from pathlib import Path
import aiofiles
from litellm import completion
from pydantic import BaseModel, Field
import logging
from datetime import datetime
import re
from rich.console import Console

console = Console()

logger = logging.getLogger(__name__)

class PostExtractionBuffer:
    """Buffer system for tracking and retrying failed LLM requests."""
    
    def __init__(self, buffer_file: Optional[Path] = None):
        # Generate a unique session ID using timestamp and random string
        session_id = f"{int(time.time())}_{hex(hash(str(time.time())))[-6:]}"
        
        # Create unique buffer file path
        if buffer_file:
            # If buffer_file is provided, insert session_id before the extension
            stem = buffer_file.stem
            suffix = buffer_file.suffix
            self.buffer_file = buffer_file.with_name(f"{stem}_{session_id}{suffix}")
        else:
            # Default buffer file with session_id
            self.buffer_file = Path(f"post_extraction_buffer_{session_id}.json")
            
        self.failed_requests: Dict[str, Dict] = {}
        self._load_buffer()
    
    def _load_buffer(self) -> None:
        """Load failed requests from buffer file if it exists."""
        if self.buffer_file.exists():
            try:
                with open(self.buffer_file, 'r') as f:
                    self.failed_requests = json.load(f)
            except Exception as e:
                logger.error(f"Error loading buffer file: {e}")
                self.failed_requests = {}

    def _save_buffer(self) -> None:
        """Save failed requests to buffer file."""
        try:
            with open(self.buffer_file, 'w') as f:
                json.dump(self.failed_requests, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving buffer file: {e}")

    def add_failed_request(self, url: str, content: str, error: str) -> None:
        """Add a failed request to the buffer."""
        self.failed_requests[url] = {
            "content": content,
            "error": error,
            "timestamp": datetime.now().isoformat(),
            "attempts": self.failed_requests.get(url, {}).get("attempts", 0) + 1
        }
        self._save_buffer()

    def remove_request(self, url: str) -> None:
        """Remove a request from the buffer after successful processing."""
        if url in self.failed_requests:
            del self.failed_requests[url]
            self._save_buffer()

    def get_failed_requests(self) -> Dict[str, Dict]:
        """Get all failed requests."""
        return self.failed_requests

    def get_retryable_requests(self, max_attempts: int = 3) -> Dict[str, Dict]:
        """Get failed requests that haven't exceeded max retry attempts."""
        return {
            url: data for url, data in self.failed_requests.items()
            if data.get("attempts", 0) < max_attempts
        }

class ExtractionTemplate(BaseModel):
    """Base model for extraction template validation."""
    template: Dict[str, Any] = Field(..., description="Template structure for extraction")
    
    class Config:
        extra = "allow"
        arbitrary_types_allowed = True

    @classmethod
    def validate_template_string(cls, template_str: str) -> bool:
        """Validate a template string against the schema."""
        try:
            template_json = json.loads(template_str)
            cls(template=template_json)
            return True
        except Exception as e:
            logger.error(f"Template validation failed: {e}")
            return False

@dataclass
class PostExtractionConfig:
    """Configuration for post-extraction processing."""
    model: str
    messages: List[Dict[str, str]]
    api_key: str
    max_tokens: int = 1000
    temperature: float = 0.7
    base_url: Optional[str] = None
    request_delay: float = 0.01  # 10 milliseconds default
    max_retries: int = 3
    retry_delay: float = 1.0
    combine_output: bool = False
    output_file: Optional[Path] = None
    custom_transform_function: Optional[Callable] = None
    buffer_file: Optional[Path] = None
    response_format: Optional[str] = None  # 'json' or 'text'

    def __post_init__(self):
        if self.output_file:
            self.output_file = Path(self.output_file)
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if self.buffer_file:
            self.buffer_file = Path(self.buffer_file)
            self.buffer_file.parent.mkdir(parents=True, exist_ok=True)

class RateLimiter:
    """Rate limiter for API calls."""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.interval = 60 / requests_per_minute
        self.last_request = 0
        self._lock = asyncio.Lock()

    async def acquire(self):
        """Acquire rate limit slot."""
        async with self._lock:
            now = time.time()
            if self.last_request:
                elapsed = now - self.last_request
                if elapsed < self.interval:
                    await asyncio.sleep(self.interval - elapsed)
            self.last_request = time.time()

class PostExtractionAgent:
    """Agent for processing extracted content using LLM models."""
    
    def __init__(self, config: PostExtractionConfig):
        self.config = config
        self.buffer = PostExtractionBuffer(config.buffer_file)
        self.results: Dict[str, Any] = {}
        self.rate_limiter = RateLimiter()
        # Convert string path to Path object if needed
        if isinstance(self.config.output_file, str):
            self.config.output_file = Path(self.config.output_file)
            # Ensure parent directory exists
            self.config.output_file.parent.mkdir(parents=True, exist_ok=True)
            # Create empty JSON file if it doesn't exist
            if not self.config.output_file.exists():
                with open(self.config.output_file, 'w') as f:
                    json.dump({}, f)
        self._setup_output()
        
    def _setup_output(self) -> None:
        """Setup output file if combining results."""
        if self.config.combine_output and self.config.output_file:
            # Ensure parent directory exists
            self.config.output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Load existing results if file exists
            if self.config.output_file.exists():
                try:
                    with open(self.config.output_file, 'r') as f:
                        self.results = json.load(f)
                except json.JSONDecodeError:
                    # If file is corrupted, backup and start fresh
                    backup_path = self.config.output_file.with_suffix(f".bak_{int(time.time())}")
                    self.config.output_file.rename(backup_path)
                    self.results = {}
            
            # Create file if it doesn't exist
            if not self.config.output_file.exists():
                self.config.output_file.touch()
                self.results = {}
            
            logger.info(f"Initialized output file at {self.config.output_file}")

    def _process_single_content(self, url: str, content: str) -> Optional[Dict]:
        """Process a single piece of content through the LLM."""
        try:
            # Replace placeholder in messages with actual content
            messages = [
                {**msg, 'content': msg['content'].replace('{here_markdown_content}', content)}
                for msg in self.config.messages
            ]
            
            # Make LLM request with retries
            max_retries = 3
            retry_delay = 1.0
            last_error = None
            
            for attempt in range(max_retries):
                try:
                    # Call completion synchronously
                    # Add response_format if specified
                    completion_args = {
                        "model": self.config.model,
                        "messages": messages,
                        "max_tokens": self.config.max_tokens,
                        "temperature": self.config.temperature,
                        "api_key": self.config.api_key,
                    }
                    if self.config.base_url:
                        completion_args["api_base"] = self.config.base_url
                    if self.config.response_format:
                        completion_args["response_format"] = {"type": self.config.response_format}
                    
                    response = completion(**completion_args)
                    raw_content = response.choices[0].message.content
                    logger.debug(f"Raw LLM response for {url}: {raw_content}")

                    # Handle response based on response_format
                    try:
                        if self.config.response_format == "json_object":
                            # For json_object format, response should already be valid JSON
                            extracted_data = raw_content if isinstance(raw_content, dict) else json.loads(raw_content)
                        else:
                            # For text format or unspecified, try parsing JSON or use as text
                            try:
                                extracted_data = json.loads(raw_content)
                            except json.JSONDecodeError:
                                # Look for JSON in markdown code blocks
                                json_match = re.search(r'```(?:json)?\s*\n([\s\S]*?)\n```', raw_content)
                                if json_match:
                                    json_content = json_match.group(1).strip()
                                    extracted_data = json.loads(json_content)
                                else:
                                    # If no JSON found and not json_object format, use raw content
                                    extracted_data = {
                                        "raw_content": raw_content,
                                        "format": "text",
                                        "timestamp": datetime.now().isoformat()
                                    }
                        
                        self.buffer.remove_request(url)  # Remove from buffer if successful
                        return extracted_data
                        
                    except Exception as e:
                        error_msg = (
                            f"Error processing LLM response for {url}:\n"
                            f"Error: {str(e)}\n"
                            f"Raw content: {raw_content[:500]}..."  # First 500 chars of response
                        )
                        logger.error(error_msg)
                        last_error = error_msg
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay * (attempt + 1))
                            
                except Exception as e:
                    error_msg = f"LLM processing error for {url}: {str(e)}"
                    logger.error(error_msg)
                    last_error = error_msg
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay * (attempt + 1))
            
            # If we get here, all retries failed
            raise Exception(last_error)
                
        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
            self.buffer.add_failed_request(url, content, str(e))
            return None

    def _save_result_sync(self, url: str, result: Dict) -> None:
        """Save results synchronously to combined output file."""
        try:
            if self.config.output_file:
                # Load existing results
                try:
                    with open(self.config.output_file, 'r', encoding='utf-8') as f:
                        current_results = json.load(f)
                        # Convert to list if it's a dict, or initialize new list
                        if isinstance(current_results, dict):
                            current_results = list(current_results.values())
                        elif not isinstance(current_results, list):
                            current_results = []
                except (json.JSONDecodeError, FileNotFoundError):
                    current_results = []

                # Add new result to list
                current_results.append(result)

                # Save atomically using temporary file
                temp_file = self.config.output_file.with_suffix('.tmp')
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(current_results, f, indent=2, ensure_ascii=False)

                # Atomic replace
                temp_file.replace(self.config.output_file)
                logger.info(f"Updated combined results file with {url}")

                # Cleanup backup files
                for backup_file in self.config.output_file.parent.glob(f"{self.config.output_file.stem}.bak_*"):
                    try:
                        backup_file.unlink()
                        logger.info(f"Cleaned up backup file: {backup_file}")
                    except Exception as e:
                        logger.warning(f"Failed to remove backup file {backup_file}: {e}")
        except Exception as e:
            logger.error(f"Error saving results for {url}: {str(e)}")

    async def _save_result(self, url: str, result: Dict) -> None:
        """Save individual or combined results."""
        try:
            if self.config.combine_output and self.config.output_file:
                self.results[url] = result
                async with aiofiles.open(self.config.output_file, 'w') as f:
                    await f.write(json.dumps(self.results, indent=2))
            elif not self.config.combine_output and self.config.output_file:
                individual_file = self.config.output_file.parent / f"{url.replace('/', '_')}.json"
                async with aiofiles.open(individual_file, 'w') as f:
                    await f.write(json.dumps(result, indent=2))
        except Exception as e:
            logger.error(f"Error saving results for {url}: {str(e)}")

    def process_content(self, url: str, content: str) -> Optional[Dict]:
        """Process content with retry mechanism."""
        logger.info(f"Starting content processing for {url}")
        
        for attempt in range(self.config.max_retries):
            logger.info(f"Processing attempt {attempt + 1}/{self.config.max_retries} for {url}")
            
            result = self._process_single_content(url, content)
            if result:
                logger.info(f"Successfully processed content for {url}")
                
                # Apply custom transformation if provided
                if self.config.custom_transform_function:
                    try:
                        # Add URL to result before transformation
                        result['url'] = url
                        
                        logger.info(f"Executing transformer function for {url}")
                        transformed_result = self.config.custom_transform_function(result)
                        logger.info(f"Successfully applied custom transformation for {url}")
                        
                        # Save the transformed result to combined output
                        if self.config.output_file:
                            self._save_result_sync(url, transformed_result)
                            logger.info(f"Saved transformed result to combined output for {url}")
                        
                        logger.info(f"Webhook response sent for {url}")
                        return transformed_result
                    except Exception as e:
                        error_msg = f"Warning: Issue in custom transform for {url}: {str(e)}"
                        logger.warning(error_msg)
                        console.print(f"[yellow]{error_msg}[/yellow]")
                        
                        # Save original result if transformation fails
                        if self.config.output_file:
                            self._save_result_sync(url, result)
                            logger.info(f"Saved original result to combined output for {url}")
                
                # Save result synchronously
                try:
                    # Always save the result, whether transformed or original
                    result_to_save = transformed_result if self.config.custom_transform_function else result
                    if self.config.output_file:
                        self._save_result_sync(url, result_to_save)
                        logger.info(f"Saved results for {url} to {self.config.output_file}")
                except Exception as e:
                    error_msg = f"Error saving results for {url}: {str(e)}"
                    logger.error(error_msg)
                    console.print(f"[red]{error_msg}[/red]")
                
                # Return the appropriate result
                return transformed_result if self.config.custom_transform_function else result
            
            # Wait before retry
            if attempt < self.config.max_retries - 1:
                logger.info(f"Attempt {attempt + 1} failed for {url}, waiting {self.config.retry_delay}s before retry")
                time.sleep(self.config.retry_delay)
        
        logger.error(f"All processing attempts failed for {url}")
        return None

    async def process_bulk_content(self, content_map: Dict[str, str]) -> Dict[str, Optional[Dict]]:
        """Process multiple pieces of content with rate limiting."""
        results = {}
        for url, content in content_map.items():
            results[url] = await self.process_content(url, content)
            await asyncio.sleep(self.config.request_delay)
        return results

    def retry_failed_requests(self) -> Dict[str, Optional[Dict]]:
        """Retry all failed requests from the buffer."""
        failed_requests = self.buffer.get_retryable_requests(self.config.max_retries)
        return asyncio.run(self.process_bulk_content(
            {url: data['content'] for url, data in failed_requests.items()}
        ))

    async def get_processing_stats(self) -> Dict[str, Any]:
        """Get detailed processing statistics."""
        return {
            "total_processed": len(self.results),
            "failed_requests": len(self.buffer.get_failed_requests()),
            "retryable_requests": len(self.buffer.get_retryable_requests(self.config.max_retries)),
            "success_rate": len(self.results) / (len(self.results) + len(self.buffer.get_failed_requests())) * 100 if self.results else 0
        }
