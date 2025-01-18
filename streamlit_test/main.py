# filename: main.py

import streamlit as st

def check_password():
    """Handles password input and validation."""
    # 初始化 session_state 的密码状态
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    # 输入密码
    password = st.text_input(
        "Please enter the rescue team password", 
        type="password",
        key="password_input"
    )

    # 提交密码的逻辑
    if st.button("Submit", key="submit_password"):
        if password == "admin123":  # 硬编码的密码
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False
            st.error("Incorrect password. Please try again.")

    return st.session_state["password_correct"]

def main():
    # 页面基本配置
    st.set_page_config(
        page_title="Wildfire Status Update System",
        page_icon="🔥",
        layout="wide",
        menu_items={},
        initial_sidebar_state="collapsed"
    )

    # 隐藏 Streamlit 默认的菜单和页脚
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="collapsedControl"] {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # 主标题
    st.title("Wildfire Status Update System")
    st.markdown("### Select Your Role")

    # 创建两列布局
    col1, col2 = st.columns(2)

    # 救援队门户
    with col1:
        st.markdown("""
        ### Rescue Team Portal
        Monitor fire situations and manage rescue operations
        """)
        if st.button("Access Rescue Team Portal", key="rescue_team", use_container_width=True):
            # 显示密码输入
            if check_password():
                st.success("Password correct! Redirecting to Rescue Team Portal...")
                st.experimental_rerun()  # 防止刷新状态丢失
                st.switch_page("rescue_team")  # 跳转到 rescue_team 页面

    # 居民门户
    with col2:
        st.markdown("""
        ### Resident Portal
        Report fires and view safety information
        """)
        if st.button("Access Resident Portal", key="resident", use_container_width=True):
            st.switch_page("resident")  # 跳转到 resident 页面

    # 添加系统功能说明
    st.markdown("---")
    st.markdown("""
    #### System Features:
    - Rescue teams can view all fire reports and manage rescue operations
    - Residents can report fire locations and view safety information
    - Real-time updates on fire development
    """)

if __name__ == "__main__":
    main()
