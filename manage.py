# -*-coding:utf-8-*-
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from ihome import create_app, db

app = create_app('development')
manager = Manager(app)

# 数据库迁移
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    return 'index'


if __name__ == '__main__':
    manager.run()
