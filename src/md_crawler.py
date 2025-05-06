import os
import re
import asyncio
import logging
import yaml
import importlib
from pathlib import Path
from urllib.parse import urlparse
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Default configuration that can be overridden by libraries.yaml
DEFAULT_CONFIG = {
    'crawler': {
        'word_count_threshold': 15,
        'markdown_options': {
            'ignore_links': True,
            'main_content_only': True,
            'clean_documentation_artifacts': True,
            'strip_empty_headings': True,
            'remove_duplicate_content': True
        },
        'cache_mode': 'BYPASS'
    }
}

def get_safe_filename(url: str) -> str:
    """Convert URL to a safe filename."""
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    if not path:
        return 'index.md'
    
    # Extract meaningful parts
    parts = path.split('/')
    if len(parts) >= 3 and parts[0] == 'en' and parts[1] == 'stable':
        # For /en/stable/page.html -> page.md
        return f"{parts[2].replace('.html', '')}.md"
    
    # Fallback: Replace unsafe characters
    safe_name = path.replace('/', '_').replace('\\', '_')
    return f"{safe_name}.md"

def get_url_from_link(link) -> str:
    """Extract URL from a link object."""
    if isinstance(link, str):
        return link
    elif isinstance(link, dict):
        return link.get('href', '')
    return ''

def should_process_url(url: str, base_domain: str, crawler_config: dict = None) -> bool:
    """
    Determine if a URL should be processed based on filtering rules.
    
    Args:
        url (str): URL to check
        base_domain (str): Base domain to enforce same-domain rule
        crawler_config (dict): Configuration containing include/exclude patterns
    """
    parsed = urlparse(url)
    
    # Skip if not from same domain
    if parsed.netloc != base_domain:
        return False
        
    # Skip fragment URLs
    if '#' in url:
        return False
    
    if crawler_config:
        # Check exclude patterns first
        if 'exclude_patterns' in crawler_config:
            for pattern in crawler_config['exclude_patterns']:
                if re.search(pattern, url):
                    logger.debug(f"URL {url} matched exclude pattern {pattern}")
                    return False
        
        # Then check include patterns if specified
        if 'include_patterns' in crawler_config:
            for pattern in crawler_config['include_patterns']:
                if re.search(pattern, url):
                    logger.debug(f"URL {url} matched include pattern {pattern}")
                    return True
            # If include patterns are specified but none matched, exclude the URL
            return False
    
    return True

def load_cleaner(cleaner_name: str):
    """Load a cleaner module by name."""
    try:
        # Get the current working directory
        cwd = Path.cwd()
        # Add the current working directory to sys.path temporarily
        import sys
        sys.path.insert(0, str(cwd))
        # Import the cleaner module
        module = importlib.import_module(f'config.cleaners.{cleaner_name}')
        cleaner_func = getattr(module, f'clean_{cleaner_name}')
        # Remove the temporary path
        sys.path.pop(0)
        return cleaner_func
    except (ImportError, AttributeError) as e:
        logger.warning(f"Failed to load cleaner {cleaner_name}: {str(e)}")
        return None

async def crawl_documentation(url: str, name: str, crawler_config: dict = None, timeout: int = 1800):
    """
    Crawl a documentation website and save all pages as markdown files.
    
    Args:
        url (str): The URL of the documentation website
        name (str): Name of the output directory where markdown files will be saved
        crawler_config (dict): Configuration from libraries.yaml
        timeout (int): Maximum time in seconds to spend crawling (default: 30 minutes)
    """
    # Get output directory from environment variable or default
    output_base = os.getenv('OUTPUT_DIR', 'docs')
    output_dir = Path(output_base) / name
    
    logger.info(f"Starting crawl process for URL: {url}")
    logger.info(f"Output will be saved in: {output_dir}")

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created output directory: {output_dir}")

    start_time = datetime.now()
    
    # Configure browser
    browser_cfg = BrowserConfig(
        headless=True
    )
    
    # Start with default config
    config = DEFAULT_CONFIG.copy()
    
    # Update with crawler-specific config if provided
    if crawler_config:
        config['crawler'].update(crawler_config)
    
    # Create run config from merged configuration
    run_cfg_args = {
        'word_count_threshold': config['crawler']['word_count_threshold'],
        'markdown_generator': DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(threshold=0.3),
            options=config['crawler']['markdown_options']
        ),
        'cache_mode': config['crawler']['cache_mode']
    }

    # Add custom scraping strategy if specified
    if 'scraping_strategy' in crawler_config:
        strat_config = crawler_config['scraping_strategy']
        if strat_config['type'] == 'custom' and 'class' in strat_config:
            # Import the custom strategy class
            module_path, class_name = strat_config['class'].rsplit('.', 1)
            module = importlib.import_module(module_path)
            strategy_class = getattr(module, class_name)
            run_cfg_args['scraping_strategy'] = strategy_class()

    run_cfg = CrawlerRunConfig(**run_cfg_args)
    
    # Initialize crawler
    logger.info("Initializing AsyncWebCrawler...")
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        try:
            # Get base domain for filtering
            base_domain = urlparse(url).netloc
            logger.info(f"Base domain: {base_domain}")
            
            # Process the main page
            main_content = await crawler.arun(url, config=run_cfg)
            main_filename = get_safe_filename(url)
            main_path = output_dir / main_filename
            # Apply cleaner if specified
            markdown_content = main_content.markdown
            if crawler_config and 'cleaner' in crawler_config:
                cleaner = load_cleaner(crawler_config['cleaner'])
                if cleaner:
                    markdown_content = cleaner(markdown_content)
                    
            with open(main_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            logger.info(f"Saved main page: {main_path}")
            
            # Only process internal links if follow_links is not False
            if not crawler_config or crawler_config.get('follow_links', True):
                internal_links = main_content.links.get("internal", [])
                logger.info(f"Found {len(internal_links)} internal links")
                
                # Process each internal link
                processed_urls = {url}  # Keep track of processed URLs to avoid duplicates
                
                for link in internal_links:
                    # Check timeout
                    if (datetime.now() - start_time).total_seconds() > timeout:
                        logger.warning(f"Timeout reached after {timeout} seconds. Stopping crawl.")
                        break

                    try:
                        link_url = get_url_from_link(link)
                        if not link_url or link_url in processed_urls:
                            continue
                            
                        if not should_process_url(link_url, base_domain, crawler_config):
                            logger.debug(f"Skipping filtered URL: {link_url}")
                            continue
                        
                        logger.info(f"Processing link: {link_url}")
                        
                        # Add delay between requests to be polite
                        await asyncio.sleep(0.5)  # 500ms delay between requests
                        
                        result = await crawler.arun(link_url, config=run_cfg)
                        
                        if result and result.success:
                            filename = get_safe_filename(link_url)
                            output_path = output_dir / filename
                            
                            # Apply cleaner if specified
                            markdown_content = result.markdown
                            if crawler_config and 'cleaner' in crawler_config:
                                cleaner = load_cleaner(crawler_config['cleaner'])
                                if cleaner:
                                    markdown_content = cleaner(markdown_content)
                                    
                            with open(output_path, "w", encoding="utf-8") as f:
                                f.write(markdown_content)
                            logger.info(f"Successfully saved: {output_path}")
                            processed_urls.add(link_url)
                        else:
                            logger.warning(f"Failed to process {link_url}")
                            
                    except Exception as e:
                        logger.error(f"Error processing link {link}: {str(e)}")
                        continue
                
                logger.info(f"Total pages processed: {len(processed_urls)}")
            
        except Exception as e:
            logger.error(f"Error during crawling: {str(e)}")
            raise

    logger.info(f"Crawling completed. Output directory: {output_dir}")

async def crawl_multiple_libraries(config_file: str):
    """
    Crawl multiple documentation websites based on a configuration file.
    
    Args:
        config_file (str): Path to the YAML configuration file containing library definitions
    """
    # Get config path from environment variable or use provided path
    config_path = os.getenv('CONFIG_PATH', config_file)
    logger.info(f"Loading library configuration from: {config_path}")
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Error loading configuration file: {str(e)}")
        raise

    if not config or 'libraries' not in config:
        raise ValueError("Invalid configuration file: 'libraries' section not found")

    libraries = config['libraries']
    if not libraries:
        logger.warning("No libraries defined in configuration file")
        return

    total_libraries = len(libraries)
    for idx, library in enumerate(libraries, 1):
        if not isinstance(library, dict) or 'name' not in library or 'url' not in library:
            logger.warning(f"Skipping invalid library entry: {library}")
            continue

        name = library['name']
        url = library['url']
        crawler_config = library.get('crawler', {})
        
        logger.info(f"\n{'='*50}")
        logger.info(f"Processing library {idx}/{total_libraries}: {name}")
        logger.info(f"{'='*50}")
        
        try:
            await crawl_documentation(url, name, crawler_config)
        except Exception as e:
            logger.error(f"Error processing library {name}: {str(e)}")
            logger.error("Moving to next library...")
            # Sleep for a few seconds before trying the next library
            await asyncio.sleep(5)
            continue

    logger.info(f"\nCompleted processing all libraries ({total_libraries} total)")
    logger.info("Check the 'docs' directory for the generated documentation")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Crawl documentation and convert to markdown")
    parser.add_argument("--config", help="Path to libraries configuration file (YAML)")
    parser.add_argument("--url", help="URL of a single documentation website")
    parser.add_argument("--name", help="Name of the output directory for single website")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    # Add support for positional arguments
    parser.add_argument("url_pos", nargs="?", help="URL of documentation website (positional)")
    parser.add_argument("name_pos", nargs="?", help="Output directory name (positional)")
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    try:
        if args.config:
            # Process multiple libraries from config file
            asyncio.run(crawl_multiple_libraries(args.config))
        elif args.url and args.name:
            # Process single library with named parameters
            asyncio.run(crawl_documentation(args.url, args.name))
        elif args.url_pos and args.name_pos:
            # Process single library with positional parameters
            asyncio.run(crawl_documentation(args.url_pos, args.name_pos))
        else:
            parser.error("Either --config or URL and name must be provided (either as named or positional arguments)")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
