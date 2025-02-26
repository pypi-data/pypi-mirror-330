import uuid
import requests
import os
from datetime import datetime
from .config import BASE_URL, ALLOWED_OPTIMISATION_TYPES, ALLOWED_VIDEO_EXTENSIONS, ALLOWED_MODES_OF_TRAVEL

def enforce_https(url):
    """
    Ensure that the URL uses HTTPS.

    Args:
        url (str): The URL to check.

    Raises:
        ValueError: If the URL does not start with 'https'.
    """
    if not url.startswith('https'):
        raise ValueError("API URL must start with 'https'")

class Urbani:
    def __init__(self, username, password):
        """
        Initialise the Urbani class with user authentication details.

        Args:
            username (str): Username for authentication.
            password (str): Password for authentication.
        """
        self.username = username
        self.password = password
        self.token, self.login_response = self.get_login_token()

    def get_login_token(self):
        """
        Authenticate and retrieve a login token.

        Returns:
            tuple: Token and login response message.
        """
        login_url = f"{BASE_URL}/api/login"
        enforce_https(login_url) 

        credentials = {
            "username": self.username,
            "password": self.password
        }
        try:
            response = requests.post(login_url, json=credentials, timeout=40)  
            response.raise_for_status()
            return response.json().get("token"), "Login successful"
        except requests.RequestException as ex:
            print(f"Error during login: {ex}") 
            return None, "Login failed"

    def make_authorised_request(self, endpoint, method='GET', data=None, json=None, files=None):
        """
        Make an authorised request to the API.

        Args:
            endpoint (str): API endpoint to be accessed.
            method (str): HTTP method (GET, POST, etc.).
            data (dict): Data to be sent in the request body.
            json (dict): JSON to be sent in the request body.
            files (dict): Files to be sent in the request.

        Returns:
            dict: JSON response from the API.
        """
        if not self.token:
            return {"error": "Authentication token is missing"}

        url = f"{BASE_URL}{endpoint}"
        enforce_https(url) 

        headers = {
            "Authorization": f"Bearer {self.token}",
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY'
        }
        try:
            response = requests.request(method, url, headers=headers, data=data, json=json, files=files, verify=True, timeout=30)  # Increased timeout
            response.raise_for_status()
            return response.json()
        except requests.RequestException as ex:
            print(f"Error making authorised request: {ex}") 
            return {"error": str(ex)}

    def calculate_route(self, coordinates, optimisation_type="shortest_path", mode_of_travel="walk"):
        """
        Calculate the optimal route based on given coordinates and optimisation criteria.

        Args:
            coordinates (list): List of three coordinates in the format [[lon1, lat1], [lon2, lat2], [lon3, lat3]].
            optimisation_type (str): Type of optimisation (e.g., 'shortest_path').
            mode_of_travel (str): Mode of travel (e.g., 'walk').

        Returns:
            dict: JSON response containing the calculated route or an error message.
        """
        if len(coordinates) != 3:
            return {"error": "Exactly three coordinates should be provided."}

        if optimisation_type not in ALLOWED_OPTIMISATION_TYPES:
            return {"error": f"Invalid optimisation type. Allowed values are: {', '.join(ALLOWED_OPTIMISATION_TYPES)}"}

        if mode_of_travel not in ALLOWED_MODES_OF_TRAVEL:
            return {"error": f"Invalid mode of travel. Allowed values are: {', '.join(ALLOWED_MODES_OF_TRAVEL)}"}

        location = str(uuid.uuid4()) 

        endpoint = "/api/route_calculator"
        route_payload = {
            "location": location,
            "feature": {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordinates
                },
                "properties": {
                    "drawingType": "route",
                    "optimisationType": optimisation_type,
                    "modeOfTravel": mode_of_travel
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        return self.make_authorised_request(endpoint, method='POST', json=route_payload)

    def analyse_video(self, upload_file_path, user_prompt, fps):
        """
        Analyse a video file with a given frame rate and user prompt.

        Args:
            upload_file_path (str): Path to the video file.
            user_prompt (str): Description of the analysis to be performed.
            fps (int): Frames per second for the analysis.

        Returns:
            dict: JSON response from the video analysis API or an error message.
        """
        if not os.path.isfile(upload_file_path):
            return {"error": "File does not exist."}

        file_extension = os.path.splitext(upload_file_path)[1].lower()
        if file_extension not in ALLOWED_VIDEO_EXTENSIONS:
            return {"error": f"Invalid video file extension. Allowed extensions are: {', '.join(ALLOWED_VIDEO_EXTENSIONS)}"}

        upload_endpoint = "/api/upload_video"
        with open(upload_file_path, 'rb') as file:
            files = {'file': file}
            upload_response = self.make_authorised_request(upload_endpoint, method='POST', files=files)

        if upload_response and 'error' not in upload_response:
            video_url = upload_response['video_url']
            convert_endpoint = "/api/convert_video"
            form_data = {
                'video_url': video_url,
                'user_prompt': user_prompt,
                'fps': fps
            }
            return self.make_authorised_request(convert_endpoint, method='POST', data=form_data)
        else:
            return upload_response

    def analyse_location(self, location_type, address=None, location=None, transaction_type=None, business_type=None):
        """
        Analyse a specific location based on provided criteria.

        Args:
            location_type (str): Type of the location (e.g., 'residential').
            address (str, optional): Address of the location.
            location (dict, optional): Dictionary containing latitude and longitude of the location.
            transaction_type (str, optional): Type of transaction (e.g., 'buy', 'rent').
            business_type (str, optional): Type of business (e.g., 'retail').

        Returns:
            dict: JSON response from the location analysis API or an error message.
        """
        endpoint = "/api/analyse-location"
        location_data = {
            "locationType": location_type,
            "transactionType": transaction_type,
            "businessType": business_type,
            "address": address,
            "location": location
        }
        return self.make_authorised_request(endpoint, method='POST', json=location_data)

    def mapspeaker(self, location):
        """
        Interact with the map speaker API to get information about a specific location.

        Args:
            location (str): The location to get information about.

        Returns:
            dict: JSON response from the map speaker API or an error message.
        """
        endpoint = f"/api/chat?location={location}"
        return self.make_authorised_request(endpoint)

    def get_pois_from_buffer(self, coordinates):
        """
        Fetch points of interest (POIs) within a specific buffer area.

        Args:
            coordinates (list): Coordinates defining the buffer area in the format [[[lon1, lat1], [lon2, lat2], ...]].

        Returns:
            dict: JSON response from the POI-fetching API or an error message.
        """
        endpoint = "/api/fetch_pois"
        buffer_data = {
            "type": "Polygon",
            "coordinates": [coordinates]
        }
        return self.make_authorised_request(endpoint, method='POST', json=buffer_data)

# Example usage
if __name__ == "__main__":
    username = os.getenv("URBANI_USERNAME")
    password = os.getenv("URBANI_PASSWORD")
    urbani = Urbani(username, password)

    print(urbani.login_response)  

    # Example of calculating a route with validation
    route = urbani.calculate_route(
        coordinates=[
            [-0.1438, 51.5416],  # Coordinates for Camden, London
            [-0.1365, 51.5136],  # Coordinates for Soho, London
            [-0.1276, 51.5074]   # Coordinates for Trafalgar Square, London
        ],
        optimisation_type="shortest_path",
        mode_of_travel="walk"
    )
    print(route)

    # Example of analysing a location
    location_analysis = urbani.analyse_location(
        location_type="residential",
        address="123 Main Street",
        location={"lat": 51.5074, "lng": -0.1278}
    )
    print(location_analysis)

    # Example of analysing video
    video_analysis = urbani.analyse_video("brixton.mp4", "count cars", 2)
    print(video_analysis)

