from flask.ext.script import Manager

from hockeyage.web import app

manager = Manager(app)


@manager.command
def hello():
    print "hello"
ear
cd 
if __name__ == "__main__":
    manager.run()