# this_file: src/d361/offline/config.py

from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from pydantic import AnyHttpUrl, BaseModel, Field, TypeAdapter

# Constants
DEFAULT_TIMEOUT = 60  # seconds
DEFAULT_RETRIES = 3
DEFAULT_MAX_CONCURRENT = 5
DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
DEFAULT_MAP_URL = TypeAdapter(AnyHttpUrl).validate_python(
    "https://docs.document360.com/sitemap-en.xml"
)


class Config(BaseModel):
    """Configuration model for d361_offline."""

    map_url: AnyHttpUrl = Field(
        default=DEFAULT_MAP_URL, description="URL of the sitemap that defines the scope"
    )
    nav_url: AnyHttpUrl | None = Field(
        default=None, description="URL of the page to gather navigation from"
    )
    output_dir: Path = Field(
        default=Path.cwd(), description="Output directory for downloaded content"
    )
    css_file: Path | None = Field(
        default=None, description="Path to CSS file for styling"
    )
    effort: bool = Field(
        default=False, description="Try harder to map all sitemap links in navigation"
    )
    max_concurrent: int = Field(
        default=DEFAULT_MAX_CONCURRENT,
        description="Maximum number of concurrent requests",
    )
    retries: int = Field(
        default=DEFAULT_RETRIES,
        description="Number of retry attempts for failed requests",
    )
    timeout: int = Field(
        default=DEFAULT_TIMEOUT, description="Request timeout in seconds"
    )
    verbose: bool = Field(default=False, description="Enable verbose logging")
    test: bool = Field(
        default=False, description="Test mode - only process first 5 items"
    )
    pause: bool = Field(
        default=False, description="Pause during navigation to allow user inspection"
    )

    def __init__(self, **data) -> None:
        super().__init__(**data)

        # Handle output_dir properly:
        # If output_dir is "." or cwd, add domain as subdirectory
        if str(self.output_dir) == "." or str(self.output_dir) == str(Path.cwd()):
            # Only proceed if we have a valid map_url
            if self.map_url:
                domain = urlparse(str(self.map_url)).netloc
                if domain:
                    self.output_dir = Path.cwd() / domain

    def model_dump(self, **kwargs) -> dict[str, Any]:
        """Override model_dump to ensure all fields are JSON serializable."""
        data = super().model_dump(**kwargs)
        # Convert AnyHttpUrl to string
        if data.get("map_url"):
            data["map_url"] = str(data["map_url"])
        if data.get("nav_url"):
            data["nav_url"] = str(data["nav_url"])
        # Convert Path to string
        if data.get("output_dir"):
            data["output_dir"] = str(data["output_dir"])
        if data.get("css_file"):
            data["css_file"] = str(data["css_file"])
        return data
