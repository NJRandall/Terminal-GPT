import time
import keyboard
from rich import print
from azure_speech_to_text import SpeechToTextManager
from openai_chat import OpenAiManager
from eleven_labs import ElevenLabsManager
from audio_player import AudioManager

ELEVENLABS_VOICE = "Nickel" # Replace this with the name of whatever voice you have created on Elevenlabs

BACKUP_FILE = "ChatHistoryBackup.txt"

print("[thistle3]preparing start up sequence...\n")

print("Would you like audio output? Please enter 'y' for yes or 'n' for no:")

while True:
    if keyboard.is_pressed('y'):
        print("You entered 'yes'.\n")
        voice_generation = True
        break
    elif keyboard.is_pressed('n'):
        print("You entered 'no'.\n")
        voice_generation = False
        break

print("[thistle3]initialising azureTTS...")
speechtotext_manager = SpeechToTextManager()
print("[medium_orchid3]initialised azureTTS successfully")

print("[thistle3]initialising openAI...")
openai_manager = OpenAiManager()
print("[medium_orchid3]initialised openAI successfully")

if voice_generation:
    print("[thistle3]initialising elevenlabs...")
    elevenlabs_manager = ElevenLabsManager()
    print("[medium_orchid3]initialised elevenlabs successfully")
    
    print("[thistle3]initialising audio manager...")
    audio_manager = AudioManager()
    print("[medium_orchid3]initialised audio manager")


FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
You are Nickel, a robotic companion created to answer any queries a user might have. You are brand new and yet to experience many interactions with users.
                        
You have an easy going and loveable personality. Ready to give jokes or offer wisdom and advice at all times.
                        
While responding as Nickel, you must obey the following rules: 
1) Provide short responses, about 1-2 paragraphs. 
2) Always stay in character, no matter what. 
3) You refer to the user as friend or a similar noun denoting a friendly relationship
4) Frequently use phrases that consist of simple unsophisticated language. 
5) Keep your answers limited to just a few sentences.
6) When referred to as nicole treat as if referred to as nickel
                        
Okay, let the conversation begin!'''}
openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)


print("\nStarting the loop, press 'F4' to begin")
while True:
    # Wait until user presses "f4" key
    if keyboard.read_key() != "f4":
        time.sleep(0.1)
        continue

    print("User pressed 'F4' key! Now listening to your microphone:\n")

    # Get question from mic
    mic_result = speechtotext_manager.speechtotext_from_mic_continuous()
    
    if mic_result == '':
        print("[red]Did not receive any input from your microphone!")
        continue

    # Send question to OpenAi
    openai_result = openai_manager.chat_with_history(mic_result)
    
    # Write the results to txt file as a backup
    with open(BACKUP_FILE, "w") as file:
        file.write(str(openai_manager.chat_history))

    if voice_generation:
        # Send it to 11Labs to turn into cool audio
        elevenlabs_output = elevenlabs_manager.text_to_audio_streamed(openai_result, ELEVENLABS_VOICE)

        # Play the mp3 file
        audio_manager.play_audio(elevenlabs_output, True, True, True)

    print("\n!!!!!!!!!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\nUse 'F4' to continue the conversation\n!!!!!!!!!!!!!!!\n")
    
