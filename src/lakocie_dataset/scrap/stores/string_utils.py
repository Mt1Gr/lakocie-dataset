from urllib.parse import urlparse
from .store_definitions import StoreChoice


def product_name_from_url(url: str, store_choice: StoreChoice):
    """Extract the product name from a URL based on the store choice."""
    match store_choice:
        case StoreChoice.KF:
            # Parse the URL, e.g., 'https://example.com/products/item123'
            parsed_url = urlparse(url)
            # Get the path of the URL, e.g., '/products/item123'
            path = parsed_url.path
            # Split the path by '/', e.g., ['', 'products', 'item123']
            path_split = path.split("/")
            # Get the last element of the split path, e.g., 'item123'
            product_name = path_split[-1]
            return product_name
        case _:
            raise ValueError(f"Unsupported store choice: {store_choice}")


def add_base_url_in_return(base_url: str):
    """A decorator that adds a base URL to the return value of a function.

    This decorator prepends a base URL to the return value of the decorated function,
    ensuring proper URL path formatting by removing trailing slashes from the base URL
    and leading slashes from the return value.

    Args:
        base_url (str): The base URL to prepend to the function's return value.

    Returns:
        callable: A decorator function that wraps the original function.

    Example:
        ```
        @add_base_url_in_return('https://example.com')
        def get_path():
            return '/api/data'
        # Returns: 'https://example.com/api/data'
        ```

    Note:
        - If the decorated function returns None, the decorator will also return None.
        - The decorator handles URL path formatting to avoid double slashes.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            no_base_url = func(*args, **kwargs)
            if no_base_url is None:
                return None
            return f"{base_url.rstrip('/')}/{no_base_url.lstrip('/')}"

        return wrapper

    return decorator
