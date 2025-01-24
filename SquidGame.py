import time
import random
import json
import socket
import threading
from pathlib import Path
from collections import deque
from colorama import Fore, Style, init
from playsound3 import playsound
import sys

# Initialize colorama
init(autoreset=True)

# Constants
LEADERBOARD_FILE = "leaderboard.json"
SOUND_DIR = "sounds/"
ASCII_ART = {
    'title': f"""{Fore.RED}
    ░██████╗░███████╗██╗░░░██╗██╗██████╗░
    ██╔═══██╗██╔════╝██║░░░██║██║██╔══██╗
    ██║██╗██║█████╗░░╚██╗░██╔╝██║██║░░██║
    ╚██████╔╝██╔══╝░░░╚████╔╝░██║██║░░██║
    ░╚═██╔═╝░███████╗░░╚██╔╝░░██║██████╔╝
    ░░░╚═╝░░░╚══════╝░░░╚═╝░░░╚═╝╚═════╝░
    {Style.RESET_ALL}""",
    
    'doll': f"""
        {Fore.RED}
          /\\_/\\  
         ( o.o ) 
          > ^ <
        {Style.RESET_ALL}""",
    
    'honeycomb': f"""
        {Fore.YELLOW}
          /-\\-/\\-\\
          \\-/\\-/ 
          /-\\-/\\-\\
          \\-/\\-/
        {Style.RESET_ALL}"""
}

# Game State
class GameState:
    def __init__(self):
        self.score = 0
        self.player_name = ""
        self.leaderboard = self.load_leaderboard()
        self.server_ip = "127.0.0.1"
        self.server_port = 5555

    def load_leaderboard(self):
        try:
            return json.loads(Path(LEADERBOARD_FILE).read_text())
        except:
            return []

    def save_leaderboard(self):
        Path(LEADERBOARD_FILE).write_text(json.dumps(self.leaderboard, indent=2))

# Network Manager
class NetworkManager:
    def __init__(self, game_state):
        self.game_state = game_state
        self.server_socket = None
        self.client_socket = None

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.game_state.server_ip, self.game_state.server_port))
        self.server_socket.listen()
        print(f"Server started on {self.game_state.server_ip}:{self.game_state.server_port}")

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.game_state.server_ip, self.game_state.server_port))
        print("Connected to server!")

# Game Modes
def red_light_green_light(game_state):
    # Implementation similar to previous but with added scoring
    pass

def honeycomb_challenge(game_state):
    print(ASCII_ART['honeycomb'])
    print(f"\n{Fore.YELLOW}=== Honeycomb Challenge ===")
    target_shape = random.choice(['circle', 'triangle', 'star', 'umbrella'])
    print(f"Carve out a {target_shape} shape!")
    
    attempts = 3
    while attempts > 0:
        # Simulated shape carving mini-game
        success = random.random() < 0.4  # 40% success chance
        if success:
            game_state.score += 100
            print(f"{Fore.GREEN}Success! {target_shape} extracted!")
            return True
        attempts -= 1
        print(f"{Fore.RED}Shape broken! Attempts left: {attempts}")
    
    print(f"{Fore.RED}Failed to extract shape!")
    return False

def marbles_game(game_state, multiplayer=False):
    print(f"\n{Fore.BLUE}=== Marbles Game ===")
    marbles = 10
    opponent_marbles = 10
    
    while marbles > 0 and opponent_marbles > 0:
        guess = random.randint(1, 5)
        player_guess = input("Guess number (1-5): ")
        
        if not player_guess.isdigit():
            print("Invalid input!")
            continue
            
        if int(player_guess) == guess:
            opponent_marbles -= 1
            print(f"{Fore.GREEN}Correct! Opponent loses a marble")
        else:
            marbles -= 1
            print(f"{Fore.RED}Wrong! You lose a marble")
        
        print(f"Marbles: You {marbles} - Opponent {opponent_marbles}")
    
    if marbles > opponent_marbles:
        game_state.score += 200
        return True
    return False

# Sound System
def play_sound(sound):
    try:
        playsound(SOUND_DIR + sound)
    except:
        print("🔊")  # Fallback sound indicator

# Leaderboard System
def show_leaderboard(game_state):
    print(f"\n{Fore.CYAN}=== LEADERBOARD ===")
    sorted_lb = sorted(game_state.leaderboard, key=lambda x: x['score'], reverse=True)
    for i, entry in enumerate(sorted_lb[:10], 1):
        print(f"{i}. {entry['name']}: {entry['score']}")

# Main Menu
def main_menu(game_state):
    print(ASCII_ART['title'])
    
    while True:
        print(f"\n{Fore.MAGENTA}Main Menu:")
        print("1. Single Player Games")
        print("2. Multiplayer Games")
        print("3. Leaderboard")
        print("4. Exit")
        
        choice = input("Select: ").strip()
        
        if choice == '1':
            single_player_menu(game_state)
        elif choice == '2':
            multiplayer_menu(game_state)
        elif choice == '3':
            show_leaderboard(game_state)
        elif choice == '4':
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid choice!")

def single_player_menu(game_state):
    while True:
        print(f"\n{Fore.YELLOW}Single Player Games:")
        print("1. Red Light, Green Light")
        print("2. Honeycomb Challenge")
        print("3. Marbles (vs AI)")
        print("4. Back")
        
        choice = input("Select: ").strip()
        
        if choice == '1':
            if red_light_green_light(game_state):
                play_sound("success.mp3")
            else:
                play_sound("fail.mp3")
        elif choice == '2':
            if honeycomb_challenge(game_state):
                play_sound("success.mp3")
            else:
                play_sound("fail.mp3")
        elif choice == '3':
            if marbles_game(game_state):
                play_sound("success.mp3")
            else:
                play_sound("fail.mp3")
        elif choice == '4':
            return
        else:
            print("Invalid choice!")

# Networked Multiplayer Implementation
def multiplayer_red_light(client_socket):
    # Implement networked version with synchronized game state
    pass

def multiplayer_menu(game_state):
    nm = NetworkManager(game_state)
    
    print("\n1. Host Game")
    print("2. Join Game")
    print("3. Back")
    
    choice = input("Select: ").strip()
    
    if choice == '1':
        nm.start_server()
        print("Waiting for players...")
        client, addr = nm.server_socket.accept()
        print(f"Player connected from {addr}")
        multiplayer_red_light(client)
    elif choice == '2':
        nm.connect_to_server()
        multiplayer_red_light(nm.client_socket)
    elif choice == '3':
        return
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    game_state = GameState()
    game_state.player_name = input("Enter your name: ").strip()
    main_menu(game_state)