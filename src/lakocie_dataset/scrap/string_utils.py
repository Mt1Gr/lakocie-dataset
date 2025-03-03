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
        @add_base_url_in_return('https://example.com')
        def get_path():
            return '/api/data'
        # Returns: 'https://example.com/api/data'

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
