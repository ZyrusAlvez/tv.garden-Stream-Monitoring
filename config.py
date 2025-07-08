from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)