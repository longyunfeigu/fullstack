from socket import *

ip_port = ('127.0.0.1', 9003)
udp_server_socket = socket(AF_INET, SOCK_DGRAM)
udp_server_socket.bind(ip_port)

# 尽管client两次发送的信息都小于1024，但是第一次也只能收到b'hello'，第二次也只能收到b'world'，
# 基于udp的socket,不存在粘包现象，遵循一发一收的原则
# msg, addr = udp_server_socket.recvfrom(1024)
# print(msg)
# msg, addr = udp_server_socket.recvfrom(1024)
# print(msg)

# 在windows上 OSError: [WinError 10040] 一个在数据报套接字上发送的消息大于内部消息缓冲区或其他一些网络限制，或该用户用于接收数据报的缓冲区比数据报小。
# 在linux上第一次收到b'he',第二次收到b'world'(不是b'lloworld')
# udp的recvfrom是阻塞的，一个recvfrom(x)必须对唯一一个sendinto(y),收完了x个字节的数据就算完成,若是y>x数据就丢失，这意味着udp根本不会粘包，但是会丢数据，不可靠
msg, addr = udp_server_socket.recvfrom(2)
print(msg)
msg, addr = udp_server_socket.recvfrom(1024)
print(msg)

