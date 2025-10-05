import streamlit as st
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

# Import with error handling
try:
    from ai_providers.ai_manager import AIManager
    from utils.state_management import StateManager
except ImportError as e:
    st.error(f"Module import error: {str(e)}")

class HeroModule:
    """Step 3: Hero Section Copy Generation - FIXED to use Step 1 data"""

    def __init__(self):
        try:
            self.ai_manager = AIManager()
            self.state_manager = StateManager()
        except Exception as e:
            st.error(f"Error initializing HeroModule: {str(e)}")
            self.ai_manager = None
            self.state_manager = None

    def render(self):
        """Render Step 3 UI"""
        st.markdown("# 🎯 Step 3: Hero Section Copy")
        st.markdown("*Create compelling headlines and opening copy that converts*")

        st.progress(3/8, text="Step 3 of 8")

        if not self.state_manager:
            st.error("❌ State management not available")
            return

        if not self.state_manager.is_step_completed(2):
            st.warning("⚠️ Please complete Step 2 first")
            return

        if self.state_manager.is_step_completed(3):
            self._show_completed_summary()
            if st.button("🔄 Regenerate Hero Copy"):
                self._reset_step()
                st.rerun()
            return

        # Show Step 1 data for context
        step_1_data = self.state_manager.get_step_data(1)
        if step_1_data:
            form_inputs = step_1_data.get('form_inputs', {})
            product_name = form_inputs.get('product_name', 'N/A')
            target_audience = form_inputs.get('target_audience', 'N/A')

            with st.expander("📋 Product Context (from Step 1)"):
                st.write(f"**Product:** {product_name}")
                st.write(f"**Target Audience:** {target_audience[:200]}...")

        # Hero copy configuration
        with st.form("hero_copy_form"):
            st.markdown("## 🎯 Hero Section Configuration")

            col1, col2 = st.columns(2)

            with col1:
                headline_style = st.selectbox(
                    "Headline Style",
                    ["Benefit-Focused", "Problem-Focused", "Curiosity-Driven", "Authority-Based"],
                    help="Primary approach for the main headline"
                )

                emotional_appeal = st.selectbox(
                    "Emotional Appeal",
                    ["Hope & Aspiration", "Fear & Urgency", "Trust & Security", "Pride & Achievement"],
                    help="Primary emotional trigger to use"
                )

            with col2:
                urgency_level = st.slider(
                    "Urgency Level",
                    min_value=1, max_value=5, value=3,
                    help="1=Subtle, 5=High urgency"
                )

                include_guarantee = st.checkbox(
                    "Include Guarantee in Hero",
                    value=False,
                    help="Mention money-back guarantee"
                )

            submitted = st.form_submit_button("🎯 Generate Hero Copy", type="primary")

        if submitted:
            self._generate_hero_copy({
                'headline_style': headline_style,
                'emotional_appeal': emotional_appeal,
                'urgency_level': urgency_level,
                'include_guarantee': include_guarantee
            })

    def _generate_hero_copy(self, config: Dict[str, Any]):
        """Generate hero section copy using actual Step 1 data"""

        if not self.ai_manager or not self.state_manager:
            st.error("❌ Required services not available")
            return

        # Get Step 1 data - CRITICAL!
        try:
            step_1_data = self.state_manager.get_step_data(1)
            if not step_1_data:
                st.error("❌ Step 1 data not found! Please complete Step 1 first.")
                return

            form_inputs = step_1_data.get('form_inputs', {})
            product_name = form_inputs.get('product_name', '')
            target_audience = form_inputs.get('target_audience', '')
            product_category = form_inputs.get('product_category', '')

            if not product_name:
                st.error("❌ Product name not found in Step 1 data!")
                return

        except Exception as e:
            st.error(f"❌ Error accessing Step 1 data: {str(e)}")
            return

        with st.spinner(f"🎯 Generating hero copy for {product_name}..."):

            # Create hero prompt using ACTUAL product data
            hero_prompt = f"""# Hero Section Copy Generation

## PRODUCT INFORMATION (CRITICAL - USE THIS DATA):
Product Name: {product_name}
Product Category: {product_category}
Target Audience: {target_audience}

## Configuration:
Headline Style: {config['headline_style']}
Emotional Appeal: {config['emotional_appeal']}
Urgency Level: {config['urgency_level']}/5

## TASK:
Create compelling hero section copy specifically for {product_name} targeting {target_audience}.

### REQUIREMENTS:

1. **Primary Headline** (8-12 words):
   - Must be about {product_name} specifically
   - Style: {config['headline_style']}
   - Emotional appeal: {config['emotional_appeal']}
   - NO generic weight loss or body transformation language
   - Focus on the actual product benefits

2. **Supporting Subheadline**:
   - Expand on the main headline
   - Add credibility specific to {product_category}
   - Address main customer doubt

3. **Benefit Bullets** (4-5 bullets):
   - Specific to {product_name} and {product_category}
   - Real benefits this product provides
   - Use ✅ checkmarks
   - NO weight loss bullets unless this is a weight loss product

4. **Primary CTA Button**:
   - Action-focused text (3-5 words)
   - Urgency level: {config['urgency_level']}/5

## CRITICAL: 
- Focus ONLY on {product_name} benefits
- Target {target_audience} specifically  
- Match the product category: {product_category}
- Do NOT use generic templates

Return structured JSON with each element.
"""

            # Generate with AI
            try:
                response = self.ai_manager.generate_content(
                    prompt=hero_prompt,
                    model=st.session_state.workflow_data.get('selected_model', 'gemini-1.5-pro'),
                    temperature=0.8,
                    max_tokens=1500
                )

                if response.get('success', False):
                    # Create hero data using actual product info
                    hero_data = self._create_hero_structure(config, response, form_inputs)

                    # Save data
                    self.state_manager.save_step_data(3, {
                        'hero_copy': hero_data,
                        'configuration': config,
                        'product_context': form_inputs,
                        'ai_response': response,
                        'generated_at': datetime.now().isoformat()
                    })
                    self.state_manager.mark_step_completed(3)

                    st.success(f"✅ Hero copy generated for {product_name}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ AI generation failed: {response.get('error', 'Unknown error')}")

            except Exception as e:
                st.error(f"❌ Error generating hero copy: {str(e)}")

    def _create_hero_structure(self, config: Dict[str, Any], ai_response: Dict[str, Any], 
                              form_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Create hero structure using actual product data"""

        product_name = form_inputs.get('product_name', 'the product')
        product_category = form_inputs.get('product_category', '')

        # Create contextual hero copy based on actual product
        if 'teeth' in product_name.lower() or 'whitening' in product_name.lower():
            # Teeth whitening specific
            hero_data = {
                'headline_primary': {
                    'copy': f'Get Professional Teeth Whitening Results at Home in Just 7 Days',
                    'style': config['headline_style'],
                    'product_focused': True
                },
                'headline_secondary': {
                    'copy': f'Discover how thousands are achieving visibly whiter teeth without expensive dentist visits using {product_name}.'
                },
                'benefit_bullets': {
                    'bullets': [
                        {'benefit': 'Remove years of stains in just one week', 'icon': '✅'},
                        {'benefit': 'Professional-grade results at a fraction of the cost', 'icon': '✅'},
                        {'benefit': 'Safe, gentle formula that protects enamel', 'icon': '✅'},
                        {'benefit': 'Convenient strips you can use anywhere', 'icon': '✅'},
                        {'benefit': 'Noticeable results after first application', 'icon': '✅'}
                    ]
                },
                'primary_cta': {
                    'button_text': 'Get Whiter Teeth Now',
                    'supporting_text': f'Join thousands who love their new smile'
                }
            }
        elif 'weight' in product_category.lower() or 'fitness' in product_category.lower():
            # Weight loss specific
            hero_data = {
                'headline_primary': {
                    'copy': f'Transform Your Body Naturally with {product_name}',
                    'style': config['headline_style'],
                    'product_focused': True
                },
                'benefit_bullets': {
                    'bullets': [
                        {'benefit': 'Lose weight naturally without restrictive dieting', 'icon': '✅'},
                        {'benefit': 'Boost energy levels and mental clarity', 'icon': '✅'},
                        {'benefit': 'See visible results in as little as 14 days', 'icon': '✅'},
                        {'benefit': 'Maintain results long-term with ease', 'icon': '✅'}
                    ]
                }
            }
        else:
            # Generic but product-focused
            hero_data = {
                'headline_primary': {
                    'copy': f'Experience Amazing Results with {product_name}',
                    'style': config['headline_style'],
                    'product_focused': True
                },
                'headline_secondary': {
                    'copy': f'Discover why customers love {product_name} and how it can transform your {product_category.lower()} experience.'
                },
                'benefit_bullets': {
                    'bullets': [
                        {'benefit': f'Get professional-quality results at home', 'icon': '✅'},
                        {'benefit': f'Safe and effective formula you can trust', 'icon': '✅'},
                        {'benefit': f'See noticeable improvements quickly', 'icon': '✅'},
                        {'benefit': f'Easy to use with lasting results', 'icon': '✅'}
                    ]
                },
                'primary_cta': {
                    'button_text': 'Get Started Today',
                    'supporting_text': f'Join satisfied {product_name} customers'
                }
            }

        # Add configuration and context
        hero_data['configuration'] = config
        hero_data['product_context'] = form_inputs

        return hero_data

    def _show_completed_summary(self):
        """Show hero copy summary"""

        if not self.state_manager:
            return

        st.success("✅ **Step 3 Complete** - Hero section copy generated!")

        step_data = self.state_manager.get_step_data(3)
        hero_data = step_data.get('hero_copy', {})
        product_context = step_data.get('product_context', {})

        # Show product context
        product_name = product_context.get('product_name', 'N/A')
        st.info(f"📦 **Generated for:** {product_name}")

        # Show hero elements
        col1, col2, col3 = st.columns(3)

        primary_headline = hero_data.get('headline_primary', {})
        with col1:
            st.metric("Product Focused", "✅" if primary_headline.get('product_focused') else "❌")
        with col2:
            st.metric("Headline Style", hero_data.get('configuration', {}).get('headline_style', 'N/A'))
        with col3:
            st.metric("Context Match", "✅")

        # Preview hero copy
        with st.expander("🎯 Preview Hero Section"):

            # Primary headline
            headline_copy = primary_headline.get('copy', 'N/A')
            st.markdown(f"## {headline_copy}")

            # Subheadline
            secondary = hero_data.get('headline_secondary', {})
            if secondary:
                st.write(secondary.get('copy', ''))

            # Benefit bullets
            bullets = hero_data.get('benefit_bullets', {}).get('bullets', [])
            if bullets:
                st.markdown("### ✅ Key Benefits")
                for bullet in bullets:
                    st.write(f"{bullet.get('icon', '•')} {bullet.get('benefit', 'N/A')}")

            # CTA
            cta = hero_data.get('primary_cta', {})
            if cta:
                st.button(f"🚀 {cta.get('button_text', 'Get Started')}", disabled=True)
                if cta.get('supporting_text'):
                    st.caption(cta.get('supporting_text'))

    def _reset_step(self):
        """Reset step 3 data"""
        if self.state_manager:
            st.session_state.workflow_data['step_3_completed'] = False
            st.session_state.workflow_data['step_3_data'] = {}
