from sqlalchemy import *

from database.db import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)

    source = Column(String(100))
    title = Column(Text)
    summary = Column(Text)

    category = Column(String(100))

    publication_date = Column(DateTime)

    url = Column(Text)

    importance = Column(Integer)

    created_at = Column(DateTime)
