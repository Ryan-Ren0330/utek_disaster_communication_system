import streamlit as st
import json

def resident_page():
    st.set_page_config(
        page_title="Resident Portal",
        page_icon="🏘️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # 隐藏默认 Streamlit 元素
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # 顶部按钮
    col1, col2 = st.columns([1,5])
    with col1:
        if st.button("🏠 Home"):
            st.session_state.show_password_box = False
            st.switch_page("main.py")

    with col2:
        st.title("Resident Information Center")

    col_left, col_right = st.columns([2,1])

    with col_left:
        st.subheader("Fire Incident Map")
        st.markdown("Map will be displayed here...")

    with col_right:
        st.subheader("Report Fire Incident")
        with st.form("fire_report"):
            loc = st.text_input("Location Description")
            desc = st.text_area("Detailed Description")
            severity = st.selectbox("Fire Severity", ["Minor", "Moderate", "Major"])
            photo = st.file_uploader("Upload Photos (Optional)")
            submitted = st.form_submit_button("Submit Report")
            if submitted:
                st.success("Fire report submitted!")

        st.markdown("---")
        st.subheader("Safety Information")
        st.markdown("- Nearest Shelters")
        st.markdown("- Recommended Evacuation Routes")
        st.markdown("- Rescue Team Locations")

if __name__ == "__main__":
    resident_page()
