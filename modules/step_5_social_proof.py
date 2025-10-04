import streamlit as st
from ai_providers.ai_manager import AIManager
from utils.state_management import StateManager

class SocialProofModule:
    """Step 5: Social Proof + Comparisons + Qualifier (V2.0)"""

    def __init__(self):
        self.ai_manager = AIManager()
        self.state_manager = StateManager()

    def render(self):
        st.markdown("# ⭐ Step 5: Social Proof & V2.0 Enhancements")
        st.markdown("*Testimonials + Comparison Table + Audience Qualifier*")

        st.progress(5/8, text="Step 5 of 8")

        if not self.state_manager.is_step_completed(4):
            st.warning("⚠️ Please complete Step 4 (PAS Copy) first")
            return

        if self.state_manager.is_step_completed(5):
            self._show_completed_summary()
            if st.button("🔄 Regenerate Social Proof"):
                self._reset_step()
                st.rerun()
            return

        # Configuration form
        with st.form("social_proof_form"):
            st.markdown("## ⭐ Social Proof Configuration")

            col1, col2 = st.columns(2)

            with col1:
                include_testimonials = st.checkbox("Include Testimonials", value=True)
                include_comparison = st.checkbox("Include Comparison Table (V2.0)", value=True)
                include_qualifier = st.checkbox("Include Audience Qualifier (V2.0)", value=True)

            with col2:
                include_before_after = st.checkbox("Include Before/After Showcase (V2.0)", value=False)
                testimonial_count = st.slider("Number of Testimonials", 2, 6, 3)
                competitors_count = st.slider("Competitors in Table", 2, 4, 3)

            submitted = st.form_submit_button("⭐ Generate Social Proof", type="primary")

        if submitted:
            self._generate_social_proof({
                'include_testimonials': include_testimonials,
                'include_comparison': include_comparison,
                'include_qualifier': include_qualifier,
                'include_before_after': include_before_after,
                'testimonial_count': testimonial_count,
                'competitors_count': competitors_count
            })

    def _generate_social_proof(self, config):
        with st.spinner("⭐ Generating social proof and V2.0 enhancements..."):

            # Simplified generation (would use full V2.0 prompts)
            social_proof_data = {
                'testimonials': [
                    {
                        'name': 'Sarah M., 34',
                        'rating': 5,
                        'quote': 'Finally found a keto supplement that actually works! No more keto flu headaches.',
                        'result': 'Lost 15 pounds in first month'
                    },
                    {
                        'name': 'Mike R., 42',
                        'rating': 5,
                        'quote': 'Entered ketosis in 2 days without any side effects. Game changer!',
                        'result': 'Sustained energy levels'
                    },
                    {
                        'name': 'Jessica T., 28',
                        'rating': 5,
                        'quote': 'Best investment for my keto journey. Smooth transition every time.',
                        'result': '3 successful keto cycles'
                    }
                ],
                'comparison_table': {
                    'products': [
                        {
                            'name': 'Our Product',
                            'recommended': True,
                            'price': '$97',
                            'guarantee': '90-day',
                            'rating': '4.8★ (1,247 reviews)',
                            'key_feature': 'Patent-pending ratio'
                        },
                        {
                            'name': 'Competitor A',
                            'price': '$147',
                            'guarantee': '30-day',
                            'rating': '4.2★ (342 reviews)',
                            'key_feature': 'Generic blend'
                        },
                        {
                            'name': 'Competitor B',
                            'price': '$127',
                            'guarantee': '60-day',
                            'rating': '4.5★ (891 reviews)',
                            'key_feature': 'Proprietary mix'
                        }
                    ]
                },
                'audience_qualifier': {
                    'is_for_you': [
                        'Starting keto for the first time',
                        'Have quit keto due to flu symptoms',
                        'Want rapid ketosis entry (48 hours)',
                        'Value science-backed formulations'
                    ],
                    'not_for_you': [
                        'Already in ketosis without issues',
                        'Looking for magic pill without diet',
                        'Not committed to keto lifestyle',
                        'Expecting overnight results'
                    ]
                },
                'data_points': {
                    'total_customers': '12,000+',
                    'success_rate': '94%',
                    'average_rating': '4.8/5',
                    'repeat_customers': '73%'
                },
                'configuration': config
            }

            # Save data
            self.state_manager.save_step_data(5, {
                'social_proof': social_proof_data,
                'configuration': config,
                'generated_at': st.session_state.workflow_data['last_updated']
            })
            self.state_manager.mark_step_completed(5)

            st.success("✅ Social proof and V2.0 enhancements generated!")
            st.rerun()

    def _show_completed_summary(self):
        st.success("✅ **Step 5 Complete** - Social proof + V2.0 enhancements generated!")

        step_data = self.state_manager.get_step_data(5)
        config = step_data.get('configuration', {})
        social_proof = step_data.get('social_proof', {})

        # Metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Testimonials", len(social_proof.get('testimonials', [])))
        with col2:
            st.metric("Comparison Table", "✅" if config.get('include_comparison') else "❌")
        with col3:
            st.metric("Audience Qualifier", "✅" if config.get('include_qualifier') else "❌")
        with col4:
            st.metric("V2.0 Features", sum([config.get('include_comparison', False), 
                                          config.get('include_qualifier', False),
                                          config.get('include_before_after', False)]))

        # Preview sections
        with st.expander("👥 Preview Testimonials"):
            for testimonial in social_proof.get('testimonials', []):
                st.write(f"**{testimonial.get('name', 'N/A')}** - {'⭐' * testimonial.get('rating', 5)}")
                st.write(f'"{testimonial.get('quote', 'N/A')}"')
                st.write(f"*Result: {testimonial.get('result', 'N/A')}*")
                st.write("---")

        if config.get('include_comparison'):
            with st.expander("📊 Preview Comparison Table (V2.0)"):
                comparison = social_proof.get('comparison_table', {})
                for product in comparison.get('products', []):
                    recommended = "⭐ RECOMMENDED" if product.get('recommended') else ""
                    st.write(f"**{product.get('name', 'N/A')} {recommended}**")
                    st.write(f"Price: {product.get('price', 'N/A')} | Guarantee: {product.get('guarantee', 'N/A')}")
                    st.write(f"Rating: {product.get('rating', 'N/A')}")
                    st.write("---")

        if config.get('include_qualifier'):
            with st.expander("✅ Preview Audience Qualifier (V2.0)"):
                qualifier = social_proof.get('audience_qualifier', {})

                col1, col2 = st.columns(2)
                with col1:
                    st.write("**✅ This IS For You If:**")
                    for item in qualifier.get('is_for_you', []):
                        st.write(f"• {item}")

                with col2:
                    st.write("**❌ This is NOT For You If:**")
                    for item in qualifier.get('not_for_you', []):
                        st.write(f"• {item}")

    def _reset_step(self):
        st.session_state.workflow_data['step_5_completed'] = False
        st.session_state.workflow_data['step_5_data'] = {}
