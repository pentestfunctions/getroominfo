# TryHackMe Room Information Retrieval Tool

This tool allows users to retrieve information about the current TryHackMe rooms they are participating in. It utilizes the TryHackMe API to fetch room details such as Room ID, Title, and Internal IP addresses.

## Installation

Ensure you have Python 3.x installed on your system. Then, follow these steps:

1. Install required Python packages:
    ```bash
    pip install requests selenium
    ```

2. Download the script:
    ```bash
    wget https://raw.githubusercontent.com/pentestfunctions/getroominfo/main/currentroom.py -O ~/.currentroom.py
    ```

3. Create a symbolic link for easy execution:
    ```bash
    sudo echo "/bin/bash ~/.currentroom.py" >> /bin/currentroom
    ```

## Usage

- Simply execute `currentroom` in your terminal. If it's your first run, the tool will prompt you to provide your TryHackMe `connect.sid` cookie. Paste in the cookie value (not the name) when prompted.
- It will then create the `~/.config/tryhackmeconfig` file ready to use, otherwise you can configure it yourself as below. 
- If you haven't created the configuration file `~/.config/tryhackmeconfig` yet, create it manually and put in the cookie value for `connect.sid` (without `connect.sid=` prefix).

### Cookie

To get your cookie, simply navigate tryhackme.com while logged in. Open the devtools (f12) on your browser and go to the network tab. On this page, check for any request you make while on the website and find the cookie value there. 

## Disclaimer

This tool is provided as-is without any warranties. Use it responsibly and respect TryHackMe's terms of service.
