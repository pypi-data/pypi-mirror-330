# Description: Configuration file for the Urbani API

BASE_URL = 'https://www.urban-i.ai'
ALLOWED_OPTIMISATION_TYPES = [
    'shortest_path', 'green_areas', 'residential_avoidance',
    'maximise_toilets', 'improve_walkability', 'avoid_crowd'
]
ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi']
ALLOWED_MODES_OF_TRAVEL = ['walk', 'drive', 'bike']