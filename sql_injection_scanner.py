from flask import Flask, request, session
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

DB_URL = "postgresql://" + "postgres" + ":" + "12345" + "@localhost:5432/postgres"
DB_CONFIG = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': '12345',
    'port': 5432
}
app = Flask(__name__)
engine = create_engine(DB_URL, echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)


@app.route("/register", methods=["POST"])
def register_user():

    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)

    session = Session(engine)

    user1 = User(username=username, password=password)
    session.add_all([user1])
    session.commit()
    
    session.close()
    return f"User registered successfully!"

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # username="'name' OR 'a'='a'" + ";--"
    # "username": "'random_string' OR 'a'='a' ;--",

    sql_query = "SELECT * FROM public.user WHERE username = " + username + "AND password = " + password
    print(sql_query)
    cursor.execute(sql_query)

    # cursor.execute("SELECT * FROM public.user WHERE username = %s AND password = %s", (username, password))


    record = cursor.fetchone()
    user_session = {}
    print("User record which is logged in: ", end="")
    print(record)
    if record:
        user_session['logged_user'] = username

    cursor.close()
    conn.close()

    return f"Login successful as: {record}" if 'logged_user' in user_session else "Login failed"

# @app.route("/delete/user/userid", methods=["POST"])


if __name__ == "__main__":
    app.run()