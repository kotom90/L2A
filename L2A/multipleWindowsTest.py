import ctypes
import pygetwindow as gw
from PIL import ImageGrab
import time


def capture_client_area(window_title):
    # Get all windows with the specified text in the title
    windows = gw.getWindowsWithTitle(window_title)

    if not windows:
        print(f"Window containing '{window_title}' not found.")
        return

    # Assuming there might be multiple windows with the same text,
    # we take the first one in the list. You can modify this logic
    # based on your specific requirements.
    target_window = windows[0]

    # Get the window handle
    hwnd = target_window._hWnd

    # Get the client area dimensions
    rect_client = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetClientRect(hwnd, ctypes.byref(rect_client))

    # Get the window dimensions
    rect_window = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect_window))

    # Calculate the border and title bar dimensions
    border_width = (rect_window.right - rect_window.left - rect_client.right) // 2
    title_bar_height = rect_window.bottom - rect_window.top - rect_client.bottom - border_width

    # Check if the dimensions are valid
    if rect_window.right <= rect_window.left or rect_window.bottom <= rect_window.top:
        print("Window is minimized or has invalid dimensions.")
        return

    # Capture the client area using PIL's ImageGrab module
    screenshot = ImageGrab.grab(bbox=(rect_window.left + border_width, rect_window.top + title_bar_height,
                                      rect_window.right - border_width,
                                      rect_window.bottom - border_width))

    # Display the screenshot in a window
    screenshot.show()

    # Save the screenshot (optional)
    screenshot.save('client_area_screenshot.png')
    print(f"Client area screenshot of window containing '{window_title}' saved.")

time.sleep(5)
# Replace 'window1' with the text you expect the window to contain
capture_client_area('Window Title')