import streamlit as st
import dotenv
import os

dotenv.load_dotenv()

def main():
    st.set_page_config(
        page_title="Wildfire Status Update System",
        page_icon="🔥",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # 隐藏默认的 Streamlit 菜单等
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.title("Wildfire Status Update System")
    st.markdown("### Select Your Role")
    
    col1, col2 = st.columns(2)

    # ------------------ 救援队入口 ------------------
    with col1:
        st.subheader("Rescue Team Portal")
        if st.button("Access Rescue Team Portal"):
            # 按下按钮后，标记需要输入密码
            st.session_state.show_password_box = True

        # 如果已经点过按钮，就显示密码输入框和提交按钮
        if st.session_state.get("show_password_box"):
            password = st.text_input("Please enter the rescue team password:",
                                     type="password",
                                     key="rescue_password_input")
            if st.button("Submit Password"):
                passwd = os.getenv("RESCUE_TEAM_PASSWORD")
                if password == passwd:
                    st.session_state.password_correct = True
                    st.success("Password correct! Redirecting...")
                    # 与 pages/1_Rescue_Team.py 对应的页面名称“Rescue Team”
                    st.switch_page("pages/rescue_team.py")
                else:
                    st.session_state.password_correct = False
                    st.error("😕 Password incorrect")

    # ------------------ 居民入口 ------------------
    with col2:
        st.subheader("Resident Portal")
        if st.button("Access Resident Portal"):
            # 与 pages/2_Resident.py 对应的页面名称“Resident”
            st.switch_page("pages/resident.py")

    st.markdown("---")
    st.markdown("#### System Features:")
    st.markdown("- Rescue teams can view all fire reports and manage rescue operations")
    st.markdown("- Residents can report fire locations and view safety information")
    st.markdown("- Real-time updates on fire development")

if __name__ == "__main__":
    main()
