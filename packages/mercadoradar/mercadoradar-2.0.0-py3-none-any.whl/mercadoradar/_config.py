import os

from dotenv import load_dotenv

load_dotenv()

api_token: str = os.getenv('MERCADORADAR_API_TOKEN')
