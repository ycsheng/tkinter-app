import socket
import tkinter as tk
from tkinter import simpledialog, messagebox
import threading

def send_message():
    recipient = recipient_var.get()
    message = message_entry.get()
    if not recipient or not message:
        messagebox.showwarning("错误", "请输入目标用户和消息内容。")
        return

    full_message = f"{recipient}:{message}"
    client_socket.sendall(full_message.encode('utf-8'))

def create_client():
    global client_socket
    global username

    server_host = '127.0.0.1'
    server_port = 8888

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    username = simpledialog.askstring("用户名", "请输入用户名：")
    client_socket.sendall(username.encode('utf-8'))

    root.title(f"聊天窗口 - 用户: {username}")

    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()

def receive_message():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            chat_box.insert(tk.END, message + "\n")
        except Exception as e:
            print("Error:", e)
            break

def on_closing():
    if messagebox.askokcancel("退出", "是否确定要退出聊天窗口？"):
        client_socket.close()
        root.destroy()

root = tk.Tk()
root.title("聊天窗口")

# 创建聊天框
chat_box = tk.Text(root, width=50, height=20)
chat_box.pack(padx=10, pady=10)

# 创建消息输入框
message_entry = tk.Entry(root, width=40)
message_entry.pack(padx=10, pady=5)

# 创建目标用户输入框
recipient_var = tk.StringVar()
recipient_entry = tk.Entry(root, textvariable=recipient_var, width=15)
recipient_entry.pack(padx=10, pady=5)

# 创建发送按钮
send_button = tk.Button(root, text="发送", command=send_message)
send_button.pack(pady=5)

# 创建客户端按钮
create_client_button = tk.Button(root, text="创建客户端", command=create_client)
create_client_button.pack(pady=5)

# 设置窗口关闭时的处理函数
root.protocol("WM_DELETE_WINDOW", on_closing)

# 进入主事件循环
root.mainloop()
