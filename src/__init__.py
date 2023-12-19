import flask
import sqlalchemy
from sqlalchemy.orm import sessionmaker

# Local imports.
from src.db.schemas import Base, User

DB_CONNECTION_STRING = 'mysql+pymysql://admin:password@127.0.0.1:3306/db'
db_engine = sqlalchemy.create_engine(
    DB_CONNECTION_STRING,
    echo=True, # Set to True to see SQL queries in the console.
)


# Start a flask app in development mode where the templates are reloaded upon change.
app = flask.Flask(
    import_name=__name__,
    template_folder='templates',
    static_folder='static'
)

@app.route("/")
def index() -> str:
    return "Hello, world!"

def init_dev_server() -> None:
    
    # Initialize connection to database.
    db_conn = db_engine.connect()
    
    # Create all tables using the metadata.
    Base.metadata.create_all(db_engine)
    
    # Create a session.
    SessionMaker = sessionmaker(bind=db_engine)
    db_session = SessionMaker()
    # app.run(
    #     port=5000,   
    # )
    
    db_session.add(User(username="test", code=123456, balance=10000))
    db_session.commit()
    
    print("Stopping the server...")
    db_conn.close() # CLose the database connection.
    db_engine.dispose() # Dispose of the database engine.
    print("Server stopped.")