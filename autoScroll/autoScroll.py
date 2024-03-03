from selenium import webdriver
import time
from pynput import keyboard 

# Initialize the browser
browser = webdriver.Chrome()

# Open the webpage
browser.get("https://www.investopedia.com/what-to-expect-in-the-markets-this-week-8603107")

# Scroll to the bottom of the webpage gradually
scroll_increment = 50  #adjust as needed
scroll_pause_time = 0.5 
scroll_position = 0
is_paused = False

def on_press(key):
    global is_paused
    if key == keyboard.Key.right: #click on right arrow to stop
        is_paused = not is_paused
        if is_paused:
            print("Scrolling paused.")
        else:
            print("Scrolling resumed.")

# Create a listener for keyboard events
listener = keyboard.Listener(on_press=on_press)
listener.start()

try:
    while True:
        if not is_paused:
            # Scroll down 
            browser.execute_script(f"window.scrollBy(0, {scroll_increment});")
            scroll_position += scroll_increment
            
            # Pause for a short while to let the page load and for smoother scrolling
            time.sleep(scroll_pause_time)
            
            # Break the loop if the scroll position exceeds the page height
            if scroll_position >= browser.execute_script("return document.body.scrollHeight"):
                break

except KeyboardInterrupt:
    print("Scrolling stopped manually.")

# Wait before close tab
time.sleep(10)

# Close the browser
browser.quit()
