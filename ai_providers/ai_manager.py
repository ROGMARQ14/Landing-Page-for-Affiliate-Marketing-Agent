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
        """Initialize API clients using Streamlit secrets - handles nested structure"""
        self.openai_available = False
        self.anthropic_available = False
        self.gemini_available = False

        # Debug: Show what secrets are available
        try:
            available_secrets = list(st.secrets.keys())
            st.write(f"🔍 Debug: Top-level secrets: {available_secrets}")

            # Check if we have nested secrets
            if 'secrets' in st.secrets:
                nested_secrets = list(st.secrets['secrets'].keys())
                st.write(f"🔍 Debug: Nested secrets found: {nested_secrets}")

        except Exception as e:
            st.error(f"Debug: Could not read secrets: {str(e)}")

        # Try to get API keys from different possible locations
        openai_key = self._get_secret_key(['OPENAI_API_KEY', 'openai_api_key', 'OPENAI_KEY', 'openai_key'])
        google_key = self._get_secret_key(['GOOGLE_API_KEY', 'google_api_key', 'GEMINI_API_KEY', 'gemini_api_key'])
        anthropic_key = self._get_secret_key(['ANTHROPIC_API_KEY', 'anthropic_api_key', 'ANTHROPIC_KEY', 'anthropic_key'])

        # Setup OpenAI
        try:
            if openai_key and OPENAI_AVAILABLE:
                self.openai_client = openai.OpenAI(api_key=openai_key)
                self.openai_available = True
                st.success("✅ OpenAI API configured successfully")
            elif OPENAI_AVAILABLE:
                st.warning("⚠️ OpenAI library available but API key not found")
            else:
                st.info("ℹ️ OpenAI library not installed")
        except Exception as e:
            st.error(f"❌ OpenAI setup error: {str(e)}")

        # Setup Google Gemini
        try:
            if google_key and GOOGLE_AVAILABLE:
                genai.configure(api_key=google_key)
                self.gemini_available = True
                st.success("✅ Google Gemini API configured successfully")
            elif GOOGLE_AVAILABLE:
                st.warning("⚠️ Google AI library available but API key not found")
            else:
                st.info("ℹ️ Google AI library not installed")
        except Exception as e:
            st.error(f"❌ Google Gemini setup error: {str(e)}")

        # Setup Anthropic
        try:
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

        # Final status
        total_available = sum([self.openai_available, self.anthropic_available, self.gemini_available])
        if total_available > 0:
            st.success(f"🎯 {total_available} AI provider(s) configured successfully!")
        else:
            st.error("❌ No AI providers available. Please check your API keys in Streamlit secrets.")

            # Show helpful error message
            st.markdown("""
            ### 🔧 How to Fix This:

            **Option 1: Fix Your Streamlit Secrets (RECOMMENDED)**
            1. Go to your Streamlit Cloud app settings
            2. Click on "Secrets" tab
            3. Instead of nested structure, use flat structure:

            ```
            OPENAI_API_KEY = "sk-your-openai-key-here"
            GOOGLE_API_KEY = "your-google-key-here"
            ```

            **Option 2: Check Your Current Secrets**
            - Make sure you're not wrapping keys in quotes or nested objects
            - Each key should be on its own line
            - No extra formatting or brackets
            """)

    def _get_secret_key(self, possible_keys: list) -> Optional[str]:
        """Try to get API key from different possible locations"""

        # First try top-level secrets
        for key_name in possible_keys:
            try:
                if key_name in st.secrets:
                    key_value = st.secrets[key_name]
                    if key_value:  # Make sure it's not empty
                        st.write(f"✅ Found {key_name} at top level")
                        return str(key_value)
            except:
                continue

        # Then try nested secrets
        try:
            if 'secrets' in st.secrets:
                nested = st.secrets['secrets']
                for key_name in possible_keys:
                    if key_name in nested:
                        key_value = nested[key_name]
                        if key_value:  # Make sure it's not empty
                            st.write(f"✅ Found {key_name} in nested secrets")
                            return str(key_value)
        except:
            pass

        # Not found anywhere
        st.warning(f"⚠️ Could not find any of these keys: {possible_keys}")
        return None

    def generate_content(self, prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 4000) -> Dict[str, Any]:
        """Generate content using specified AI model"""

        # Check if any providers are available
        if not (self.openai_available or self.anthropic_available or self.gemini_available):
            return {
                "error": "No AI providers available. Please configure API keys in Streamlit Cloud secrets.",
                "success": False
            }

        # Try to generate content
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
                        return self._generate_openai(prompt, "gpt-4", temperature, max_tokens)
                    elif self.gemini_available:
                        return self._generate_gemini(prompt, temperature, max_tokens)
                    elif self.anthropic_available:
                        return self._generate_anthropic(prompt, "claude-3-5-sonnet-20240620", temperature, max_tokens)
                    else:
                        return {"error": "No available providers", "success": False}

            except Exception as e:
                if attempt == 2:  # Last attempt
                    return {"error": f"Failed after 3 attempts: {str(e)}", "success": False}
                else:
                    time.sleep(random.uniform(1, 3))
                    continue

        return {"error": "Unexpected error", "success": False}

    def _generate_openai(self, prompt: str, model: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """Generate content using OpenAI"""
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
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

    def _generate_gemini(self, prompt: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """Generate content using Gemini"""
        try:
            model = genai.GenerativeModel('gemini-1.5-pro')

            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )

            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )

            return {
                "content": response.text,
                "model_used": "gemini-1.5-pro",
                "tokens_used": len(response.text) // 4,
                "success": True
            }

        except Exception as e:
            return {"error": f"Gemini API error: {str(e)}", "success": False}

    def _generate_anthropic(self, prompt: str, model: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """Generate content using Anthropic"""
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
                "success": False
            }

        except Exception as e:
            return {"error": f"Anthropic API error: {str(e)}", "success": False}

    def get_available_models(self) -> list:
        """Return available models"""
        models = []

        if self.openai_available:
            models.extend(["gpt-4", "gpt-3.5-turbo"])

        if self.anthropic_available:
            models.extend(["claude-3-5-sonnet-20240620"])

        if self.gemini_available:
            models.extend(["gemini-1.5-pro"])

        return models

    def get_provider_status(self) -> Dict[str, bool]:
        """Get provider status"""
        return {
            "openai": self.openai_available,
            "anthropic": self.anthropic_available, 
            "gemini": self.gemini_available
        }
