from snownlp import SnowNLP
import pandas as pd
import numpy as np

from mydb import ConnDB

try:
    db = ConnDB()
    comments = db.get_comments()

    for comment in comments:
        scmt = pd.Series(comment)
        if scmt.hasnans:
            scmt = scmt.fillna(value='无')
        cmt = scmt.to_list()
        if cmt[3]:
            sn = SnowNLP(cmt[3])
            sentiments = sn.sentiments
        else:
            cmt[3] = '无'
            sentiments = 0
        cmt.append(sn.sentiments)
        print(cmt)
        db.update_comment(cmt)
except:
    print('clean data error')
