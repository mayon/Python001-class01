import pymysql

dbInfo = {
    'host': 'localhost',
    'port' : 3306,
    'user' : 'root',
    'password' : 'root1234',
    'db' : 'smzdm'
}

class ConnDB(object):
    def __init__(self):
        super().__init__()
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']

    def run(self, sql, value = None):
        conn = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            db = self.db,
            charset = 'utf8'
        )
        cur = conn.cursor()
        try:
            if value:
                cur.execute(sql, value)
            else:
                cur.execute(sql);
            result = cur.fetchall()
            cur.close()
            conn.commit()
        except:
            print('error')
            result = None
            conn.rollback()
        conn.close()
        return result
    
    def insert_goods(self, value):
        table_name = 'goods'
        sql = 'INSERT INTO ' + table_name + '(title,link,tag) VALUES(%s,%s,%s);';
        self.run(sql, value)

    def insert_comment(self, value):
        table_name = 'comment'
        sql = 'INSERT INTO ' + table_name + '(author, comment_time, content, goods_title, goods_author, created_time, tag) VALUES(%s,%s,%s,%s,%s,%s,%s);';
        self.run(sql, value)

    def get_comments(self):
        table_name = 'comment'
        sql = 'SELECT id,author,comment_time,content, goods_title, goods_author FROM ' + table_name;
        return self.run(sql)

    def update_comment(self, value):
        table_name = 'comment'
        sql = f'UPDATE {table_name} SET author="{value[1]}", comment_time="{value[2]}", content="{value[3]}", goods_title="{value[4]}", goods_author="{value[5]}", sentiment={value[6]} WHERE id={value[0]}'
        print(sql)
        return self.run(sql)

if __name__ == '__main__':
    db = ConnDB()
    result = db.run(('test movie','http://test'))