import socket
def check_ip(host,port,timeout=5):
    try:
        # 创建一个socket对象
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置超时时间
        sock.settimeout(timeout)
        # 尝试连接到服务器
        sock.connect((host, port))
        # 如果连接成功，关闭socket并返回True
        sock.close()
        return True
    except socket.error as e:
        # 如果连接失败，打印异常并返回False
        print(f"连接到 {host}:{port} 失败: {e}")
        return False