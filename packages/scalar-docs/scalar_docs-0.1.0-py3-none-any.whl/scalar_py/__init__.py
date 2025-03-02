import json
import os
import urllib.parse
from dataclasses import dataclass, field, asdict
from typing import Callable, Dict, List, Optional, Union

import requests

# Constants
DEFAULT_CDN = "https://cdn.jsdelivr.net/npm/@scalar/api-reference"
CUSTOM_THEME_CSS = """
    /* basic theme */
    .light-mode {
        --scalar-color-1: #2a2f45;
        --scalar-color-2: #757575;
        --scalar-color-3: #8e8e8e;
        --scalar-color-accent: #e0234d;
        --scalar-background-1: #fff;
        --scalar-background-2: #f6f6f6;
        --scalar-background-3: #e7e7e7;
        --scalar-background-accent: #8ab4f81f;
        --scalar-border-color: rgba(0, 0, 0, 0.1);
    }
    .dark-mode {
        --scalar-color-1: rgba(255, 255, 255, 1);
        --scalar-color-2: #b2bac2;
        --scalar-color-3: #6e748b;
        --scalar-color-accent: #e0234d;
        --scalar-background-1: #11131e;
        --scalar-background-2: #1c2132;
        --scalar-background-3: #2f354a;
        --scalar-background-accent: #8ab4f81f;
        --scalar-border-color: rgba(255, 255, 255, 0.1);
    }
    /* Document Sidebar */
    .light-mode .t-doc__sidebar,
    .dark-mode .t-doc__sidebar {
        --scalar-sidebar-background-1: var(--scalar-background-1);
        --scalar-sidebar-item-hover-color: currentColor;
        --scalar-sidebar-item-hover-background: var(--scalar-background-2);
        --scalar-sidebar-item-active-background: var(--scalar-background-3);
        --scalar-sidebar-border-color: var(--scalar-border-color);
        --scalar-sidebar-color-1: var(--scalar-color-1);
        --scalar-sidebar-color-2: var(--scalar-color-2);
        --scalar-sidebar-color-active: var(--scalar-color-1);
        --scalar-sidebar-search-background: var(--scalar-background-2);
        --scalar-sidebar-search-border-color: var(--scalar-background-2);
        --scalar-sidebar-search-color: var(--scalar-color-3);
    }

    /* advanced */
    .light-mode {
        --scalar-button-1: rgb(49 53 56);
        --scalar-button-1-color: #fff;
        --scalar-button-1-hover: rgb(28 31 33);
        --scalar-color-green: #069061;
        --scalar-color-red: #ef0006;
        --scalar-color-yellow: #edbe20;
        --scalar-color-blue: #0082d0;
        --scalar-color-orange: #fb892c;
        --scalar-color-purple: #5203d1;
        --scalar-scrollbar-color: rgba(0, 0, 0, 0.18);
        --scalar-scrollbar-color-active: rgba(0, 0, 0, 0.36);
    }
    .dark-mode {
        --scalar-button-1: #f6f6f6;
        --scalar-button-1-color: #000;
        --scalar-button-1-hover: #e7e7e7;
        --scalar-color-green: #30beb0;
        --scalar-color-red: #e91e63;
        --scalar-color-yellow: #ffc90d;
        --scalar-color-blue: #2cb6f6;
        --scalar-color-orange: #ff5656;
        --scalar-color-purple: #6223e0;
        --scalar-scrollbar-color: rgba(255, 255, 255, 0.24);
        --scalar-scrollbar-color-active: rgba(255, 255, 255, 0.48);
    }
    /* Document Header */
"""

# Data models
@dataclass
class CustomOptions:
    page_title: str = "API Reference"

@dataclass
class Spec:
    content: Optional[str] = None  # JSON string representation of the OpenAPI spec
    url: Optional[str] = None  # URL pointing to the OpenAPI spec

@dataclass
class MetaDataOptions:
    title: str = ""
    description: str = ""
    ogDescription: str = ""
    ogTitle: str = ""
    ogImage: str = ""
    twitterCard: str = ""
    
@dataclass
class ServerOptions:
    url: str
    description: str

@dataclass
class DefaultHttpClientOptions:
    targetKey: str
    clientKey: str

@dataclass
class ApiKeyAuth:
    token: str

@dataclass
class OAuth2Auth:
    clientId: str
    scopes: Optional[List[str]] = None

@dataclass
class Authentication:
    preferredSecurityScheme: Optional[str] = None
    preferredSecuritySchemes: Optional[List[Union[str, List[str]]]] = None
    apiKey: Optional[ApiKeyAuth] = None
    oAuth2: Optional[OAuth2Auth] = None



@dataclass
class Options:
    cdn: str = "https://cdn.jsdelivr.net/npm/@scalar/api-reference"
    layout: str = "modern"
    spec: Optional[Spec] = field(default_factory=Spec)
    specContent: Optional[Union[str, Dict, Callable[[], Dict]]] = None
    proxyUrl: str = "https://proxy.scalar.com"
    isEditable: bool = False
    showSidebar: bool = True
    hideModels: bool = False   
    hideDownloadButton: bool = False
    hideSearch: bool = False
    darkMode: bool = False
    hideDarkModeToggle: bool = False
    customCss: str = ""
    searchHotKey: str = "k"
    baseServerURL: str = ""
    servers: Optional[List[ServerOptions]] = None
    favicon: str = ""
    hiddenClients: Optional[Union[List[str], bool]] = field(default_factory=list) # hiddenClients: true OR hiddenClients: ["http", "curl"]
    authentication: Optional[Authentication] = None
    withDefaultFonts: bool = True
    defaultOpenAllTags: bool = False
    theme: str = "default"
    metaData: MetaDataOptions = field(default_factory=MetaDataOptions)
    hideTestRequestButton: bool = False
    pathRouting: str = ""
    hideClientButton: bool = False
    custom_options: CustomOptions = field(default_factory=CustomOptions)

# Helper functions
def safe_json_configuration(options: Options) -> str:
    """
    Serializes the options to JSON and escapes double quotes with HTML entities.
    """
    options_dict = asdict(options)
    json_data = json.dumps(options_dict)
    escaped_json = json_data.replace('"', '&quot;')
    return escaped_json

def specContent_handler(specContent: Union[str, Dict, Callable[[], Dict], None]) -> str:
    """
    Processes specContent which can be a callable, dict, or string.
    """
    if callable(specContent):
        result = specContent()
        return json.dumps(result)
    elif isinstance(specContent, dict):
        return json.dumps(specContent)
    elif isinstance(specContent, str):
        return specContent
    else:
        return ""

def ensure_file_url(file_path: str) -> str:
    """
    Ensures the file path is a valid file:// URL.
    """
    if file_path.startswith("file://"):
        path_without_prefix = file_path[len("file://"):]
        if not os.path.isabs(path_without_prefix):
            current_dir = os.getcwd()
            resolved_path = os.path.join(current_dir, path_without_prefix)
            return "file://" + os.path.abspath(resolved_path)
        return file_path
    else:
        if os.path.isabs(file_path):
            return "file://" + file_path
        current_dir = os.getcwd()
        resolved_path = os.path.join(current_dir, file_path)
        return "file://" + os.path.abspath(resolved_path)

def fetch_content_from_url(url: str) -> str:
    """
    Fetches the content from a given HTTP/HTTPS URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        raise Exception(f"Error fetching content from URL {url}: {e}")

def read_file_from_url(file_url: str) -> str:
    """
    Reads content from a file:// URL.
    """
    parsed = urllib.parse.urlparse(file_url)
    if parsed.scheme != "file":
        raise Exception(f"Unsupported URL scheme: {parsed.scheme}")
    file_path = parsed.path
    if not os.path.exists(file_path):
        raise Exception(f"File does not exist: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise Exception(f"Error reading file from {file_path}: {e}")

def api_reference_html(options_input: Options) -> str:
    """
    Generates the HTML for the Scalar API Reference based on the provided options.
    
    - If neither spec.url nor spec.content is provided, an exception is raised.
    - If only spec.url is provided, the content is fetched from that URL (or read as a file if a local path).
    - The options are serialized (with escaped double quotes) and injected into a script tag.
    """
    options = options_input

    if not options.spec or (not options.spec.url and not options.spec.content):
        raise Exception("Either 'spec.url' or 'spec.content' must be provided")

    if options.spec and options.spec.content is None and options.spec.url:
        if options.spec.url.startswith("http"):
            content = fetch_content_from_url(options.spec.url)
        else:
            file_url = ensure_file_url(options.spec.url)
            content = read_file_from_url(file_url)
        options.spec.content = content

    data_config = safe_json_configuration(options)
    spec_content_html = specContent_handler(options.spec.content)
    page_title = options.custom_options.page_title or "API Documentation"
    
    custom_theme_css = CUSTOM_THEME_CSS if not options.theme else ""

    html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <title>{page_title}</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style>{custom_theme_css}</style>
      </head>
      <body>
        <script id="api-reference" type="application/json" data-configuration="{data_config}">{spec_content_html}</script>
        <script src="{options.cdn}"></script>
      </body>
    </html>
    """
    return html.strip()
