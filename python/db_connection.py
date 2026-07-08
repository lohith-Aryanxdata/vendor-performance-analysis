import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv

script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, "..", ".env")
load_dotenv(dotenv_path)

def get_engine():
    user = os.getenv("MYSQL_USER")
    password = quote_plus(os.getenv("MYSQL_PASSWORD"))  # encode special characters
    host = os.getenv("MYSQL_HOST")
    db = os.getenv("MYSQL_DB")
    
    connection_str = f"mysql+pymysql://{user}:{password}@{host}/{db}"
    engine = create_engine(connection_str)
    return engine