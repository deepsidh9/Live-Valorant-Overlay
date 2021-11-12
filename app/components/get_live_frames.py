import os
import time

import cv2
import numpy as np
import socketio
import win32con
import win32gui
import win32ui

from live_details import LiveDetails

live_details_helper = LiveDetails()

# standard Python
socket_io = socketio.Client()
print("client is created")


def after_connect(args):
    print('after connect', args['data'])


def kill_self(args):
    print('kill_self', args['data'])
    os._exit(0)


socket_io.on('after connect', after_connect)
socket_io.on('kill_self', kill_self)


def get_hwnd():
    return win32gui.FindWindow(None, "VALORANT  ")


def convert(o):
    if isinstance(o, np.int64):
        return int(o)
    raise TypeError


def start_frame_grabbing():
    hwnd = get_hwnd()
    all_events = []
    i = 0
    while(True):
        start = time.time()
        w = 1920  # set this
        h = 1200  # set this

        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)
        #if you want to save the image, uncomment the following 2 lines:
        # bmpfilenamename = "out{}.bmp".format(i)
        # dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
        bmpstr = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(bmpstr, dtype='uint8')
        img.shape = (h, w, 4)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        detected_events = live_details_helper.get_live_details(img)
        if detected_events:
            all_events.append(detected_events)
            # response = requests.post('http://localhost:4445/register_events', json={"events":detected_events})
            socket_io.emit('new_event', {'event': detected_events})
        end = time.time()
        # print("Time elapsed for 1 frame event detection:",end-start)
        if end-start < 1:
            time.sleep(1-(end-start))
        i = i+1
        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())


if __name__ == "__main__":
    # start_frame_grabbing()
    socket_io.connect('http://127.0.0.1:4445/')
    task = socket_io.start_background_task(start_frame_grabbing)
    socket_io.wait()
