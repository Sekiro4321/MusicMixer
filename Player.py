import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import random

def play_music(folder,mp3_list,index):
    while True:
        song_name = mp3_list[index]
        file_path = os.path.join(folder, song_name)  

        if not os.path.exists(file_path):
            print(f"File not found in {folder} Folder")
            return
        
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play() 

        print(f"Now Playing: {index+1}. {song_name}")
        print(f"Commands: [P]ause ,[R]esume, [S]top, [C #]=Change, [N]ext, [P]revious, [M]=Random play")

        while True:

            comm = input("> ").upper()
            flag = 1
            if comm == "P":
                pygame.mixer.music.pause()
                print(f"Paused {song_name}")

            elif comm == "R":
                pygame.mixer.music.unpause()
                print(f"Resumed {song_name}")

            elif comm == "S":
                pygame.mixer.music.stop()
                print("Stopped")
                return
            
            elif comm == "M":
                if len(mp3_list)<=1:
                    print("One one song available")
                    continue
                else:
                    new_index = index
                    while new_index==index: 
                        new_index = random.randint(0, len(mp3_list) - 1)

                    index = new_index
                pygame.mixer.music.stop()
                break
            
            elif comm.startswith("C "):
                    try:
                        new_index = int(comm.split()[1]) - 1
                        if 0 <= new_index < len(mp3_list):
                            index = new_index
                            pygame.mixer.music.stop()
                            break   
                        else:
                            print("Song number out of range")
                    except:
                        print("Usage: C <song-number>")

            elif comm == "N":
                index = (index + 1) %len(mp3_list)
                pygame.mixer.music.stop()
                break

            elif comm == "B":
                index = (index - 1) %len(mp3_list)
                pygame.mixer.music.stop()
                break

            else:
                print("Invalid Command Bro...")

def main():

    try:
        pygame.mixer.init()
    except pygame.error as e:
        print(f"Audio Initialization Falied: {e}")
        return
    
    CONFIG_FILE = os.path.expanduser("~/.mp3configfile")

    last_folder = ""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            last_folder = f.read().strip()

    print("***** MP3 PLAYER *****")

    if last_folder:
        print(f"Last used folder: {last_folder}")
        folder = input("Enter your music folder path (leave empty to reuse): ").strip()
        if folder == "":
            folder = last_folder
    else:
        folder = input("Enter your music folder path: ").strip()
        
    folder = os.path.expanduser(folder)

    if not os.path.isdir(folder):
        print(f"No folder named '{folder}' exists")
        return
    
    with open(CONFIG_FILE, "w") as f:
        f.write(folder)
    
    mp3_list = [file for file in os.listdir(folder) if file.endswith(".mp3")]

    if not mp3_list:
        print(f"No .mp3 file found in that folder")
        return

    while True:

        choice_input = input("Enter song # to play, [L]ist for listing, [Q]uit to quit: ")

        if choice_input.upper() == "Q":
            print("Bye")
            break

        elif choice_input.upper() == "L":
            print("My song list:")
            for index,song in enumerate(mp3_list, start=1):
                print(f"{index}. {song}")
            continue

        if not choice_input.isdigit():
            print(f"Enter a Valid Number")
            continue

        choice = int(choice_input)-1

        if 0 <= choice <= len(mp3_list):
            play_music(folder,mp3_list,choice)
        else:
            print(f"Invalid")

if __name__ == "__main__":
    main()
