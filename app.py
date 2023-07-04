
# notes on the venv and start up
# mac:
#     python3 -m venv env
#     source ./env/bin/activate
    
# Windows: python -m venv env
# .\env\Scripts\activate

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

debug = False

# imports 
from models import(Base, session, 
                   Book, engine)  #get our def initions models.py
import datetime
import csv


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

# functions 
# add books to the database
# edit books
# delete books
# search books

# data clearning
def clean_date(date_str):
    """ will take the date as string from csv and convert to datetime"""
    months_list = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    #using the index of the list where 0 = January and adding the index to it.abs
    month = int(months_list.index( split_date[0] ) + 1) 
    day =  int(split_date[1].split(',')[0]) #This cuts off the string from the comma and only keeps the string
    year = int(split_date[2])  
    if debug:
        print(split_date)
        print(month)
        print(day)
        print(year) 
        print(datetime.date(year, month, day)) # needs the yead, month, day as int
    return datetime.date(year, month, day)

# add data from csv
def add_csv():
    """
    add all the book from the csc, 
    clean the data, add it to our database
    """
    with open('/Users/curtisoneal/Documents/DataScience/TreeHouse SQLAlchemy/book-database/suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            print(row)


# loop running the pogram
def app():
    app_running = True
    while app_running:
        choice = menu() # the return value from choice
        if choice == '1':
            # TODO add book
            pass
        elif choice == '2':
            # TODO View all books
            pass
        elif choice == '3':
            # TODO Search book
            pass      
        elif choice == '4':
            # TODO book Analysis
            pass 
        else: 
            # TODO exit app -- our menu function is ensuring that we can only get strings 1-5
            print('GOODBYE')
            app_running = False
            return
 

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    #app()
    #add_csv()
    clean_date('July 1, 2015')
    clean_date('May 3, 2019')  