import time
import keyboard
import sys
from rich import print
from azure_speech_to_text import SpeechToTextManager
from openai_chat import OpenAiManager
from eleven_labs import ElevenLabsManager
from audio_player import AudioManager
from profiles import Characters 

BACKUP_FILE = "ChatHistoryBackup.txt"

personalities = ["[green]Nickel", "[green]Ura"] 

print("\n[dark_sea_green2]Program successfully booted.\n")

#TODO: Rename variable
print("Avaliable personalities: "+ ", ".join(personalities))
selectedProfile = input("Enter the name of desired profile: ").lower()
[ELEVENLABS_VOICE, FIRST_SYSTEM_MESSAGE] = Characters.profile(selectedProfile)

print("\nWould you like audio output? Please enter 'y' for yes or 'n' for no:")

#TODO: prevent key presses from appearing on the command line
while True:
    if keyboard.is_pressed('y'):
        print("You entered 'yes'.\n")
        voice_generation = True
        break
    elif keyboard.is_pressed('n'):
        print("You entered 'no'.\n")
        voice_generation = False
        break

print("[light_cyan1]connecting to azureTTS...")
speechtotext_manager = SpeechToTextManager()
print("[steel_blue]connected to azureTTS successfully")

print("[light_cyan1]connecting to openAI...")
openai_manager = OpenAiManager()
print("[steel_blue]connected to openAI successfully")

if voice_generation:
    print("[light_cyan1]connecting to elevenlabs...")
    elevenlabs_manager = ElevenLabsManager()
    print("[steel_blue]connected to elevenlabs successfully")
    
    print("[light_cyan1]preparing audio manager...")
    audio_manager = AudioManager()
    print("[steel_blue]audio manager ready")

openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

# Conversation main body
print("\nStarting the loop, press 'F4' for audio input or 'T' for text input:")

while True:    
    if keyboard.is_pressed('f4'):
        print("User pressed 'F4' key! Now listening to your microphone:\n")
        mic_result = speechtotext_manager.speechtotext_from_mic_continuous() # Get question from mic
        if mic_result == '':
            print("[red]Did not receive any input from your microphone!")
            continue

        openai_result = openai_manager.chat_with_history(mic_result)

    elif keyboard.is_pressed('t'):
        print("User pressed 'T' key!")
        text_result = input("Ask {} a question: ".format(selectedProfile))
        
        openai_result = openai_manager.chat_with_history(text_result)

    elif keyboard.is_pressed('esc'):
        print("\n[hot_pink3]Terminating the chat...")
        sys.exit()

    else: # Wait until user presses a key
        time.sleep(0.1)
        continue
    
    # Write the results to txt file as a backup
    with open(BACKUP_FILE, "w") as file:
        file.write(str(openai_manager.chat_history))

    if voice_generation:
        # Send it to 11Labs to turn into  audio
        elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result, ELEVENLABS_VOICE, False)

        # Play the mp3 file
        audio_manager.play_audio(elevenlabs_output, True, True, True)

    print("\n" + "~"*45)
    print("FINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT:\n")
    print("Use 'F4' or 'T' to continue the conversation.\nOr use 'Esc' to terminate the program.")
    print("~"*45)
    
