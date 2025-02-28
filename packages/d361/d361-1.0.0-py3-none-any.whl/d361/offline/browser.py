# this_file: src/d361/offline/browser.py


from loguru import logger
from playwright.async_api import Browser, BrowserContext, Page


async def setup_browser(headless: bool = True) -> tuple[Browser, BrowserContext]:
    """Set up browser for web scraping.

    Args:
        headless: Whether to run browser in headless mode

    Returns:
        Tuple of (Browser, BrowserContext)
    """
    from playwright.async_api import async_playwright

    playwright = await async_playwright().start()
    browser_type = playwright.chromium

    # Configure browser with more reliable settings
    browser = await browser_type.launch(
        headless=headless,
        args=[
            "--disable-blink-features=AutomationControlled",  # Hide automation flags
            "--disable-features=IsolateOrigins,site-per-process",  # Disable site isolation
            "--disable-web-security",  # Allow cross-origin requests
            "--disable-setuid-sandbox",  # For Linux compatibility
            "--no-sandbox",  # For Linux compatibility
            "--disable-dev-shm-usage",  # For Docker/CI systems
            "--disable-accelerated-2d-canvas",  # Reduce memory usage
            "--no-first-run",  # Skip first run dialogs
            "--no-default-browser-check",  # Skip default browser check
            "--disable-notifications",  # Disable notifications
            "--disable-extensions",  # Disable extensions
        ],
        ignore_default_args=["--enable-automation"],  # Avoid detection
    )

    logger.info(f"Browser setup complete (headless: {headless})")

    # Set up context with more realistic browser behavior
    context = await browser.new_context(
        viewport={
            "width": 1920,
            "height": 1080,
        },  # Larger viewport for better visibility
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        accept_downloads=True,
        java_script_enabled=True,
        bypass_csp=True,  # Bypass Content Security Policy
        ignore_https_errors=True,  # Ignore HTTPS errors
    )

    # Set default navigation timeout to prevent hanging
    context.set_default_navigation_timeout(60000)  # 60 seconds
    context.set_default_timeout(30000)  # 30 seconds for other operations

    return browser, context


async def scroll_to_bottom(page: Page, selector: str, max_scrolls: int = 30) -> None:
    """Scroll through a tree view to load all virtual scroll items.

    Args:
        page: Playwright page object
        selector: CSS selector for the scrollable element
        max_scrolls: Maximum number of scroll attempts
    """
    try:
        # Check if the element exists
        element = await page.query_selector(selector)
        if not element:
            logger.warning(f"Element not found with selector: {selector}")
            return

        logger.info(f"Starting to scroll element with selector: {selector}")

        # First attempt to find viewport element which is what we need to scroll in Document360
        viewport_selector = f"{selector} cdk-virtual-scroll-viewport"
        viewport = await page.query_selector(viewport_selector)

        # If viewport isn't found, fallback to the original selector
        scroll_target = viewport_selector if viewport else selector

        prev_height = 0
        same_height_count = 0
        scroll_position = 0

        for i in range(max_scrolls):
            # Get current scroll height
            current_height = await page.evaluate(f"""() => {{
                const element = document.querySelector('{scroll_target}');
                return element ? element.scrollHeight : 0;
            }}""")

            # Get current scroll position
            scroll_position = await page.evaluate(f"""() => {{
                const element = document.querySelector('{scroll_target}');
                return element ? element.scrollTop : 0;
            }}""")

            client_height = await page.evaluate(f"""() => {{
                const element = document.querySelector('{scroll_target}');
                return element ? element.clientHeight : 0;
            }}""")

            logger.debug(
                f"Scroll info: height={current_height}, position={scroll_position}, visible={client_height}"
            )

            if (
                current_height == prev_height
                and scroll_position + client_height >= current_height - 50
            ):
                same_height_count += 1
                if same_height_count >= 3:  # If height hasn't changed for 3 iterations
                    logger.info(
                        "Scroll height stabilized and reached bottom, assuming all items loaded"
                    )
                    break
            else:
                same_height_count = 0

            # Scroll further down
            await page.evaluate(f"""() => {{
                const element = document.querySelector('{scroll_target}');
                if (element) {{
                    // Scroll in larger increments to reach bottom faster
                    element.scrollTop += element.clientHeight * 2;
                }}
            }}""")

            logger.debug(
                f"Scroll attempt {i + 1}/{max_scrolls}, height: {current_height}"
            )
            prev_height = current_height
            await page.wait_for_timeout(800)  # Longer wait for items to load

        # Final scroll to very bottom to ensure everything is loaded
        await page.evaluate(f"""() => {{
            const element = document.querySelector('{scroll_target}');
            if (element) {{
                element.scrollTop = element.scrollHeight;
            }}
        }}""")
        await page.wait_for_timeout(1000)

        logger.info(f"Completed scrolling with {prev_height} final height")
    except Exception as e:
        logger.error(f"Error scrolling: {e}")


async def expand_all_items(page: Page, selector: str, max_attempts: int = 5) -> int:
    """Recursively expand all items in a tree view by clicking collapsed triangle icons.

    Args:
        page: Playwright page object
        selector: CSS selector for the tree view
        max_attempts: Maximum number of expansion iterations

    Returns:
        Number of nodes expanded
    """
    try:
        logger.info(f"Starting expansion of tree items using selector: {selector}")
        expanded_count = 0

        # First, make sure all virtualized content is loaded by scrolling to bottom
        await scroll_to_bottom(page, selector, max_scrolls=30)

        # Now scroll back to the top to start expanding from the top
        await page.evaluate(f"""() => {{
            const element = document.querySelector('{selector} cdk-virtual-scroll-viewport') ||
                           document.querySelector('{selector}');
            if (element) {{
                element.scrollTop = 0;
            }}
        }}""")
        await page.wait_for_timeout(1000)

        for attempt in range(1, max_attempts + 1):
            logger.info(f"Expansion iteration {attempt}/{max_attempts}")

            # Look for collapsed arrows - may vary by Document360 version
            collapsed_selectors = [
                f"{selector} .tree-arrow .fa-angle-right",
                f"{selector} .expand-icon.collapsed",
                f"{selector} .collapsed-icon",
                ".tree-arrow .fa-angle-right",  # Fallback
                ".fa-caret-right",  # Another common icon
            ]

            found_any = False
            total_found = 0

            for collapse_selector in collapsed_selectors:
                try:
                    # Count how many collapsed items exist before clicking
                    count = await page.evaluate(f"""() => {{
                        return document.querySelectorAll('{collapse_selector}').length;
                    }}""")

                    if count > 0:
                        found_any = True
                        total_found += count
                        logger.info(
                            f"Found {count} collapsed items with selector: {collapse_selector}"
                        )

                        # Click items in smaller batches to avoid DOM detachment issues
                        for batch_start in range(0, count, 5):
                            batch_end = min(batch_start + 5, count)
                            logger.debug(
                                f"Processing batch {batch_start}-{batch_end} of {count}"
                            )

                            # Get fresh references to elements for each batch
                            collapsed_icons = await page.query_selector_all(
                                collapse_selector
                            )

                            # Process only this batch
                            for i in range(
                                batch_start, min(batch_end, len(collapsed_icons))
                            ):
                                icon = collapsed_icons[i]
                                try:
                                    # Check if element is still attached and visible
                                    is_visible = await icon.is_visible()
                                    if is_visible:
                                        await icon.scroll_into_view_if_needed()
                                        await icon.click()
                                        expanded_count += 1
                                        # Short wait after each click
                                        await page.wait_for_timeout(200)
                                except Exception as e:
                                    logger.debug(
                                        f"Error expanding item: {str(e).split('\n')[0]}"
                                    )
                                    continue

                            # After each batch, wait a bit longer to let DOM settle
                            await page.wait_for_timeout(500)
                except Exception as e:
                    logger.debug(
                        f"Error processing selector {collapse_selector}: {str(e).split('\n')[0]}"
                    )
                    continue

            # If no collapsed items were found with any selector, we're done
            if not found_any:
                logger.info("No more collapsed items found")
                break

            # After an expansion iteration, scroll through to ensure we can see all items
            logger.info(
                f"Completed expansion iteration {attempt}, scrolling to check for more items..."
            )
            await scroll_to_bottom(page, selector)

        logger.info(f"Expanded {expanded_count} navigation items in total")
        return expanded_count

    except Exception as e:
        logger.error(f"Error expanding items: {e}")
        return 0
