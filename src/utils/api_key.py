import os
from dotenv import load_dotenv


load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if __name__ == "__main__":
    print(GOOGLE_API_KEY)
