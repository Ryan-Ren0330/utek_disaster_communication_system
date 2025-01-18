import streamlit as st
from streamlit_folium import st_folium
import folium
import datetime
import dotenv
import json
import requests

dotenv.load_dotenv()

def rescue_team_page():
    # 如果没验证过密码，或密码标记为错误，就不给访问
    if "password_correct" not in st.session_state or not st.session_state["password_correct"]:
        st.warning("You must enter the correct password first!")
        st.stop()

    st.set_page_config(
        page_title="Rescue Team Dashboard",
        page_icon="🚒",
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

    # 顶部按钮布局
    col1, col2, col3 = st.columns([1,4,1])
    with col1:
        if st.button("🏠 Home"):
            # 回到主页后可以重置一下密码相关状态
            st.session_state.show_password_box = False
            st.switch_page("main.py")

    with col3:
        if st.button("🚪 Logout"):
            st.session_state.password_correct = False
            st.session_state.show_password_box = False
            st.switch_page("main.py")

    with col2:
        st.title("Rescue Team Command Center")
    # 初始化 fire_reports 数据
    if "fire_reports" not in st.session_state:
        st.session_state["fire_reports"] = request_fire_reports()
        st.success("Fire reports loaded successfully!")
    if not st.session_state["fire_reports"]:
        st.markdown("No reports available.")

    # # 模拟数据（用于测试，可以用 resident.py 的数据代替）
    # if not st.session_state["fire_reports"]:
    #     st.session_state["fire_reports"] = [
    #         {
    #             "timestamp": datetime.datetime.now() - datetime.timedelta(minutes=10),
    #             "location": "Toronto, ON",
    #             "description": "Major fire near downtown area.",
    #             "severity": "Major",
    #             "gps": [43.651070, -79.347015],
    #             "photo": None,
    #             "user_id": "user_1",
    #             "chat_history": [
    #                 {"sender": "user_1", "message": "Please send help!", "timestamp": datetime.datetime.now() - datetime.timedelta(minutes=15)},
    #             ]
    #         },
    #         {
    #             "timestamp": datetime.datetime.now() - datetime.timedelta(minutes=30),
    #             "location": "North York, ON",
    #             "description": "Minor fire near a park.",
    #             "severity": "Minor",
    #             "gps": [43.761539, -79.411079],
    #             "photo": None,
    #             "user_id": "user_2",
    #             "chat_history": []
    #         },
    #     ]

    # 主页面内容
    col1, col2 = st.columns([2, 1])

    # 地图显示
    with col1:
        st.subheader("Fire Incident Map")
        # 显示所有火灾报告的定位点
        m = folium.Map(location=[43.7, -79.4], zoom_start=10)
        for report in st.session_state["fire_reports"]:
            print("report")
            print(report)
            folium.Marker(
                location=report["gps"],
                popup=report["description"],
                tooltip=report["location"],
                icon=folium.Icon(color="red" if report["severity"] == "Major" else "orange")
            ).add_to(m)
        st_folium(m, width=700, height=500)

    # 信息板
    with col2:
        st.subheader("Information Board")
        if st.button("Refresh Reports"):
            st.session_state["fire_reports"] = request_fire_reports()
        if not st.session_state["fire_reports"]:
            st.markdown("No reports available.")
        else:
            for idx, report in enumerate(sorted(st.session_state["fire_reports"], key=lambda x: x["timestamp"], reverse=True)):
                with st.expander(f"[{report['severity']}] {report['location']} ({report['timestamp']})"):
                    st.write(f"**Description:** {report['description']}")
                    st.write(f"**Reported at:** {report['timestamp']}")
                    st.write(f"**User ID:** {report['user_id']}")

                    # 显示地图定位
                    st.markdown(f"**Location GPS:** {report['gps']}")

                    # 显示上传的照片
                    if report["photo"]:
                        st.image(report["photo"], caption="Uploaded Photo", use_column_width=True)
                    else:
                        st.markdown("*No photo uploaded.*")

                    # 聊天记录
                    if report["chat_history"]:
                        st.markdown("**Chat History:**")
                        for chat in report["chat_history"]:
                            st.write(f"[{chat['timestamp'].strftime('%H:%M:%S')}] **{chat['sender']}**: {chat['message']}")
                    
                    # 发送消息
                    st.markdown("---")
                    message = st.text_input(f"Send message to {report['user_id']}", key=f"message_input_{idx}")
                    if st.button("Send", key=f"send_button_{idx}"):
                        if message:
                            # 保存消息到聊天记录
                            report["chat_history"].append({
                                "sender": "Rescue Team",
                                "message": message,
                                "timestamp": datetime.datetime.now()
                            })
                            st.success("Message sent successfully!")
                        else:
                            st.error("Message cannot be empty.")


def request_fire_reports():
    url = "http://localhost:5000/api/fire_reports"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []


if __name__ == "__main__":
    rescue_team_page()
