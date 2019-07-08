import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import *

class DBConnector:
    def __init__(self, db_name):
        """Database connector.

            Attributes:
                engine (object) :
                session (object) :

            Args:
                db_path (str) : Database path.

        """
        self.db_name = db_name
        db_path = 'sqlite:///./' + self.db_name + '.db'
        self.engine = create_engine(db_path, echo=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close(self):
        """Close database session and dispose database engine.
        """
        self.session.close()
        self.engine.dispose()

    def update_schema(self):
        try:
            # Create all table for that database
            eval(self.db_name + "_schema").Base.metadata.create_all(self.engine, checkfirst=True)
        except Exception as e:
            print("Error occurs in update_schema: " + str(e))
            self.close()
            sys.exit(1)


def setup_db(db_names):
    """Setup databases.
    """
    try:
        for db_name in db_names:
            db_connector = DBConnector(db_name)
            db_connector.update_schema()
            db_connector.close()
    except Exception as e:
        print("Error occurs in setup_db: " + str(e))
        sys.exit(1)
