import os
import sys
import logging

import pandas as pd
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)
Base = declarative_base()


class Features(Base):
    """Create a data model for the database to be set up for capturing photo features
    """

    __tablename__ = 'features'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=False, nullable=False)
    contrast = Column(Float, unique=False, nullable=False)
    shadow = Column(Float, unique=False, nullable=False)
    dark = Column(Float, unique=False, nullable=False)
    light = Column(Float, unique=False, nullable=False)
    highlight = Column(Float, unique=False, nullable=False)
    R_average = Column(Float, unique=False, nullable=False)
    G_average = Column(Float, unique=False, nullable=False)
    B_average = Column(Float, unique=False, nullable=False)
    sharpness = Column(Float, unique=False, nullable=False)
    red_average_H = Column(Float, unique=False, nullable=False)
    red_average_S = Column(Float, unique=False, nullable=False)
    red_average_L = Column(Float, unique=False, nullable=False)
    orange_average_H = Column(Float, unique=False, nullable=False)
    orange_average_S = Column(Float, unique=False, nullable=False)
    orange_average_L = Column(Float, unique=False, nullable=False)
    yellow_average_H = Column(Float, unique=False, nullable=False)
    yellow_average_S = Column(Float, unique=False, nullable=False)
    yellow_average_L = Column(Float, unique=False, nullable=False)
    green_average_H = Column(Float, unique=False, nullable=False)
    green_average_S = Column(Float, unique=False, nullable=False)
    green_average_L = Column(Float, unique=False, nullable=False)
    cyan_average_H = Column(Float, unique=False, nullable=False)
    cyan_average_S = Column(Float, unique=False, nullable=False)
    cyan_average_L = Column(Float, unique=False, nullable=False)
    blue_average_H = Column(Float, unique=False, nullable=False)
    blue_average_S = Column(Float, unique=False, nullable=False)
    blue_average_L = Column(Float, unique=False, nullable=False)
    purple_average_H = Column(Float, unique=False, nullable=False)
    purple_average_S = Column(Float, unique=False, nullable=False)
    purple_average_L = Column(Float, unique=False, nullable=False)


def _generate_engine_string():
    conn_type = "mysql+pymysql"
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST")
    port = os.getenv("MYSQL_PORT")
    db_name = os.getenv("DATABASE_NAME")
    engine_string = f"{conn_type}://{user}:{password}@{host}:{port}/{db_name}"
    return engine_string


def create_db(args):
    """ Create database in RDS or local with feature tables. """

    # Connect to RDS
    engine_string = _generate_engine_string()
    try:
        engine = sqlalchemy.create_engine(engine_string)
    except:
        logger.error("Please enter correct credentials to access database.")
        sys.exit(1)

    # Create schema
    Features.metadata.create_all(engine)
    logger.info("Database created.")

    # Log available tables
    query = "show tables;"
    df = pd.read_sql(query, con=engine)
    logger.info('Tables available: {}'.format(list(df.iloc[:, 0])))

