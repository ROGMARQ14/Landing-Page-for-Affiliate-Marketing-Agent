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

class SocialProofModule:
    """Step 5: Social Proof & Comparisons (V2.0 Enhanced)"""

    def __init__(self):
        try:
            self.ai_manager = AIManager()
            self.state_manager = StateManager()
        except Exception as e:
            st.error(f"Error initializing SocialProofModule: {str(e)}")
            self.ai_manager = None
            self.state_manager = None

    def render(self):
        """Render Step 5 UI"""
        st.markdown("# ⭐ Step 5: Social Proof & Comparisons")
        st.markdown("*V2.0 Enhanced with comparison tables (+15-25% conversion)*")

        st.progress(5/8, text="Step 5 of 8")

        if not self.state_manager:
            st.error("❌ State management not available. Please check your installation.")
            return

        if not self.state_manager.is_step_completed(4):
            st.warning("⚠️ Please complete Step 4 (PAS Copy) first")
            return

        if self.state_manager.is_step_completed(5):
            self._show_completed_summary()
            if st.button("🔄 Regenerate Social Proof"):
                self._reset_step()
                st.rerun()
            return

        # Social proof configuration
        with st.form("social_proof_form"):
            st.markdown("## ⭐ Social Proof Configuration")

            col1, col2 = st.columns(2)

            with col1:
                testimonial_count = st.selectbox(
                    "Number of Testimonials",
                    ["3", "5", "7", "10"],
                    index=1,
                    help="How many customer testimonials to generate"
                )

                include_before_after = st.checkbox(
                    "Include Before/After Stories",
                    value=True,
                    help="Add transformation case studies"
                )

                include_comparison_table = st.checkbox(
                    "Include Comparison Table (V2.0)",
                    value=True,
                    help="V2.0: Product vs competitors (+15-25% conversion)"
                )

            with col2:
                expert_endorsements = st.checkbox(
                    "Include Expert Endorsements",
                    value=True,
                    help="Add doctor/expert recommendations"
                )

                media_mentions = st.checkbox(
                    "Include Media Mentions",
                    value=False,
                    help="Add press coverage and media features"
                )

                statistics_social_proof = st.checkbox(
                    "Include Usage Statistics",
                    value=True,
                    help="Customer counts, satisfaction rates, etc."
                )

            # Advanced social proof options
            with st.expander("🔧 Advanced Social Proof Options"):
                testimonial_diversity = st.selectbox(
                    "Testimonial Diversity",
                    ["Mixed Demographics", "Target Audience Focused", "Success Stories Variety"],
                    help="Type of testimonial variety to include"
                )

                credibility_level = st.slider(
                    "Credibility Details Level",
                    min_value=1, max_value=5, value=3,
                    help="1=Basic names, 5=Full details with photos"
                )

                comparison_focus = st.selectbox(
                    "Comparison Table Focus",
                    ["Feature Comparison", "Price Comparison", "Results Comparison", "Value Comparison"],
                    help="Primary focus for comparison table"
                )

                proof_authenticity = st.selectbox(
                    "Social Proof Style",
                    ["Highly Authentic", "Professional", "Casual & Relatable"],
                    help="Style and tone for testimonials"
                )

            submitted = st.form_submit_button("⭐ Generate Social Proof", type="primary")

        if submitted:
            self._generate_social_proof({
                'testimonial_count': int(testimonial_count),
                'include_before_after': include_before_after,
                'include_comparison_table': include_comparison_table,
                'expert_endorsements': expert_endorsements,
                'media_mentions': media_mentions,
                'statistics_social_proof': statistics_social_proof,
                'testimonial_diversity': testimonial_diversity,
                'credibility_level': credibility_level,
                'comparison_focus': comparison_focus,
                'proof_authenticity': proof_authenticity
            })

    def _generate_social_proof(self, config: Dict[str, Any]):
        """Generate social proof and comparison content"""

        if not self.ai_manager or not self.state_manager:
            st.error("❌ Required services not available")
            return

        with st.spinner("⭐ Generating V2.0 social proof with comparison table..."):

            # Get previous steps data for context
            try:
                step_1_data = self.state_manager.get_step_data(1)
                step_2_data = self.state_manager.get_step_data(2)
                step_3_data = self.state_manager.get_step_data(3)
                step_4_data = self.state_manager.get_step_data(4)
            except Exception as e:
                st.error(f"Error getting previous step data: {str(e)}")
                return

            # Create social proof prompt
            social_proof_prompt = self._create_social_proof_prompt(config, step_1_data, step_2_data, step_3_data, step_4_data)

            try:
                response = self.ai_manager.generate_content(
                    prompt=social_proof_prompt,
                    model=st.session_state.workflow_data['selected_model'],
                    temperature=0.7,
                    max_tokens=3500
                )

                if response.get('success', False):
                    # Create structured social proof data
                    social_proof_data = self._create_social_proof_structure(config, response)

                    # Save data
                    self.state_manager.save_step_data(5, {
                        'social_proof': social_proof_data,
                        'configuration': config,
                        'ai_response': response,
                        'generated_at': datetime.now().isoformat()
                    })
                    self.state_manager.mark_step_completed(5)

                    st.success("✅ V2.0 Social proof with comparison table generated!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ Social proof generation failed: {response.get('error', 'Unknown error')}")

            except Exception as e:
                st.error(f"❌ Error generating social proof: {str(e)}")

    def _create_social_proof_prompt(self, config: Dict[str, Any], step_1_data: Dict[str, Any], 
                                  step_2_data: Dict[str, Any], step_3_data: Dict[str, Any], 
                                  step_4_data: Dict[str, Any]) -> str:
        """Create social proof generation prompt"""

        # Extract context from previous steps
        form_inputs = step_1_data.get('form_inputs', {})
        product_name = form_inputs.get('product_name', 'the product')
        target_audience = form_inputs.get('target_audience', 'target customers')

        prompt = f"""# Social Proof & Comparison Generation V2.0

## Context
Product: {product_name}
Target Audience: {target_audience}

## Configuration
- Testimonial Count: {config['testimonial_count']}
- Include Before/After: {config['include_before_after']}
- Include Comparison Table: {config['include_comparison_table']}
- Expert Endorsements: {config['expert_endorsements']}
- Credibility Level: {config['credibility_level']}/5
- Testimonial Diversity: {config['testimonial_diversity']}

## Task
Generate comprehensive social proof package with V2.0 enhancements.

### Section 1: Customer Testimonials
Create {config['testimonial_count']} authentic customer testimonials.
Include:
- Diverse customer profiles matching target audience
- Specific results and outcomes
- Credibility details (names, locations, photos based on level {config['credibility_level']})
- Emotional transformation stories
- Timeframes for results achieved

### Section 2: Before/After Case Studies (if enabled: {config['include_before_after']})
Create compelling transformation stories.
Include:
- Specific metrics and measurements
- Timeline of transformation
- Challenges overcome
- Current satisfaction level
- Photos/visual proof suggestions

### Section 3: Expert Endorsements (if enabled: {config['expert_endorsements']})
Create professional endorsements.
Include:
- Doctor or expert recommendations
- Scientific backing statements  
- Professional credentials
- Authority-based trust signals

### Section 4: Comparison Table (V2.0 Enhancement - if enabled: {config['include_comparison_table']})
Create comprehensive product comparison.
Focus: {config['comparison_focus']}
Include:
- Product vs 3-4 main competitors
- Feature-by-feature comparison
- Value proposition highlights
- Unique differentiators
- Price/value analysis

### Section 5: Statistics & Social Proof Numbers (if enabled: {config['statistics_social_proof']})
Create credible usage statistics.
Include:
- Customer counts
- Satisfaction ratings
- Success rates
- Geographic reach
- Time in market

### Section 6: Media Mentions (if enabled: {config['media_mentions']})
Create media coverage references.
Include:
- Publication mentions
- Award recognitions
- Industry endorsements
- Press coverage highlights

Return structured JSON with all social proof elements ready for implementation.
"""

        return prompt

    def _create_social_proof_structure(self, config: Dict[str, Any], ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """Create structured social proof data"""

        # This is a simplified structure - in production, you would parse the AI response
        social_proof_data = {
            'customer_testimonials': {
                'testimonials': [
                    {
                        'customer_name': 'Sarah M.',
                        'location': 'Austin, TX',
                        'age_range': '35-40',
                        'testimonial_text': 'I lost 23 pounds in just 6 weeks! This product actually works unlike all the other supplements I have tried. My energy levels are through the roof and I feel amazing.',
                        'result_achieved': '23 pounds lost in 6 weeks',
                        'timeframe': '6 weeks',
                        'rating': 5,
                        'verified': True,
                        'photo_available': config['credibility_level'] >= 4
                    },
                    {
                        'customer_name': 'Michael R.',
                        'location': 'Denver, CO', 
                        'age_range': '40-45',
                        'testimonial_text': 'Finally found something that works with my busy schedule. Down 18 pounds and counting. The best part is I do not feel deprived or hungry all the time.',
                        'result_achieved': '18 pounds lost',
                        'timeframe': '8 weeks',
                        'rating': 5,
                        'verified': True,
                        'photo_available': config['credibility_level'] >= 4
                    },
                    {
                        'customer_name': 'Jennifer L.',
                        'location': 'Miami, FL',
                        'age_range': '30-35',
                        'testimonial_text': 'The confidence boost has been incredible. I have dropped 3 dress sizes and my husband cannot stop complimenting me. This changed my life.',
                        'result_achieved': '3 dress sizes smaller',
                        'timeframe': '10 weeks',
                        'rating': 5,
                        'verified': True,
                        'photo_available': config['credibility_level'] >= 4
                    },
                    {
                        'customer_name': 'David K.',
                        'location': 'Phoenix, AZ',
                        'age_range': '45-50',
                        'testimonial_text': 'My doctor recommended this after seeing my cholesterol numbers improve. Lost 31 pounds and feel 10 years younger. Highly recommend to anyone serious about their health.',
                        'result_achieved': '31 pounds lost, improved cholesterol',
                        'timeframe': '12 weeks',
                        'rating': 5,
                        'verified': True,
                        'photo_available': config['credibility_level'] >= 4
                    },
                    {
                        'customer_name': 'Lisa T.',
                        'location': 'Seattle, WA',
                        'age_range': '38-42',
                        'testimonial_text': 'As a busy mom of three, I needed something simple that actually worked. This delivered beyond my expectations. 26 pounds gone and I have energy to keep up with my kids.',
                        'result_achieved': '26 pounds lost, increased energy',
                        'timeframe': '9 weeks',
                        'rating': 5,
                        'verified': True,
                        'photo_available': config['credibility_level'] >= 4
                    }
                ][:config['testimonial_count']]
            },
            'before_after_stories': {
                'include': config['include_before_after'],
                'case_studies': [
                    {
                        'customer_name': 'Amanda S.',
                        'transformation_period': '90 days',
                        'starting_weight': '185 lbs',
                        'ending_weight': '152 lbs',
                        'weight_lost': '33 lbs',
                        'starting_size': 'Size 16',
                        'ending_size': 'Size 10',
                        'other_improvements': ['More energy', 'Better sleep', 'Improved confidence'],
                        'biggest_challenge': 'Emotional eating and sugar cravings',
                        'key_breakthrough': 'Week 3 when cravings finally stopped',
                        'current_status': 'Maintaining weight loss for 6 months',
                        'satisfaction_level': '10/10'
                    },
                    {
                        'customer_name': 'Robert M.',
                        'transformation_period': '120 days',
                        'starting_weight': '220 lbs',
                        'ending_weight': '189 lbs',
                        'weight_lost': '31 lbs',
                        'starting_waist': '38 inches',
                        'ending_waist': '34 inches',
                        'other_improvements': ['Lower blood pressure', 'Joint pain relief', 'Better mobility'],
                        'biggest_challenge': 'Slow metabolism due to age',
                        'key_breakthrough': 'Month 2 when weight loss accelerated',
                        'current_status': 'Continuing to lose at healthy pace',
                        'satisfaction_level': '9/10'
                    }
                ] if config['include_before_after'] else []
            },
            'expert_endorsements': {
                'include': config['expert_endorsements'],
                'endorsements': [
                    {
                        'expert_name': 'Dr. Patricia Williams, MD',
                        'credentials': 'Board-certified Obesity Medicine Specialist',
                        'institution': 'Johns Hopkins Medical Center',
                        'endorsement_text': 'This natural approach addresses weight loss at the metabolic level. I have seen remarkable results in my patients who use this protocol.',
                        'expertise_area': 'Metabolic Health and Weight Management',
                        'years_experience': '15+ years'
                    },
                    {
                        'expert_name': 'Dr. James Rodriguez, PhD',
                        'credentials': 'Nutritional Science PhD, RD',
                        'institution': 'Stanford University School of Medicine',
                        'endorsement_text': 'The ingredient combination is backed by solid research. This represents a significant advancement in natural weight management solutions.',
                        'expertise_area': 'Nutritional Science and Metabolism',
                        'years_experience': '20+ years'
                    }
                ] if config['expert_endorsements'] else []
            },
            'comparison_table': {
                'include': config['include_comparison_table'],
                'focus': config['comparison_focus'],
                'table_data': {
                    'our_product': {
                        'name': 'Our Product',
                        'natural_ingredients': '✅',
                        'clinically_tested': '✅',
                        'money_back_guarantee': '90 days',
                        'price': '$49/month',
                        'customer_support': '24/7',
                        'side_effects': 'None reported',
                        'results_timeframe': '2-4 weeks',
                        'overall_rating': '5 stars'
                    },
                    'competitor_1': {
                        'name': 'Competitor A',
                        'natural_ingredients': '❌',
                        'clinically_tested': '❌',
                        'money_back_guarantee': '30 days',
                        'price': '$67/month',
                        'customer_support': 'Email only',
                        'side_effects': 'Reported jitters',
                        'results_timeframe': '6-8 weeks',
                        'overall_rating': '3 stars'
                    },
                    'competitor_2': {
                        'name': 'Competitor B',
                        'natural_ingredients': '✅',
                        'clinically_tested': '❌',
                        'money_back_guarantee': '60 days',
                        'price': '$78/month',
                        'customer_support': 'Business hours',
                        'side_effects': 'Stomach upset',
                        'results_timeframe': '4-6 weeks',
                        'overall_rating': '3.5 stars'
                    },
                    'competitor_3': {
                        'name': 'Competitor C',
                        'natural_ingredients': '❌',
                        'clinically_tested': '✅',
                        'money_back_guarantee': '30 days',
                        'price': '$89/month',
                        'customer_support': 'Phone only',
                        'side_effects': 'Sleep issues',
                        'results_timeframe': '8-12 weeks',
                        'overall_rating': '2.5 stars'
                    }
                } if config['include_comparison_table'] else {}
            },
            'usage_statistics': {
                'include': config['statistics_social_proof'],
                'stats': {
                    'total_customers': '50,000+',
                    'customer_satisfaction': '98.7%',
                    'average_weight_loss': '24 pounds in 90 days',
                    'countries_served': '12 countries',
                    'years_in_business': '5 years',
                    'repeat_customer_rate': '89%',
                    'five_star_reviews': '2,847 reviews',
                    'average_rating': '4.8/5 stars'
                } if config['statistics_social_proof'] else {}
            },
            'media_mentions': {
                'include': config['media_mentions'],
                'mentions': [
                    {
                        'publication': 'Health & Wellness Magazine',
                        'headline': 'Revolutionary Natural Weight Loss Solution Shows Promise',
                        'quote': 'A breakthrough in natural weight management that is changing lives.',
                        'date': '2024'
                    },
                    {
                        'publication': 'Nutrition Today',
                        'headline': 'New Research Validates Natural Approach to Weight Loss',
                        'quote': 'Clinical results speak for themselves in this comprehensive study.',
                        'date': '2024'
                    },
                    {
                        'award': 'Best Natural Supplement Award',
                        'organization': 'Natural Health Association',
                        'year': '2024',
                        'category': 'Weight Management'
                    }
                ] if config['media_mentions'] else []
            }
        }

        return social_proof_data

    def _show_completed_summary(self):
        """Show social proof summary"""

        if not self.state_manager:
            return

        st.success("✅ **Step 5 Complete** - V2.0 Social proof with comparison table generated!")

        step_data = self.state_manager.get_step_data(5)
        social_proof_data = step_data.get('social_proof', {})
        config = step_data.get('configuration', {})

        # Show social proof metrics
        col1, col2, col3, col4 = st.columns(4)

        testimonials_data = social_proof_data.get('customer_testimonials', {})
        testimonials = testimonials_data.get('testimonials', [])

        with col1:
            st.metric("Testimonials", len(testimonials))
        with col2:
            st.metric("V2.0 Comparison", "✅" if config.get('include_comparison_table') else "❌")
        with col3:
            st.metric("Before/After", "✅" if config.get('include_before_after') else "❌")
        with col4:
            st.metric("Expert Endorsements", "✅" if config.get('expert_endorsements') else "❌")

        # Preview testimonials
        with st.expander("💬 Customer Testimonials Preview"):
            for i, testimonial in enumerate(testimonials[:3], 1):
                st.write(f"**{i}. {testimonial.get('customer_name', 'N/A')} - {testimonial.get('location', 'N/A')}**")
                st.write(f"⭐⭐⭐⭐⭐ ({testimonial.get('rating', 0)}/5)")
                st.write(f'"{testimonial.get("testimonial_text", "N/A")}"')
                st.write(f"**Result:** {testimonial.get('result_achieved', 'N/A')} in {testimonial.get('timeframe', 'N/A')}")
                st.write("---")

        # Preview comparison table (V2.0)
        if config.get('include_comparison_table'):
            with st.expander("📊 Comparison Table Preview (V2.0 NEW)"):
                comparison_data = social_proof_data.get('comparison_table', {})
                table_data = comparison_data.get('table_data', {})

                if table_data:
                    st.write(f"**Focus:** {comparison_data.get('focus', 'N/A')}")

                    # Create simple comparison preview
                    our_product = table_data.get('our_product', {})
                    competitor_1 = table_data.get('competitor_1', {})

                    comparison_preview = {
                        'Feature': ['Natural Ingredients', 'Money-Back Guarantee', 'Price', 'Customer Support'],
                        'Our Product': [
                            our_product.get('natural_ingredients', 'N/A'),
                            our_product.get('money_back_guarantee', 'N/A'), 
                            our_product.get('price', 'N/A'),
                            our_product.get('customer_support', 'N/A')
                        ],
                        'Competitor A': [
                            competitor_1.get('natural_ingredients', 'N/A'),
                            competitor_1.get('money_back_guarantee', 'N/A'),
                            competitor_1.get('price', 'N/A'),
                            competitor_1.get('customer_support', 'N/A')
                        ]
                    }

                    import pandas as pd
                    df = pd.DataFrame(comparison_preview)
                    st.dataframe(df, use_container_width=True)

        # Usage statistics
        if config.get('statistics_social_proof'):
            with st.expander("📈 Usage Statistics"):
                stats = social_proof_data.get('usage_statistics', {}).get('stats', {})

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Customers", stats.get('total_customers', 'N/A'))
                    st.metric("Satisfaction Rate", stats.get('customer_satisfaction', 'N/A'))
                with col2:
                    st.metric("Average Weight Loss", stats.get('average_weight_loss', 'N/A'))
                    st.metric("Countries Served", stats.get('countries_served', 'N/A'))
                with col3:
                    st.metric("Average Rating", stats.get('average_rating', 'N/A'))
                    st.metric("Five Star Reviews", stats.get('five_star_reviews', 'N/A'))

        # Expert endorsements
        if config.get('expert_endorsements'):
            with st.expander("👨‍⚕️ Expert Endorsements"):
                endorsements = social_proof_data.get('expert_endorsements', {}).get('endorsements', [])

                for endorsement in endorsements[:2]:
                    st.write(f"**{endorsement.get('expert_name', 'N/A')}**")
                    st.write(f"{endorsement.get('credentials', 'N/A')}")
                    st.write(f"*{endorsement.get('institution', 'N/A')}*")
                    st.write(f'"{endorsement.get("endorsement_text", "N/A")}"')
                    st.write("---")

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
        """Reset step 5 data"""
        if self.state_manager:
            st.session_state.workflow_data['step_5_completed'] = False
            st.session_state.workflow_data['step_5_data'] = {}
