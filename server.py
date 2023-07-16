import socket
import threading

clients = {}
lock = threading.Lock()

def handle_client(client_socket, client_name):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            # 解析消息格式：目标用户:实际消息
            recipient, message = message.split(':', 1)
            with lock:
                if recipient in clients:
                    recipient_socket = clients[recipient]
                    recipient_socket.sendall(f"{client_name}: {message}".encode('utf-8'))
        except Exception as e:
            print("Error:", e)
            break

    with lock:
        del clients[client_name]
    client_socket.close()

def main():
    server_host = '127.0.0.1'
    server_port = 8888

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print("Server is listening on {}:{}".format(server_host, server_port))

    while True:
        client_socket, addr = server_socket.accept()
        print("Connected to:", addr)

        # 接收客户端传递的用户名
        client_name = client_socket.recv(1024).decode('utf-8')
        with lock:
            clients[client_name] = client_socket

        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_name))
        client_handler.start()

if __name__ == "__main__":
    main()
