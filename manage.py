from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import APP
from database.models import db, Movie, Actor

migrate = Migrate(APP, db)
manager = Manager(APP)

manager.add_command('db', MigrateCommand)

# custom seed command
@manager.command
def seed():
    # seed movie
    Movie(title='6 Underground', release_date='2019-12-13').insert()
    Movie(title='Now You See Me', release_date='2013-05-21').insert()
    Movie(title='Deadpool', release_date='2016-01-21').insert()

    # seed actor
    Actor(name='Ryan Reynolds', age=43, gender='male').insert()
    Actor(name='Melanie Laurent', age=36, gender='female').insert()
    Actor(name='Adria Arjona', age=27, gender='female').insert()
    Actor(name='Dave Franco', age=34, gender='male').insert()

if __name__ == '__main__':
    manager.run()
