"""Base configuration for AI models."""

import os
from typing import Dict, Optional
import google.generativeai as genai
from rich import print


class BaseGenerativeModel:
    _instance = None
    _model = None

    @classmethod
    def get_instance(cls) -> 'BaseGenerativeModel':
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initialize the base model configuration."""
        self._setup_model()

    def _setup_model(self):
        """Configure and setup the AI model."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("[red]Error: GEMINI_API_KEY environment variable not found![/red]")
            print("[yellow]Please set your Gemini API key using:[/yellow]")
            print("[yellow]export GEMINI_API_KEY='your-api-key'[/yellow]")
            raise ValueError("GEMINI_API_KEY not found")

        try:
            genai.configure(api_key=api_key)
            self._model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                generation_config=self.default_generation_config()
            )
            print("[green]Gemini API configured successfully![/green]")
        except Exception as e:
            print(f"[red]Error configuring Gemini API: {e}[/red]")
            raise

    @staticmethod
    def default_generation_config() -> Dict:
        """Get default generation configuration."""
        return {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 1024,
        }

    def get_model(self, custom_config: Optional[Dict] = None) -> genai.GenerativeModel:
        """Get the configured model instance."""
        if custom_config:
            return genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                generation_config=custom_config
            )
        return self._model 