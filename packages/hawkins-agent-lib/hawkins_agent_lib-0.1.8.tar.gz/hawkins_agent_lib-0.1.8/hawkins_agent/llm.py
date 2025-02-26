"""LLM integration using lite_llm

This module handles the interaction with language models through lite_llm,
providing a consistent interface for model management and response parsing.
"""

from typing import Dict, Any, List, Optional
import json
import logging
from .mock import LiteLLM
from .types import Message, MessageRole

logger = logging.getLogger(__name__)

class LLMManager:
    """Manages LLM interactions and response parsing"""

    def __init__(self, model: str = "gpt-3.5-turbo"):
        """Initialize the LLM manager

        Args:
            model: The name of the LLM model to use
        """
        self.model = model
        self.llm = LiteLLM(model=model)

    async def generate_response(self, 
                              messages: List[Message],
                              tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Generate a response from the LLM

        Args:
            messages: List of conversation messages
            tools: Optional list of available tools

        Returns:
            The generated response including content and potential tool calls
        """
        try:
            # Log the incoming request
            logger.info("Starting response generation")
            logger.info(f"Generating response with model: {self.model}")

            # Format messages for the provider
            formatted_messages = []
            for msg in messages:
                formatted_messages.append({
                    "role": msg.role.value,
                    "content": msg.content
                })

            # Log the request being sent
            logger.info("Sending request to LiteLLM")
            if tools:
                logger.info(f"With {len(tools)} available tools")

            # Generate response
            response = await self.llm.generate(formatted_messages)

            # Log response received
            logger.info("Received response from LLM")
            if isinstance(response, dict):
                logger.info(f"Response structure: {list(response.keys())}")

            return response

        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}", exc_info=True)
            raise