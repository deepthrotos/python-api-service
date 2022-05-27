from dotenv import load_dotenv
import os

load_dotenv()

depth_map_url = os.getenv("DEPTH_MAP_URL")
test_depth_map_url = os.getenv("TEST_DEPTH_MAP_URL")
