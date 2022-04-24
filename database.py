from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# usage SQLlite only for demo purposes
# connection with database, creating connection session object to connect with database
engine = create_engine('sqlite:///database.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


# function to initialize tables in database
def init_db():
    import models
    Base.metadata.create_all(bind=engine)
