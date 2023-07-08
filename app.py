
# notes on the venv and start up
# mac:
#     python3 -m venv env
#     source ./env/bin/activate
    
# Windows: python -m venv env
# .\env\Scripts\activate

# If running tests in interactive python do the installs

# Both:
#     pip install sqlalchemy
#     pip freeze > requirements.txt

# git init notes
# git remote add origin https://github.com/CurtisONeal/book-database-sql.git
# git add .  
# git commit -m 'Iinitial commit'
# git push origin main/master

# git push origin master

# reminder for second commit.... if you just tried git push
# git push --set-upstream origin master

# starting up the app reminder to test for typos:
# python3 app.py # to see the db created

debug = True

# imports 
# 
# get our def initions models.py
#import models
import datetime
import csv
import time

# #models doesn't seem to be importing across all of these
from sqlalchemy import( create_engine, Column, Integer, String, Date)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
# from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///books.db',echo=False)  # creates a local database on your machine
#This connect cimplictly makes a db at least locally if you makd a typo

#Sessions keep track of everything you want to add or do
Session = sessionmaker(bind=engine) #binds our session to the database
Base = declarative_base()

session = Session()


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column('Title', String) # By passing the string in, we make the db column name Title
    author = Column('Author', String) 
    published_date = Column('Published', Date)
    price = Column('Price', Integer)
    def __repr__(self):
        return f'Title: {self.title}, Author: {self.author}, Date Published: {self.published_date}, Price: {self.price}'


# functions 
# add books to the database
# search books

# main menu - add, search, analysis, exit, view 
def menu():
    """"Provide prompts, get input, gete keep input"""
    while True:
        print(''' 
              \nPROGRAMMING BOOKS
              \r1) Add book
              \r2) View all books
              \r3) Search for a book
              \r4) Book Analysis
              \r5) Exit''')
        choice = input('What would you like to do? ')
        if choice in ['1','2','3','4','5']:
            return choice # return will be the only way out of the menu
        else:
            input(''' 
                   \rPlease choose one of the options above.
                   \rA number from 1-5.
                   \rPress enter to try again. ''' )

#sub menu
#    edit books
#    delete books
def submenu():
    while True:
        print(''' 
              \r1) Edit
              \r2) Delete
              \r3) Return to main menu ''')
        choice = input('What would you like to do? ')
        if choice in ['1','2','3']:
            return choice # return will be the only way out of the menu
        else:
            input(''' 
                   \rPlease choose one of the options above.
                   \rA number from 1-3.
                   \rPress enter to try again. ''' )


# data clearning
def clean_date(date_str):
    """ will take the date as string from csv and convert to datetime"""
    months_list = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    #using the index of the list where 0 = January and adding the index to it.abs

    try:
        month = int(months_list.index( split_date[0] ) + 1) 
        day =  int(split_date[1].split(',')[0]) #This cuts off the string from the comma and only keeps the string
        year = int(split_date[2])  
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
              \n ****** DATE ERROR *******
              \rThe Date fomat should include a valid Month Day, Year from the past.
              \rEx: January 13, 2003
              \rPress enter to try again: 
               \r************************** ''')
            #print(datetime.date(year, month, day)) # needs the yead, month, day as int  
        return None
    else:
        return return_date

def clean_price(price_str):
    """ will take the csv content from a field and remove the period to make an int"""
    try:
        price_float = float(price_str)
    except ValueError:
            input('''
            \n ****** PRICE ERROR *******
            \rThe Price fomat should be a number without a currency symbol 
            \r followed by a decimal and two numbers.
            \rEx: 20.31
            \rPress enter to try again: 
            \r************************** ''')
    else:
        return int(price_float) * 100 # price is in cents

def clean_id(id_str, options):
    """ will take input choice as str check if a numeral and make an int"""
    try:
        book_id = int(id_str)
    except ValueError:
            input('''
                \n ****** ID ERROR *******
                \rThe ID should be a number
                \rPress enter to try again.
                \r************************** ''')
            return
    else:
        if book_id in options:
            return book_id
        else:
            input(f'''
                \n ****** ID ERROR *******
                \rOption: {options}
                \rPress enter to try again.
                \r************************** ''')
            return

def edit_check(column_name, curent_value, ):
    """ For prce and published date we'll need to do different things, and show examples """
    print(f'\n*** EDIT {column_name} ****')
    if column_name == 'Price':
        print(f'\rCurrent Value: {curent_value/100}')
    elif column_name == 'Date':
        print(f'\rCurrent Value: {curent_value.strftime("%B %d, %Y")}')
    else:
        print(f'\rCurrent Value: {curent_value}')
    
    if column_name == 'Date' or column_name == 'Price':
        while True:
            changes = input('What would you like to change the value to be? ')
            if column_name == 'Date':
                changes = clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            elif column_name == 'Price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
    else:
        return input('What would you like to change the value to be? ')

# add data from csv
def add_csv():
    """
    add all the book from the csc, 
    clean the data, add it to our database
    """
    with open('/Users/curtisoneal/Documents/DataScience/TreeHouse SQLAlchemy/book-database/suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title == row[0] ).one_or_none() 
            # returns a book if there is one or none if not. 
            if book_in_db == None:
                if debug:
                    print(row)
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
        session.commit()
    return 0
            
# loop running the program
def app():
    app_running = True
    while app_running:
        choice = menu() # the return value from choice
        if choice == '1':
            # TODO add book
            title = input('Title: ')
            author = input('Author: ')
            date_error = True
            while date_error:
                date = input('Date Published (Ex: October 25, 2017): ') # edge February 31, 2004 doesn't exist
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input('Price (Ex: 25.56): ') # edge case $5.99
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book( title=title, author=author, published_date= date, price= price_error)
            session.add(new_book)
            session.commit()
            print('Book Added!')
            time.sleep(1.5)
        elif choice == '2':
            # TODO View all books
            for book in session.query(Book):
                print(f' {book.id} | {book.title} | {book.author} ')
            input('\nPress enter to return to the main menu. ')
        elif choice == '3':
            # Search book
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id) 
            id_error = True
            while id_error:
                id_choice = input(f'''.
                    \nId Options: {id_options}
                    \rBook id: ''')  
                id_choice = clean_id(id_choice, id_options)
                if id_choice in id_options:
                    selected_book = session.query(Book).filter(Book.id == id_choice ).first() 
                    print(f'''
                          \nYou chose:
                          \r{selected_book.title} by {selected_book.author}
                          \rPublished: {selected_book.published_date}
                          \rPrice: ${selected_book.price / 100:.2f}''')
                    id_error = False
                    sub_choice = submenu()
                    if sub_choice == '1':
                        # edit
                        selected_book.title = edit_check('Title', selected_book.title)
                        selected_book.author = edit_check('Author', selected_book.author)
                        selected_book.published_date = edit_check('Date', selected_book.published_date)
                        selected_book.price = edit_check('Price', selected_book.price)
                        session.commit()
                        print('Book updated')
                        time.sleep(1.5)
                        #print(session.dirty) # to show if our changes in the session were saved
                    elif sub_choice == '2':
                        #delete
                        session.delete(selected_book)
                        session.commit()
                        print('Book deleted!')
                        time.sleep(1.5)
                        # Note 3 will automatically jomp to the top.
        elif choice == '4':
            # TODO book Analysis oldest, newest, and total number in db.
            oldest_book = session.query(Book).order_by(Book.published_date).first()
            newest_book = session.query(Book).order_by(Book.published_date.desc()).first()
            total_books = session.query(Book).count()
            python_books = session.query(Book).filter(Book.title.like('%ython%')).count()
            print(f'''
                  \n**** BOOOK ANALYSIS ****
                  \rOldest Book: {oldest_book}
                  \rNewest Book: {newest_book}
                  \rTotal Books: {total_books}
                  \rNumber of Python Books: {python_books} 
                  ''') #Todo could make formatting nice - like prices
            input("\nPress Enter to return to main menu. ")

        else: 
            # TODO exit app -- our menu function is ensuring that we can only get strings 1-5
            print('GOODBYE')
            app_running = False
            return
 

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
    
    for book in session.query(Book):
        print(book)