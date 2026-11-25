
from database import SessionLocal
from models import User, Task, Comment

# Create a database session
db = SessionLocal()

try:
    # Check users table
    users = db.query(User).all()
    print("Users table:", len(users), "records")

    # Check tasks table
    tasks = db.query(Task).all()
    print("Tasks table:", len(tasks), "records")

    # Check comments table
    comments = db.query(Comment).all()
    print("Comments table:", len(comments), "records")

    print("\nAll SQLAlchemy models are working!")

except Exception as error:
    print("Error:", error)

finally:
    db.close()
