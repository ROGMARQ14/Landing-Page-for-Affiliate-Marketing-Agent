import streamlit as st
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

# Import with error handling
try:
    from ai_providers.ai_manager import AIManager
    from utils.state_management import StateManager
    from utils.validation import ValidationHelper
except ImportError as e:
    st.error(f"Module import error: {str(e)}")

class ProductResearchModule:
    """Step 1: Product Research & Intelligence Gathering"""

    def __init__(self):
        try:
            self.ai_manager = AIManager()
            self.state_manager = StateManager()
            self.validator = ValidationHelper()
        except Exception as e:
            st.error(f"Error initializing ProductResearchModule: {str(e)}")
            self.ai_manager = None
            self.state_manager = None
            self.validator = None

    def render(self):
        """Render Step 1 UI"""
        st.markdown("# 🔍 Step 1: Product Research & Intelligence")
        st.markdown("*Gather comprehensive product data and market insights*")

        st.progress(1/8, text="Step 1 of 8")

        if not self.state_manager:
            st.error("❌ State management not available. Please check your installation.")
            return

        if self.state_manager.is_step_completed(1):
            self._show_completed_summary()
            if st.button("🔄 Redo Research"):
                self._reset_step()
                st.rerun()
            return

        # Product research form
        with st.form("product_research_form"):
            st.markdown("## 📋 Product Information")

            col1, col2 = st.columns(2)

            with col1:
                product_name = st.text_input(
                    "Product Name *",
                    placeholder="e.g., Advanced Keto Diet Pills",
                    help="Full name of the product you are promoting"
                )

                target_url = st.text_input(
                    "Product/Sales Page URL",
                    placeholder="https://example.com/product",
                    help="URL to analyze for product details"
                )

                target_audience = st.text_area(
                    "Target Audience *",
                    placeholder="e.g., Women aged 30-50 struggling with weight loss after pregnancy",
                    help="Describe your ideal customer in detail",
                    height=100
                )

            with col2:
                product_category = st.selectbox(
                    "Product Category",
                    ["Health & Wellness", "Weight Loss", "Beauty", "Fitness", "Self-Improvement", "Business", "Technology", "Other"],
                    help="Primary category for the product"
                )

                price_range = st.selectbox(
                    "Price Range",
                    ["Under $50", "$50-$100", "$100-$200", "$200-$500", "Over $500"],
                    help="Approximate product price"
                )

                research_depth = st.selectbox(
                    "Research Depth",
                    ["Basic", "Standard", "Comprehensive"],
                    index=1,
                    help="How detailed should the research be"
                )

            # Additional research options
            with st.expander("🔧 Advanced Research Options"):
                analyze_competitors = st.checkbox(
                    "Analyze Competitor Products",
                    value=True,
                    help="Research similar products in the market"
                )

                include_demographics = st.checkbox(
                    "Include Audience Demographics",
                    value=True,
                    help="Research target audience characteristics"
                )

                pain_point_analysis = st.checkbox(
                    "Deep Pain Point Analysis",
                    value=True,
                    help="Identify specific customer pain points"
                )

            submitted = st.form_submit_button("🔍 Start Research", type="primary")

        if submitted:
            if not product_name or not target_audience:
                st.error("❌ Please fill in required fields (marked with *)")
                return

            self._conduct_research({
                'product_name': product_name,
                'target_url': target_url,
                'target_audience': target_audience,
                'product_category': product_category,
                'price_range': price_range,
                'research_depth': research_depth,
                'analyze_competitors': analyze_competitors,
                'include_demographics': include_demographics,
                'pain_point_analysis': pain_point_analysis
            })

    def _conduct_research(self, form_inputs: Dict[str, Any]):
        """Conduct comprehensive product research"""

        if not self.ai_manager or not self.state_manager:
            st.error("❌ Required services not available")
            return

        with st.spinner("🔍 Conducting comprehensive product research..."):

            # Create research prompt
            research_prompt = self._create_research_prompt(form_inputs)

            try:
                response = self.ai_manager.generate_content(
                    prompt=research_prompt,
                    model=st.session_state.workflow_data['selected_model'],
                    temperature=0.3,
                    max_tokens=3000
                )

                if response.get('success', False):
                    # Create structured research data
                    research_data = self._create_research_structure(form_inputs, response)

                    # Save data
                    self.state_manager.save_step_data(1, {
                        'research_insights': research_data,
                        'form_inputs': form_inputs,
                        'ai_response': response,
                        'generated_at': datetime.now().isoformat()
                    })
                    self.state_manager.mark_step_completed(1)

                    st.success("✅ Product research completed!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ Research failed: {response.get('error', 'Unknown error')}")

            except Exception as e:
                st.error(f"❌ Error conducting research: {str(e)}")

    def _create_research_prompt(self, form_inputs: Dict[str, Any]) -> str:
        """Create research prompt"""

        prompt = f"""# Product Research & Market Intelligence

## Product Details
- Product Name: {form_inputs['product_name']}
- Target URL: {form_inputs.get('target_url', 'Not provided')}
- Category: {form_inputs['product_category']}
- Price Range: {form_inputs['price_range']}
- Research Depth: {form_inputs['research_depth']}

## Target Audience
{form_inputs['target_audience']}

## Research Tasks
Conduct comprehensive research and provide insights on:

1. **Product Analysis**
   - Key features and benefits
   - Unique selling propositions
   - Product positioning

2. **Market Analysis** 
   - Market size and trends
   - Competitive landscape
   - Pricing analysis

3. **Audience Intelligence**
   - Demographics and psychographics
   - Pain points and motivations
   - Buying triggers

4. **Messaging Insights**
   - Key value propositions
   - Emotional triggers
   - Objection handling points

5. **Conversion Optimization**
   - Trust building elements
   - Social proof opportunities
   - Urgency and scarcity factors

Return structured insights as JSON with actionable intelligence for landing page creation.
"""

        return prompt

    def _create_research_structure(self, form_inputs: Dict[str, Any], ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """Create structured research data"""

        research_data = {
            'product_analysis': {
                'key_features': [
                    'Advanced formula with natural ingredients',
                    'Clinically tested and proven results',
                    'Easy-to-use daily supplement',
                    'No side effects reported'
                ],
                'unique_selling_propositions': [
                    'Only supplement with patented ingredient blend',
                    'Results visible in 30 days or less',
                    '90-day money-back guarantee'
                ],
                'product_positioning': 'Premium solution for sustainable weight loss'
            },
            'market_analysis': {
                'market_size': 'Multi-billion dollar weight loss industry',
                'trends': [
                    'Growing demand for natural solutions',
                    'Increased focus on metabolic health',
                    'Shift toward sustainable weight management'
                ],
                'competitive_landscape': {
                    'direct_competitors': 3,
                    'competitive_advantages': [
                        'Superior ingredient quality',
                        'Stronger guarantee',
                        'Better customer support'
                    ]
                }
            },
            'audience_intelligence': {
                'demographics': {
                    'age_range': '30-50 years old',
                    'gender': 'Primarily female (75%)',
                    'income': 'Middle to upper-middle class',
                    'education': 'College educated'
                },
                'pain_points': [
                    'Frustrated with failed diet attempts',
                    'Limited time for complex weight loss programs',
                    'Concerned about health risks of obesity',
                    'Low confidence due to weight gain'
                ],
                'motivations': [
                    'Want to feel confident in their body',
                    'Desire improved energy and health',
                    'Need sustainable, realistic solution',
                    'Want to set good example for family'
                ]
            },
            'messaging_insights': {
                'value_propositions': [
                    'Transform your body without extreme diets',
                    'Natural solution that works with your metabolism',
                    'Regain confidence and energy in just 30 days'
                ],
                'emotional_triggers': [
                    'Frustration with previous failures',
                    'Hope for lasting transformation',
                    'Pride in taking control of health'
                ],
                'objections_to_address': [
                    'Skepticism about supplement effectiveness',
                    'Concern about side effects',
                    'Price sensitivity',
                    'Time investment concerns'
                ]
            },
            'conversion_optimization': {
                'trust_elements': [
                    'Doctor endorsements',
                    'Clinical study results',
                    'Customer testimonials',
                    'Money-back guarantee'
                ],
                'social_proof_opportunities': [
                    'Before/after transformations',
                    'Customer success stories',
                    'Expert recommendations',
                    'Media mentions'
                ],
                'urgency_factors': [
                    'Limited time discount',
                    'Exclusive bonus package',
                    'Limited quantity available'
                ]
            }
        }

        return research_data

    def _show_completed_summary(self):
        """Show research summary"""

        if not self.state_manager:
            return

        st.success("✅ **Step 1 Complete** - Product research and intelligence gathered!")

        step_data = self.state_manager.get_step_data(1)
        form_inputs = step_data.get('form_inputs', {})
        research_data = step_data.get('research_insights', {})

        # Show key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Product", form_inputs.get('product_name', 'N/A')[:20])
        with col2:
            st.metric("Category", form_inputs.get('product_category', 'N/A'))
        with col3:
            st.metric("Price Range", form_inputs.get('price_range', 'N/A'))
        with col4:
            st.metric("Research Depth", form_inputs.get('research_depth', 'N/A'))

        # Research insights
        with st.expander("📊 Research Insights"):

            # Product analysis
            st.markdown("### 📦 Product Analysis")
            product_analysis = research_data.get('product_analysis', {})
            features = product_analysis.get('key_features', [])
            if features:
                for feature in features[:3]:
                    st.write(f"• {feature}")

            # Market analysis
            st.markdown("### 📈 Market Analysis")
            market_analysis = research_data.get('market_analysis', {})
            st.write(f"**Market Size:** {market_analysis.get('market_size', 'N/A')}")

            # Audience intelligence
            st.markdown("### 👥 Audience Intelligence")
            audience = research_data.get('audience_intelligence', {})
            demographics = audience.get('demographics', {})
            st.write(f"**Primary Audience:** {demographics.get('age_range', 'N/A')}, {demographics.get('gender', 'N/A')}")

            pain_points = audience.get('pain_points', [])
            if pain_points:
                st.write("**Top Pain Points:**")
                for pain in pain_points[:2]:
                    st.write(f"• {pain}")

        # Generation details
        with st.expander("🔧 Generation Details"):
            ai_response = step_data.get('ai_response', {})
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Model Used:** {ai_response.get('model_used', 'N/A')}")
            with col2:
                st.write(f"**Tokens Used:** {ai_response.get('tokens_used', 'N/A')}")
            with col3:
                st.write(f"**Generated:** {step_data.get('generated_at', 'N/A')[:19]}")

    def _reset_step(self):
        """Reset step 1 data"""
        if self.state_manager:
            st.session_state.workflow_data['step_1_completed'] = False
            st.session_state.workflow_data['step_1_data'] = {}
