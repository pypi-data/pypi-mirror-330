# 这是一个tcp客户端解决方案，里面包含文字传输，音视频传输基本方法，能基于此快速搭建一个TCP客户端
import socket
import time
import struct

def init_tcp_client(ip, port):  # 服务器端口
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_address = (ip, port)
    try:
        tcp_client.connect(tcp_server_address)
        return tcp_client
    except:
        print("连接失败，可能是服务器未开启。")


def send_characters_message_client(tcp_client, data):  # 客户端发送文字信息,一次通信
    try:
        tcp_client.send(data.encode())
        response = tcp_client.recv(4096).decode()
        return response
    except:
        print("服务器异常")
        return False


def send_audio_message_client(tcp_client, data, data_length):
    while True:
        try:
            # 发送数据长度（4字节，大端序）
            data_len = len(data)
            tcp_client.send(struct.pack("!I", data_len))

            # 分批发送音频数据
            counts = (data_len + data_length - 1) // data_length  # 向上取整
            for i in range(counts):
                start = i * data_length
                end = min(start + data_length, data_len)
                tcp_client.send(data[start:end])

            # 等待服务器响应
            response = tcp_client.recv(4096).decode()
            if response == "音频数据传输有误":
                print("音频传输失败！启动重传机制")
                time.sleep(10)
            else:
                return response  # 音频传输无误，结束这段音频传输
        except Exception as e:
            print(f"服务器异常：{e}")
            tcp_client.close()
            return False