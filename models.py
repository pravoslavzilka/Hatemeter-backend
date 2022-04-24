from sqlalchemy import Column, Integer, String
from database import Base


# database structure
class Website(Base):
    __tablename__ = "websites"
    id = Column(Integer, primary_key=True)
    url = Column(String(750), unique=True)
    title = Column(String(250))
    paragraph_sequence = Column(String(2500))
    negative_columns = Column(String(1500))
    negative_count = Column(Integer)
    positive_count = Column(Integer)

    def __init__(self, url, title):
        self.title = title
        self.url = url

