import pymysql

dbInfo = {
    'host': 'localhost',
    'port' : 3306,
    'user' : 'root',
    'password' : 'root1234',
    'db' : 'maoyan'
}

class ConnDB(object):
    def __init__(self):
        super().__init__()
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']

    def run(self, value):
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
            table_name = 'movie'
            sql = 'INSERT INTO ' + table_name + '(title,link,content,file_tyle,time) VALUES(%s,%s,%s,%s,%s);';
            cur.execute(sql, value);
            cur.close()
            conn.commit()
        except:
            print('error')
            conn.rollback()
        conn.close()

if __name__ == '__main__':
    db = ConnDB()
    result = db.run(('test movie','http://test','test movie info','喜剧','2020-12-30'))