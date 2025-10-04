import streamlit as st
import json
import time
import random
from typing import Dict, Any, Optional

# Import AI providers with error handling
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

class AIManager:
    """Manages communication with multiple AI providers"""

    def __init__(self):
        self.setup_api_clients()

    def setup_api_clients(self):
        """Initialize API clients using Streamlit secrets"""
        self.openai_available = False
        self.anthropic_available = False
        self.gemini_available = False

        try:
            # OpenAI
            if OPENAI_AVAILABLE and 'OPENAI_API_KEY' in st.secrets:
                openai.api_key = st.secrets['OPENAI_API_KEY']
                self.openai_available = True

            # Anthropic
            if ANTHROPIC_AVAILABLE and 'ANTHROPIC_API_KEY' in st.secrets:
                self.anthropic_client = anthropic.Anthropic(api_key=st.secrets['ANTHROPIC_API_KEY'])
                self.anthropic_available = True

            # Google Gemini
            if GOOGLE_AVAILABLE and 'GOOGLE_API_KEY' in st.secrets:
                genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
                self.gemini_available = True

        except Exception as e:
            st.warning(f"⚠️ API setup warning: {str(e)}")

    def generate_content(self, prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 4000) -> Dict[str, Any]:
        """Generate content using specified AI model with error handling and retry logic"""

        # Check if any providers are available
        if not (self.openai_available or self.anthropic_available or self.gemini_available):
            return {
                "error": "No AI providers available. Please configure API keys in Streamlit Cloud secrets.",
                "success": False
            }

        for attempt in range(3):  # Retry up to 3 times
            try:
                if model.startswith('gpt') and self.openai_available:
                    return self._generate_openai(prompt, model, temperature, max_tokens)
                elif model.startswith('claude') and self.anthropic_available:
                    return self._generate_anthropic(prompt, model, temperature, max_tokens)
                elif model.startswith('gemini') and self.gemini_available:
                    return self._generate_gemini(prompt, temperature, max_tokens)
                else:
                    # Fallback to available provider
                    if self.gemini_available:
                        return self._generate_gemini(prompt, temperature, max_tokens)
                    elif self.anthropic_available:
                        return self._generate_anthropic(prompt, "claude-3-5-sonnet-20240620", temperature, max_tokens)
                    elif self.openai_available:
                        return self._generate_openai(prompt, "gpt-4-turbo-preview", temperature, max_tokens)
                    else:
                        return {"error": f"Model {model} not available and no fallback providers configured", "success": False}

            except Exception as e:
                if attempt == 2:  # Last attempt
                    return {"error": f"Failed after 3 attempts: {str(e)}", "success": False}
                else:
                    time.sleep(random.uniform(1, 3))  # Random delay before retry
                    continue

        return {"error": "Unexpected error in content generation", "success": False}

    def _generate_openai(self, prompt: str, model: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """Generate content using OpenAI models"""
        try:
            # Use the new OpenAI client format
            client = openai.OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.9
            )

            content = response.choices[0].message.content

            return {
                "content": content,
                "model_used": model,
                "tokens_used": response.usage.total_tokens,
                "success": True
            }

        except Exception as e:
            return {"error": f"OpenAI API error: {str(e)}", "success": False}

    def _generate_anthropic(self, prompt: str, model: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """Generate content using Anthropic Claude models"""
        try:
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text

            return {
                "content": content,
                "model_used": model,
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
                "success": True
            }

        except Exception as e:
            return {"error": f"Anthropic API error: {str(e)}", "success": False}

    def _generate_gemini(self, prompt: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """Generate content using Google Gemini models"""
        try:
            model = genai.GenerativeModel('gemini-1.5-pro')

            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                top_p=0.9,
                top_k=40
            )

            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )

            return {
                "content": response.text,
                "model_used": "gemini-1.5-pro",
                "tokens_used": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0,
                "success": True
            }

        except Exception as e:
            return {"error": f"Gemini API error: {str(e)}", "success": False}

    def estimate_cost(self, prompt: str, model: str) -> Dict[str, Any]:
        """Estimate cost for generating content with specified model"""

        # Rough token count estimation (1 token ≈ 4 characters for English)
        estimated_input_tokens = len(prompt) // 4
        estimated_output_tokens = 2000  # Average output length

        # Pricing per 1000 tokens (as of 2024)
        pricing = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo-preview": {"input": 0.01, "output": 0.03},
            "claude-3-5-sonnet-20240620": {"input": 0.003, "output": 0.015},
            "gemini-1.5-pro": {"input": 0.0035, "output": 0.0105}
        }

        if model not in pricing:
            return {"error": f"Pricing not available for {model}"}

        input_cost = (estimated_input_tokens / 1000) * pricing[model]["input"]
        output_cost = (estimated_output_tokens / 1000) * pricing[model]["output"] 
        total_cost = input_cost + output_cost

        return {
            "estimated_input_tokens": estimated_input_tokens,
            "estimated_output_tokens": estimated_output_tokens,
            "estimated_cost": round(total_cost, 4),
            "currency": "USD"
        }

    def get_available_models(self) -> list:
        """Return list of available AI models based on configured API keys"""
        models = []

        if self.openai_available:
            models.extend([
                "gpt-4-turbo-preview",
                "gpt-4"
            ])

        if self.anthropic_available:
            models.extend([
                "claude-3-5-sonnet-20240620"
            ])

        if self.gemini_available:
            models.extend([
                "gemini-1.5-pro"
            ])

        return models

    def validate_json_response(self, content: str) -> Dict[str, Any]:
        """Validate and parse JSON response from AI model"""
        try:
            # Try to find JSON content within the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_content = content[start_idx:end_idx]
                parsed_json = json.loads(json_content)

                return {
                    "json_content": parsed_json,
                    "raw_content": content,
                    "valid": True
                }
            else:
                return {
                    "error": "No valid JSON found in response",
                    "raw_content": content,
                    "valid": False
                }

        except json.JSONDecodeError as e:
            return {
                "error": f"JSON parsing error: {str(e)}",
                "raw_content": content,
                "valid": False
            }

    def get_provider_status(self) -> Dict[str, bool]:
        """Get status of all AI providers"""
        return {
            "openai": self.openai_available,
            "anthropic": self.anthropic_available, 
            "gemini": self.gemini_available
        }
