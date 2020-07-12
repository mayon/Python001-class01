# Scrapy 深度学习

##1、Scrapy 性能调优

- **setting 优化：** requests 是同步任务，scrapy 是异步任务，下面是相关的参数配置。

```
# setting.py 

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests     for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16
```

- Twisted 异步 IO 框架：多任务模型分文同步模型和异步模型，Scrapy 使用的是 Twisted 模型。该框架，任务之间相互独立，用于大量 I/O 密集操作。

## 2、创建多进程

**创建的子进程个数一般等于系统 CPU 核数 `multiprocessing.cpu_count()`。**

- `os.fork()：` 通常用于研究进程底层原理

```
import os
import time
# 用于研究底层原理
res = os.fork()    
# 开辟子进程后，以下内容会执行两遍
print(f'res == {res}')
if res == 0:
    print(f'我是子进程，pid: {os.getpid()}, 我的父进程是: {os.getppid()}')
else:
    print(f'我是父进程, pid: {os.getpid()}')
```

- `multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={})`: 高度封装
    - group: 分组，实际上很少使用
    - target: 调用对象，传入方法名，`不指定 target 时，默认调用 Process 类里的 run() 方法`
    - name: 进程别名
    - args: 被调用对象 target 的参数元祖
    - kwargs: 调用对象的字典

```
from multiprocessing import Process
def f(*args):
    print(f'hello {args}')
if __name__ == '__main__':
    p = Process(target=f, args=('join', 'sherlock'))
    p.start()
    p.join()     # 默认 join 到当前进程

# join([timeout = None])
# 如果 timeout == None，则该方法将阻塞，直到调用该方法的进程终止。
# 如果 timeout > 0, 则它最多会阻塞 timeout second。
# 如果进程终止或方法超时，该方法返回 None。
# 通过检查进程的 exitcode ，用以确定进程是否终止。
# 一个进程可以 join 多次，但进程不可以 join self，否则会造成死锁。
# 若尝试在 start 进程之前 join，会引发错误。
```

- 自定义 Process Class

```
import os
import time
from multiprocessing import Process

class MyProcess(Process):
    def __init__(self, num):
        self.num = num
        super().__init__()
    def run(self):    # 重写 Process 中 run
        while True:
            print(f"This's process {self.num}, Pid is {os.getpid()}")
            time.sleep(2)
    
for i in range(2):
    p = MyProcess(i)
    p.start()
```

## 3. 多进程通信

- **资源抢占问题：** 多进程同时运行时可能会引发资源抢占的问题，可以通过 `锁机制` 进行解决。
- **全局变量问题：**
    - 进程之间无法直接通过 `全局变量` 进行通信。
    - 父进程创建子进程时会对全局变量进行备份，子进程中修改全局变量对父进程没有任何影响。
- **进程通信方式：**
    1. **队列(Queue)**
        - `get(blocked=False, timeout=None)` 
            - blocked 为 True，获取值时若没有值，则等待 timeout 后再次获取，此时如有值则取出，若没有则抛出 Queue.empty 异常。
            - blocked 为 False，立刻获取值，如果没有值，直接抛出异常。
        - `put(blocked=False, timeout=None)`: 设置 Queue 最大存储值时会对 put 操作产生影响。
            - blocked 为 True，若队列未满直接 put，若队列已满，则等待 timeout 后再次 check 队列，此时若未满则 put，若已满则抛出 Queue.full 异常，
            - blocked 为 False，立刻 put，如果队列已满，直接抛出异常。
        ```
        from multiprocessing import Process, Queue
        def f(q):
            print('queque put')
            q.put([42, None, 'hello'])
        if __name__ == '__main__':
            q = Queue()
            p = Process(target=f, args=(q,))
            p.start()
            print(q.get())
            p.join()
        ```
    2. **管道(Pipe)**: Queue 的底层实现，默认为双工管道
        - 两个链接对象都有 send() 和 recv() 方法。
        - 如果两个进程同事尝试读取和写入管道的同一端，则管道中的数据可能损坏。
        - 同时使用管道不同段的进程不存在损坏的风险。
        ```
        from multiprocessing import Process, Pipe
        def f(conn):
            conn.send([42, None, 'hello'])
            conn.close()
        if __name__ == '__main__':
            parent_conn, child_conn = Pipe()
            p = Process(target=f, args=(child_conn,))
            p.start()
            print(parent_conn.recv())
            p.join()
        ```
    3. **共享内存（shared memory）**： 不同进程共享一块内存
        - 并发编程时，尽量避免使用共享状态，使用多个进程时尤其如此；
        - 如果真的需要使用共享数据，可使用 multiprocessing 中的方法
            - 使用 Value（一维） 或 Array 将数据存储在共享内存映射中
            - 因为无法主动申请或者释放内存，此处需要单独定义数据类型
        ```
        from multiprocessing import Process, Value, Array
        def f(n, a):
            n.value = 3.1415927
            for i in a:
                a[i] = -a[i]
        if __name__ == '__main__':
            num = Value('d', 0.0)        # 定义数据类型
            arr = Array('i', range(10))  # 定义数据类型
            p = Process(target=f, args=(num, arr))
            p.start()
            p.join()
            print(num)
            print(arr[:])
        ```
## 4、多进程锁机制

解决线程之间争抢资源的问题，但是不能指定线程运行顺序。

- `l = mp.Lock()`
    - `l.acquire()`: 线程内锁定
    - `l.release()`: 线程内解锁

## 5、进程池

```
from multiprocessing.pool import Pool
from time import sleep, time
import random
import os

def run(name):
    print('%s sub progress start, PID: %d' % (name, os.getpid()))
    start = time()
    sleep(random.choice([1, 2, 3, 4]))
    end = time()
    print('%s sub progress end, PID: %d, Time: %f' % (name, os.getpid(), end - start))

if __name__ == '__main__':
    print('Parent progress start')
    p = Pool(4)
    for i in range(10):
        p.apply_async(run, args=(i, ))  # 异步进程池
    p.close()    # 使用进程池，必须在 join() 之前调用 close()， 
                 # 并且在 close() 之后不能再继续往进程池添加新的进程
    p.join()     # 会等待进程池中全部进程结束
    print('Parent progress end')
    p.terminate() # 不管进程中是否还有任务，强制结束进程
```

## 6、多线程模型

    - 线程和进程的区别：
        - 多线程运行在一个进程中，即运行在一个 CPU 核心上
        - 多进程容易造成资源大量开销
    - 阻塞和非阻塞：描述发起端的行为
        - 阻塞：得到调用结果之前，线程会被挂起
        - 非阻塞：不能理解得到结果，不会阻塞现成
    - 同步和异步：描述接收端的行为
        - 同步：得到结果之前，调用不会返回
        - 异步：请求发出后，调用立刻返回，没有返回结果，通过回调得到返回结果
    - 协程：调度进程和线程，类似于系统的调度行为，但可以由用户控制

## 7、创建多线程

函数式
```
import threading
def run(n):
    print('current task:', n)
if __name__ == '__main__':
    t1 = threading.Thread(target=run, args=('thread 1', ))
    t2 = threading.Thread(target=run, args=('thread 2', ))
    t1.start()
    t2.start()
```

自定义类
```
import threading
class MyThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def run(self):
        print('current task : %s' % self.name)
if __name__ == '__main__':
    t1 = MyThread('my thread 1')
    t2 = MyThread('my thread 2')
    t1.start()
    t2.start()
```

## 8、多线程锁机制
- 普通锁：`threading.Lock() `
- 嵌套锁：`threading.RLock()`
- 高级锁：
    - Timer: 定时器, Timer(1, funcName)
    - Event: 事件，定义一个 flag，e.set() -> flag=True 、e.clear() -> flag = False
    - 信号量：内部实现一个计数器，占用信号量的线程数超过指定值时阻塞
    - 条件锁：该机制会使线程等待，只有满足某条件时，才释放 n 个线程, 类似生产者/消费者模式

## 9、线程池

- 一般线程池: `from multiprocessing.dummy import Pool as ThreadPool`

- 并行任务的高级封装（python 3.2 +）:`from concurrent.futures import ThreadPoolExecutor`

## 10、多线程和 GL

进程与线程性能对比
GIL 全局解释锁（Global Interpreter Lock）
- 每个进程只有一个 GIL 锁
- 拿到 GIL 锁可以使用 CPU
- CPython 解释器不是真正意义的多线程，属于伪并发

## 11、常见队列操作
普通队列
```
import queue
q = queue.Queue()
q.put(1111)
q.put(2222)
print(q.get())
print(q.get())
q.task_done()
print(q.qsize())
print(q.empty())
print(q.full())
```
优先级队列
- 每个元素都是元祖，数字越小优先级越高，同优先级，先进先出
```
import queue
q = queue.PriorityQueue()
q.put((1, 'work'))              
q.put((-1, 'life'))
print(q.get())
print(q.get())
```

---

## 学习体会

通过这周学习之后，对进程和线程有了非常清晰的认识，以前做前端开发的时候，没有跟进程打过交道，至于多线程之间的交互，都由浏览器解决了，自己也没有详细了解过。

这周接触到线程和进程底层原理，不过还属于初步涉猎，希望通过后期的学习可以进一步加强对线程和进程的了解和认识。

