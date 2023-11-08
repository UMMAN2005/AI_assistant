import os
import subprocess
from word2number import w2n
import sys
from random import choice
from time import sleep
import openai
import pyautogui
import pygame.mixer
import speech_recognition as sr
from gtts import gTTS
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
# from webdriver_manager.chrome import ChromeDriverManager

# ANSI colors
RESET = "\033[0m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"

# Initialize pygame mixer
pygame.mixer.init()

# Load the pre-trained model and tokenizer
# model_name = "gpt2"  # You can use other models too
# model = GPT2LMHeadModel.from_pretrained(model_name)
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)


# OpenAI API key
api_key = "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"

# Set OpenAI API key
openai.api_key = api_key

# Initialize a variable to store recognized speech
guy = ""

# Initialize the microphone
microphone = sr.Microphone(device_index=1)

# Dictionary of the applications and their executables
apps_dict = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "code": r"C:\Users\user\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "calc": r"calc.exe",
    "editor": r"notepad.exe",
    "expl": r"explorer.exe",
    "excel": r"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE",
    "word": r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE",
    "point": r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE",
    "access": r"C:\Program Files (x86)\Microsoft Office\root\Office16\MSACCESS.EXE"
}

# Dictionary of the system commands
system_commands_dict = {
    "down": "shutdown /s /t 0",
    "restart": "shutdown /r /t 0",
    "reboot": "shutdown /r /t 0",
    "lock": "rundll32.exe user32.dll,LockWorkStation",
    "sleep": "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
}

# Create colors' list
colors_list = [RED, BLUE, GREEN, YELLOW]


def initialize_driver():
    chrome_driver_path = r"C:\Users\user\AppData\Local\Programs\Google Chrome Drivers\chromedriver.exe"
    chrome_binary_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = chrome_binary_path
    chrome_options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
    # driver_ = webdriver.Chrome(ChromeDriverManager().install())
    driver_ = webdriver.Chrome(options=chrome_options)
    return driver_


def words_to_numbers(word):
    try:
        number = w2n.word_to_num(word)
        return number
    except ValueError:
        return "Invalid input, please enter a valid word representation of a number."


def execute_code_on_browser_close(url_):
    driver = initialize_driver()
    driver.get(url_)

    # Continuously check if the browser is still open
    while True:
        try:
            # noinspection PyStatementEffect
            driver.title  # Access a property of the WebDriver to check if it's still open
            sleep(1)  # Pause for a second before checking again
        except WebDriverException:
            # WebDriverException is raised when the browser is closed
            print("Browser has been closed!")
            break


def play_audio(text):
    print("Playing audio:", text)
    # Generate audio from text using gTTS
    speech = gTTS(text=text, lang="en", slow=False, tld="com.au")

    # Save the audio to a temporary file
    temp_audio_file = "temp_audio.mp3"
    speech.save(temp_audio_file)

    # Create a pygame Sound object from the temporary audio file
    sound = pygame.mixer.Sound(temp_audio_file)

    # Play the audio
    sound.play()

    # Wait for a moment to allow the user to hear the audio
    sleep(2)

    # Clean up: Remove the temporary audio file
    os.remove(temp_audio_file)


# Function to create a note file
def create_note_file(note, file_path):
    print("Creating note:", note)
    with open(file_path, "a") as f:
        f.write(note + "\n")


# Function to add a note to an existing file
def add_note_again(note, file_path):
    print("Adding note again:", note)
    with open(file_path, "a") as f:
        f.write(note + "\n")


# Function to get audio input from the microphone
def get_audio():
    r = sr.Recognizer()
    with microphone as source:
        try:
            print("Listening...")
            audio = r.listen(source, timeout=10)
            print("Recognizing...")
            said = r.recognize_google(audio)
            print("Heard:", said)
            global guy
            guy = said

            if "help" in str(said).casefold():
                subprocess.Popen(['start', help_file_path], shell=True)

            elif "not" in str(said).casefold():
                note = said.casefold().replace("note ", "", 1).replace("note", "", 1)\
                    .replace("not ", "", 1).replace("not", "", 1)
                play_audio("Note saved successfully.")
                file_path = os.path.expanduser(r"C:\Users\user\Desktop\PyCharm\pythonProject8-AI_assistant\AI_files"
                                               r"\AI_notes\notes.txt")
                create_note_file(note, file_path)

                # while True:
                #     time.sleep(1)
                #     play_audio("Would you like to save another note?")
                #     print("Listening...")
                #     another_note_audio = r.listen(source, timeout=10)
                #     response = r.recognize_google(another_note_audio)
                #     if "yes" in str(response).casefold():
                #         play_audio("What would you like to add to the notes?")
                #         print("Listening...")
                #         note_audio = r.listen(source, timeout=10)
                #         note = r.recognize_google(note_audio)
                #         add_note_again(note, file_path)
                #         play_audio("The note was saved again")
                #     elif "no" in str(response).casefold():
                #         play_audio("Okay")
                #         break

            elif "joke" in str(said).casefold():
                with open(r"C:\Users\user\Desktop\PyCharm\pythonProject8-AI_assistant\AI_files\Jokes.txt", "r") as file:
                    jokes_list = file.readlines()
                    joke = choice(jokes_list)
                    play_audio(joke)

            elif "search" in str(said).casefold():
                user_input = said.casefold().replace("search ", "", 1)
                search = user_input.strip().replace(" ", "_")
                url = r"https://wikipedia.org/wiki/" + search
                play_audio("Searching...")
                execute_code_on_browser_close(url)

            elif "repeat" in str(said).casefold():
                user_input = said.casefold().replace("repeat ", "", 1)
                play_audio(user_input)

            elif "sleep" in str(said).casefold():
                user_input = said.casefold().replace("sleep ", "", 1)
                number = words_to_numbers(user_input)
                try:
                    print(f"Sleeping {int(number)} seconds...")
                    play_audio(f"Sleeping {int(number)} seconds")
                    sleep(int(number))
                    play_audio("Waked up")
                except ValueError:
                    print("Invalid input, please enter a valid word representation of a number.")

            elif "open" in str(said).casefold():
                user_input = said.casefold().replace("open ", "", 1)
                if "settings" in user_input:
                    subprocess.Popen(['start', 'ms-settings:'], shell=True)
                elif "shell" in user_input:
                    subprocess.Popen(['powershell.exe'], shell=True)
                    flag_ = False
                    return flag_
                elif "term" in user_input:
                    subprocess.Popen(['cmd.exe'], shell=True)
                    flag_ = False
                    return flag_
                for app, path in apps_dict.items():
                    if app in user_input:
                        play_audio("The application is opening...")
                        subprocess.Popen(path)

            elif "system" in str(said).casefold():
                user_input = said.casefold().replace("system ", "", 1)
                for key, command in system_commands_dict.items():
                    if key in user_input:
                        play_audio("Command will be executed!")
                        sleep(2)
                        subprocess.call(command, shell=True)

            # elif "jarvis" in str(said).casefold():
            #     said = str(said).casefold()
            #     new_string = said.replace("jarvis ", "")
            #     completion = openai.Completion.create(model="gpt-3.5-turbo",
            #                                           messages=[{"role": "user", "content": new_string}])
            #     text = completion.choices[0].message.content
            #     play_audio(text)

            # elif "ask" in str(said).casefold():
            #     said = str(said).casefold()
            #     user_input = said.replace("ask ", "")
            #
            #     # Tokenize and generate a response
            #     input_ids = tokenizer.encode(user_input, return_tensors="pt")
            #     output = model.generate(input_ids, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2)
            #
            #     # Decode and print the response.
            #     response = tokenizer.decode(output[0], skip_special_tokens=True)
            #
            #     # Write to a file
            #     random_color = choice(colors_list)
            #     with open("Responses.txt", "a", encoding="utf-8") as responses_file:
            #         print(random_color, response, "\n\n", RESET, file=responses_file)
            #
            #     # Play answer
            #     play_audio(response)

            elif "screenshot" in str(said).casefold():
                print("Getting the screenshot...")
                screenshot_dir = os.path.expanduser(r"C:\Users\user\Desktop\PyCharm\pythonProject8-AI_assistant"
                                                    r"\AI_files\AI_screenshots")
                file_name = "screenshot"
                extension = ".png"
                file_path = os.path.join(screenshot_dir, file_name + extension)

                if os.path.exists(file_path):
                    counter = 1
                    while os.path.exists(file_path):
                        new_filename = file_name + str(counter) + extension
                        file_path = os.path.join(screenshot_dir, new_filename)
                        counter += 1

                capture_screenshot(file_path)
                print("Screenshot captured and saved")
                play_audio("Screenshot was saved")

        except sr.WaitTimeoutError:
            print("No speech detected within the timeout!")

        except sr.exceptions.UnknownValueError:
            print("No speech detected!")

        except KeyboardInterrupt:
            play_audio("The execution of code has been stopped!")
            sleep(1.5)
            sys.exit(1)
    return True


# Function to capture a screenshot and save it to a file
def capture_screenshot(file_path):
    try:
        # Ensure the directory where the screenshot should be saved exists
        screenshot_dir = os.path.dirname(file_path)
        os.makedirs(screenshot_dir, exist_ok=True)

        # Capture the screenshot and save it to the specified file_path
        pyautogui.screenshot(file_path)
    except Exception as e:
        print("Exception:", str(e))
        play_audio("An error occurred!")


def main(flag__):
    while flag__:
        if "stop" in str(guy).casefold():
            play_audio("See you soon!")
            sleep(1)
            break
        flag__ = get_audio()
        continue


if __name__ == "__main__":
    flag = True
    help_file_path = r"C:\Users\user\Desktop\PyCharm\pythonProject8-AI_assistant\AI_files\AI_HELP.txt"
    print("Say \"help\" for getting help!")
    play_audio("The Execution of code has been started!")
    sleep(1.5)
    try:
        main(flag)
    except KeyboardInterrupt as error:
        play_audio("The execution of code has been stopped!")
        sleep(1.5)
        sys.exit(1)
