from pynput import keyboard
import json
import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument(
    "-r", "--reset", help="reset log counter to given value for all keys"
)

args = argParser.parse_args()

KEYS = "1234567890abcdefghijklmnopqrstuvwxyz"

if args.reset:
    print("RESET")
    reset_value = int(args.reset)
    keyCount = {key: reset_value for key in KEYS}
else:
    keyCount = {key: 0 for key in KEYS}
    try:
        with open("./log.json", "r") as f:
            try:
                keyCount = json.load(f)
            except ValueError:
                print("existing log could not be parsed as json")
    except FileNotFoundError:
        print("log file could not be found in current working directory")


def printLog(keyCount):
    for key, value in keyCount.items():
        print(f"{key}: {value}")

    for _ in keyCount:
        print("\033[1A", end="\x1b[2K")


def on_press(key):
    try:
        if keyCount[key.char]:
            keyCount[key.char] += 1
        else:
            keyCount[key.char] = 1
    except (AttributeError, KeyError):
        print("non-alpha key pressed")
    printLog(keyCount)


def on_release(key):
    if key == keyboard.Key.esc:
        with open("./log.json", "w") as f:
            json.dump(keyCount, f)
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    printLog(keyCount)
    listener.join()
