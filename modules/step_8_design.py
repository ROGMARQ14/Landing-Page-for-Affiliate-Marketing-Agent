import streamlit as st
from ai_providers.ai_manager import AIManager
from utils.state_management import StateManager

class DesignModule:
    """Step 8: Design & Technical Specifications"""

    def __init__(self):
        self.ai_manager = AIManager()
        self.state_manager = StateManager()

    def render(self):
        st.markdown("# 🎨 Step 8: Design & Technical Specifications")
        st.markdown("*V2.0 Enhanced with Progressive Disclosure & Mobile-First Design*")

        st.progress(8/8, text="Step 8 of 8 - Final Step!")

        if not self.state_manager.is_step_completed(7):
            st.warning("⚠️ Please complete Step 7 (Assembly) first")
            return

        if self.state_manager.is_step_completed(8):
            self._show_completed_summary()
            if st.button("🔄 Regenerate Design Specs"):
                self._reset_step()
                st.rerun()
            return

        # Design configuration
        with st.form("design_specs_form"):
            st.markdown("## 🎨 Design & Technical Configuration")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Layout Options:**")
                layout_type = st.selectbox("Layout Type", ["Single Column", "Split Hero", "Full Width"])
                mobile_first = st.checkbox("Mobile-First Design", value=True)
                hero_viewport = st.slider("Hero Viewport Height", 50, 80, 60)

                st.markdown("**Performance:**")
                optimize_images = st.checkbox("WebP Image Optimization", value=True)
                lazy_loading = st.checkbox("Lazy Loading", value=True)
                minify_css = st.checkbox("Minified CSS", value=True)

            with col2:
                st.markdown("**V2.0 Enhancements:**")
                progressive_disclosure = st.checkbox("Progressive Disclosure (Complex Products)", value=False)
                interactive_comparison = st.checkbox("Interactive Comparison Table", value=True)
                before_after_slider = st.checkbox("Before/After Image Slider", value=False)

                st.markdown("**Accessibility:**")
                wcag_compliance = st.selectbox("WCAG Compliance", ["AA", "AAA"], index=0)
                high_contrast = st.checkbox("High Contrast Mode Support", value=True)
                keyboard_nav = st.checkbox("Full Keyboard Navigation", value=True)

            submitted = st.form_submit_button("🎨 Generate Design Specifications", type="primary")

        if submitted:
            self._generate_design_specs({
                'layout_type': layout_type,
                'mobile_first': mobile_first,
                'hero_viewport': hero_viewport,
                'optimize_images': optimize_images,
                'lazy_loading': lazy_loading,
                'minify_css': minify_css,
                'progressive_disclosure': progressive_disclosure,
                'interactive_comparison': interactive_comparison,
                'before_after_slider': before_after_slider,
                'wcag_compliance': wcag_compliance,
                'high_contrast': high_contrast,
                'keyboard_nav': keyboard_nav
            })

    def _generate_design_specs(self, config):
        with st.spinner("🎨 Generating comprehensive design specifications..."):

            # Generate design specifications
            design_data = {
                'layout_specifications': {
                    'type': config['layout_type'],
                    'hero_viewport_height': f"{config['hero_viewport']}%",
                    'mobile_first': config['mobile_first'],
                    'breakpoints': {
                        'mobile': '320px - 768px',
                        'tablet': '769px - 1024px', 
                        'desktop': '1025px+'
                    }
                },
                'visual_design': {
                    'color_palette': {
                        'primary_cta': '#E67E22',
                        'text_primary': '#2C3E50',
                        'text_secondary': '#7F8C8D',
                        'background': '#FFFFFF',
                        'accent': '#27AE60',
                        'warning': '#E74C3C'
                    },
                    'typography': {
                        'font_primary': 'Inter, Roboto, Arial, sans-serif',
                        'headline_desktop': '48-56px',
                        'headline_mobile': '28-32px',
                        'body_text': '17-19px',
                        'line_height': '1.6'
                    },
                    'spacing_system': {
                        'grid': '8px',
                        'section_padding': '80px desktop, 60px mobile',
                        'element_spacing': '24-40px'
                    }
                },
                'performance_targets': {
                    'load_time': '<3 seconds on 3G',
                    'lcp': '<2.5 seconds',
                    'fid': '<100ms',
                    'cls': '<0.1',
                    'total_page_weight': '<500KB'
                },
                'image_specifications': {
                    'format': 'WebP with JPEG fallback',
                    'max_size': '100KB per image',
                    'hero_image': '1200x800px',
                    'product_images': '800x600px',
                    'lazy_loading': config['lazy_loading']
                },
                'v2_enhancements': {
                    'progressive_disclosure': {
                        'enabled': config['progressive_disclosure'],
                        'accordion_height': '56px minimum',
                        'tab_button_height': '48px',
                        'animation_duration': '250ms ease'
                    },
                    'comparison_table': {
                        'interactive': config['interactive_comparison'],
                        'zebra_striping': True,
                        'mobile_layout': 'Stacked cards',
                        'recommended_highlight': '#F0F8FF background'
                    },
                    'before_after_slider': {
                        'enabled': config['before_after_slider'],
                        'slider_width': '800px desktop',
                        'divider_style': '4px white line with drag handle',
                        'touch_enabled': True
                    }
                },
                'accessibility': {
                    'wcag_level': config['wcag_compliance'],
                    'high_contrast': config['high_contrast'],
                    'keyboard_navigation': config['keyboard_nav'],
                    'color_contrast_ratio': '7:1 for AA, 4.5:1 minimum',
                    'focus_indicators': 'Visible focus rings',
                    'aria_labels': 'Complete ARIA labeling'
                },
                'technical_implementation': {
                    'html_version': 'HTML5 semantic structure',
                    'css_methodology': 'Mobile-first, Flexbox/Grid',
                    'javascript': 'Vanilla JS, progressive enhancement',
                    'framework_compatibility': 'Works with any CSS framework',
                    'browser_support': 'IE11+, all modern browsers'
                },
                'ab_testing_setup': {
                    'headline_variants': 'Data-testid attributes for easy swapping',
                    'cta_button_variants': 'CSS class-based color changes',
                    'section_toggles': 'Show/hide sections for testing',
                    'tracking_ready': 'Google Analytics, Facebook Pixel ready'
                },
                'configuration': config,
                'design_complete': True
            }

            # Save data
            self.state_manager.save_step_data(8, {
                'design_specifications': design_data,
                'configuration': config,
                'generated_at': st.session_state.workflow_data['last_updated']
            })
            self.state_manager.mark_step_completed(8)

            st.success("✅ Design specifications generated!")
            st.balloons()  # Celebration for completing all steps!
            st.rerun()

    def _show_completed_summary(self):
        st.success("🎉 **Step 8 Complete** - All specifications generated!")
        st.success("🚀 **Workflow Complete!** Your landing page is ready for export.")

        step_data = self.state_manager.get_step_data(8)
        design = step_data.get('design_specifications', {})
        config = step_data.get('configuration', {})

        # Key specifications
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Layout", config.get('layout_type', 'N/A'))
        with col2:
            st.metric("Hero Height", f"{config.get('hero_viewport', 60)}%")
        with col3:
            st.metric("Mobile First", "✅" if config.get('mobile_first') else "❌")
        with col4:
            v2_count = sum([
                config.get('progressive_disclosure', False),
                config.get('interactive_comparison', False),
                config.get('before_after_slider', False)
            ])
            st.metric("V2.0 Features", v2_count)

        # Performance targets
        with st.expander("⚡ Performance Targets"):
            performance = design.get('performance_targets', {})
            for target, value in performance.items():
                st.write(f"**{target.replace('_', ' ').title()}:** {value}")

        # Design specifications
        with st.expander("🎨 Visual Design System"):
            visual = design.get('visual_design', {})

            st.markdown("**Color Palette:**")
            colors = visual.get('color_palette', {})
            for color_name, hex_value in colors.items():
                st.write(f"• {color_name.replace('_', ' ').title()}: {hex_value}")

            st.markdown("**Typography:**")
            typography = visual.get('typography', {})
            for typo_element, value in typography.items():
                st.write(f"• {typo_element.replace('_', ' ').title()}: {value}")

        # V2.0 Enhancements
        with st.expander("🚀 V2.0 Enhancement Specifications"):
            v2_enhancements = design.get('v2_enhancements', {})

            for enhancement, specs in v2_enhancements.items():
                if specs.get('enabled', True):
                    st.markdown(f"**{enhancement.replace('_', ' ').title()}:**")
                    for spec_name, spec_value in specs.items():
                        if spec_name != 'enabled':
                            st.write(f"  • {spec_name.replace('_', ' ').title()}: {spec_value}")

        # Accessibility
        with st.expander("♿ Accessibility Specifications"):
            accessibility = design.get('accessibility', {})
            for a11y_feature, value in accessibility.items():
                st.write(f"**{a11y_feature.replace('_', ' ').title()}:** {value}")

        # Export ready message
        st.info("🎯 **Ready for Export!** Use the sidebar to generate HTML, Markdown, or Word documents.")

    def _reset_step(self):
        st.session_state.workflow_data['step_8_completed'] = False
        st.session_state.workflow_data['step_8_data'] = {}
