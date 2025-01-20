import streamlit as st
from streamlit_folium import st_folium
import folium
import datetime
import json
import requests
import base64
from streamlit_geolocation import streamlit_geolocation

def resident_page():
    st.set_page_config(
        page_title="Resident Portal",
        page_icon="🏘️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Initialize session state
    if 'location' not in st.session_state:
        st.session_state.location = None
    if 'fire_reports' not in st.session_state:
        st.session_state.fire_reports = []
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'user_id' not in st.session_state:
        st.session_state.user_id = f"user_{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # Hide default Streamlit UI
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Top navigation buttons
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("🏠 Home"):
            st.session_state.show_password_box = False
            st.switch_page("main.py")

    with col2:
        st.title("Resident Information Center")

    # Layout columns
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Fire Incident Map")

        # Default location (Toronto)
        default_location = [43.7, -79.4]

        # Determine map center based on session state
        if (
            st.session_state.location
            and st.session_state.location.get('latitude') is not None
            and st.session_state.location.get('longitude') is not None
        ):
            map_center = [
                st.session_state.location['latitude'],
                st.session_state.location['longitude']
            ]
        else:
            map_center = default_location

        # Initialize Folium map
        m = folium.Map(location=map_center, zoom_start=12)

        # Mark user's current location
        if (
            st.session_state.location
            and st.session_state.location.get('latitude') is not None
            and st.session_state.location.get('longitude') is not None
        ):
            folium.Marker(
                location=[
                    st.session_state.location['latitude'],
                    st.session_state.location['longitude']
                ],
                popup="Your Location",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

        # Add fire reports to the map
        for report in st.session_state.fire_reports:
            folium.Marker(
                location=report["gps"],
                popup=f"""
                <b>{report['location']}</b><br>
                Severity: {report['severity']}<br>
                {report['description']}
                """,
                tooltip=report["location"],
                icon=folium.Icon(
                    color="red" if report["severity"] == "Major"
                    else "orange" if report["severity"] == "Moderate"
                    else "green"
                )
            ).add_to(m)

        # Render the map
        st_folium(m, width=700, height=500)



    with col_right:
        st.subheader("Report Fire Incident")
        st.subheader("🔍 Location Status")

    # Get location from geolocation function
        location_data = streamlit_geolocation()
        if location_data != "No Location Info" and isinstance(location_data, dict):
            if "latitude" in location_data and "longitude" in location_data:
                st.session_state.location = {
                    "latitude": location_data["latitude"],
                    "longitude": location_data["longitude"]
                }
                st.info(f"Current GPS: {st.session_state.location}")
            else:
                st.warning(f"Unexpected data: {location_data}")
        else:
            st.warning("No location captured yet. Press the button to allow location access.")
        with st.form("fire_report"):
            loc = st.text_input("Location Description")
            desc = st.text_area("Detailed Description")
            severity = st.selectbox("Fire Severity", ["Minor", "Moderate", "Major"])
            photo = st.file_uploader("Upload Photos (Optional)")
            submitted = st.form_submit_button("Submit Report")
            if submitted:
                if not loc or not desc:
                    st.error("Please fill in all required fields.")
                elif not (
                    st.session_state.location
                    and st.session_state.location.get('latitude') is not None
                    and st.session_state.location.get('longitude') is not None
                ):
                    st.error("Location data is required. Please allow location access.")
                else:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    user_id = f"user_{timestamp}" if not st.session_state.user_id else st.session_state.user_id
                    photo_data = base64.b64encode(photo.read()).decode('utf-8') if photo else None
                    report_data = {
                        "location": loc,
                        "description": desc,
                        "severity": severity,
                        "photo": photo_data,
                        "timestamp": timestamp,
                        "gps": [
                            st.session_state.location['latitude'],
                            st.session_state.location['longitude']
                        ],
                        "user_id": user_id,
                        "chat_history": []
                    }
                    response = submit_fire_report(report_data)
                    if response.get("status") == "success":
                        st.session_state.fire_reports.append(report_data)
                        st.success("Fire report submitted successfully!")
                        
                    else:
                        st.error("Failed to submit fire report.")

        st.markdown("---")
        st.subheader("Messages from Rescue Team")

        # Fetch chat history
        if not st.session_state.user_id:
            st.session_state.user_id = f"user_{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        user_id = st.session_state.user_id
        
        # Refresh button to get the latest chat history
        if st.button("🔄 Refresh Messages"):
            st.session_state.chat_history = fetch_history(user_id)
            st.success("Chat history refreshed!")

        # Display chat history
        if st.session_state.chat_history:
            for chat in st.session_state.chat_history:
                sender = chat.get("sender", "Rescue Team")
                message = chat.get("message", "No message")
                timestamp = chat.get("timestamp", "Unknown time")
                st.markdown(f"**{sender}** [{timestamp}]: {message}")
        else:
            st.markdown("No messages from the rescue team yet.")

        st.markdown("---")
        st.subheader("Safety Information")
        st.markdown("- Nearest Shelters")
        st.markdown("- Recommended Evacuation Routes")
        st.markdown("- Rescue Team Locations")


def submit_fire_report(data):
    url = "http://localhost:8000/api/form"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            return {"status": "error", "message": "Failed to submit fire report."}
        return response.json()
    except Exception as e:
        print(e)
        return {"status": "error", "message": "An error occurred."}


def fetch_history(user_id):
    url = "http://localhost:8000/api/fetch_chat_history"
    headers = {"Content-Type": "application/json"}
    data = {"user_id": user_id}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return []


if __name__ == "__main__":
    resident_page()
