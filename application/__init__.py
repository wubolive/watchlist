import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'
""" 数据库链接信息，配置来自环境变量 """
DB_USER = os.environ.get('DATABASE_USERNAME')
DB_PASS = os.environ.get('DATABASE_PASSWORD')
DB_HOST = os.environ.get('DATABASE_HOST')
DB_PORT = os.environ.get('DATABASE_PORT')
DB_NAME = os.environ.get('DATABASE_DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(DB_USER, DB_PASS, DB_HOST,
                                                                                             DB_PORT, DB_NAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'login'
# login_manager.login_message = 'Your custom message'


@app.context_processor
def inject_user():
    from .models import User
    user = User.query.first()
    return dict(user=user)  # 返回字典，等同于 return {'user': user}


from . import views, errors, commands
