import argparse
from multiprocessing.pool import Pool
import os
import json
import time
from ip import findips
from ip import ping
from ip import tcp

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n",  type=int, help="the process count.")
    parser.add_argument("-f",  required=True, choices=['ping', 'tcp'], help="the port number.")
    parser.add_argument("-ip", required=True, default=".txt", help="the test type.")
    parser.add_argument("-w",  help="the file name.")
    parser.add_argument("-m",  choices=['proc', 'thread'], help="choose process or thread.")
    parser.add_argument("-v",  default=False, action="store_true", help="print time.")
    args = parser.parse_args()
    print('-' * 20)
    print("-n  {0}".format(args.n))
    print("-f  {0}".format(args.f))        
    print("-ip {0}".format(args.ip))       
    print("-w  {0}".format(args.w))    
    print("-m  {0}".format(args.m))
    print("-v  {0}".format(args.v))
    print('-' * 20)
    return args

def main(args): 
    thread_count = args.n or 1
    p = Pool(thread_count)
    start = time.time()

    if args.f == 'ping':
        args_ips = args.ip.split('-')
        if args_ips[1]:
            ips = findips(args_ips[0], args_ips[1])
        else:
            ips = args_ips
        for ip in ips:
            p.apply_async(ping, args=(ip, ))     # 异步进程池

    elif args.f == 'tcp':
        ip = args.ip
        port_dict = {
            'ip': ip,
            'port': {}
        }
        for port in range(1, 10001):
            result = p.apply_async(tcp, args=(ip, port))  # 异步进程池
            presult = result.get()
            if presult:
                port_dict['port'][port] = 'Open'
        print(port_dict)

        json_str = json.dumps(port_dict)
        path = os.path.abspath(os.path.dirname(__file__))
        filename = args.w or f'{path}/result.json'
        with open(filename, 'w') as f:
            f.write(json_str)

    p.close()
    p.join()
    p.terminate()

    end = time.time()
    if args.v:
        print('Time : ', end - start)
 
if __name__ == '__main__':
    main(parseArgs())