"""Webson Module

This module provides the main functionality for the Webson package,
which leverages the IntelliBricks framework and Playwright to transform
raw webpage content into structured data using an underlying Language Model (LLM).

Key Components:
    - Webson: The main class offering methods to retrieve webpage content and "cast" it to a structured format.
    - Asynchronous and synchronous methods: Use Playwright for headless browser automation and IntelliBricks for LLM integration.

Usage Example:
    >>> from intellibricks.llms import Synapse
    >>> from webson import Webson
    >>>
    >>> # Create a Webson instance with a Synapse LLM
    >>> llm = Synapse.of("google/genai/gemini-pro-experimental")
    >>> webson = Webson(llm=llm, timeout=5000)
    >>>
    >>> # Retrieve the HTML content of a webpage synchronously
    >>> html = webson.get_contents("https://example.com")
    >>> print(html)
    >>>
    >>> # Cast the webpage to a structured data model
    >>> import msgspec
    >>> class PageSummary(msgspec.Struct):
    ...     title: str
    ...     description: str
    >>>
    >>> summary = webson.cast("https://example.com", to=PageSummary)
    >>> print(summary)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast, Any, Sequence

import msgspec
from architecture import log
from architecture.utils.functions import run_sync
from intellibricks.llms import Synapse, SynapseCascade, SynapseProtocol
from intellibricks.llms.util import get_struct_from_schema
from markdownify import markdownify as md
from playwright.async_api import async_playwright, Browser
from playwright.async_api._generated import Playwright as AsyncPlaywright

from ._const import SYSTEM_PROMPT
from ._types import JsonSchema
from ._functions import find_urls_in_string

if TYPE_CHECKING:
    from openai import OpenAI

# Create a debug logger for internal tracing
debug_logger = log.create_logger(__name__, level=log.DEBUG)


class Webson(msgspec.Struct):
    """
    A class for extracting webpage contents and converting them into structured data using an LLMs.

    Attributes:
        llm (SynapseProtocol):
            The underlying LLM interface used for generating structured outputs.
        timeout (int | None):
            Optional timeout (in milliseconds) for page loads in Playwright.
    """

    llm: SynapseProtocol
    """The synapse weaver used to perform its operations."""

    timeout: int | None = None
    """Timeout (in milliseconds) to use for page loads. If None, the default timeout is used."""

    @classmethod
    def create(cls, llm: SynapseProtocol | OpenAI | None) -> Webson:
        """
        Creates a Webson instance from an LLM instance.

        This factory method accepts an instance of either Synapse, SynapseCascade, or OpenAI.
        When an OpenAI instance is provided, it wraps it as a Synapse using the 'gpt-4o' model.

        Args:
            llm (SynapseProtocol | OpenAI): The LLM instance to be used.

        Returns:
            Webson: A new instance of Webson configured with the appropriate llm.

        Example:
            >>> from intellibricks.llms import Synapse
            >>> from webson import Webson
            >>> llm = Synapse.of("google/genai/gemini-pro-experimental")
            >>> webson = Webson.create(llm)
        """
        match llm:
            case Synapse():
                _llm = llm
            case SynapseCascade():
                _llm = llm
            case OpenAI():
                _llm = Synapse(model="gpt-4o", api_key=llm.api_key)
        # Return a new Webson instance (assuming additional initialization as needed)
        return cls(llm=_llm)

    def get_contents(self, url: str) -> str:
        """
        Synchronously retrieves the entire HTML content of a webpage.

        Internally, this method calls the asynchronous version (`get_contents_async`)
        and blocks until the content is retrieved.

        Args:
            url (str): The URL of the webpage to retrieve.

        Returns:
            str: The HTML content of the webpage.

        Example:
            >>> html = webson.get_contents("https://example.com")
            >>> print(html)
        """
        return run_sync(self.get_contents_async, url)

    async def get_contents_async(self, url: str, browser: Browser | None = None) -> str:
        """
        Asynchronously retrieves the entire HTML content of a webpage using Playwright.

        This method launches a headless Chromium browser (if browser not provided), opens a new page,
        navigates to the specified URL, and returns the page's HTML content.

        Args:
            url (str): The URL of the webpage to retrieve.
            browser (Browser | None): Optional Playwright browser instance to reuse.

        Returns:
            str: The HTML content of the webpage.

        Example:
            >>> contents = await webson.get_contents_async("https://example.com")
            >>> print(contents)
        """
        if browser is None:
            async with async_playwright() as p:
                contents = await self._get_contents(url, p)
                debug_logger.debug(f"Page contents: {contents[:100]}")
                return contents
        else:
            contents = await self._get_contents_with_browser(url, browser)
            debug_logger.debug(f"Page contents: {contents[:100]}")
            return contents

    async def _get_contents(self, url: str, playwright: AsyncPlaywright) -> str:
        """Helper method to handle content retrieval with a new Playwright instance."""
        chromium = playwright.chromium
        browser = await chromium.launch(headless=True)
        try:
            return await self._get_contents_with_browser(url, browser)
        finally:
            await browser.close()

    async def _get_contents_with_browser(self, url: str, browser: Browser) -> str:
        """Helper method to retrieve content using an existing browser instance."""
        page = await browser.new_page()
        try:
            await page.goto(url, timeout=self.timeout)
            debug_logger.debug("Getting page contents")
            return await page.content()
        finally:
            await page.close()

    def cast[T: msgspec.Struct](
        self, typ: type[T], url: str, *, browser: Browser | None = None, details: str | None = None
    ) -> T:
        """
        Synchronously casts a webpage's content into a structured output.

        This method retrieves the page's HTML content, converts it to markdown,
        and then invokes the underlying LLM (via `cast_async`) to produce structured data.

        Args:
            url (str): The URL of the webpage to cast.
            to (type[T]): The msgspec.Struct subclass type that defines the desired output schema.

        Returns:
            T: An instance of the structured output as defined by the `to` type.

        Example:
            >>> import msgspec
            >>> class PageData(msgspec.Struct):
            ...     title: str
            ...     content: str
            >>> data = webson.cast("https://example.com", to=PageData)
            >>> print(data.title)
        """
        return run_sync(self.cast_async, typ, url, browser=browser, details=details)

    async def cast_async[T: msgspec.Struct](
        self, typ: type[T], url: str, *, browser: Browser | None = None, details: str | None = None
    ) -> T:
        """
        Asynchronously casts a webpage's content into a structured output.

        The method performs the following steps:
            1. Retrieves the raw HTML content of the specified URL.
            2. Converts the HTML content to markdown for improved text processing.
            3. Uses the underlying LLM to generate a structured output based on the provided schema.

        Args:
            typ (type[T]): The msgspec.Struct subclass type defining the desired output structure.
            url (str): The URL of the webpage to cast.

        Returns:
            T: An instance of the structured output as defined by the `to` type.

        Example:
            >>> structured_data = await webson.cast_async(PageData, "https://example.com")
            >>> print(structured_data)
        """
        # Retrieve the raw HTML page contents asynchronously.
        page_contents = await self.get_contents_async(url, browser=browser)

        # Convert the HTML to markdown for easier parsing.
        page_md = cast(str, md(page_contents))
        
        extra = f"## Extra details: \n\n {details}" if details else ""

        # Use the LLM to generate a structured response based on the markdown.
        completion = await self.llm.complete_async(
            f"<page>\n\n{page_md}\n\n</page> \n\n {extra}",
            system_prompt=SYSTEM_PROMPT,
            response_model=typ,
            timeout=self.timeout
        )
        return completion.parsed

    def suggest_schema_from_query(self, query: str) -> dict[str, Any]:
        """
        Synchronously extracts a structured JSON schema from a user's query.

        Given a query (e.g., "go to https://amazon.com and give me title, price, category
        of each product on the homepage"), this method asks the LLM to generate a JSON schema
        that defines the expected output structure (without including URLs).

        Args:
            query (str): The natural language query describing the desired data extraction.

        Returns:
            dict[str, Any]: A JSON schema as a Python dictionary.

        Example:
            >>> schema = webson.suggest_schema_from_query(
            ...     "go to https://amazon.com and extract title, price, and category for each product"
            ... )
            >>> print(schema)
        """
        return run_sync(self.suggest_schema_from_query_async, query)

    async def suggest_schema_from_query_async(self, query: str) -> dict[str, Any]:
        """
        Asynchronously extracts a structured JSON schema from a user's query.

        This method sends the query to the LLM with a system prompt that instructs
        it to analyze the query and generate a JSON schema that represents the desired structure.
        If the query contains a URL (e.g., "go to https://amazon.com"), that URL is omitted from the schema.

        Args:
            query (str): The natural language query describing the desired extraction.

        Returns:
            dict[str, Any]: A JSON schema as a Python dictionary.

        Example:
            >>> schema = await webson.suggest_schema_from_query_async(
            ...     "go to https://amazon.com and list title, price, and category of products"
            ... )
            >>> print(schema)
        """
        completion = self.llm.complete(
            f"<query>\n\n{query}\n\n</query>",
            system_prompt=(
                "You are a helpful assistant. Your task is to analyse the user query and try to extract "
                "a structured json schema based on what the user is asking for. If you find an url in the query, "
                'like "go to https://...", you should not include this url in the final schema.'
            ),
            response_model=JsonSchema,
        )

        json_schema = completion.parsed.schema
        return json_schema

    def query_to_struct(self, query: str) -> Sequence[tuple[str, type[msgspec.Struct]]]:
        """
        Synchronously performs a high-level cast operation based on a natural language query.

        This method allows the user to describe what data they need from one or more websites.
        It automatically extracts URLs, generates a JSON schema from the query, and casts each webpage
        into a structured output. For more granular control, consider using `cast`/`cast_async` directly.

        Args:
            query (str): A natural language query that includes one or more URLs and specifies the desired data fields.

        Returns:
            Sequence[tuple[str, type[msgspec.Struct]]]:
                A sequence of tuples, each containing:
                    - a URL (str) extracted from the query, and
                    - the corresponding structured output (an instance of a msgspec.Struct subclass).

        Example:
            >>> results = webson.query_to_struct(
            ...     "Extract product details (title, price, rating) from https://amazon.com and https://walmart.com."
            ... )
            >>> for url, output in results:
            ...     print(url, output)
        """
        return run_sync(self.query_to_struct_async, query)

    async def query_to_struct_async(
        self, query: str
    ) -> Sequence[tuple[str, type[msgspec.Struct]]]:
        """
        Asynchronously performs a high-level cast operation based on a natural language query.

        The method follows these steps:
            1. Extracts a JSON schema from the query using the underlying LLM.
            2. Converts the JSON schema into a `msgspec.Struct` subclass via `get_struct_from_schema`.
            3. Extracts all URLs present in the query using `find_urls_in_string`.
            4. For each URL, retrieves the webpage content and casts it into the structured format using `cast_async`.

        The final result is a sequence of tuples, each containing the URL and its corresponding structured output.

        Args:
            query (str): A natural language query specifying one or more URLs and the desired output structure.

        Returns:
            Sequence[tuple[str, type[msgspec.Struct]]]:
                A sequence of tuples where each tuple consists of:
                    - a URL (str) extracted from the query, and
                    - the structured output (an instance of a msgspec.Struct subclass) obtained from that URL.

        Example:
            >>> results = await webson.query_to_struct_async(
            ...     "Extract product info (title, price, rating) from https://amazon.com."
            ... )
            >>> for url, output in results:
            ...     print(url, output)
        """
        # Extract the JSON schema from the query.
        # (Make sure that 'suggest_schema_from_query' is implemented or use 'suggest_schema_from_query' instead.)
        json_schema = self.suggest_schema_from_query(query)
        struct: type[msgspec.Struct] = get_struct_from_schema(json_schema)
        # Extract the URLs from the query using a helper function.
        urls = find_urls_in_string(query)
        # Retrieve and cast the webpage asynchronously.
        casted = [(url, await self.cast_async(url, to=struct)) for url in urls]
        return casted
