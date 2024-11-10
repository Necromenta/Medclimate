import os
from dotenv import load_dotenv
#%%

load_dotenv()

DATABASE_CONFIG = {
    "dbname": os.getenv("DB_NAME"),    # Your existing database name
    "user": os.getenv("DB_USER"),   # Your PostgreSQL username
    "password": os.getenv("DB_PASSWORD"), # Your PostgreSQL password
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}
# %%
