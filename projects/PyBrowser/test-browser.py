from selenium import webdriver
from os import system as cmd
from time import sleep
import keyboard
import sys
import threading

show = False
url = "https://www.google.com"

def main():
    pass

def new_url(*args):
    global url
    global show
    tmp = show
    show = False
    sleep(0.01)
    new = input("New url: ")
    if new:
        url = new
    show = tmp
    cmd("cls")
    sleep(0.1)
    return True


def stop(*args):
    sys.exit(0)
    return False

# Créer une instance du navigateur [Firefox](https://www.google.com/search?q=Firefox)
driver = webdriver.Firefox()
# list_windows = driver.window_handles
# # driver.switch_to_window(list_windows[-1])
# driver.switch_to.window(list_windows[-1])

# Ouvrir une page dans le navigateur
driver.get(url)

page_url = url

keyboard.hook_key("n", new_url)
keyboard.hook_key("q", stop)


while True:

    if show:
        cmd("cls")
        print(driver.switch_to.active_element.text)
        print()
        # try:
        #     logs = driver.get_log("client")
        #
        #     # Parcourir les messages de log
        #     print(enumerate(logs))
        # except:
        #     print("-- No logs --")
        # print(driver.page_source)
        sleep(1)

    script = """
return document.addEventListener('mousemove', function(event) {
    var x = event.clientX;
    var y = event.clientY;
    console.log("Position de la souris - X: " + x + ", Y: " + y);
    return "Position de la souris - X: " + x + ", Y: " + y;
    
});
    """
    result = driver.execute_script(script)
    print(result)
    if page_url != url:
        page_url = url
        driver.get(url)
