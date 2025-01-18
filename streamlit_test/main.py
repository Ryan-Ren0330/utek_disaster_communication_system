import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "admin123":  # Hardcoded password
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Please enter the rescue team password", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        return False
    
    return st.session_state["password_correct"]

def main():
    st.set_page_config(
        page_title="Wildfire Status Update System",
        page_icon="🔥",
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
    
    # Main page title
    st.title("Wildfire Status Update System")
    st.markdown("### Select Your Role")

    # Create two-column layout
    col1, col2 = st.columns(2)

    # Rescue Team Portal
    with col1:
        st.markdown("""
        ### Rescue Team Portal
        Monitor fire situations and manage rescue operations
        """)
        if st.button("Access Rescue Team Portal", key="rescue_team", use_container_width=True):
            if check_password():
                st.switch_page("pages/rescue_team.py")
            else:
                st.error("Please enter the correct password to access the Rescue Team Portal")

    # Resident Portal
    with col2:
        st.markdown("""
        ### Resident Portal
        Report fires and view safety information
        """)
        if st.button("Access Resident Portal", key="resident", use_container_width=True):
            st.switch_page("pages/resident.py")

    # Add system information
    st.markdown("---")
    st.markdown("""
    #### System Features:
    - Rescue teams can view all fire reports and manage rescue operations
    - Residents can report fire locations and view safety information
    - Real-time updates on fire development
    """)

if __name__ == "__main__":
    main()