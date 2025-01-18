import streamlit as st
import json
import requests
import datetime

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
            timestamp = datetime.datetime.now().isoformat()
            user_id = timestamp
            if submitted:
                report_data = {
                    "location": loc,
                    "description": desc,
                    "severity": severity,
                    "photo": photo.getvalue() if photo else None,
                    "timestamp": timestamp,
                    "gps": [43.651070, -79.347015],
                    "user_id": user_id,
                    "chat_history": []
                }
                response = submit_fire_report(report_data)
                if response.get("status") == "success":
                    st.success("Fire report submitted successfully!")
                else:
                    print(response)
                    st.error("Failed to submit fire report.")

        st.markdown("---")
        st.subheader("Safety Information")
        st.markdown("- Nearest Shelters")
        st.markdown("- Recommended Evacuation Routes")
        st.markdown("- Rescue Team Locations")


def submit_fire_report(data):
    url = "http://localhost:5000/api/form"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(response.text)
        return {"status": "error", "message": "Failed to submit fire report."}
    return response.json()


if __name__ == "__main__":
    resident_page()
