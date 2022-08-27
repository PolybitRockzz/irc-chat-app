import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
import json
import os

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

jsondata = json.load(open('settings.json'))
login_info = False

init()

colors = [Fore.BLUE, Fore.CYAN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.WHITE
]

client_color = random.choice(colors)

def print_bar(txt):
    i = 55 - len(txt)
    print(client_color + ("█" * int(i/2) + txt + "█" * int(i/2)) + Fore.RESET)
    print("\n")

title = f"""{client_color}
   _____                              _   _      _   
  / ____| IRC                        | \ | |    | |  
 | |     ___  _ __ ___  _ __ ___  ___|  \| | ___| |_ 
 | |    / _ \| '_ ` _ \| '_ ` _ \/ __| . ` |/ _ \ __|
 | |___| (_) | | | | | | | | | | \__ \ |\  |  __/ |_ 
  \_____\___/|_| |_| |_|_| |_| |_|___/_| \_|\___|\__|                                                                           
{Fore.RESET}"""

print(title)
print_bar(" Homepage ")
name = ""
if jsondata['name'] == "":
    name = input("Enter a nickname: ")
    jsondata['name'] = name
    with open('settings.json', 'w') as f:
        json.dump(jsondata, f)
else:
    name = jsondata['name']

clear()

while True:
    print(title)
    print_bar(" Homepage ")
    if not login_info:
        print(f"{Fore.GREEN}[+] Logged in as {name}{Fore.RESET}\n")
        login_info = True
    print("[1] - Connect to a server ")
    print("[2] - Change nickname ")
    print("[3] - Exit ")
    choice = int(input("> "))

    if choice == 1:
        clear()
        print(title)
        print_bar(" Joining Room... ")
        SERVER_HOST = input("Enter a server IP: ")
        SERVER_PORT = int(input("Enter the server port: "))
        clear()
        print(title)
        print_bar(f" Room: {SERVER_HOST}:{SERVER_PORT} ")

        try:
            s = socket.socket()
            print(f"{Fore.YELLOW}[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...{Fore.RESET}", end="\r")
            s.connect((SERVER_HOST, SERVER_PORT))
            print(f"{Fore.GREEN}[+] Connected to {SERVER_HOST}:{SERVER_PORT} !                                {Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[-] Couldn't connect to server: {type(e).__name__}                              {Fore.RESET}")
            input("")
            continue

        s.send(f"{Fore.GREEN}[+] {client_color}{name}{Fore.GREEN} has entered the chat!{Fore.RESET}".encode())

        def listen_for_messages():
            while True:
                try:
                    msg = s.recv(1024).decode()
                except Exception as e:
                    return
                print(msg)

        t = Thread(target=listen_for_messages)
        t.daemon = True
        t.start()

        while True:
            to_send =  input()
            if to_send.lower() == '-exit':
                exit_text = f"{Fore.RED}[-] {client_color}{name}{Fore.RED} left the chat!{Fore.RESET}"
                s.send(exit_text.encode())
                break
            else:
                date_now = datetime.now().strftime('%H:%M')
                to_send = f"{client_color}<{name}>{Fore.RESET} {to_send} [{date_now}]"
                s.send(to_send.encode())
        try:
            s.close()
            print(f"{Fore.RED}[-] Left the server {SERVER_HOST}:{SERVER_PORT}{Fore.RESET}\n")
            input("Ok > ")
            clear()
        except Exception as e:
            print(f"{Fore.RED}[-] Left the server {SERVER_HOST}:{SERVER_PORT}{Fore.RESET}\n")
            input("Ok > ")
    
    elif choice == 2:
        clear()
        print(title)
        print_bar(" Change Nickname ")
        name = input("Enter a new nickname: ")
        jsondata['name'] = name
        with open('settings.json', 'w') as f:
            json.dump(jsondata, f)
        login_info = False
        clear()

    elif choice == 3:
        clear()
        print(title)
        print_bar(" Exit ")
        break

print(f"{Fore.RED}[-] Logging off...{Fore.RESET}")