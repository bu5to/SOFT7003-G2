from datetime import date
import click
from base import Session, engine, Base
#from flask.cli import with_appcontext
from flask.cli import with_appcontext
from models import User

@click.command()
@with_appcontext
def create_tables():
    Base.metadata.drop_all(bind=engine, tables=[User.__table__])
    Base.metadata.create_all(engine)

    session = Session()

    u1 = User("testuser", "Sample Text", "testuser@brookes.ac.uk", "password")

    session.add(u1)

    session.commit()
    print("Tables have been created.")
    session.close()