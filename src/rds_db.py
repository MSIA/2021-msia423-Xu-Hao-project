import sys
import logging

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)
Base = declarative_base()


class PhotoFeatures(Base):
    """Data model for the database to be set up for capturing photo features。"""

    __tablename__ = 'photo_features'

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


def create_db(args):
    """Create database in RDS or local with feature tables.

    Args:
        args.engine_string (str): engine string for database's creation.

    Returns:
        None
    """

    # Connect to RDS
    engine_string = args.engine_string
    try:
        engine = sqlalchemy.create_engine(engine_string)
    except:
        logger.error("Please enter correct credentials to access database.")
        sys.exit(1)

    # Create schema
    PhotoFeatures.metadata.create_all(engine)
    logger.info("Database created.")


class PhotoManager:

    def __init__(self, app=None, engine_string=None):
        """
        Args:
            app Flask: Flask app
            engine_string (str): Engine string
        """
        if app:
            self.db = SQLAlchemy(app)
            self.session = self.db.session
        elif engine_string:
            engine = sqlalchemy.create_engine(engine_string)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        else:
            raise ValueError("Need either an engine string or a Flask app to initialize")

    def close(self) -> None:
        """Closes session
        Returns: None
        """
        self.session.close()
