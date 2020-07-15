# Pandas 学习笔记

## 1. `sklearn` 实验数据

- 曳尾花数据: 
    ```
    from sklearn import datasets
    iris = datasets.load_iris()
    x, y = iris.data, iris.target
    iris.feature_names
    iris.target_names
    ```

- 数据切割：
    ```
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(x,y, test_size = 0.25)
    ```

- 其他数据：
    ```
    from sklearn import datasets
    boston = datasets.load_boston()
    digits = datasets.load_digits()
    ```

## 2、`Pandas` 深度学习

- 模块引入：
    ```
    import numpy as np
    import pandas as pd
    import matplotlib as plt  # 依赖
    ```
- Series:
    ```
    pd.Series(['abc at amazom.com', 'admin@164.com', 'test@qq.com', 'test@m.at'])
    pd.Series([11,22,33], index=['a','b','c'])
    pd.Series({'a':1, 'b': 2, 'c':3})
    ```

- DataFrame：
    ```
    pd.DataFrame(['a', 'b', 'c', 'd'])
    pd.DataFrame([
        ['a', 'b'],
        ['c', 'd']
    ])

    ```

- 数据导入：
    ```
    pd.read_csv('book_utf8.csv')
    pd.read_excel(r'test.xlsx')
    pd.read_sql(sql, conn)
    ```

- 数据信息：
    ```
    df2.index
    df2.values   # <numpy.ndarray>
    df.shape
    df.info()
    df.describe()
    x.hasnans
    df.isnull().sum()
    df.columns = ['star', 'vote', 'shorts']
    ```

- 数据加工：
    ```
    # 矩阵变换
    df.T
    df.T.T
    df2.stack()
    df2.unstack()
    df2.unstack()

    # 空值处理
    df.ffill()
    df.ffill(axis=1)
    df.fillna('-')
    df.fillna(value= x.mean())
    df.dropna()
    df.drop_duplicates()

    # 数据修改
    df.replace(np.NaN, 0)
    df.replace([4,5,], 1000)
    df.replace({4:400, 5:500})

    # 数据删除
    df.drop(1, axis=0)  # default: axis=0
    df.drop('A', axis=1)

    # 数据切片
    df.head(3)
    df[ ['A', 'B'] ]
    df.iloc[:, [0,3]]
    df.loc[ [0,3] ]
    df.loc[ 0:2 ]
    df['C'].replace(4, 400)
    df['还行']
    df[1:3]
    df.loc[1:3, ['star']]

    # 数学运算
    df['A'] + df['C']
    df['A'] < df['C']
    df.count()
    df.sum()
    df['A'].sum()
    df.mean()
    df.max()
    df.min()
    df.median()
    df.mode()
    df.var()
    df.std()

    # 格式美化：
    df.reset_index()

    # 数据聚合：
    df.sort_values(by=['A', 'C'], ascending=[True, False])
    df.groupby('type').count()
    df.groupby('type').sum()   
    df.groupby('type').aggregate({ 'type': 'count', 'Feb': 'sum' })
    df.groupby('group').mean()
    df.groupby('group').mean().to_dict()
    df.groupby('group').agg('mean')
    df.groupby('group').transform('mean')
    ```

- 数据合并：
    ```
    pd.merge(data1, data2)
    pd.merge(data2, data3, on='group')
    pd.merge(data3, data2)
    pd.merge(data3, data2, left_on='age', right_on='salary')
    pd.merge(data3, data2, on='group', how='inner')
    pd.merge(data3, data2, on='group', how='left')
    pd.merge(data3, data2, on='group', how='right')
    pd.merge(data3, data2, on='group', how='outer')
    pd.concat([ data1, data2 ])
    ```

- 数据导出：
    ```
    df.to_excel( excel_writer=r'file.xlsx' )
    df.to_excel( excel_writer=r'file.xlsx', sheet_name= 'sheet1' )
    df.to_excel( excel_writer=r'file.xlsx', sheet_name= 'sheet1', index= False)
    df.to_excel( excel_writer=r'file.xlsx', sheet_name= 'sheet1', index= False, columns=['col1', 'col2'])
    ```

- 数据图形化： `matplotlib` 和 `seaborn`
    ```
    import pandas as pd
    import numpy as np
    dates = pd.date_range('20200101', periods=12)
    df = pd.DataFrame(np.random.randn(12, 4), index=dates, columns=list('ABCD'))

    import matplotlib.pyplot as plt
    print('image1')
    plt.plot(df.index, df['A'])
    plt.show()
    print('image2')
    plt.plot(df.index, df['A'], color='#FFAA00', linestyle='--', linewidth=3, marker='D')
    plt.show()

    # seaborn 其实是在 matplotlib 的基础上进行了更高级的 API 封装，从而使绘图更容易、更美观
    import seaborn as sns

    print('image3')
    plt.scatter(df.index, df['A'])
    plt.show()

    print('image4')
    sns.set_style('darkgrid')
    plt.scatter(df.index, df['A'])
    plt.show()
    ```

## 3、`jieba` 中文分词

- jieba 分词示例：

    > 新新词类，会默认通过 Viterbi 算法进行识别

    ```
    jieba.cut(string, cut_all=False)  
    jieba.cut(string, cut_all=True)
    jieba.cut(string, HMM=False)
    jieba.cut_for_search(string)
    ```

- 关键词提取
    1. 基于 TF-IDF 算法进行关键词抽取
    ```
    tfidf = jieba.analyse.extract_tags( text, 
                                    topK=5,          # 权重最大的 topK 个关键词
                                    withWeight=True) # 返回每个关键字的权重
    ```
    2. 基于 TextRank 算法进行关键词抽取
    ```
    textrank = jieba.analyse.textrank(text, topK=5, withWeight=False)
    ```

- 添加黑名单
    ```
    stop_words = r'stop_words.txt'  # 一行一个单词
    jieba.analyse.set_stop_words(stop_words)
    textrank = jieba.analyse.textrank(text, topK=5, withWeight=False)
    pprint.pprint(textrank)
    ```

- 自定义词库
    ```
    user_dict = r'user_dict.txt'
    jieba.load_userdict(user_dict)
    result = jieba.cut(string, cut_all=False)
    ```
- 分词和合词
    ```
    jieba.suggest_freq('中出', True)       # 合词
    jieba.suggest_freq(('中','将'), True)  # 分词
    ```

## 4. `snownlp` 情感分析
- 常用操作
    | 代码 | 用处 | 说明 |
    |-|-|-|
    | s = SnowNLP(text) | 文本分析 | |
    | s.words | 中文分词 | |
    | list(s.tags) | 词性标注 | 隐马尔可夫模型 |
    | s.sentiments | 情感分析 | 0 ~ 1，朴素贝叶斯分类器 |
    | s.pinyin | 转拼音 | Trie 叔 |
    | s.han | 繁体简化 |
    | s.keywords(limit=5) | 关键字提取 |
    | s.tf | 词频 |
    | s.idf | 词条信息量 |


- 模型训练：
    ```
    from snownlp import seg
    seg.train('train.txt')
    seg.save('seg.marshal')
    # 修改 snownlp/seg/__init__py 的 data_path 指向新的模型即可
    ```

---

## 学习心得

本周学习内容集中在数据处理这一块，尤其是 Pandas 这个库，有大量的常用方法需要掌握。在处理数据时，有大量跟数据库类似的操作，目前刚接触，用起来不熟练，需要反复 debug。

感觉这周的学习内容很适合上一周第二题作业，对抓取回来的数据进行清洗、展示。接下来要把上周第二题补上，以便练习这周学到的各种方法。