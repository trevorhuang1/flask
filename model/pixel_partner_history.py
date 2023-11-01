# Kyle's Original Testing IPYNB: https://bearythegreenbear.github.io/csp-blog//2023/10/26/db-testing_IPYNB_2_.html

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from PIL import Image
import base64
from io import BytesIO
import json # NOTE: Can replace with Flask jsonify later

Base = declarative_base()

# Initialize DB
def initializeDatabase():
    # Global so all functions can use
    global engine, Session, session

    # Create a database connection and session
    engine = create_engine('sqlite:///database2.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create the database table
    Base.metadata.create_all(engine)

# Clear database
def clearDatabase():
    initializeDatabase()
    session.query(Images).delete()
    session.commit()
    session.close()

    #session.close()
class Images(Base):
    __tablename__ = 'images'
    imageName = Column(String, primary_key=True, nullable=False, unique=False)  # Added nullable=False for primary key
    imageFunc = Column(String, nullable=False, unique=False)  # Added nullable=False for non-nullable columns
    imageBase64 = Column(String, nullable=False, unique=False)

# Insert data into the database
def createImage(name, func, image):
    initializeDatabase()
    newImage = Images(imageName=name, imageFunc=func, imageBase64=image)
    session.add(newImage)
    session.commit()

# Query data from the database
def queryImages():
    initializeDatabase()
    images = session.query(Images).all()
    image_list = []

    for image in images:
        image_data = {
            'name': image.imageName,
            'func': image.imageFunc,
            'image': image.imageBase64
        }
        image_list.append(image_data)

    return json.dumps(image_list)  # Return JSON

# Debugging
def debugDatabase():
    print('debugged')

# Testing
if __name__ == "__main__": 
    initializeDatabase()
    createImage('Oregon_Caves.jpg', "pixelate", imageToBase64(Image.open('Oregon_Caves.jpg')))
    createImage('National_Monuments.jpg', "combine", imageToBase64(Image.open('National_Monuments.jpg')))
    """
    session.rollback()

    session.query(Images).delete()
    session.commit()

    #session.close()
    """
    