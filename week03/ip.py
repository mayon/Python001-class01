import struct
import socket
import os

def findips(start, end):
    ipstruct = struct.Struct('>I')
    start, = ipstruct.unpack(socket.inet_aton(start))
    end, = ipstruct.unpack(socket.inet_aton(end))
    return [socket.inet_ntoa(ipstruct.pack(i)) for i in range(start, end+1)]

def ping(ip):
    cmd_str = 'ping -c1 ' + ip
    res = os.system(cmd_str)
    if res < 1:
        print('-' * 25 + f' Ping Success  {ip} ' + '-' * 25)
        return ip
    else:
        return None

def tcp(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((ip, port))
        print(f'{ip} port {port} is open')
        return port
    except Exception as err:
        # print(f'{ip} port {port} is not open')
        return None
    finally:
        server.close()