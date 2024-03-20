import pygetwindow as gw

def print_all_window_titles():
    # Get a list of all open windows
    windows = gw.getAllTitles()

    # Print the titles
    for window_title in windows:
        print(window_title)

# Call the function to print all window titles
print_all_window_titles()