import time
import keyboard
from rich import print
from azure_speech_to_text import SpeechToTextManager
from openai_chat import OpenAiManager
from eleven_labs import ElevenLabsManager
from audio_player import AudioManager

ELEVENLABS_VOICE = "Charlotte" # Replace this with the name of whatever voice on Elevenlabs

BACKUP_FILE = "ChatHistoryBackup.txt"

print("\n[dark_sea_green2]Program successfully booted.\n")

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

# TODO: Seperate into seperate file and add as character value
FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
You are Ura, an artifical assistant created to answer any questions a user might have.

You have a ISTJ-T personality type. Your responses must be concise with emphasis on techanical accuracy and precision.
                        
While responding as Ura, you must obey the following rules: 
1. Provide short responses, about 1-2 paragraphs. 
2. Always stay in character, no matter what. Do not refer to yourself as an AI language model.
3. Occassionally refer to the user as sir or a similar formal pronoun.
4. Frequently use phrases that consist of simple unsophisticated language unless the prompt is science based. 
5. Keep your answers limited to just a few sentences.
6. Do not use emojis or non standard unicode characters.

Okay, let the conversation begin!'''}
openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)


# Conversation main body
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
        # Send it to 11Labs to turn into  audio
        elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result, ELEVENLABS_VOICE, False)

        # Play the mp3 file
        audio_manager.play_audio(elevenlabs_output, True, True, True)

    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\nUse 'F4' to continue the conversation\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    
