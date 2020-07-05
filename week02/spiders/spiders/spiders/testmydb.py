from mydb import ConnDB

db = ConnDB()
result = db.run(('test movie','http://test','test movie info','喜剧','2020-12-31'))