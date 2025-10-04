import streamlit as st
import json
import re
from typing import Dict, Any, Optional
from ai_providers.ai_manager import AIManager
from utils.state_management import StateManager

class ProductResearchModule:
    """Step 1: Product Research Module - V2.0 Enhanced"""

    def __init__(self):
        self.ai_manager = AIManager()
        self.state_manager = StateManager()

        # Load the enhanced V1.0 prompt (our previously created prompt)
        self.prompt_template = """# SYSTEM CONFIGURATION
Model: {model}
Temperature: 0.3
Top-P: 0.90
Top-K: 30
Max Tokens: 3000

# ROLE & CONTEXT
You are a Senior Product Research Analyst specializing in direct response marketing and PPC campaign optimization. Your expertise encompasses competitive analysis, customer psychology profiling, and conversion-focused market research.

# TASK OBJECTIVE
Conduct comprehensive product intelligence gathering for PPC landing page generation. Focus on pain point validation, competitive positioning, and psychological triggers that drive conversions.

# INPUT VARIABLES
Product Name: {product_name}
Target URL/Product Page: {target_url}
Industry/Category: {industry}
Target Audience: {target_audience}
Campaign Budget: {budget_range}

# RESEARCH FRAMEWORK

Analyze the following dimensions and return comprehensive JSON:

1. **Product Analysis**
   - Core value proposition
   - Key features and benefits
   - Pricing structure and offers
   - Unique differentiators vs competitors

2. **Target Audience Profiling** 
   - Demographics and psychographics
   - Primary pain points (severity 1-10)
   - Desired outcomes and aspirations
   - Customer journey stage (awareness/consideration/decision)

3. **Competitive Landscape**
   - Top 3-5 direct competitors
   - Competitive advantages/disadvantages
   - Market positioning gaps
   - Pricing comparison

4. **Conversion Intelligence**
   - High-intent keywords for PPC
   - Emotional triggers and objections
   - Trust signals needed
   - Urgency/scarcity opportunities

5. **PPC Campaign Strategy**
   - Recommended ad message match
   - Landing page structure recommendations
   - A/B testing priorities

Please return ONLY a valid JSON object with comprehensive data for each dimension."""

    def render(self):
        """Render Step 1 UI"""
        st.markdown("# 🔍 Step 1: Product Research & Intelligence")
        st.markdown("*Foundation step that drives all subsequent copy generation*")

        # Progress indicator
        progress_col1, progress_col2 = st.columns([3, 1])
        with progress_col1:
            st.progress(1/8, text="Step 1 of 8")
        with progress_col2:
            st.markdown("**12.5%**")

        # Check if step is already completed
        is_completed = self.state_manager.is_step_completed(1)
        if is_completed:
            self._show_completed_summary()
            if st.button("🔄 Regenerate Research", type="secondary"):
                self._reset_step()
                st.rerun()

        # Main input form
        with st.form("product_research_form"):
            st.markdown("## 📋 Product Information")

            col1, col2 = st.columns(2)

            with col1:
                product_name = st.text_input(
                    "Product Name *",
                    placeholder="e.g., KetoBurn Pro Electrolyte Complex",
                    help="The exact name of the product you're creating a landing page for"
                )

                industry = st.selectbox(
                    "Industry/Category *",
                    [
                        "Health & Wellness",
                        "Fitness & Nutrition", 
                        "Software/SaaS",
                        "Education/Courses",
                        "Finance/Investment",
                        "Beauty & Skincare",
                        "Home & Garden",
                        "Business Services",
                        "Other"
                    ]
                )

                budget_range = st.selectbox(
                    "Monthly PPC Budget Range",
                    [
                        "Under $1,000",
                        "$1,000 - $5,000", 
                        "$5,000 - $15,000",
                        "$15,000 - $50,000",
                        "Over $50,000"
                    ]
                )

            with col2:
                target_url = st.text_input(
                    "Product URL (Optional)",
                    placeholder="https://example.com/product-page",
                    help="URL of existing product page for competitive analysis"
                )

                target_audience = st.text_area(
                    "Target Audience Description *",
                    placeholder="e.g., Health-conscious adults 25-45 starting keto diet, experiencing keto flu symptoms, looking for quick solutions to maintain energy levels",
                    height=100,
                    help="Describe your ideal customer in detail"
                )

            # Advanced options (collapsible)
            with st.expander("🔧 Advanced Research Options"):
                research_depth = st.radio(
                    "Research Depth",
                    ["Quick Analysis (5 min)", "Standard Research (10 min)", "Deep Analysis (15 min)"],
                    index=1,
                    help="Deeper analysis provides more comprehensive competitive intelligence"
                )

                focus_areas = st.multiselect(
                    "Focus Areas",
                    [
                        "Competitive Analysis",
                        "Customer Psychology", 
                        "Keyword Research",
                        "Pricing Strategy",
                        "Trust Signals",
                        "A/B Testing Priorities"
                    ],
                    default=["Competitive Analysis", "Customer Psychology", "Keyword Research"]
                )

                include_affiliates = st.checkbox(
                    "Include Affiliate Marketing Insights",
                    value=True,
                    help="Analyze comparison opportunities and audience qualifier insights"
                )

            # Submit button
            submitted = st.form_submit_button(
                "🚀 Generate Product Research", 
                type="primary",
                use_container_width=True
            )

        # Process form submission
        if submitted:
            if not product_name or not target_audience:
                st.error("❌ Please fill in all required fields (marked with *)")
                return

            self._generate_research({
                'product_name': product_name,
                'target_url': target_url,
                'industry': industry,
                'target_audience': target_audience,
                'budget_range': budget_range,
                'research_depth': research_depth,
                'focus_areas': focus_areas,
                'include_affiliates': include_affiliates
            })

    def _generate_research(self, form_data: Dict[str, Any]):
        """Generate AI-powered product research"""

        # Show processing message
        with st.spinner("🔍 Conducting comprehensive product research..."):

            # Format the prompt with user data
            formatted_prompt = self.prompt_template.format(
                model=st.session_state.workflow_data['selected_model'],
                product_name=form_data['product_name'],
                target_url=form_data['target_url'] or "Not provided",
                industry=form_data['industry'],
                target_audience=form_data['target_audience'],
                budget_range=form_data['budget_range']
            )

            # Add focus areas and affiliate context
            if form_data['include_affiliates']:
                formatted_prompt += """

# AFFILIATE MARKETING FOCUS
Include specific analysis for:
- Comparison table opportunities (vs 3-4 competitors)
- Audience qualifier insights ("Is this for you?" vs "Not for you")
- Before/after transformation potential (if applicable)
- Trust building through transparency requirements
"""

            # Generate content using AI Manager
            response = self.ai_manager.generate_content(
                prompt=formatted_prompt,
                model=st.session_state.workflow_data['selected_model'],
                temperature=0.3,
                max_tokens=3000
            )

            if response.get('success', False):
                # Validate and parse JSON response
                json_validation = self.ai_manager.validate_json_response(response['content'])

                if json_validation['valid']:
                    # Save research data
                    research_data = {
                        'form_inputs': form_data,
                        'ai_response': json_validation['json_content'],
                        'raw_response': response['content'],
                        'model_used': response.get('model_used'),
                        'tokens_used': response.get('tokens_used'),
                        'generated_at': st.session_state.workflow_data['last_updated']
                    }

                    self.state_manager.save_step_data(1, research_data)
                    self.state_manager.mark_step_completed(1)

                    st.success("✅ Product research completed successfully!")
                    time.sleep(1)
                    st.rerun()

                else:
                    st.error(f"❌ Error parsing AI response: {json_validation.get('error')}")
                    with st.expander("🔍 View Raw Response"):
                        st.text(response['content'])
            else:
                st.error(f"❌ AI generation failed: {response.get('error')}")

    def _show_completed_summary(self):
        """Show summary of completed research"""
        step_data = self.state_manager.get_step_data(1)

        if not step_data:
            return

        ai_response = step_data.get('ai_response', {})
        form_inputs = step_data.get('form_inputs', {})

        # Success message
        st.success("✅ **Step 1 Complete** - Product research generated successfully!")

        # Key insights cards
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Product", 
                form_inputs.get('product_name', 'N/A'),
                delta=f"{form_inputs.get('industry', '')}"
            )

        with col2:
            competitors_count = len(ai_response.get('competitive_landscape', {}).get('top_competitors', []))
            st.metric(
                "Competitors Analyzed",
                competitors_count,
                delta=f"Market positioning identified"
            )

        with col3:
            pain_points_count = len(ai_response.get('target_audience_profile', {}).get('primary_pain_points', []))
            st.metric(
                "Pain Points Identified", 
                pain_points_count,
                delta=f"Conversion opportunities"
            )

        # Detailed insights (collapsible)
        with st.expander("📊 View Detailed Research Insights"):
            if ai_response:

                # Target audience insights
                st.markdown("### 👥 Target Audience Profile")
                audience_profile = ai_response.get('target_audience_profile', {})

                if audience_profile.get('primary_pain_points'):
                    st.markdown("**Primary Pain Points:**")
                    for pain in audience_profile['primary_pain_points'][:3]:  # Show top 3
                        severity = pain.get('severity', 'N/A')
                        st.write(f"• {pain.get('pain', 'N/A')} (Severity: {severity}/10)")

                # Competitive analysis
                st.markdown("### 🏢 Competitive Landscape")
                competitive_data = ai_response.get('competitive_landscape', {})

                if competitive_data.get('top_competitors'):
                    for i, competitor in enumerate(competitive_data['top_competitors'][:3], 1):
                        st.write(f"{i}. **{competitor.get('name', 'N/A')}** - {competitor.get('key_differentiator', 'N/A')}")

                # PPC strategy insights
                st.markdown("### 🎯 PPC Strategy Recommendations")
                ppc_strategy = ai_response.get('ppc_campaign_strategy', {})

                if ppc_strategy.get('high_intent_keywords'):
                    st.markdown("**High-Intent Keywords:**")
                    keywords = ppc_strategy['high_intent_keywords'][:5]  # Show top 5
                    keyword_text = ", ".join([kw.get('keyword', '') for kw in keywords if kw.get('keyword')])
                    st.write(keyword_text)

        # Show generation details
        with st.expander("🔧 Generation Details"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Model Used:** {step_data.get('model_used', 'N/A')}")
            with col2:
                st.write(f"**Tokens Used:** {step_data.get('tokens_used', 'N/A')}")
            with col3:
                st.write(f"**Generated:** {step_data.get('generated_at', 'N/A')[:19]}")

    def _reset_step(self):
        """Reset step 1 data"""
        st.session_state.workflow_data['step_1_completed'] = False
        st.session_state.workflow_data['step_1_data'] = {}
