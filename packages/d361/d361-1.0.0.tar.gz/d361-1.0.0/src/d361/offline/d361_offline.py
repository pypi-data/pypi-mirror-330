# this_file: src/d361/offline/d361_offline.py

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from loguru import logger

from .browser import setup_browser
from .config import Config
from .content import extract_page_content
from .generator import (
    create_output_directory,
    generate_html_file,
    generate_markdown_file,
    generate_navigation_html,
)
from .navigation import extract_navigation
from .parser import parse_sitemap


class D361Offline:
    """Main Document360 offline documentation generator class."""

    def __init__(self, config: Config) -> None:
        """Initialize with configuration."""
        self.config = config
        self.output_dir = config.output_dir
        self.prep_file = self.output_dir / "prep.json"
        logger.info(f"Initialized D361Offline with output directory: {self.output_dir}")

    async def prep(self) -> dict[str, Any]:
        """Prepare for documentation generation by extracting sitemap and navigation."""
        logger.info("Starting preparation phase")

        # Parse sitemap to get URLs
        urls = await parse_sitemap(
            sitemap_url=str(self.config.map_url),
            test=self.config.test,
            pause=self.config.pause,
        )
        if not urls:
            msg = "No URLs found in sitemap"
            raise ValueError(msg)

        logger.info(f"Found {len(urls)} URLs in sitemap")

        # Extract navigation structure
        # Use non-headless mode for navigation extraction to ensure JavaScript loads correctly
        browser, context = await setup_browser(headless=False)
        nav_structure: dict[str, Any] = {"items": []}
        try:
            nav_url = (
                str(self.config.nav_url) if self.config.nav_url else next(iter(urls))
            )
            logger.info(f"Using navigation URL: {nav_url}")

            nav_structure = await extract_navigation(
                page=await context.new_page(),
                nav_url=nav_url,
                test=self.config.test,
            )

            if not nav_structure:
                logger.warning(
                    "Failed to extract navigation structure, using empty structure"
                )
                nav_structure = {"items": []}

            # Generate and save navigation files as mentioned in FIXME
            try:
                # Create output directory if it doesn't exist
                os.makedirs(self.output_dir, exist_ok=True)

                # Save nav.json
                nav_json_path = self.output_dir / "nav.json"
                with open(nav_json_path, "w") as f:
                    json.dump(nav_structure, f, indent=2)
                logger.info(f"Saved navigation structure to {nav_json_path}")

                # Generate nav.html
                nav_html = generate_navigation_html(nav_structure)
                nav_html_path = self.output_dir / "nav.html"
                with open(nav_html_path, "w") as f:
                    f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Navigation</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        nav {{ max-width: 800px; margin: 0 auto; }}
        ul {{ list-style-type: none; padding-left: 20px; }}
        li {{ margin: 5px 0; }}
        a {{ text-decoration: none; color: #0366d6; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    {nav_html}
</body>
</html>""")
                logger.info(f"Saved navigation HTML to {nav_html_path}")

                # Generate nav.md
                nav_md_path = self.output_dir / "nav.md"
                with open(nav_md_path, "w") as f:
                    f.write("# Navigation\n\n")

                    def write_items(
                        items: list[dict[str, Any]], level: int = 0
                    ) -> None:
                        for item in items:
                            indent = "  " * level
                            title = item.get("title", "Untitled")
                            link = item.get("link", "")
                            if link:
                                f.write(f"{indent}- [{title}]({link})\n")
                            else:
                                f.write(f"{indent}- {title}\n")

                            children = item.get("children", [])
                            if children:
                                write_items(children, level + 1)

                    write_items(nav_structure.get("items", []))

                logger.info(f"Saved navigation markdown to {nav_md_path}")

            except Exception as e:
                logger.error(f"Error generating navigation files: {e}")

        finally:
            await browser.close()

        # Prepare state
        state: dict[str, Any] = {
            "config": self.config.model_dump(),
            "timestamp": datetime.now().isoformat(),
            "urls": list(urls),
            "navigation": nav_structure,
        }

        # Save state to prep file
        os.makedirs(self.output_dir, exist_ok=True)
        with open(self.prep_file, "w") as f:
            json.dump(state, f, indent=2)

        logger.info(f"Saved preparation state to {self.prep_file}")
        return state

    async def fetch(self, prep_file: Path | None = None) -> dict[str, Any]:
        """Fetch content for all URLs in the state file."""
        logger.info("Starting fetch phase")

        # Load state from prep file
        prep_path = prep_file or self.prep_file
        if not prep_path.exists():
            msg = f"Prep file not found: {prep_path}"
            raise FileNotFoundError(msg)

        with open(prep_path) as f:
            state = json.load(f)

        urls = state.get("urls", [])
        if not urls:
            msg = "No URLs found in state file"
            raise ValueError(msg)

        logger.info(f"Loaded {len(urls)} URLs from state file")

        # Setup browser
        browser, context = await setup_browser()

        try:
            # Set limits based on configuration
            max_concurrent = self.config.max_concurrent
            max_urls = 5 if self.config.test else len(urls)

            # Track processed URLs and results
            processed_urls = set()
            results = {}

            # Process URLs in batches
            for i in range(0, min(max_urls, len(urls)), max_concurrent):
                batch = urls[i : min(i + max_concurrent, max_urls)]
                tasks = []

                for url in batch:
                    if url in processed_urls:
                        continue

                    async def process_url(url):
                        for attempt in range(self.config.retries + 1):
                            try:
                                logger.info(
                                    f"Fetching content for {url} (attempt {attempt + 1})"
                                )
                                page = await context.new_page()
                                try:
                                    await page.goto(
                                        url, timeout=self.config.timeout * 1000
                                    )
                                    content = await extract_page_content(page)
                                    if content:
                                        return url, content
                                    else:
                                        logger.warning(
                                            f"No content extracted from {url}"
                                        )
                                finally:
                                    await page.close()
                            except Exception as e:
                                logger.error(
                                    f"Error fetching {url} (attempt {attempt + 1}): {e}"
                                )
                                if attempt < self.config.retries:
                                    delay = (attempt + 1) * 5  # Exponential backoff
                                    logger.info(f"Retrying in {delay} seconds...")
                                    await asyncio.sleep(delay)

                        return url, None

                    tasks.append(process_url(url))
                    processed_urls.add(url)

                # Wait for all tasks in the batch to complete
                batch_results = await asyncio.gather(*tasks)

                # Add results to the dictionary
                for url, content in batch_results:
                    if content:
                        results[url] = content

                # Add a pause between batches if configured
                if self.config.pause and i + max_concurrent < max_urls:
                    logger.info(f"Pausing for {self.config.pause} seconds...")
                    await asyncio.sleep(self.config.pause)

            # Update state with fetched content
            state["content"] = results
            state["timestamp"] = datetime.now().isoformat()

            # Save updated state
            with open(self.output_dir / "fetch.json", "w") as f:
                json.dump(state, f, indent=2)

            logger.info(f"Fetched content for {len(results)} URLs")
            logger.info(f"Saved fetch state to {self.output_dir / 'fetch.json'}")

            return state

        finally:
            await browser.close()

    async def build(self, fetch_file: Path | None = None) -> None:
        """Build HTML and Markdown output from fetched content."""
        logger.info("Starting build phase")

        # Load state from fetch file
        fetch_path = fetch_file or (self.output_dir / "fetch.json")
        if not fetch_path.exists():
            msg = f"Fetch file not found: {fetch_path}"
            raise FileNotFoundError(msg)

        with open(fetch_path) as f:
            state = json.load(f)

        content_dict = state.get("content", {})
        if not content_dict:
            msg = "No content found in fetch file"
            raise ValueError(msg)

        logger.info(f"Loaded content for {len(content_dict)} URLs from fetch file")

        # Create output directory structure
        await create_output_directory(self.output_dir, self.config.css_file)

        # Generate navigation HTML
        nav_structure = state.get("navigation", {"items": []})
        nav_html = generate_navigation_html(nav_structure)

        # Determine CSS filename
        css_filename = (
            self.config.css_file.name if self.config.css_file else "style.css"
        )

        # Process each URL
        for url, content in content_dict.items():
            try:
                # Generate HTML file
                await generate_html_file(
                    url, content, self.output_dir, nav_html, css_filename
                )

                # Generate Markdown file
                await generate_markdown_file(url, content, self.output_dir)

            except Exception as e:
                logger.error(f"Error building output for {url}: {e}")

        logger.info(f"Build completed: Generated files for {len(content_dict)} URLs")
        logger.info(f"Output directory: {self.output_dir}")

    async def all(self, prep_file: Path | None = None) -> None:
        """Run the entire process: prep, fetch, and build."""
        logger.info("Starting all phases: prep, fetch, build")

        # Run prep phase
        await self.prep()

        # Run fetch phase
        await self.fetch(self.prep_file)

        # Run build phase
        await self.build(self.output_dir / "fetch.json")

        logger.info("All phases completed successfully")
        logger.info(f"Output directory: {self.output_dir}")
