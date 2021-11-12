import datetime  # datetime

import win32api  # screenshot
import win32con  # screenshot
import win32gui  # screenshot
import win32ui  # screenshot


def screenshot():

    # Identifying the main desktop window
    hdesktop = win32gui.GetDesktopWindow()

    # determines the size of the monitors in pixels
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    # DesktopContext
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)

    # Buffer of context
    mem_dc = img_dc.CreateCompatibleDC()

    # Create a image object
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)

    # copy the context of window
    mem_dc.BitBlt((0, 0), (width, height), img_dc,
                  (left, top), win32con.SRCCOPY)

    # Save
    data_hoje = datetime.now().strftime('%Y-%b-%d')
    relog = datetime.now().strftime('%Hh%Mm%Ss')
    screenshot.SaveBitmapFile(
        mem_dc, f".\\{data_hoje}\\{data_hoje}_{relog}.bmp")

    # releasing the processes
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())
