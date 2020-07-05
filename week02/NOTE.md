# 第二周学习笔记

## 异常捕获

##### 美化异常输出 ： `pip install pretty_errors`

##### 异常输出语法：

1. **常规**

```

try:
    pass
except Exception as e:
    print(e)
```

2. **异常链捕获**

```
try:
    pass
except (ZeroDivisionError, Exception) as e:
    print(e)
```

3. **自定义异常**

```
class UserInputError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self, ErrorInfo)
        self.errorinfo = ErrorInfo
        self.errorinf = ErrorInfo
    def __str__(self):
        return self.errorinfo
userinput = input('Please input a number:')
try:
    if (not userinput.isdigit()):
        raise UserInputError('input error')
    else :
        print(f'your input number : {userinput}')
except UserInputError as ue:
    print(ue)
finally:
    del userinput
```

## Python + MySql 

#### MySql 常用操作

- **启动 `mysql`：** 系统偏好设置 -> mysql -> Start Mysql Server

- **查看 `mysql` 进程服务：** `ps -ef|grep mysql`

- **`mysql` 常用命令：**

```
$ /usr/local/mysql/bin/mysql -u root -p
$ root1234

mysql > create database maoyan;
mysql > show databases;
mysql > use maoyan;
mysql > show tables;
mysql > create table movie(
     > id int(4) auto_increment not null primary key, 
     > title char(200) not null, 
     > link char(200) not null, 
     > content char(200), 
     > file_tyle char(200), 
     > time char(200)
     > );
mysql > insert into movie values(null,"test movie","test movie info","http://test","喜剧","2020-12-12");
mysql > select * from moive;
+----+--------------+-------------+-----------------+------------+------------------+
| id | title        | link        | content         | file_tyle  | time             |
+----+--------------+-------------+-----------------+------------+------------------+
|  1 | test11 movie | http://test | test movie info | 喜剧       | 2020-12-12       |
+----+--------------+-------------+-----------------+------------+------------------+
```

#### 数据库插件 pymysql 

```
dbInfo = {
    'host': 'localhost',
    'port' : '1008',
    'user' : 'root',
    'password' : 'rootroot',
    'db' : 'maoyan'
}
...
conn = pymysql.connect(
    host = self.host,
    port = self.port,
    user = self.user,
    password = self.password,
    db = self.db,
    charset = 'utf8mb4'
)

cur = conn.cursor()                             // get current cursor 
count = cur.execute('select * from maoyanDb;')  // get result count
result = cur.fetchnone()                        // fetch one result
result = cur.fetchall()                         // fetch all result

values = [(id, 'testuser' + str(id)) for id in range(4, 21)];
cur.executemany('INSERT INTO ' + table_name + ' values(%s,%s)', values);

cur.close()
conn.commit()
conn.rollback()                                // try -> except

```
