"""RAG tool implementation using HawkinsRAG"""

from typing import Dict, Any, Optional
from hawkins_rag import HawkinsRAG
from .base import BaseTool
from ..types import ToolResponse
import logging
import tempfile
import os
import json
import traceback

logger = logging.getLogger(__name__)

class RAGTool(BaseTool):
    """Tool for retrieving information from knowledge base using HawkinsRAG"""

    def __init__(self, 
                 knowledge_base: HawkinsRAG,
                 max_results: int = 5,
                 min_relevance_score: float = 0.7):
        """Initialize RAG tool

        Args:
            knowledge_base: HawkinsRAG instance for document storage and retrieval
            max_results: Maximum number of results to return
            min_relevance_score: Minimum relevance score for results
        """
        super().__init__(name="RAGTool")
        self.kb = knowledge_base
        self.max_results = max_results
        self.min_relevance_score = min_relevance_score

    @property
    def description(self) -> str:
        return """Query the knowledge base for relevant information."""

    async def execute(self, **kwargs) -> ToolResponse:
        """Query the knowledge base

        Args:
            query: Search query string

        Returns:
            ToolResponse with search results
        """
        try:
            query = kwargs.get('query', '')
            if not query:
                logger.error("Empty query received")
                return ToolResponse(
                    success=False,
                    result=None,
                    error="Query cannot be empty"
                )

            logger.info(f"Executing query on knowledge base: {query}")

            try:
                # Query the knowledge base
                logger.debug("Sending query to HawkinsRAG...")
                results = self.kb.query(query)
                logger.debug(f"Received raw results type: {type(results)}")
                logger.debug(f"Raw results: {json.dumps(results, indent=2)}")

                # Format results for agent consumption
                formatted_results = []

                if isinstance(results, dict):
                    # Handle structured response format
                    logger.info(f"Processing structured response, keys: {list(results.keys())}")

                    # Extract actual results from response structure
                    if 'results' in results:
                        results = results['results']
                    elif 'response' in results:
                        if isinstance(results['response'], str):
                            results = {'content': results['response']}
                        else:
                            results = results['response']
                    elif 'message' in results:
                        results = {'content': results['message']}

                # Convert results to list if single result
                result_list = results if isinstance(results, list) else [results]

                for result in result_list[:self.max_results]:
                    try:
                        # Handle different result formats
                        if isinstance(result, str):
                            content = result
                        elif isinstance(result, dict):
                            content = result.get('content', str(result))
                        else:
                            content = str(result)

                        formatted_results.append({
                            'content': content,
                            'relevance': 1.0,  # Default score
                            'source': 'knowledge_base'
                        })
                    except Exception as format_error:
                        logger.error(f"Error formatting result: {str(format_error)}")
                        continue

                logger.info(f"Processed {len(formatted_results)} results")

                return ToolResponse(
                    success=True,
                    result={
                        'query': query,
                        'results': formatted_results
                    },
                    error=None
                )

            except Exception as query_error:
                error_msg = f"Query execution failed: {str(query_error)}\n{traceback.format_exc()}"
                logger.error(error_msg)
                return ToolResponse(
                    success=False,
                    result=None,
                    error=error_msg
                )

        except Exception as e:
            error_msg = f"RAG tool execution failed: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            return ToolResponse(
                success=False,
                result=None,
                error=error_msg
            )

    async def add_document(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Add a document to the knowledge base

        Args:
            content: Document content to add
            metadata: Optional metadata about the document

        Returns:
            bool indicating success
        """
        temp_file = None
        try:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
            temp_file.write(content)
            temp_file.close()

            logger.info(f"Adding document with content length: {len(content)}")
            if metadata:
                logger.info(f"Document metadata: {json.dumps(metadata)}")

            # Load document into knowledge base
            self.kb.load_document(temp_file.name, source_type="text")
            logger.info("Successfully added document to knowledge base")
            return True

        except Exception as e:
            logger.error(f"Failed to add document: {str(e)}\n{traceback.format_exc()}")
            return False

        finally:
            # Clean up temporary file
            if temp_file and os.path.exists(temp_file.name):
                try:
                    os.unlink(temp_file.name)
                except Exception as e:
                    logger.error(f"Failed to clean up temporary file: {str(e)}")