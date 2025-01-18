# Wildfire Status Updates System

A real-time communication platform designed to facilitate information exchange between residents and rescue teams during wildfire emergencies. The system provides an interactive map interface, incident reporting capabilities, and two-way communication features.

## Features

- 🗺️ Interactive map interface showing fire incidents
- 📍 Real-time location tracking
- 📱 Two-way communication between residents and rescue teams
- 📸 Photo upload capabilities
- 🚨 Severity classification system
- 🔒 Secure rescue team portal
- 📊 Comprehensive incident management dashboard

## Directory Structure

```
wildfire-status-system/
├── app/
│   ├── main.py
│   ├── pages/
│   │   ├── resident.py
│   │   └── rescue_team.py
│   ├── backend/
│   │   └── app_form_service.py
│   └── data/
│       └── form_data.json
├── requirements.txt
└── .env

```

## Files Overview

- `main.py`: Main application entry point with role selection interface
- `resident.py`: Resident portal for reporting incidents and receiving updates
- `rescue_team.py`: Secure rescue team dashboard for managing incidents
- `app_form_service.py`: Backend Flask service handling data and API endpoints
- `form_data.json`: JSON file storing incident reports and chat histories

## Prerequisites

- Python 
- pip (Python package installer)
- Modern web browser with location services enabled

## Dependencies

```
streamlit==1.41.1
Flask==3.0.3
folium==0.19.4
requests==2.32.3
python-dotenv==0.21.0
streamlit-folium==0.24.0
streamlit-geolocation==0.0.10
altair==5.5.0
pandas==2.2.3
numpy==2.2.1
Pillow==11.1.0
geocoder==1.38.1
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Ken-2511/utek_disaster_communication_system.git
cd wildfire-status-system
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the root directory with the following content:
```
RESCUE_TEAM_PASSWORD=your_secure_password
```

## Running the Application

1. Start the Flask backend service:
```bash
cd app
python app_form_service.py
```
The backend service will run on http://localhost:5000

2. In a new terminal, start the Streamlit application:
```bash
cd app
streamlit run main.py
```
The application will open in your default web browser at http://localhost:8501

## Usage

### For Residents:
1. Click "Access Resident Portal"
2. Allow location access when prompted
3. Report incidents using the form
4. Monitor rescue team responses in the message center

### For Rescue Teams:
1. Click "Access Rescue Team Portal"
2. Enter the secure password
3. View all reported incidents on the map
4. Manage incidents through the information board
5. Communicate with residents through the chat interface

## Security Notes

- Keep the .env file secure and never commit it to version control
- Regularly update the rescue team password
- Ensure secure deployment in production environments

## Development

To contribute to the project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Project Structure Details

### Frontend (Streamlit)
- Built with Streamlit for rapid deployment
- Uses Folium for interactive maps
- Implements streamlit-geolocation for location tracking

### Backend (Flask)
- RESTful API design
- JSON file-based storage
- Handles form submissions and chat history

## Troubleshooting

Common issues and solutions:

1. Location not working
   - Ensure location services are enabled in your browser
   - Allow location access when prompted

2. Cannot access rescue team portal
   - Verify the correct password in .env file
   - Check if .env file is in the correct location

3. Map not loading
   - Check internet connection
   - Clear browser cache

## License

[MIT License](LICENSE)

## Contact

For support or queries, please contact [zhenghao.ni@mail.utoronto.ca]

## Acknowledgments

- Streamlit team for the excellent framework
- Folium contributors for the mapping capabilities
- All contributors to this project
