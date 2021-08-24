# watchlist


#### 需要设置环境变量
```.env
DATABASE_HOST=<数据库地址>
DATABASE_PORT=3306
DATABASE_DB_NAME=<数据库名称>
DATABASE_USERNAME=<数据库账号>
DATABASE_PASSWORD=<数据库密码>
```

#### flask command 命令
- 初始化数据库表：`flask initdb`
- 删除表后重新创建：`flask initdb --drop`
- 初始化虚拟数据：`flask forge`
- 设置管理员账号密码: `flask admin`

#### 启动程序
```.bash
python manage.py
```


#### Docker运行
```.bash
docker build -t watchlist
docker-compose up -d
```

访问服务：http://127.0.0.1:5000