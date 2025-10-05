import keyboard
import pyautogui
from PIL import ImageGrab
import pytesseract
import threading
import time
from typing import Union
from llm import llm

pyautogui.FAILSAFE = False

MODES = ["code", "quiz"]


class HurrahTyper:
    def __init__(
            self,
            mode: Union[str, int] = MODES[0],
            remove_auto_brackets: bool = False
    ) -> None:
        self.__modes = MODES
        self.__remove_auto_brackets = remove_auto_brackets

        self.screen_width, self.screen_height = ImageGrab.grab().size

        self.code_bbox = (0, 70, self.screen_width, 1390)
        self.quiz_bbox = (0, 130, self.screen_width, self.screen_height-50)

        self.stop_typing = False
        self.pause_typing = False
        self.typing_thread = None
        self.current_text = ""
        self.current_index = 0
        self.is_running = False
        self.line_index = 0
        self.char_index = 0
        self.set_mode(mode)

    def set_mode(self, mode):
        if mode in self.__modes or type(mode) == int and mode < len(self.__modes):
            if type(mode) == int:
                mode = self.__modes[mode]
            self.__mode = mode
            print("Mode set to:", mode)
        else:
            raise Exception("Invalid mode:", mode)

    def set_remove_auto_brackets(self, remove_auto_brackets):
        self.__remove_auto_brackets = bool(remove_auto_brackets)
        print("Remove auto brackets set to:", bool(remove_auto_brackets))

    def stop(self):
        print("Stopping typing...")
        self.stop_typing = True

    def toggle_pause(self):
        self.pause_typing = not self.pause_typing
        status = "Paused" if self.pause_typing else "Resumed"
        print(f"Typing {status}...")

    def capture_and_process(self):
        if self.typing_thread and self.typing_thread.is_alive():
            print("Processing in progress. Wait until it's done or stop it first.")
            return

        bbox = self.code_bbox if self.__mode == "code" else self.quiz_bbox

        print("Capturing screen...")
        image = ImageGrab.grab(bbox=bbox)
        image.save('test.png')
        print("Extracting text...")
        text = pytesseract.image_to_string(image)
        print("Sending to LLM...")
        print(text)
        self.current_text = llm(text, self.__mode)

        if self.__mode == "code":
            self.current_index = 0
            self.stop_typing = False
            self.pause_typing = False
            print("Typing started...")
            self.typing_thread = threading.Thread(target=self.type_text)
            self.typing_thread.start()
        elif self.__mode == "quiz":
            print("Showing quiz answer popup...")
            self.show_quiz_answer(self.current_text)

    def type_text(self):
        lines = [line.strip() for line in self.current_text.split('\n') if line.strip() != '']

        for i in range(self.line_index, len(lines)):
            line = lines[i]

            start_char = self.char_index if i == self.line_index else 0

            for j in range(start_char, len(line)):
                if self.stop_typing:
                    self.line_index = i
                    self.char_index = j
                    print("Typing stopped.")
                    return

                while self.pause_typing:
                    time.sleep(0.1)

                pyautogui.write(line[j], interval=0.05)

            self.char_index = 0
            if i != len(lines) - 1:
                pyautogui.press('enter')

        self.line_index = 0
        self.char_index = 0
        print("Typing completed.")


    def show_quiz_answer(self, answer):
        if answer == '1':
            pyautogui.moveTo(1216,17)
        elif answer == '2':
            pyautogui.moveTo(1228,425)
        elif answer == '3':
            pyautogui.moveTo(1267,922)
        else:
            pyautogui.moveTo(1411,1337)

    def start(self):
        if self.is_running:
            print("Hurrah Typer is already running.")
            return

        self.is_running = True
        self.stop_typing = False

        keyboard.add_hotkey('alt', self.stop)
        keyboard.add_hotkey('ctrl', self.capture_and_process)
        keyboard.add_hotkey('f8', self.toggle_pause)

        print(f"Hurrah Typer started in {self.__mode} mode.")
        print(f"Press Ctrl to capture and process, F8 to pause/resume, Alt to stop.")

    def stop_listener(self):
        if not self.is_running:
            return

        self.is_running = False
        self.stop_typing = True

        try:
            keyboard.remove_hotkey('alt')
            keyboard.remove_hotkey('ctrl')
            keyboard.remove_hotkey('f8')
        except:
            pass

        print("Hurrah Typer stopped.")

    @property
    def mode(self):
        return self.__mode

    @property
    def modes(self):
        return self.__modes

    @property
    def remove_auto_brackets(self):
        return self.__remove_auto_brackets