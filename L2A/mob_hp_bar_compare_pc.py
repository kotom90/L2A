import os
import time

#Windows and image stuff
import cv2
import numpy as np
from PIL import Image
import pyautogui
import ctypes
import pygetwindow as gw
from PIL import ImageGrab

#OCR
import matplotlib.pyplot as plt
import pytesseract
import re


pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR_5.3.3\tesseract.exe'


#script directory
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)
dirTargetDropIconImage = 'ItemDropIcon.png'
dirGameScreenShot = 'screenshot.png'
dirHPBarFull = 'hPBarFull_Master.png'
dropIconImagePng = cv2.imread(dirTargetDropIconImage)
grayDropIcon_np = cv2.cvtColor(dropIconImagePng, cv2.COLOR_BGR2GRAY)
gameBarHPFull = cv2.imread(dirHPBarFull)
gameBarHPFullGray = cv2.cvtColor(gameBarHPFull, cv2.COLOR_BGR2GRAY)

targetNameAndMaxHpWidth = 379
targetNameAndMaxHpHeight = 24

dropIconWidth = 15
dropIconHeight = 15
dropIconPngThreshold = 0
dropIconCoordinates = [0,0]
dropIconRegion = (0,0,0,0)


hpBarOffsetX = 19
hpBarOffsetY = -31
hpBarWidth = 385
hpBarHeight = 5
hpBarCoordinates = [0,0]
hpBarRegion = (0,0,0,0)

playerStatsBarOffsetX = 50
playerStatsBarOffsetY = 27
playerStatsBarWidth = 110
playerStatsBarHeight = 38
playerStatsBarCoordinates = [0,0]
playerStatsBarRegion = (0,0,0,0)

#pyautogui.screenshot(dirGameScreenShot)
def findDropIcon():
    global dropIconPngThreshold
    global dropIconCoordinates
    global dropIconRegion
    global hpBarRegion
    global hpBarCoordinates
    global targetNameAndMaxHpWidth
    global targetNameAndMaxHpHeight
    global playerStatsBarCoordinates
    global playerStatsBarRegion
    global playerStatsBarCoordinates
    global playerStatsBarRegion

    dropIconCoordinates = [0,0]
    hpBarCoordinates = [0,0]
    playerStatsBarCoordinates = [0,0]

    dropIconPngThreshold = 0

    #screenshot = pyautogui.screenshot()
    #screenshot_np = np.array(screenshot)

    screenshot, clientXpos, clientYpos = capture_client_area()
    screenshot_np = np.array(screenshot)
    gameShotImage = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)

    """
    playerStatsBarCoordinates[0] = clientXpos + playerStatsBarOffsetX
    playerStatsBarCoordinates[1] = clientYpos + playerStatsBarOffsetY
    playerStatsBarRegion = (playerStatsBarCoordinates[0], playerStatsBarCoordinates[1], playerStatsBarWidth, playerStatsBarHeight)
    HPMPGrayShotNP = takeScreenshotRegionAndGray(playerStatsBarRegion)

    # DO OCR HERE
    #print("tried OCR")

    # Simple binary thresholding
    _, binary_image = cv2.threshold(HPMPGrayShotNP, 145, 255, cv2.THRESH_BINARY_INV)

    # Set pixels to white (255) on the X axis from pixel 46 to 54
    binary_image[:, 49:57] = 255

    # Resize the thresholded image to make the letters appear larger
    scale_factor = 5.0
    resized_image = cv2.resize(binary_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

    cv2.imwrite('output_image.png', resized_image)
    # Perform OCR on the resized image with configuration parameters
    custom_config = r'--psm 6 -l eng'
    corrected_result = pytesseract.image_to_string(Image.fromarray(resized_image), config=custom_config)

    corrected_result = re.sub(r'[\$\[\]]', '5', corrected_result)
    corrected_result = re.sub(r'S', '5', corrected_result)
    corrected_result = re.sub(r'\?', '9', corrected_result)
    corrected_result = re.sub(r'\]', '1', corrected_result)
    corrected_result = re.sub(r'\.', '', corrected_result)
    corrected_result = re.sub(r'\/', '', corrected_result)
    # Print the OCR result in the terminal
    print(f"OCR Result for {corrected_result}")
    """
    #gameShotImagePng = cv2.imread(dirGameScreenShot)

    #convert to gray images
    grayGameShot = cv2.cvtColor(gameShotImage, cv2.COLOR_BGR2GRAY)

    #match hp bar to screenshot
    result= cv2.matchTemplate(grayGameShot, grayDropIcon_np,cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(result)
    dropIconPngThreshold = max_val

    if dropIconPngThreshold < 0.8:
        return False
    dropIconCoordinates = list(max_loc)
    #print("max val :", max_val)
    print("Location of max correlation:", max_loc)
    time.sleep(0.5)
    #top left and bottom right coordinates
    dropIconCoordinates[0] += clientXpos
    dropIconCoordinates[1] += clientYpos
    #take reference from dropiconCoordinates
    hpBarCoordinates = dropIconCoordinates.copy()
    
    hpBarCoordinates[0] += hpBarOffsetX
    hpBarCoordinates[1] += hpBarOffsetY

    print(hpBarCoordinates[0], hpBarCoordinates[1])
    print(dropIconCoordinates[0], dropIconCoordinates[1])

    hpBarRegion = (hpBarCoordinates[0],hpBarCoordinates[1],hpBarWidth,hpBarHeight)
    dropIconRegion = (dropIconCoordinates[0],dropIconCoordinates[1],dropIconWidth,dropIconHeight)

    targetnameRegion = (dropIconCoordinates[0] + 13 ,dropIconCoordinates[1] - 55 ,targetNameAndMaxHpWidth,targetNameAndMaxHpHeight)
    #newShotGray = takeScreenshotRegionAndGray(targetnameRegion, False)

    #preprocess_and_ocr(newShotGray)

    return True
    #print("HP BAR COORDS: ", hpBarRegion)
    #bottom_right= (dropIconCoordinates[0] + hpBarWidth, dropIconCoordinates[1] + hpBarHeight)

def isDropIconVisible():
    global dropIconRegion
    dropIconRegionGray_np = takeScreenshotRegionAndGray(dropIconRegion)
    result= cv2.matchTemplate(dropIconRegionGray_np, grayDropIcon_np,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(result)
    
    if max_val < 0.8:
        return False
    else:
        return True


def takeScreenshotRegionAndGray(region, shouldGray = True):
    screenshotRegion = pyautogui.screenshot(region=region)
    screenshotRegion_np = np.array(screenshotRegion)
    screenshotRegion_np = cv2.cvtColor(screenshotRegion_np, cv2.COLOR_BGR2RGB)
    #time.sleep(1)
    #newShot = cv2.imread(dirGameScreenShot)
    if shouldGray:
        screenshotRegion_np = cv2.cvtColor(screenshotRegion_np, cv2.COLOR_BGR2GRAY)
    return screenshotRegion_np

def getTargetHpPercentage():
    #print("HP BAR COORDS: ", hpBarRegion)
    #start_time = time.time()

    #print("Location of max correlation:", dropIconCoordinates)

    """if max_val < 0.8:
        print("NO TARGET no drop icon")
        return -1"""

    #print(dropIconCoordinates[0], dropIconCoordinates[1])
    #cv2.imshow('l2', image)
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #dimensions of full bar HP
    #fullBarHeight, fullBarWidth = hpBarImage.shape[:2]

    newShotGray = takeScreenshotRegionAndGray(hpBarRegion)
    
    #cv2.imshow('Rainforest', newShotGray)
    #cv2.waitKey(0)

    #croppedHPBarOnlyGray = newShotGray[dropIconCoordinates[1]:dropIconCoordinates[1] + #hpBarHeight, dropIconCoordinates[0]:dropIconCoordinates[0] + hpBarWidth]
    #cv2.imwrite('grayshotfull.png',croppedHPBarOnlyGray)

    try:
        difference = cv2.absdiff(newShotGray, gameBarHPFullGray)
        percentage_diff = (np.sum(difference) / difference.size) * 100
        #print(percentage_diff)
        #print(difference)
        #print(difference.size)
        #print(np.sum(difference))
        #print(difference[0])

        difPos = hpBarWidth
        for index, i in enumerate(difference[0]):
            if i != 0:
                #print("FOUND NON ZERO!")
                difPos = index
                break

        #print('difpos is ', difPos)
        print('Pixel difference percentage:', difPos/hpBarWidth * 100)

        #cv2.rectangle(gameShotImage, dropIconCoordinates, bottom_right, (0,255,0),1)

        #cv2.imshow('Rainforest', croppedHPBarOnlyGray)
        #cv2.waitKey(0)

        #cv2.imshow('l2', result)
        #cv2.waitKey(0)
        #end_time = time.time()
        # Calculate the elapsed time
        #elapsed_time = end_time - start_time
        #print(f"Elapsed time: {elapsed_time} seconds")
        #template= cv2.imread('Yellowing-leaf.png',0)
        return difPos/hpBarWidth * 100
    except cv2.error as e:
        print("NO TARGET")
        return -1
    
def capture_client_area():
    window_title = "ClientWindow"
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
    
    return screenshot, rect_window.left + border_width, rect_window.top + title_bar_height