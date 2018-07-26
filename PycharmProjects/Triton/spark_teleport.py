import os
import re

if __name__ == "__main__":
    old_folder = "Z:\\Tetervak\\transcripts"
    new_folder = "Z:\\Tetervak\\transcripts_new"
    history_files = [f for f in os.listdir(old_folder) if os.path.isfile(os.path.join(old_folder, f))]
    new_names = []
    for i in range(len(history_files)):
        new_names[i] = history_files[i].replace("fox", "xmpp.triton.e-burg.ru_current.xml")

    for i in range(len(history_files)):
        with open(os.path.join(old_folder, history_files[i]), "rb") as file:
            contents = file.read()
            with open(os.path.join(new_folder, new_names[i]), 'wb') as new_file:
                new_file.write(contents)
                new_file.close()
            file.close()

