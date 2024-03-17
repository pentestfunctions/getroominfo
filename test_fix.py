from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # Import By
import time
import os
import requests
import json
import subprocess
import shutil

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

options = Options()
options.add_argument('--headless')

# Cookie Handling
config_file = os.path.expanduser("~/.config/tryhackmeconfig")
try:
    with open(config_file, 'r') as file:
        session_id = file.read().strip()
except FileNotFoundError:
    print(f"Configuration file not found at {config_file}. Please make sure the file exists.")
    exit(1)
except Exception as e:
    print(f"Error reading session ID from configuration file: {e}")
    exit(1)

# WebDriver Initialization
try:
    driver = webdriver.Chrome(options=options)
except Exception as e:
    print(f"Error initializing WebDriver: {e}")
    exit(1)

# Set the cookie
cookie = {'name': 'connect.sid', 'value': session_id}
cookie_str = f"{cookie['name']}={cookie['value']}"

def make_request(cookie_str):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.6',
        'cookie': cookie_str
    }
    print("Retrieving current room details.... Please be patient")
    try:
        response = requests.get('https://tryhackme.com/api/vm/running', headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        exit(1)

    if not data:
        print("User doesn't appear to be in any live rooms currently")
        return None

    clear_screen()
    print("Room Details:")
    print("-------------")

    output = ""
    for item in data:
        output += f"Room ID: {item['roomId']}\n"
        output += f"Title: {item['title']}\n"
        if item['internalIP'] is None:
            output += "Internal IP: Machine might still be booting up\n\n"
        else:
            output += f"Internal IP: {item['internalIP']}\n\n"

    if shutil.which('lolcat'):
        try:
            process = subprocess.Popen(['lolcat'], stdin=subprocess.PIPE)
            process.communicate(input=output.encode())
        except Exception as e:
            print(f"Error executing lolcat: {e}")
    else:
        print(output)

    return data

data = make_request(cookie_str)

if data:
    for item in data:
        url = f"https://tryhackme.com/room/{item['roomId']}"
        
        driver.get('https://tryhackme.com')
        driver.add_cookie(cookie)
        driver.get(url)

        time.sleep(4)

        # Use find_elements method with By.CSS_SELECTOR
        questions = driver.find_elements(By.CSS_SELECTOR, '.room-task-question-details')
        answer_inputs = driver.find_elements(By.CSS_SELECTOR, '.room-task-input-questions .form-control.room-answer-field')
    
        print("Remaining questions:")
        for question, answer_input in zip(questions, answer_inputs):
            question_text = question.text.strip()
            if question_text:
                answer_format = answer_input.get_attribute('placeholder').strip() if answer_input else 'No format found'
                if answer_format.lower() != 'no answer needed':
                    print(f"\033[92mQuestion: {question_text}\033[0m | \033[91mAnswer format: {answer_format}\033[0m")
                else:
                    pass

driver.quit()
