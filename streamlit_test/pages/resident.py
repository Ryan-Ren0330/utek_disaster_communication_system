import streamlit as st

def resident_page():
    st.set_page_config(
        page_title="Resident Portal",
        page_icon="🏘️",
        layout="wide",
        menu_items={},  # Hide menu
        initial_sidebar_state="collapsed"  # Hide sidebar
    )

    # Hide streamlit default elements
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="collapsedControl"] {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Header with Home button
    header_col1, header_col2 = st.columns([1, 5])
    with header_col1:
        if st.button("🏠 Home"):
            st.switch_page("main.py")
            
    with header_col2:
        st.title("Resident Information Center")

    # Main content
    col1, col2 = st.columns([2,1])

    with col1:
        st.subheader("Fire Incident Map")
        # Map will be added here later
        st.markdown("Map will be displayed here")

    with col2:
        st.subheader("Report Fire Incident")
        # Add fire reporting form
        with st.form("fire_report"):
            st.text_input("Location Description")
            st.text_area("Detailed Description")
            st.selectbox("Fire Severity", ["Minor", "Moderate", "Major"])
            st.file_uploader("Upload Photos (Optional)")
            st.form_submit_button("Submit Report")

        st.markdown("---")
        st.subheader("Safety Information")
        # Display nearby safety information
        st.markdown("- Nearest Shelters")
        st.markdown("- Recommended Evacuation Routes")
        st.markdown("- Rescue Team Locations")

if __name__ == "__main__":
    resident_page()