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

    def run(self, value, sql):
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
            cur.execute(sql, value);
            cur.close()
            conn.commit()
        except:
            print('error')
            conn.rollback()
        conn.close()
    
    def insert_goods(self, value):
        table_name = 'goods'
        sql = 'INSERT INTO ' + table_name + '(title,link,tag) VALUES(%s,%s,%s);';
        self.run(value, sql)

    def insert_comment(self, value):
        table_name = 'comment'
        sql = 'INSERT INTO ' + table_name + '(author,comment_time,content, goods_title, goods_author, created_time) VALUES(%s,%s,%s,%s,%s,%s);';
        self.run(value, sql)

if __name__ == '__main__':
    db = ConnDB()
    result = db.run(('test movie','http://test'))