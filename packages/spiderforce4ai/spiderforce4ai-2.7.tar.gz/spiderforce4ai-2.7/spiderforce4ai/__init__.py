# spiderforce4ai/__init__.py

from .post_extraction_agent import PostExtractionAgent, PostExtractionConfig, ExtractionTemplate
import asyncio
import aiohttp
import json
import logging

logger = logging.getLogger(__name__)
import logging
from typing import List, Dict, Union, Optional, Tuple, Callable, Any
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse
from pathlib import Path
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import re
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.console import Console
import aiofiles
import httpx
import requests
from multiprocessing import Pool

console = Console()

def extract_metadata_headers(markdown: str, url: str = '') -> str:
    """Extract metadata and headers from markdown content."""
    lines = markdown.split('\n')
    metadata = {}
    headers = []
    
    def parse_metadata_line(line):
        """Parse a single metadata line correctly."""
        first_colon = line.find(':')
        if first_colon == -1:
            return None, None
            
        key = line[:first_colon].strip()
        value = line[first_colon + 1:].strip()
        
        # Handle the case where value starts with "URL:" - this means it's a missing description
        if value.startswith('URL:'):
            return key, ''
            
        return key, value
    
    # Process each line
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if it's a metadata line (contains : but isn't a header)
        if ':' in line and not line.startswith('#'):
            key, value = parse_metadata_line(line)
            if key:
                metadata[key] = value
        # Check if it's a header
        elif line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            text = line.lstrip('#').strip()
            if 1 <= level <= 6:
                headers.append(f"H{level}: {text}")
    
    # Construct output
    output = []
    output.append(f"URL: {url}")
    output.append(f"Title: {metadata.get('Title', url.split('/')[-2].replace('-', ' ').title())}")
    output.append(f"Description: {metadata.get('Description', '')}")
    output.append(f"CanonicalUrl: {metadata.get('CanonicalUrl', url)}")
    output.append(f"Language: {metadata.get('Language', 'en')}")
    output.append("")  # Empty line
    output.extend(headers)
    
    return '\n'.join(output)

def slugify(url: str) -> str:
    """Convert URL to a valid filename."""
    parsed = urlparse(url)
    # Combine domain and path, remove scheme and special characters
    slug = f"{parsed.netloc}{parsed.path}"
    slug = re.sub(r'[^\w\-]', '_', slug)
    slug = re.sub(r'_+', '_', slug)  # Replace multiple underscores with single
    return slug.strip('_')

@dataclass
class CrawlResult:
    """Store results of a crawl operation."""
    url: str
    status: str  # 'success' or 'failed'
    markdown: Optional[str] = None
    error: Optional[str] = None
    timestamp: str = None
    config: Dict = None
    extraction_result: Optional[Dict] = None  # Store post-extraction results
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

@dataclass
class CrawlConfig:
    """Configuration for crawling settings."""
    target_selector: Optional[str] = None  # Optional - specific element to target
    remove_selectors: Optional[List[str]] = None  # Optional - elements to remove
    remove_selectors_regex: Optional[List[str]] = None  # Optional - regex patterns for removal
    max_concurrent_requests: int = 1  # Default to single thread
    request_delay: float = 0.5  # Delay between requests
    timeout: int = 30  # Request timeout
    output_dir: Path = Path("spiderforce_reports")  # Default to spiderforce_reports in current directory
    webhook_url: Optional[str] = None  # Optional webhook endpoint
    webhook_timeout: int = 10  # Webhook timeout
    webhook_headers: Optional[Dict[str, str]] = None  # Optional webhook headers
    webhook_payload_template: Optional[str] = None  # Optional custom webhook payload template
    save_reports: bool = False  # Whether to save crawl reports
    report_file: Optional[Path] = None  # Optional report file location
    combine_to_one_markdown: Optional[str] = None  # 'full' or 'metadata_headers'
    combined_markdown_file: Optional[Path] = None  # Optional path for combined file
    
    # Post-extraction settings
    post_extraction_agent: Optional[Dict[str, Any]] = None  # LLM configuration
    post_extraction_agent_save_to_file: Optional[str] = None  # Extraction output file
    post_agent_transformer_function: Optional[Callable] = None  # Custom transformer

    def __post_init__(self):
        # Initialize empty lists/dicts for None values
        self.remove_selectors = self.remove_selectors or []
        self.remove_selectors_regex = self.remove_selectors_regex or []
        self.webhook_headers = self.webhook_headers or {}
        
        # Ensure output_dir is a Path and exists
        self.output_dir = Path(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup report file if save_reports is True
        if self.save_reports:
            if self.report_file is None:
                self.report_file = self.output_dir / "crawl_report.json"
            else:
                self.report_file = Path(self.report_file)
        
        # Setup combined markdown file if needed
        if self.combine_to_one_markdown:
            if self.combined_markdown_file is None:
                self.combined_markdown_file = self.output_dir / "combined_content.md"
            else:
                self.combined_markdown_file = Path(self.combined_markdown_file)
            # Create or clear the combined file
            self.combined_markdown_file.write_text('')

        # Validate post-extraction agent configuration if provided
        if self.post_extraction_agent:
            if "messages" not in self.post_extraction_agent:
                raise ValueError("Post-extraction agent configuration must include 'messages'")
            if "model" not in self.post_extraction_agent:
                raise ValueError("Post-extraction agent configuration must include 'model'")
            if "api_key" not in self.post_extraction_agent:
                raise ValueError("Post-extraction agent configuration must include 'api_key'")

    def to_dict(self) -> Dict:
        """Convert config to dictionary for API requests."""
        payload = {}
        # Only include selectors if they are set
        if self.target_selector:
            payload["target_selector"] = self.target_selector
        if self.remove_selectors:
            payload["remove_selectors"] = self.remove_selectors
        if self.remove_selectors_regex:
            payload["remove_selectors_regex"] = self.remove_selectors_regex
        return payload
    
def _send_webhook_sync(result: CrawlResult, config: CrawlConfig) -> None:
    """Synchronous version of webhook sender for parallel processing."""
    if not config.webhook_url:
        return

    try:
        # Use custom payload template if provided, otherwise use default
        if config.webhook_payload_template:
            # Replace variables in the template
            payload_str = config.webhook_payload_template.format(
                url=result.url,
                status=result.status,
                markdown=result.markdown if result.status == "success" else None,
                error=result.error if result.status == "failed" else None,
                timestamp=result.timestamp,
                config=config.to_dict(),
                extraction_result=result.extraction_result if result.extraction_result else None
            )
            payload = json.loads(payload_str)  # Parse the formatted JSON string
        else:
            # Use default payload format
            payload = {
                "url": result.url,
                "status": result.status,
                "markdown": result.markdown if result.status == "success" else None,
                "error": result.error if result.status == "failed" else None,
                "timestamp": result.timestamp,
                "config": config.to_dict(),
                "extraction_result": result.extraction_result if result.extraction_result else None
            }

        response = requests.post(
            config.webhook_url,
            json=payload,
            headers=config.webhook_headers,
            timeout=config.webhook_timeout
        )
        response.raise_for_status()
    except Exception as e:
        console.print(f"[yellow]Warning: Failed to send webhook for {result.url}: {str(e)}[/yellow]")

async def _send_webhook_async(result: CrawlResult, config: CrawlConfig):
    """Asynchronous webhook sender."""
    if not config.webhook_url:
        return

    try:
        # Prepare payload similar to sync version
        payload = {
            "url": result.url,
            "status": result.status,
            "markdown": result.markdown if result.status == "success" else None,
            "error": result.error if result.status == "failed" else None,
            "timestamp": result.timestamp,
            "config": config.to_dict(),
            "extraction_result": result.extraction_result if result.extraction_result else None
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                config.webhook_url,
                json=payload,
                headers=config.webhook_headers,
                timeout=config.webhook_timeout
            )
            response.raise_for_status()
    except Exception as e:
        console.print(f"[yellow]Warning: Failed to send webhook for {result.url}: {str(e)}[/yellow]")

async def _save_markdown_async(url: str, markdown: str, config: CrawlConfig):
    """Save markdown content to file and/or append to combined file asynchronously."""
    try:
        # Save individual file if not combining or if combining in full mode
        if not config.combine_to_one_markdown or config.combine_to_one_markdown == 'full':
            filename = f"{slugify(url)}.md"
            filepath = config.output_dir / filename
            async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                await f.write(markdown)

        # Handle combined markdown file
        if config.combine_to_one_markdown:
            content = markdown if config.combine_to_one_markdown == 'full' else extract_metadata_headers(markdown, url)
            combined_content = f"\n----PAGE----\n{url}\n\n{content}\n----PAGE END----\n"
            
            async with aiofiles.open(config.combined_markdown_file, 'a', encoding='utf-8') as f:
                await f.write(combined_content)
    except Exception as e:
        console.print(f"[red]Error saving markdown for {url}: {str(e)}[/red]")

def _save_markdown_sync(url: str, markdown: str, config: CrawlConfig) -> None:
    """Synchronous version of markdown saver for parallel processing."""
    try:
        # Save individual file if not combining or if combining in full mode
        if not config.combine_to_one_markdown or config.combine_to_one_markdown == 'full':
            filepath = config.output_dir / f"{slugify(url)}.md"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown)
        
        # Handle combined markdown file
        if config.combine_to_one_markdown:
            content = markdown if config.combine_to_one_markdown == 'full' else extract_metadata_headers(markdown, url)
            combined_content = f"\n----PAGE----\n{url}\n\n{content}\n----PAGE END----\n"
            
            with open(config.combined_markdown_file, 'a', encoding='utf-8') as f:
                f.write(combined_content)
    except Exception as e:
        console.print(f"[red]Error saving markdown for {url}: {str(e)}[/red]")

def _process_url_parallel(args: Tuple[str, str, CrawlConfig]) -> CrawlResult:
    """Process a single URL for parallel processing."""
    url, base_url, config = args
    try:
        # Make the conversion request
        endpoint = f"{base_url}/convert"
        payload = {
            "url": url,
            **config.to_dict()
        }
        
        response = requests.post(endpoint, json=payload, timeout=config.timeout)
        if response.status_code != 200:
            result = CrawlResult(
                url=url,
                status="failed",
                error=f"HTTP {response.status_code}: {response.text}",
                config=config.to_dict()
            )
            _send_webhook_sync(result, config)
            return result
        
        # Parse JSON response - THIS IS WHERE THE ERROR LIKELY OCCURS
        try:
            response_data = response.json()
            # Make sure we're accessing 'markdown' correctly
            markdown = response_data.get('markdown', '')  # Use get() with default value
            if not markdown and response.text:  # Fallback to raw text if no markdown
                markdown = response.text
        except json.JSONDecodeError:
            # If response isn't JSON, use raw text
            markdown = response.text
        
        # Save markdown if output directory is configured
        if config.output_dir:
            _save_markdown_sync(url, markdown, config)
        
        result = CrawlResult(
            url=url,
            status="success",
            markdown=markdown,
            config=config.to_dict()
        )
        
        # Send webhook for successful result
        _send_webhook_sync(result, config)
        
        # Add delay if configured
        if config.request_delay:
            time.sleep(config.request_delay)
        
        return result
            
    except Exception as e:
        result = CrawlResult(
            url=url,
            status="failed",
            error=str(e),
            config=config.to_dict()
        )
        # Send webhook for error result
        _send_webhook_sync(result, config)
        return result

async def _save_report_async(results: List[CrawlResult], config: CrawlConfig, retry_stats: Dict = None):
    """Save crawl report to JSON file asynchronously."""
    if not config.report_file:
        return

    # Separate successful and failed results
    successful_results = [r for r in results if r.status == "success"]
    failed_results = [r for r in results if r.status == "failed"]

    report = {
        "timestamp": datetime.now().isoformat(),
        "config": config.to_dict(),
        "results": {
            "successful": [asdict(r) for r in successful_results],
            "failed": [asdict(r) for r in failed_results]
        },
        "summary": {
            "total": len(results),
            "successful": len(successful_results),
            "failed": len(failed_results),
            "retry_info": retry_stats or {}
        }
    }

    async with aiofiles.open(config.report_file, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(report, indent=2))

def _save_report_sync(results: List[CrawlResult], config: CrawlConfig, retry_stats: Dict = None) -> None:
    """Synchronous version of report saver."""
    if not config.report_file:
        return

    # Create report similar to async version
    successful_results = [r for r in results if r.status == "success"]
    failed_results = [r for r in results if r.status == "failed"]
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "config": config.to_dict(),
        "results": {
            "successful": [asdict(r) for r in successful_results],
            "failed": [asdict(r) for r in failed_results]
        },
        "summary": {
            "total": len(results),
            "successful": len(successful_results),
            "failed": len(failed_results),
            "retry_info": retry_stats or {}
        }
    }

    with open(config.report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

class SpiderForce4AI:
    """Main class for interacting with SpiderForce4AI service."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = None
        self._executor = ThreadPoolExecutor()
        self.crawl_results: List[CrawlResult] = []
        self._retry_stats = {}

    async def _ensure_session(self):
        """Ensure aiohttp session exists."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _close_session(self):
        """Close aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()

    async def crawl_url_async(self, url: str, config: CrawlConfig) -> CrawlResult:
        """Crawl a single URL asynchronously."""
        await self._ensure_session()
        
        try:
            endpoint = f"{self.base_url}/convert"
            payload = {
                "url": url,
                **config.to_dict()
            }
            
            async with self.session.post(endpoint, json=payload, timeout=config.timeout) as response:
                if response.status != 200:
                    error_text = await response.text()
                    result = CrawlResult(
                        url=url,
                        status="failed",
                        error=f"HTTP {response.status}: {error_text}",
                        config=config.to_dict()
                    )
                else:
                    markdown = await response.text()
                    result = CrawlResult(
                        url=url,
                        status="success",
                        markdown=markdown,
                        config=config.to_dict()
                    )

                    if config.output_dir:
                        await _save_markdown_async(url, markdown, config)
                    
                    await _send_webhook_async(result, config)
                
                self.crawl_results.append(result)
                return result
                
        except Exception as e:
            result = CrawlResult(
                url=url,
                status="failed",
                error=str(e),
                config=config.to_dict()
            )
            self.crawl_results.append(result)
            return result

    def crawl_url(self, url: str, config: CrawlConfig) -> CrawlResult:
        """Synchronous version of crawl_url_async."""
        return asyncio.run(self.crawl_url_async(url, config))

    async def _retry_failed_urls(self, failed_results: List[CrawlResult], config: CrawlConfig, progress=None) -> List[CrawlResult]:
        """Retry failed URLs with optional progress tracking."""
        if not failed_results:
            return []

        failed_count = len(failed_results)
        total_count = len(self.crawl_results)
        failure_ratio = (failed_count / total_count) * 100
        
        console.print(f"\n[yellow]Retrying failed URLs: {failed_count} ({failure_ratio:.1f}% failed)[/yellow]")
        retry_results = []
        
        # Create or use provided progress bar
        should_close_progress = progress is None
        if progress is None:
            progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            )
            progress.start()

        retry_task = progress.add_task("[yellow]Retrying failed URLs...", total=len(failed_results))

        for result in failed_results:
            progress.update(retry_task, description=f"[yellow]Retrying: {result.url}")
            
            try:
                new_result = await self.crawl_url_async(result.url, config)
                if new_result.status == "success":
                    console.print(f"[green]✓ Retry successful: {result.url}[/green]")
                else:
                    console.print(f"[red]✗ Retry failed: {result.url} - {new_result.error}[/red]")
                retry_results.append(new_result)
            except Exception as e:
                console.print(f"[red]✗ Retry error: {result.url} - {str(e)}[/red]")
                retry_results.append(CrawlResult(
                    url=result.url,
                    status="failed",
                    error=f"Retry error: {str(e)}",
                    config=config.to_dict()
                ))
            
            progress.update(retry_task, advance=1)
            await asyncio.sleep(config.request_delay)

        if should_close_progress:
            progress.stop()

        return retry_results

    async def crawl_urls_async(self, urls: List[str], config: CrawlConfig) -> List[CrawlResult]:
        """Crawl multiple URLs asynchronously with progress bar."""
        await self._ensure_session()
        post_extraction_results = {}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            crawl_task = progress.add_task("[cyan]Crawling URLs...", total=len(urls))
            
            async def crawl_with_progress(url):
                result = await self.crawl_url_async(url, config)
                progress.update(crawl_task, advance=1, description=f"[cyan]Crawled: {url}")
                return result

            # Set up concurrency control
            semaphore = asyncio.Semaphore(config.max_concurrent_requests)
            
            # Semaphore for crawling
            crawl_semaphore = asyncio.Semaphore(config.max_concurrent_requests)
            
            async def crawl_with_semaphore(url):
                async with crawl_semaphore:
                    result = await crawl_with_progress(url)
                    await asyncio.sleep(config.request_delay)
                    return result

            # Perform initial crawl
            initial_results = await asyncio.gather(*[crawl_with_semaphore(url) for url in urls])
            
            # Handle failed URLs
            failed_results = [r for r in initial_results if r.status == "failed"]
            initial_failed = len(failed_results)
            total_urls = len(urls)
            failure_ratio = (initial_failed / total_urls) * 100

            # Retry failed URLs if ratio is acceptable
            results = initial_results
            retry_successful = 0
            
            if failed_results and failure_ratio <= 20:
                retry_results = await self._retry_failed_urls(failed_results, config, progress)
                retry_successful = len([r for r in retry_results if r.status == "success"])
                
                # Update results list
                for retry_result in retry_results:
                    for i, result in enumerate(results):
                        if result.url == retry_result.url:
                            results[i] = retry_result
                            break

            # Process LLM requests sequentially after all crawling is complete
            if config.post_extraction_agent:
                console.print("\n[cyan]Processing content with LLM...[/cyan]")
                llm_task = progress.add_task("[cyan]LLM Processing...", total=len([r for r in results if r.status == "success"]))
                
                post_config = PostExtractionConfig(
                    model=config.post_extraction_agent["model"],
                    messages=config.post_extraction_agent["messages"],
                    api_key=config.post_extraction_agent["api_key"],
                    max_tokens=config.post_extraction_agent.get("max_tokens", 1000),
                    temperature=config.post_extraction_agent.get("temperature", 0.7),
                    base_url=config.post_extraction_agent.get("base_url"),
                    combine_output=bool(config.post_extraction_agent_save_to_file),
                    output_file=config.post_extraction_agent_save_to_file,
                    custom_transform_function=config.post_agent_transformer_function
                )
                agent = PostExtractionAgent(post_config)
                
                for result in results:
                    if result.status == "success":
                        try:
                            result.extraction_result = agent.process_content(result.url, result.markdown)
                            progress.update(llm_task, advance=1)
                        except Exception as e:
                            console.print(f"[red]Error in post-extraction processing for {result.url}: {str(e)}[/red]")
            
            # Process LLM requests sequentially after all crawling is complete
            llm_successful = 0
            if config.post_extraction_agent:
                console.print("\n[cyan]Starting post-extraction processing...[/cyan]")
                successful_results = [r for r in results if r.status == "success"]
                llm_task = progress.add_task("[cyan]Post-extraction processing...", total=len(successful_results))
                
                post_config = PostExtractionConfig(
                    model=config.post_extraction_agent["model"],
                    messages=config.post_extraction_agent["messages"],
                    api_key=config.post_extraction_agent["api_key"],
                    max_tokens=config.post_extraction_agent.get("max_tokens", 1000),
                    temperature=config.post_extraction_agent.get("temperature", 0.7),
                    base_url=config.post_extraction_agent.get("base_url"),
                    combine_output=bool(config.post_extraction_agent_save_to_file),
                    output_file=config.post_extraction_agent_save_to_file,
                    custom_transform_function=config.post_agent_transformer_function
                )
                agent = PostExtractionAgent(post_config)
                
                for result in successful_results:
                    try:
                        result.extraction_result = await agent.process_content(result.url, result.markdown)
                        if result.extraction_result:
                            llm_successful += 1
                        progress.update(llm_task, advance=1)
                    except Exception as e:
                        console.print(f"[red]Error in post-extraction processing for {result.url}: {str(e)}[/red]")
                        await asyncio.sleep(1)  # Add delay after error
                    await asyncio.sleep(0.5)  # Rate limiting between requests
            
            # Calculate final statistics
            final_successful = len([r for r in results if r.status == "success"])
            final_failed = len([r for r in results if r.status == "failed"])
            
            # Update retry stats
            self._retry_stats = {
                "initial_failures": initial_failed,
                "failure_ratio": failure_ratio,
                "retry_successful": retry_successful if initial_failed > 0 else 0,
                "retry_failed": final_failed,
                "llm_successful": llm_successful
            }

            # Print summary
            console.print(f"\n[green]Crawling Summary:[/green]")
            console.print(f"Total URLs processed: {total_urls}")
            console.print(f"Initial failures: {initial_failed} ({failure_ratio:.1f}%)")
            console.print(f"Final results:")
            console.print(f"  ✓ Successful: {final_successful}")
            console.print(f"  ✗ Failed: {final_failed}")
            
            if initial_failed > 0:
                console.print(f"Retry success rate: {retry_successful}/{initial_failed} ({(retry_successful/initial_failed)*100:.1f}%)")
            
            # Save final report
            if config.save_reports:
                await _save_report_async(results, config, self._retry_stats)
                console.print(f"📊 Report saved to: {config.report_file}")
            
            return results

    def crawl_urls(self, urls: List[str], config: CrawlConfig) -> List[CrawlResult]:
        """Synchronous version of crawl_urls_async."""
        return asyncio.run(self.crawl_urls_async(urls, config))

    async def crawl_sitemap_async(self, sitemap_url: str, config: CrawlConfig) -> List[CrawlResult]:
        """Crawl URLs from a sitemap asynchronously."""
        await self._ensure_session()
        
        try:
            console.print(f"[cyan]Fetching sitemap from {sitemap_url}...[/cyan]")
            async with self.session.get(sitemap_url, timeout=config.timeout) as response:
                sitemap_text = await response.text()
        except Exception as e:
            console.print(f"[red]Error fetching sitemap: {str(e)}[/red]")
            raise

        try:
            root = ET.fromstring(sitemap_text)
            namespace = {'ns': root.tag.split('}')[0].strip('{')}
            urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
            console.print(f"[green]Found {len(urls)} URLs in sitemap[/green]")
        except Exception as e:
            console.print(f"[red]Error parsing sitemap: {str(e)}[/red]")
            raise

        return await self.crawl_urls_async(urls, config)

    def crawl_sitemap(self, sitemap_url: str, config: CrawlConfig) -> List[CrawlResult]:
        """Synchronous version of crawl_sitemap_async."""
        return asyncio.run(self.crawl_sitemap_async(sitemap_url, config))

    def crawl_sitemap_parallel(self, sitemap_url: str, config: CrawlConfig) -> List[CrawlResult]:
        """Crawl sitemap URLs in parallel using multiprocessing."""
        # Fetch and parse sitemap
        try:
            response = requests.get(sitemap_url, timeout=config.timeout)
            response.raise_for_status()
            root = ET.fromstring(response.text)
            namespace = {'ns': root.tag.split('}')[0].strip('{')}
            urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
            console.print(f"[green]Found {len(urls)} URLs in sitemap[/green]")
        except Exception as e:
            console.print(f"[red]Error processing sitemap: {str(e)}[/red]")
            raise

        # Process URLs in parallel
        process_args = [(url, self.base_url, config) for url in urls]
        results = []

        with Pool(processes=config.max_concurrent_requests) as pool:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TextColumn("({task.completed}/{task.total})"),
            ) as progress:
                task = progress.add_task("[cyan]Crawling URLs...", total=len(urls))
                    
                for result in pool.imap_unordered(_process_url_parallel, process_args):
                    results.append(result)
                    progress.update(task, advance=1)
                    status = "✓" if result.status == "success" else "✗"
                    progress.description = f"[cyan]Last: {status} {result.url}"

        # Process LLM requests sequentially after all crawling is complete
        if config.post_extraction_agent:
            console.print("\n[cyan]Starting post-extraction processing...[/cyan]")
            successful_results = [r for r in results if r.status == "success"]
                
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
            ) as progress:
                llm_task = progress.add_task("[cyan]Post-extraction processing...", total=len(successful_results))
                    
                post_config = PostExtractionConfig(
                    model=config.post_extraction_agent["model"],
                    messages=config.post_extraction_agent["messages"],
                    api_key=config.post_extraction_agent["api_key"],
                    max_tokens=config.post_extraction_agent.get("max_tokens", 1000),
                    temperature=config.post_extraction_agent.get("temperature", 0.7),
                    base_url=config.post_extraction_agent.get("base_url"),
                    combine_output=bool(config.post_extraction_agent_save_to_file),
                    output_file=config.post_extraction_agent_save_to_file,
                    custom_transform_function=config.post_agent_transformer_function
                )
                agent = PostExtractionAgent(post_config)
                    
                for result in successful_results:
                    try:
                        # Process content synchronously since it's not an async method
                        extraction_result = agent.process_content(result.url, result.markdown)
                        if extraction_result:
                            result.extraction_result = extraction_result
                            logger.info(f"Successfully processed and transformed content for {result.url}")
                        progress.update(llm_task, advance=1)
                    except Exception as e:
                        console.print(f"[red]Error in post-extraction processing for {result.url}: {str(e)}[/red]")
                        time.sleep(1)  # Add delay after error
                    time.sleep(0.5)  # Rate limiting between requests

        # Calculate statistics and handle retries
        failed_results = [r for r in results if r.status == "failed"]
        initial_failed = len(failed_results)
        failure_ratio = (initial_failed / len(urls)) * 100
        retry_successful = 0

        if failed_results and failure_ratio <= 20:
            console.print(f"\n[yellow]Retrying {initial_failed} failed URLs...[/yellow]")
            for result in failed_results:
                new_result = _process_url_parallel((result.url, self.base_url, config))
                if new_result.status == "success":
                    retry_successful += 1
                    console.print(f"[green]✓ Retry successful: {result.url}[/green]")
                else:
                    console.print(f"[red]✗ Retry failed: {result.url}[/red]")
                
                # Update results list
                for i, r in enumerate(results):
                    if r.url == new_result.url:
                        results[i] = new_result
                        break

        # Calculate final statistics
        final_successful = len([r for r in results if r.status == "success"])
        final_failed = len([r for r in results if r.status == "failed"])

        # Print summary
        console.print(f"\n[green]Crawling Summary:[/green]")
        console.print(f"Total URLs processed: {len(urls)}")
        console.print(f"Initial failures: {initial_failed} ({failure_ratio:.1f}%)")
        console.print(f"Final results:")
        console.print(f"  ✓ Successful: {final_successful}")
        console.print(f"  ✗ Failed: {final_failed}")
        
        if initial_failed > 0:
            console.print(f"Retry success rate: {retry_successful}/{initial_failed} ({(retry_successful/initial_failed)*100:.1f}%)")

# Save report
        if config.save_reports:
            self._retry_stats = {
                "initial_failures": initial_failed,
                "failure_ratio": failure_ratio,
                "retry_successful": retry_successful,
                "retry_failed": final_failed
            }
            _save_report_sync(results, config, self._retry_stats)
            console.print(f"📊 Report saved to: {config.report_file}")

        return results

    def crawl_urls_server_parallel(self, urls: List[str], config: CrawlConfig) -> List[CrawlResult]:
        """Crawl URLs in parallel using multiprocessing."""
        console.print(f"[cyan]Processing {len(urls)} URLs in parallel...[/cyan]")

        # Process URLs in parallel
        process_args = [(url, self.base_url, config) for url in urls]
        results = []

        with Pool(processes=config.max_concurrent_requests) as pool:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TextColumn("({task.completed}/{task.total})"),
            ) as progress:
                task = progress.add_task("[cyan]Crawling URLs...", total=len(urls))
                    
                for result in pool.imap_unordered(_process_url_parallel, process_args):
                    results.append(result)
                    progress.update(task, advance=1)
                    status = "✓" if result.status == "success" else "✗"
                    progress.description = f"[cyan]Last: {status} {result.url}"

        # Process LLM requests sequentially after all crawling is complete
        if config.post_extraction_agent:
            console.print("\n[cyan]Starting post-extraction processing...[/cyan]")
            successful_results = [r for r in results if r.status == "success"]
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
            ) as progress:
                llm_task = progress.add_task("[cyan]Post-extraction processing...", total=len(successful_results))
                
                post_config = PostExtractionConfig(
                    model=config.post_extraction_agent["model"],
                    messages=config.post_extraction_agent["messages"],
                    api_key=config.post_extraction_agent["api_key"],
                    max_tokens=config.post_extraction_agent.get("max_tokens", 1000),
                    temperature=config.post_extraction_agent.get("temperature", 0.7),
                    base_url=config.post_extraction_agent.get("base_url"),
                    combine_output=bool(config.post_extraction_agent_save_to_file),
                    output_file=config.post_extraction_agent_save_to_file,
                    custom_transform_function=config.post_agent_transformer_function
                )
                agent = PostExtractionAgent(post_config)
                
                for result in successful_results:
                    try:
                        # Process content synchronously since it's not an async method
                        extraction_result = agent.process_content(result.url, result.markdown)
                        if extraction_result:
                            result.extraction_result = extraction_result
                            logger.info(f"Successfully processed and transformed content for {result.url}")
                        progress.update(llm_task, advance=1)
                    except Exception as e:
                        console.print(f"[red]Error in post-extraction processing for {result.url}: {str(e)}[/red]")
                        time.sleep(1)  # Add delay after error
                    time.sleep(0.5)  # Rate limiting between requests

        # Calculate statistics
        successful = len([r for r in results if r.status == "success"])
        failed = len([r for r in results if r.status == "failed"])

        # Print summary
        console.print(f"\n[green]Crawling Summary:[/green]")
        console.print(f"Total URLs processed: {len(urls)}")
        console.print(f"✓ Successful: {successful}")
        console.print(f"✗ Failed: {failed}")

        # Save report if enabled
        if config.save_reports:
            self._retry_stats = {
                "initial_failures": failed,
                "failure_ratio": (failed / len(urls)) * 100,
                "retry_successful": 0,
                "retry_failed": failed
            }
            _save_report_sync(results, config, self._retry_stats)
            console.print(f"📊 Report saved to: {config.report_file}")

        return results

    def crawl_sitemap_server_parallel(self, sitemap_url: str, config: CrawlConfig) -> List[CrawlResult]:
        """
        Crawl sitemap URLs using server-side parallel processing.
        """
        console.print(f"[cyan]Fetching sitemap from {sitemap_url}...[/cyan]")
        
        try:
            response = requests.get(sitemap_url, timeout=config.timeout)
            response.raise_for_status()
            root = ET.fromstring(response.text)
            namespace = {'ns': root.tag.split('}')[0].strip('{')}
            urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
            console.print(f"[green]Found {len(urls)} URLs in sitemap[/green]")
            
            # Process URLs using server-side parallel endpoint
            return self.crawl_urls_server_parallel(urls, config)
            
        except Exception as e:
            console.print(f"[red]Error processing sitemap: {str(e)}[/red]")
            raise

    async def __aenter__(self):
        """Async context manager entry."""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self._close_session()

    def __enter__(self):
        """Sync context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Sync context manager exit."""
        self._executor.shutdown(wait=True)

# Version info
#__version__ = "2.3.1"
#__author__ = "Piotr Tamulewicz"
#__email__ = "pt@petertam.pro"
