
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

# start up notes:
# python3 app.py # to see the db created

# import models.py
from models import(Base, session, 
                   Book, engine)



# main menu - add, search, analysis, exit, view 
# functions 
# add books to the database
# edit books
# delete books
# search books
# data clearning
# loop running the pogram

if __name__ == '__main__':
    Base.metadata.create_all(engine)