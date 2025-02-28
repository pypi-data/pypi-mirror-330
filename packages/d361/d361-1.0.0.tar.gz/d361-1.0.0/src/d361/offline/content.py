# this_file: src/d361/offline/content.py

from loguru import logger
from playwright.async_api import Page


async def extract_page_content(page: Page) -> dict[str, str] | None:
    """Extract title and article content from a page."""
    try:
        # Extract title
        title = None
        for selector in [
            "h1.article-title",
            ".article-title",
            "#main-content h1",
            "h1",
        ]:
            title_element = await page.query_selector(selector)
            if title_element:
                title = await title_element.inner_text()
                title = title.strip()
                break

        # Extract article content
        content = None
        for selector in [
            "#articleContent",
            "d360-article-content",
            ".article-content",
            "article",
        ]:
            content_element = await page.query_selector(selector)
            if content_element:
                content = await content_element.inner_html()
                break

        if not content and not title:
            logger.warning("No content or title found in page")
            return None

        return {
            "title": title or "Untitled",
            "content": content or "<p>No content available</p>",
        }

    except Exception as e:
        logger.error(f"Error extracting page content: {e}")
        return None
