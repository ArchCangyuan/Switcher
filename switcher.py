import win32gui
import win32con
import win32process
import win32api
PROCESS_ALL_ACCESS = 2097151
import hid
import time
#Get the list of all devices matching this vendor_id/product_id
import socket
# HOST = '192.168.123.26'        # 连接本地服务器
# host = socket.gethostbyname("raspberrypi")
# print(host == HOST)
PORT = 80               # 设置端口号
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # 选择IPv4地址以及TCP协议
sock.bind(("192.168.2.135", PORT))          # 绑定端口
sock.listen()
pos = dict()
def switch_to(hwnd, extra):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    print("Window %s:" % win32gui.GetWindowText(hwnd))
    print("\tLocation: (%d, %d)" % (x, y))
    print("\t    Size: (%d, %d)" % (w, h))
    thread,process = win32process.GetWindowThreadProcessId(hwnd)
    # phndl = win32api.OpenProcess(PROCESS_ALL_ACCESS,0,process)
    # print("Process %d:" % process)
    blacklist = {"NvContainer", "NvSvc", "RxDiag","UxdService", "Default IME"}
    name = win32gui.GetWindowText(hwnd)
    filtered = True
    for i in blacklist:
        if i in name:
            filtered = False
    if x >= 2553 and len(name) > 0 and filtered:
        # str = win32api.GetModuleFileName(phndl)
        # print("Process %s:" % str)
        # if "头号" in win32gui.GetWindowText(hwnd):
        win32gui.MoveWindow(hwnd, x - 2553,y,w,h, False)
        pos[hwnd] = (x,y,w,h)
def switch_from(hwnd, extra):
    for hwnd in pos.keys():
        x,y,w,h = pos[hwnd]
        win32gui.MoveWindow(hwnd, x,y,w,h, False)
prev = "Online"
# connection, address = sock.accept()              # 接受客户端的连接请求
while True:  
    try:
        connection, address = sock.accept()              # 接受客户端的连接请求
        online = len(hid.enumerate(1133)) != 0
        if not online:
            connection.send(b'Offline')       #服务器已经连接
            if prev == "Online":
                win32gui.EnumWindows(switch_to, None)
            prev = 'Offline'
        else:
            connection.send(b'Online')
            if prev == "Offline":
                win32gui.EnumWindows(switch_from, None)
                pos.clear()
            prev = 'Online'
        connection.close()
        time.sleep(0.03)
    except KeyboardInterrupt: # When ‘Ctrl+C’ is pressed, the child program destroy() will be executed.
        connection.close() 
        sock.close()