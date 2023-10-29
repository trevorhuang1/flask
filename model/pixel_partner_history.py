# Kyle's Original Testing IPYNB: https://bearythegreenbear.github.io/csp-blog//2023/10/26/db-testing_IPYNB_2_.html

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import json # NOTE: Can replace with Flask jsonify later

Base = declarative_base()

class Images(Base):
    __tablename__ = 'images'
    imageName = Column(String, primary_key=True, nullable=False)  # Added nullable=False for primary key
    imageFunc = Column(String, nullable=False)  # Added nullable=False for non-nullable columns
    imageBase64 = Column(String, nullable=False)

# Create a database connection and session
engine = create_engine('sqlite:///database2.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create the database table
Base.metadata.create_all(engine)

# Insert data into the database
def createImage(name, func, image):
    newImage = Images(imageName=name, imageFunc=func, imageBase64=image)
    session.add(newImage)
    session.commit()

# Query data from the database
def queryImages():
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

createImage("test1", "pixelate", "base-64sdfsdfsdfsdf")
createImage("test2", "combine", "base-64yayayayayaya")
createImage("test3", "a", "sdfsdfasfsdf-ballin")
createImage("test4", "b", "waltuh")
print(queryImages())

session.rollback()

session.query(Images).delete()
session.commit()

session.close()