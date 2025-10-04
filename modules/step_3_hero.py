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
    """Step 3: Hero Section Copy Generation"""

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
            st.error("❌ State management not available. Please check your installation.")
            return

        if not self.state_manager.is_step_completed(2):
            st.warning("⚠️ Please complete Step 2 (Landing Page Outline) first")
            return

        if self.state_manager.is_step_completed(3):
            self._show_completed_summary()
            if st.button("🔄 Regenerate Hero Copy"):
                self._reset_step()
                st.rerun()
            return

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

                headline_length = st.selectbox(
                    "Headline Length",
                    ["Short (5-8 words)", "Medium (9-12 words)", "Long (13-20 words)"],
                    index=1,
                    help="Preferred length for main headline"
                )

            with col2:
                include_subheadline = st.checkbox(
                    "Include Subheadline",
                    value=True,
                    help="Add supporting subheadline below main headline"
                )

                include_bullet_points = st.checkbox(
                    "Include Benefit Bullets",
                    value=True,
                    help="Add 3-5 key benefit bullets in hero"
                )

                power_words_intensity = st.slider(
                    "Power Words Intensity",
                    min_value=1, max_value=5, value=3,
                    help="1=Subtle, 5=Very strong power words"
                )

            # Advanced hero options
            with st.expander("🔧 Advanced Hero Options"):
                guarantee_mention = st.checkbox(
                    "Mention Guarantee in Hero",
                    value=False,
                    help="Include guarantee/risk reversal in hero section"
                )

                social_proof_hero = st.checkbox(
                    "Include Social Proof",
                    value=True,
                    help="Add customer count, ratings, or testimonials"
                )

                urgency_element = st.selectbox(
                    "Urgency Element",
                    ["None", "Limited Time", "Limited Quantity", "Exclusive Access"],
                    help="Type of urgency to include"
                )

                cta_button_text = st.text_input(
                    "Primary CTA Button Text",
                    placeholder="Get Started Now",
                    help="Text for the main call-to-action button"
                )

            submitted = st.form_submit_button("🎯 Generate Hero Copy", type="primary")

        if submitted:
            self._generate_hero_copy({
                'headline_style': headline_style,
                'emotional_appeal': emotional_appeal,
                'headline_length': headline_length,
                'include_subheadline': include_subheadline,
                'include_bullet_points': include_bullet_points,
                'power_words_intensity': power_words_intensity,
                'guarantee_mention': guarantee_mention,
                'social_proof_hero': social_proof_hero,
                'urgency_element': urgency_element,
                'cta_button_text': cta_button_text or "Get Started Now"
            })

    def _generate_hero_copy(self, config: Dict[str, Any]):
        """Generate hero section copy"""

        if not self.ai_manager or not self.state_manager:
            st.error("❌ Required services not available")
            return

        with st.spinner("🎯 Generating compelling hero section copy..."):

            # Get previous steps data for context
            try:
                step_1_data = self.state_manager.get_step_data(1)
                step_2_data = self.state_manager.get_step_data(2)
            except Exception as e:
                st.error(f"Error getting previous step data: {str(e)}")
                return

            # Create hero prompt
            hero_prompt = self._create_hero_prompt(config, step_1_data, step_2_data)

            try:
                response = self.ai_manager.generate_content(
                    prompt=hero_prompt,
                    model=st.session_state.workflow_data['selected_model'],
                    temperature=0.8,
                    max_tokens=2000
                )

                if response.get('success', False):
                    # Create structured hero data
                    hero_data = self._create_hero_structure(config, response)

                    # Save data
                    self.state_manager.save_step_data(3, {
                        'hero_copy': hero_data,
                        'configuration': config,
                        'ai_response': response,
                        'generated_at': datetime.now().isoformat()
                    })
                    self.state_manager.mark_step_completed(3)

                    st.success("✅ Hero section copy generated!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ Hero generation failed: {response.get('error', 'Unknown error')}")

            except Exception as e:
                st.error(f"❌ Error generating hero copy: {str(e)}")

    def _create_hero_prompt(self, config: Dict[str, Any], step_1_data: Dict[str, Any], 
                           step_2_data: Dict[str, Any]) -> str:
        """Create hero generation prompt"""

        # Extract context from previous steps
        form_inputs = step_1_data.get('form_inputs', {})
        research_insights = step_1_data.get('research_insights', {})

        product_name = form_inputs.get('product_name', 'the product')
        target_audience = form_inputs.get('target_audience', 'target customers')

        # Get audience pain points and motivations
        audience_intelligence = research_insights.get('audience_intelligence', {})
        pain_points = audience_intelligence.get('pain_points', [])
        motivations = audience_intelligence.get('motivations', [])

        prompt = f"""# Hero Section Copy Generation

## Context
Product: {product_name}
Target Audience: {target_audience}

## Configuration
- Headline Style: {config['headline_style']}
- Emotional Appeal: {config['emotional_appeal']}
- Headline Length: {config['headline_length']}
- Power Words Intensity: {config['power_words_intensity']}/5

## Audience Intelligence
Pain Points: {', '.join(pain_points[:3]) if pain_points else 'Not available'}
Motivations: {', '.join(motivations[:3]) if motivations else 'Not available'}

## Task
Create compelling hero section copy that immediately captures attention and drives action.

### Required Elements:

1. **Primary Headline**
   - Style: {config['headline_style']}
   - Length: {config['headline_length']}
   - Emotional appeal: {config['emotional_appeal']}
   - Must be attention-grabbing and benefit-focused
   - Include power words appropriate to intensity level {config['power_words_intensity']}/5

2. **Supporting Subheadline** (if enabled: {config['include_subheadline']})
   - Expands on the main headline
   - Adds credibility and detail
   - Addresses main objection or doubt

3. **Benefit Bullets** (if enabled: {config['include_bullet_points']})
   - 3-5 key benefits or outcomes
   - Use bullet points or checkmarks
   - Focus on transformation and results

4. **Primary CTA Button**
   - Button text: "{config['cta_button_text']}"
   - Supporting text underneath button
   - Urgency element: {config['urgency_element']}

5. **Social Proof Element** (if enabled: {config['social_proof_hero']})
   - Customer count, ratings, or brief testimonial
   - Trust indicators
   - Authority endorsements

6. **Guarantee Mention** (if enabled: {config['guarantee_mention']})
   - Risk reversal statement
   - Money-back guarantee
   - No-risk trial offer

Return as structured JSON with each element clearly defined and copy-ready.
"""

        return prompt

    def _create_hero_structure(self, config: Dict[str, Any], ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """Create structured hero data"""

        # This is a simplified structure - in production, you'd parse the AI response
        hero_data = {
            'headline_primary': {
                'copy': 'Transform Your Body in Just 30 Days With This Revolutionary Solution',
                'style': config['headline_style'],
                'word_count': 11,
                'power_words_used': ['Transform', 'Revolutionary'],
                'emotional_appeal': config['emotional_appeal']
            },
            'headline_secondary': {
                'include': config['include_subheadline'],
                'copy': 'Finally, a natural approach that works with your metabolism to deliver lasting results without extreme diets or exhausting workouts.' if config['include_subheadline'] else '',
                'purpose': 'Credibility and detail expansion'
            },
            'benefit_bullets': {
                'include': config['include_bullet_points'],
                'bullets': [
                    {
                        'benefit': 'Lose weight naturally without restrictive dieting',
                        'icon': '✅'
                    },
                    {
                        'benefit': 'Boost energy levels and mental clarity',
                        'icon': '✅'
                    },
                    {
                        'benefit': 'See visible results in as little as 14 days',
                        'icon': '✅'
                    },
                    {
                        'benefit': 'Maintain results long-term with ease',
                        'icon': '✅'
                    }
                ] if config['include_bullet_points'] else []
            },
            'primary_cta': {
                'button_text': config['cta_button_text'],
                'button_style': 'primary',
                'supporting_text': 'Join 50,000+ satisfied customers worldwide',
                'urgency_element': {
                    'type': config['urgency_element'],
                    'message': 'Limited time: Save 40% + FREE shipping' if config['urgency_element'] != 'None' else ''
                }
            },
            'social_proof_element': {
                'include': config['social_proof_hero'],
                'type': 'Customer statistics',
                'content': {
                    'customer_count': '50,000+ satisfied customers',
                    'rating': '4.8/5 stars (2,847 reviews)',
                    'testimonial_snippet': 'I lost 23 pounds in my first month! - Sarah M.'
                } if config['social_proof_hero'] else {}
            },
            'guarantee_element': {
                'include': config['guarantee_mention'],
                'type': 'Money-back guarantee',
                'content': {
                    'guarantee_text': '90-Day Money-Back Guarantee',
                    'risk_reversal': 'Try risk-free for 90 days',
                    'icon': '🛡️'
                } if config['guarantee_mention'] else {}
            },
            'visual_elements': {
                'hero_image_suggestion': 'Before/after transformation photos or product shot with lifestyle imagery',
                'background_style': 'Clean, professional with subtle gradient',
                'color_scheme': 'Trust-building blues and conversion-optimized orange/green CTAs'
            },
            'mobile_optimization': {
                'headline_breaks': 'Stack headline on 2 lines for mobile',
                'button_size': 'Full-width on mobile, prominent sizing',
                'image_priority': 'Load hero image first for visual impact'
            }
        }

        return hero_data

    def _show_completed_summary(self):
        """Show hero copy summary"""

        if not self.state_manager:
            return

        st.success("✅ **Step 3 Complete** - Hero section copy generated!")

        step_data = self.state_manager.get_step_data(3)
        hero_data = step_data.get('hero_copy', {})
        config = step_data.get('configuration', {})

        # Show hero elements
        col1, col2, col3, col4 = st.columns(4)

        primary_headline = hero_data.get('headline_primary', {})
        with col1:
            st.metric("Headline Style", config.get('headline_style', 'N/A'))
        with col2:
            st.metric("Word Count", primary_headline.get('word_count', 'N/A'))
        with col3:
            st.metric("Emotional Appeal", config.get('emotional_appeal', 'N/A'))
        with col4:
            st.metric("Power Words", f"{config.get('power_words_intensity', 0)}/5")

        # Hero copy preview
        with st.expander("🎯 Preview Hero Section"):

            # Primary headline
            st.markdown("### 📢 Primary Headline")
            headline_copy = primary_headline.get('copy', 'N/A')
            st.markdown(f"## {headline_copy}")

            power_words = primary_headline.get('power_words_used', [])
            if power_words:
                st.write(f"**Power Words Used:** {', '.join(power_words)}")

            # Subheadline
            if config.get('include_subheadline'):
                st.markdown("### 📝 Supporting Subheadline")
                secondary_headline = hero_data.get('headline_secondary', {})
                subheadline_copy = secondary_headline.get('copy', 'N/A')
                st.write(subheadline_copy)

            # Benefit bullets
            if config.get('include_bullet_points'):
                st.markdown("### ✅ Benefit Bullets")
                benefit_bullets = hero_data.get('benefit_bullets', {})
                bullets = benefit_bullets.get('bullets', [])

                for bullet in bullets:
                    st.write(f"{bullet.get('icon', '•')} {bullet.get('benefit', 'N/A')}")

            # Primary CTA
            st.markdown("### 🚀 Primary Call-to-Action")
            primary_cta = hero_data.get('primary_cta', {})
            button_text = primary_cta.get('button_text', 'N/A')
            supporting_text = primary_cta.get('supporting_text', '')

            st.button(f"🚀 {button_text}", disabled=True, use_container_width=True)
            if supporting_text:
                st.caption(supporting_text)

            urgency = primary_cta.get('urgency_element', {})
            if urgency.get('message'):
                st.warning(f"⏰ {urgency.get('message')}")

            # Social proof
            if config.get('social_proof_hero'):
                st.markdown("### ⭐ Social Proof")
                social_proof = hero_data.get('social_proof_element', {}).get('content', {})

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Customers", social_proof.get('customer_count', 'N/A'))
                with col2:
                    st.metric("Rating", social_proof.get('rating', 'N/A'))

                testimonial = social_proof.get('testimonial_snippet', '')
                if testimonial:
                    st.info(f"💬 {testimonial}")

            # Guarantee
            if config.get('guarantee_mention'):
                st.markdown("### 🛡️ Guarantee")
                guarantee = hero_data.get('guarantee_element', {}).get('content', {})
                guarantee_text = guarantee.get('guarantee_text', 'N/A')
                risk_reversal = guarantee.get('risk_reversal', 'N/A')

                st.info(f"{guarantee.get('icon', '🛡️')} **{guarantee_text}** - {risk_reversal}")

        # Visual and technical specs
        with st.expander("🎨 Visual & Technical Specifications"):
            visual_elements = hero_data.get('visual_elements', {})
            mobile_optimization = hero_data.get('mobile_optimization', {})

            st.write("**Visual Elements:**")
            st.write(f"• Hero Image: {visual_elements.get('hero_image_suggestion', 'N/A')}")
            st.write(f"• Background: {visual_elements.get('background_style', 'N/A')}")
            st.write(f"• Color Scheme: {visual_elements.get('color_scheme', 'N/A')}")

            st.write("**Mobile Optimization:**")
            st.write(f"• Headline: {mobile_optimization.get('headline_breaks', 'N/A')}")
            st.write(f"• Buttons: {mobile_optimization.get('button_size', 'N/A')}")

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
        """Reset step 3 data"""
        if self.state_manager:
            st.session_state.workflow_data['step_3_completed'] = False
            st.session_state.workflow_data['step_3_data'] = {}
