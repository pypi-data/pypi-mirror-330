# setup.py
from setuptools import setup, find_packages

# Read the README.md file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="spiderforce4ai",
    version="2.6.9",
    author="Piotr Tamulewicz",
    author_email="pt@petertam.pro",
    description="Python wrapper for SpiderForce4AI HTML-to-Markdown conversion service with LLM post-processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://petertam.pro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.11",
    install_requires=[
        "aiohttp>=3.8.0",
        "asyncio>=3.4.3",
        "rich>=10.0.0",
        "aiofiles>=0.8.0",
        "httpx>=0.24.0",
        "litellm>=1.26.0",
        "pydantic>=2.6.0",
        "requests>=2.31.0",
        "aiofiles>=23.2.1",
        "et-xmlfile>=1.1.0",
        "multidict>=6.0.4",
        "openai>=1.12.0",
        "pandas>=2.2.0",
        "numpy>=1.26.0",
        "yarl>=1.9.4",
        "typing_extensions>=4.9.0"
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-asyncio>=0.21.1',
            'pytest-cov>=4.1.0',
            'black>=23.7.0',
            'isort>=5.12.0',
            'mypy>=1.4.1',
        ],
    },
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/spiderforce4ai/issues",
        "Documentation": "https://petertam.pro/docs/spiderforce4ai",
        "Source Code": "https://github.com/yourusername/spiderforce4ai",
    },
    keywords=[
        "web-scraping",
        "markdown",
        "html-to-markdown",
        "llm",
        "ai",
        "content-extraction",
        "async",
        "parallel-processing"
    ],
    entry_points={
        'console_scripts': [
            'spiderforce4ai=spiderforce4ai.cli:main',
        ],
    },
    package_data={
        'spiderforce4ai': ['py.typed'],
    },
    zip_safe=False,
)