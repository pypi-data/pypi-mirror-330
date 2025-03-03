"""
IndoxRouter Client - A Python client for the IndoxRouter API
"""

import os
import requests
from typing import Dict, List, Optional, Any, Union


class IndoxRouterClient:
    """
    Client for making API requests to the IndoxRouter API.

    This client allows users to interact with the IndoxRouter API
    to access multiple LLM providers through a unified interface.
    """

    def __init__(self, api_key: str, base_url: str = None):
        """
        Initialize the IndoxRouter client.

        Args:
            api_key: API key for authentication (generated from the IndoxRouter website)
            base_url: Base URL for the API (default: https://api.indoxrouter.com)
        """
        self.api_key = api_key
        self.base_url = base_url or "https://api.indoxrouter.com"
        self.session = requests.Session()
        self.session.headers.update(
            {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        )

        # Verify the API key by making a test request
        self._verify_api_key()

    def _verify_api_key(self):
        """Verify that the API key is valid by making a test request."""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/user")
            response.raise_for_status()
            self.user_data = response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Invalid API key or connection error: {str(e)}")

    def generate(
        self,
        prompt: str,
        model: str = None,
        provider: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Generate a response from a model.

        Args:
            prompt: The prompt to send to the model
            model: The model to use (e.g., "gpt-4", "claude-3-opus")
            provider: The provider to use (e.g., "openai", "anthropic")
            temperature: Controls randomness (0-1)
            max_tokens: Maximum number of tokens to generate
            **kwargs: Additional parameters to pass to the API

        Returns:
            A dictionary containing the response from the API
        """
        if not model and not provider:
            # Use the default model if none specified
            model = "gpt-4o-mini"
            provider = "openai"

        payload = {
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs,
        }

        if model:
            payload["model"] = model
        if provider:
            payload["provider"] = provider

        response = self.session.post(f"{self.base_url}/api/v1/generate", json=payload)
        response.raise_for_status()
        return response.json()

    def list_models(self, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List available models.

        Args:
            provider: Filter models by provider

        Returns:
            A list of available models
        """
        url = f"{self.base_url}/api/v1/models"
        if provider:
            url += f"?provider={provider}"

        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def list_providers(self) -> List[Dict[str, Any]]:
        """
        List available providers.

        Returns:
            A list of available providers
        """
        response = self.session.get(f"{self.base_url}/api/v1/providers")
        response.raise_for_status()
        return response.json()

    def get_balance(self) -> Dict[str, Any]:
        """
        Get the user's current balance.

        Returns:
            A dictionary containing the user's balance information
        """
        response = self.session.get(f"{self.base_url}/api/v1/user/balance")
        response.raise_for_status()
        return response.json()

    def get_user_info(self) -> Dict[str, Any]:
        """
        Get information about the authenticated user.

        Returns:
            A dictionary containing user information
        """
        response = self.session.get(f"{self.base_url}/api/v1/user")
        response.raise_for_status()
        return response.json()
