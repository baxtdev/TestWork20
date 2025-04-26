import os,redis
from dotenv import load_dotenv

load_dotenv()

SYNC_DATABASE_URL = os.environ.get('SYNC_DATABASE_URL') 
DATABASE_URL = os.environ.get('DATABASE_URL')
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_BROKER_URL =f"redis://{REDIS_HOST}:6379/0"
API_KEY = "your_api_key" 

redis_client = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)

