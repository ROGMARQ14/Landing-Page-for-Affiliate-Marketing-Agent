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
        """Initialize API clients using Streamlit secrets with better error handling"""
        self.openai_available = False
        self.anthropic_available = False
        self.gemini_available = False

        # Debug: Show what secrets are available
        try:
            available_secrets = list(st.secrets.keys())
            st.write(f"Debug: Available secrets: {available_secrets}")
        except:
            st.write("Debug: Could not read secrets")

        try:
            # OpenAI - try multiple possible key names
            openai_key = None
            possible_openai_keys = ['OPENAI_API_KEY', 'openai_api_key', 'OPENAI_KEY', 'openai_key']

            for key_name in possible_openai_keys:
                if key_name in st.secrets:
                    openai_key = st.secrets[key_name]
                    break

            if openai_key and OPENAI_AVAILABLE:
                openai.api_key = openai_key
                self.openai_client = openai.OpenAI(api_key=openai_key)
                self.openai_available = True
                st.success("✅ OpenAI API configured successfully")
            elif OPENAI_AVAILABLE:
                st.warning("⚠️ OpenAI library available but API key not found in secrets")
            else:
                st.warning("⚠️ OpenAI library not installed")

        except Exception as e:
            st.error(f"❌ OpenAI setup error: {str(e)}")

        try:
            # Anthropic - try multiple possible key names  
            anthropic_key = None
            possible_anthropic_keys = ['ANTHROPIC_API_KEY', 'anthropic_api_key', 'ANTHROPIC_KEY', 'anthropic_key']

            for key_name in possible_anthropic_keys:
                if key_name in st.secrets:
                    anthropic_key = st.secrets[key_name]
                    break

            if anthropic_key and ANTHROPIC_AVAILABLE:
                self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
                self.anthropic_available = True
                st.success("✅ Anthropic API configured successfully")
            elif ANTHROPIC_AVAILABLE:
                st.info("ℹ️ Anthropic library available but API key not configured")
            else:
                st.info("ℹ️ Anthropic library not installed")

        except Exception as e:
            st.warning(f"⚠️ Anthropic setup warning: {str(e)}")

        try:
            # Google Gemini - try multiple possible key names
            google_key = None
            possible_google_keys = ['GOOGLE_API_KEY', 'google_api_key', 'GEMINI_API_KEY', 'gemini_api_key']

            for key_name in possible_google_keys:
                if key_name in st.secrets:
                    google_key = st.secrets[key_name]
                    break

            if google_key and GOOGLE_AVAILABLE:
                genai.configure(api_key=google_key)
                self.gemini_available = True
                st.success("✅ Google Gemini API configured successfully")
            elif GOOGLE_AVAILABLE:
                st.warning("⚠️ Google AI library available but API key not found in secrets")
            else:
                st.warning("⚠️ Google AI library not installed")

        except Exception as e:
            st.error(f"❌ Google Gemini setup error: {str(e)}")

        # Show final status
        total_available = sum([self.openai_available, self.anthropic_available, self.gemini_available])
        if total_available > 0:
            st.success(f"🎯 {total_available} AI provider(s) configured successfully!")
        else:
            st.error("❌ No AI providers available. Check your API keys in Streamlit secrets.")

    def generate_content(self, prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 4000) -> Dict[str, Any]:
        """Generate content using specified AI model"""

        # Check if any providers are available
        if not (self.openai_available or self.anthropic_available or self.gemini_available):
            return {
                "error": "No AI providers available. Please configure API keys in Streamlit Cloud secrets.",
                "success": False
            }

        # Show which provider will be used
        provider_used = "Unknown"
        if model.startswith('gpt') and self.openai_available:
            provider_used = "OpenAI"
        elif model.startswith('claude') and self.anthropic_available:
            provider_used = "Anthropic"
        elif model.startswith('gemini') and self.gemini_available:
            provider_used = "Google Gemini"

        st.info(f"🤖 Using {provider_used} for content generation...")

        # Try to generate content with retry logic
        for attempt in range(3):
            try:
                if model.startswith('gpt') and self.openai_available:
                    return self._generate_openai(prompt, model, temperature, max_tokens)
                elif model.startswith('claude') and self.anthropic_available:
                    return self._generate_anthropic(prompt, model, temperature, max_tokens)
                elif model.startswith('gemini') and self.gemini_available:
                    return self._generate_gemini(prompt, temperature, max_tokens)
                else:
                    # Fallback to any available provider
                    if self.openai_available:
                        st.info("🔄 Falling back to OpenAI...")
                        return self._generate_openai(prompt, "gpt-4", temperature, max_tokens)
                    elif self.gemini_available:
                        st.info("🔄 Falling back to Gemini...")
                        return self._generate_gemini(prompt, temperature, max_tokens)
                    elif self.anthropic_available:
                        st.info("🔄 Falling back to Anthropic...")
                        return self._generate_anthropic(prompt, "claude-3-5-sonnet-20240620", temperature, max_tokens)
                    else:
                        return {"error": f"No available providers for model {model}", "success": False}

            except Exception as e:
                if attempt == 2:  # Last attempt
                    return {"error": f"Failed after 3 attempts: {str(e)}", "success": False}
                else:
                    time.sleep(random.uniform(1, 3))
                    continue

        return {"error": "Unexpected error in content generation", "success": False}

    def _generate_openai(self, prompt: str, model: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """Generate content using OpenAI models"""
        try:
            response = self.openai_client.chat.completions.create(
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
                "tokens_used": len(response.text) // 4,  # Rough estimate
                "success": True
            }

        except Exception as e:
            return {"error": f"Gemini API error: {str(e)}", "success": False}

    def get_available_models(self) -> list:
        """Return list of available AI models"""
        models = []

        if self.openai_available:
            models.extend([
                "gpt-4",
                "gpt-4-turbo-preview", 
                "gpt-3.5-turbo"
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

    def get_provider_status(self) -> Dict[str, bool]:
        """Get status of all AI providers"""
        return {
            "openai": self.openai_available,
            "anthropic": self.anthropic_available, 
            "gemini": self.gemini_available
        }
