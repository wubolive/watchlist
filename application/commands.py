import click

from application import app, db
from application.models import User, Movie


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """
    初始化数据库表：flask initdb
    删除表后重新创建：flask initdb --drop
    """
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """
    初始化虚拟数据：flask forge
    """
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988', 'platform': 'imdb'},
        {'title': 'Dead Poets Society', 'year': '1989', 'platform': 'imdb'},
        {'title': 'A Perfect World', 'year': '1993', 'platform': 'imdb'},
        {'title': 'Leon', 'year': '1994', 'platform': 'imdb'},
        {'title': 'Mahjong', 'year': '1996', 'platform': 'imdb'},
        {'title': 'Swallowtail Butterfly', 'year': '1996', 'platform': 'imdb'},
        {'title': 'King of Comedy', 'year': '1999', 'platform': 'imdb'},
        {'title': 'Devils on the Doorstep', 'year': '1999', 'platform': 'imdb'},
        {'title': 'WALL-E', 'year': '2008', 'platform': 'imdb'},
        {'title': 'The Pork of Music', 'year': '2012', 'platform': 'imdb'},
        {'title': '盛夏未来', 'year': '2021', 'platform': 'douban'},
        {'title': '人之怒', 'year': '2021', 'platform': 'douban'}
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'], platform=m['platform'])
        db.session.add(movie)

    db.session.commit()
    click.echo('初始化成功.')


@app.cli.command()
@click.option('--username', prompt=True, help='请输入用来登入的用户名')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='请输入用来登入的密码')
def admin(username, password):
    """
    设置管理员账号密码: flask admin
    """
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')
