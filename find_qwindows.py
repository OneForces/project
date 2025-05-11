import os

for root, dirs, files in os.walk(os.path.expanduser("~")):
    if "qwindows.dll" in files:
        print("Найден:", os.path.join(root, "qwindows.dll"))
        break
