import re


class URLNotFoundException(Exception):
    """Exception raised when no URL is found in the string."""

    pass


def find_urls_in_string(text: str) -> list[str]:
    """
    Finds all URLs within a given string and returns them as a list.

    This function uses a regular expression to identify URLs within the input string.
    It looks for common URL schemes like http://, https://, ftp://, and file://,
    followed by a domain and potentially a path, query parameters, and fragment.

    If no URL is found, a URLNotFoundException is raised.

    Args:
        text: The input string to search for URLs within.

    Returns:
        list[str]: A list containing all URLs found in the string.

    Raises:
        TypeError: If the input `text` is not a string.
        URLNotFoundException: If no URL is found in the string.

    Examples:
        >>> find_urls_in_string("Visit my website at https://www.example.com for more info.")
        ['https://www.example.com']

        >>> try:
        ...     find_urls_in_string("No URL here.")
        ... except URLNotFoundException:
        ...     print("No URL found!")
        No URL found!

        >>> find_urls_in_string("Check out http://example.org/path/to/resource?query=param#fragment")
        ['http://example.org/path/to/resource?query=param#fragment']

        >>> find_urls_in_string("Download the file from ftp://fileserver.com/pub/document.pdf")
        ['ftp://fileserver.com/pub/document.pdf']

        >>> find_urls_in_string("Local file path: file:///path/to/local/resource.txt")
        ['file:///path/to/local/resource.txt']

        >>> find_urls_in_string("Multiple URLs: https://example.com and http://example.org")
        ['https://example.com', 'http://example.org']

        >>> try:
        ...     find_urls_in_string("")
        ... except URLNotFoundException:
        ...     print("No URL found in empty string!")
        No URL found in empty string!
    """
    if not isinstance(text, str):
        raise TypeError("Input 'text' must be a string.")

    if not text:  # Handle empty strings efficiently
        raise URLNotFoundException("No URL found in empty string!")

    # Regular expression to find URLs
    url_pattern = re.compile(
        r"""
        \b                                  # Start at a word boundary
        (?:                                 # Non-capturing group for schemes
            https?://|                      # http:// or https://
            ftp://|                         # ftp://
            file:///                        # file:/// (local file paths)
        )
        (?:                                 # Non-capturing group for domain and path
            [-a-zA-Z0-9+&@#/%?=~_|!:,.;]*    # Domain, subdomains, and path characters
            [-a-zA-Z0-9+&@#/%=~_|]           # Allow one more character at the end (avoiding trailing punctuation)
        )
        \b                                  # End at a word boundary
        """,
        re.VERBOSE | re.IGNORECASE,
    )

    # Find all matching URLs in the text
    matches = url_pattern.findall(text)
    if matches:
        return matches
    else:
        raise URLNotFoundException(f"No URL found in the string: '{text}'")
