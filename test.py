
my_posts=[{
        "id":1,
        "title": "Check Out this beautiful place",
        "content": "content of post 1",
        "published":True,
        "rating": None
    },{
        "id":10,
        "title": "Check Out this beautiful place",
        "content": "content of post 2",
        "published":True,
        "rating": None
    }]

def find_index_post(id):
    for ix, post in enumerate(my_posts):
        if post['id']==id:
            return ix

new_post={
        "id":10,
        "title": "Check Out this beautiful place in cameroon",
        "content": "content of post updated",
        "published":True,
        "rating": None
    }
index=find_index_post(10)
if index is not None:
    old_post=my_posts[index]
    if new_post["title"] is not None:
        old_post["title"]=new_post["title"]
    if new_post["content"] is not None:
        old_post["content"]=new_post["content"]
    print(old_post)




import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connection successful!")
    
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()
    
    # Example query
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Current Time:", result)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Connection closed.")

except Exception as e:
    print(f"Failed to connect: {e}")
