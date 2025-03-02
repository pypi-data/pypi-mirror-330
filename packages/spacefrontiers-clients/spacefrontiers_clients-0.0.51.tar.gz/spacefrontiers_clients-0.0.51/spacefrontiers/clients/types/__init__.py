import time
import typing
from datetime import datetime
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer

StrBool = Annotated[
    bool, PlainSerializer(lambda x: str(x), return_type=str, when_used="unless-none")
]
ModelName = Literal[
    "deepseek-ai/DeepSeek-R1",
    "meta-llama/llama-3.3-70b-versatile",
    "anthropic/claude-3.7-sonnet",
    "qwen/qwen-2.5-72b-instruct",
]


class Snippet(BaseModel):
    """A class representing a text snippet from a document.

    Attributes:
        field (str): The field name from which the snippet was extracted
        text (str): The actual text content of the snippet
        payload (dict | None): Additional metadata associated with the snippet
        score (float): Relevance or ranking score of the snippet
        snippet_id (str | None): Unique identifier for the snippet
    """

    field: str
    text: str
    payload: dict | None = None
    score: float = 0.0
    snippet_id: str | None = None


class SearchDocument(BaseModel):
    """A class representing a search result document containing snippets.

    Attributes:
        source (str): The source identifier of the document
        document (dict): The complete document data
        snippets (list[Snippet]): List of relevant snippets from the document
        score (float): Overall relevance or ranking score of the document
    """

    source: str
    document: dict
    snippets: list[Snippet]
    score: float = 0.0

    def join_snippet_texts(self, separator: str = " <...> ") -> str:
        """Joins the text of multiple snippets with intelligent separators.

        Consecutive snippets (based on chunk_id) are joined with a space,
        while non-consecutive snippets are joined with the specified separator.

        Args:
            separator (str): The separator to use between non-consecutive snippets.
                Defaults to " <...> ".

        Returns:
            str: The concatenated snippet texts with appropriate separators.
        """
        parts = []
        for i, snippet in enumerate(self.snippets):
            if i > 0:
                if (
                    self.snippets[i - 1].payload["chunk_id"] + 1
                    == self.snippets[i].payload["chunk_id"]
                ):
                    parts.append(" ")
                else:
                    parts.append(separator)
            parts.append(snippet.text)
        return "".join(parts)


class StorageSearchRequest(BaseModel):
    """A class representing a search request configuration.

    Attributes:
        query (str | None): The search query string
        source (str): The data source to search in
        query_language (str | None): Language of the query for language-specific processing
        limit (int): Maximum number of results to return (0-16384)
        offset (int): Number of results to skip for pagination (0-16384)
        filters (dict[str, list[Any]]): Dictionary of filters to apply to the search
        snippet_configs (dict[str, int]): Configuration for snippet sizes by field
        fields (list[str] | None): Specific fields to include in the search
        excluded_fields (list[str] | None): Fields to exclude from the search
        scoring (Literal): Scoring method to use ("default", "temporal", "pr", "quantized_pr")
        collector (Literal): Collection method ("top_docs" or "reservoir_sampling")
        term_field_mapping (dict[str, dict[str, list[str]]] | None): Custom mapping of terms to fields
    """

    query: str | None
    source: str
    query_language: str | None = None
    limit: int = Field(default=10, ge=0, le=1024 * 16)
    offset: int = Field(default=0, ge=0, le=1024 * 16)
    filters: dict[str, list[Any]] | None = None
    snippet_configs: dict[str, int] = Field(
        default_factory=lambda: {
            "title": 1024,
            "abstract": 1024,
            "content": 1024,
        }
    )
    fields: list[str] | None = None
    excluded_fields: list[str] | None = None
    scoring: Literal["default", "temporal", "pr", "quantized_pr"] = "default"
    collector: Literal["top_docs", "reservoir_sampling"] = "top_docs"
    term_field_mapping: dict[str, dict[str, list[str]]] | None = None


class SearchResponse(BaseModel):
    """A class representing the response from a search request.

    Attributes:
        search_documents (list[SearchDocument]): List of retrieved documents with their snippets
        count (int): Total number of results found
        has_next (bool): Whether there are more results available

    Methods:
        empty_response(): Creates and returns an empty search response
    """

    search_documents: list[SearchDocument]
    count: int
    has_next: bool
    total_count: int | None = None

    @staticmethod
    def empty_response() -> "SearchResponse":
        return SearchResponse(
            search_documents=[],
            count=0,
            has_next=False,
        )


class BaseChunk(BaseModel):
    """A class representing a base chunk of text from a document.

    Attributes:
        document_id (str): Unique identifier for the source document
        field (str): The field name containing the chunk
        chunk_id (int): Sequential identifier for the chunk within the document
        start_index (int): Starting character position of the chunk in the field
        length (int): Length of the chunk in characters
        metadata (dict): Additional metadata associated with the chunk
        updated_at (int): Timestamp of when the chunk was last updated
    """

    document_id: str
    field: str
    chunk_id: int
    start_index: int
    length: int
    metadata: dict
    updated_at: int = Field(default_factory=lambda: int(time.time()))

    def get_unique_id(self) -> str:
        """Generates a unique identifier for the chunk.

        Returns:
            str: A unique string identifier combining document_id, field, and chunk_id
                in the format 'document_id@field@chunk_id'
        """
        return f"{self.document_id}@{self.field}@{self.chunk_id}"


class PreparedChunk(BaseChunk):
    """A prepared chunk that includes the actual text content.

    Attributes:
        text (str): The text content of the chunk
    """

    text: str


class LlmConfig(BaseModel):
    """Configuration for the Language Learning Model.

    Attributes:
        model_name (ModelName): Name of the LLM model to use
        api_key (str | None): API key for accessing the model
        max_context_length (int | None): Maximum context length for the model
    """

    model_name: ModelName = "meta-llama/llama-3.3-70b-versatile"
    api_key: str | None = None
    max_context_length: int | None = None

    model_config = ConfigDict(protected_namespaces=tuple())


class Range(BaseModel):
    """A class representing a numeric range with left and right bounds.

    Attributes:
        left (int): The lower bound of the range
        right (int): The upper bound of the range
    """

    left: int
    right: int


class Query(BaseModel):
    """A class representing a search query with various metadata and processing options.

    Attributes:
        original_query (str | None): The original user query
        reformulated_query (str | None): The processed or reformulated query
        keywords (list[str]): Extracted or relevant keywords
        ids (list[str]): Related document IDs
        is_recent (bool): Flag for recent content queries
        date (tuple[datetime, datetime] | None): Date range for temporal queries
        content_type (str | None): Type of content to search for
        related_queries (list[str]): List of related search queries
        query_language (str | None): Two-letter language code of the query
        instruction (str | None): User instruction on how to render answer
        knowledge_source (Literal["search", "no_search", "research", "specified_document"]):
            The source of knowledge for the query (default: "search")
        representation (Literal["serp", "qa", "digest", "summary"]):
            Format for displaying results (default: "serp")
    """

    original_query: str | None = None
    reformulated_query: str | None = None
    keywords: list[str] = Field(default_factory=list)
    ids: list[str] = Field(default_factory=list)
    is_recent: bool = False
    date: tuple[datetime, datetime] | None = None
    content_type: str | None = None
    related_queries: list[str] = Field(default_factory=list)
    query_language: str | None = None
    instruction: str | None = None
    knowledge_source: Literal[
        "search", "no_search", "research", "specified_document"
    ] = Field(default="search")
    representation: Literal["serp", "qa", "digest", "summary"] = Field(default="serp")
    classified_aspects: list[str] = Field(default_factory=list)

    @staticmethod
    def default_query(query: str | None) -> "Query":
        """Creates a default Query object with minimal configuration.

        Args:
            query (str | None): The query string to use for both original and reformulated fields

        Returns:
            Query: A new Query object with basic configuration
        """
        return Query(
            original_query=query,
            reformulated_query=query,
        )

    def __format__(self, __format_spec: str) -> str:
        return str(self)

    def __str__(self) -> str:
        if self.reformulated_query:
            return str(self.reformulated_query)
        elif self.original_query:
            return str(self.original_query)
        else:
            return "<no-query>"


class QueryClassifierConfig(BaseModel):
    """Configuration for query classification.

    Attributes:
        related_queries (int): Number of related queries to generate (default: 0)
        llm_config (LlmConfig | None): Language model configuration for classification
    """

    related_queries: int = 0


class ConversationRequest(BaseModel):
    """A class representing a conversation request with an identifier and query.

    Attributes:
        id (str): Unique identifier for the conversation
        query (str): The query or message text for the conversation
        sources (list[str]): The list of sources to use
        llm_config (LlmConfig): Language model configuration
    """

    id: str
    query: str
    sources: list[str] | None = None
    llm_config: LlmConfig = Field(default_factory=LlmConfig)


class ConversationResponse(BaseModel):
    """Response from the search and processing conversation.

    Attributes:
        id (str): Unique identifier for the conversation
        answer (str): The answer to the query
        search_documents (list[SearchDocument]): List of retrieved and processed documents
        text_related_queries: (list[dict[str, str]]): Substrings that may be highlighted
        query (Query | None): Processed query information
    """

    id: str
    answer: str
    search_documents: list[SearchDocument]
    text_related_queries: list[dict[str, str]] = Field(default_factory=lambda: [])
    query: Query | None = None


class SearchRequest(BaseModel):
    """A class representing a search request with configuration options.

    Attributes:
        query (str): The search query string
        sources (list[str] | None): List of data sources to search in
        filters (dict[str, typing.Any] | None): Dictionary of filters to apply to the search
        possible_languages (list[str] | None): Possible languages of the user for language-specific processing
        query_classifier (QueryClassifierConfig | None): Configuration for query classification
    """

    query: str
    sources: list[str] | None = None
    filters: dict[str, typing.Any] | None = None
    possible_languages: list[str] | None = None
    query_classifier: QueryClassifierConfig | None = None
