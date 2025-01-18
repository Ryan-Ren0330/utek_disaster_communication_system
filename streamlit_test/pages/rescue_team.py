# filename: rescue_team.py

import streamlit as st

def rescue_team_page():
    # Check if password is correct
    if "password_correct" not in st.session_state or not st.session_state["password_correct"]:
        st.switch_page("main.py")  # Redirect to main page if not authenticated
        return

    st.set_page_config(
        page_title="Rescue Team Dashboard",
        page_icon="🚒",
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
    
    # Header with Home and Logout buttons
    header_col1, header_col2, header_col3 = st.columns([1, 4, 1])
    with header_col1:
        if st.button("🏠 Home"):
            st.switch_page("main.py")
            
    with header_col3:
        if st.button("🚪 Logout"):
            st.session_state["password_correct"] = False
            st.switch_page("main.py")
            
    with header_col2:
        st.title("Rescue Team Command Center")

    # Main content
    col1, col2, col3 = st.columns([2,1,1])

    with col1:
        st.subheader("Fire Incident Map")
        # Map will be added here later
        st.markdown("Map will be displayed here")

    with col2:
        st.subheader("Fire Incidents")
        # List of all fire reports will be displayed here
        st.markdown("List of fire reports will appear here")

    with col3:
        st.subheader("Operation Controls")
        # Add control buttons
        st.button("Refresh Data")
        st.button("Deploy Rescue Team")
        st.button("Update Status")
        
        # Add status filter
        st.selectbox(
            "Filter by Status",
            ["All", "Pending", "In Progress", "Resolved"]
        )

if __name__ == "__main__":
    rescue_team_page()