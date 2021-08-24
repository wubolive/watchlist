from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

from application import app, db
from application.models import User, Movie


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        # 获取表单数据
        title = request.form.get('title')
        year = request.form.get('year')
        platform = request.form['platform']
        # 验证表单数据
        if not title or not year or not platform or len(year) != 4 or len(title) > 60 or len(platform) > 10:
            flash('您输入的内容有误')
            return redirect(url_for('index'))
        # 保存表单到数据库
        movie = Movie(title=title, year=year, platform=platform)
        db.session.add(movie)
        db.session.commit()
        flash('数据插入成功')
        return redirect(url_for('index'))

    roles = User.query.first()
    page = request.args.get('page', 1, type=int)    # 从查询字符串获取当前页数
    per_page = request.args.get('per_page', 10, type=int)
    paginate = Movie.query.order_by('id').paginate(page, per_page, error_out=False)
    movies = paginate.items
    return render_template('index.html', roles=roles, paginate=paginate, movies=movies)


# 留言版
@app.route('/movie/guestbook', methods=['GET', 'POST'])
def guestbook():
    return redirect(url_for('guestbook'))


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        platform = request.form['platform']

        if not title or not year or not platform or len(year) != 4 or len(title) > 60 or len(platform) > 10:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        movie.platform = platform  # 更新平台
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


# 登入
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('登入成功！')
            return redirect(url_for('index'))

        flash('账号或密码错误！')
        return redirect(url_for('login'))

    return render_template('login.html')


# 用户注册
@app.route('/regist', methods=['GET', 'POST'])
def regist():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not username or not password or not confirm_password:
            error = '请输入正确的用户信息'
        elif User.query.filter_by(username=username).first():
            error = '该用户已存在!'
        elif password != confirm_password:
            error = '两次密码不一致，请重新输入'
        else:
            user = User(username=username, name=username, role='user')
            user.set_password(password)
            db.session.add(user)

            db.session.commit()
            flash('用户注册成功.')
            return redirect(url_for('login'))

    return render_template('regist.html', error=error)


@app.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页

