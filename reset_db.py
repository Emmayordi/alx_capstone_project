from StayFitBlog import app, db
# Import all your models here
from StayFitBlog.models import User  # Add other models as needed
"""
def reset_database():
    with app.app_context():
    users = User.query.all()
    for user in users:
        print(user.id, user.name, user.email)

        print("Database has been reset.")

if __name__ == "__main__":
    reset_database()
"""
# to see what is in database
'''
with app.app_context():
    users = User.query.all()
    for user in users:
        print(user.id, user.name, user.email)
'''
#this is to drop and to create new

with app.app_context():
    db.drop_all()  
    db.create_all() 
    users = User.query.all()
