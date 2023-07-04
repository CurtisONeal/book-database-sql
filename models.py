# imports

from sqlalchemy import( create_engine, Column, 
                       Integer, String, Date)
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///books.db',echo=True)  # creates a local database on your machine
#This connect cimplictly makes a db at least locally if you makd a typo

#Sessions keep track of everything you want to add or do
Session = sessionmaker(bind=engine) #binds our session to the database
session = Session()
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column('Title', String) # By passing the string in, we make the db column name Title
    author = Column('Author', String) 
    published_date = Column('Published', Date)
    price = Column('Price', Integer)
    
    def __repr__(self):
        return f'Title: {self.title}, Author: {self.author}, Date Published: {self.date_published}, Price: {self.price}'

# create a db 
# books.db
# create a model 
# title, author, date published, price