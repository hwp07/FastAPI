from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

# địa chỉ MYSQL
url_database = "mysql+pymysql://root:21082007@localhost:3306/ecommerce_db"

engine = create_engine(url_database)

SeeionLocal = sessionmaker(
    autoflush=False,
    autocommit= False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SeeionLocal()

    try:
        yield db
    finally:
        db.close()