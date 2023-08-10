#!/usr/bin/python3

import os
import time
import shutil
import logging

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        filename="comparecaptcha.log",
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def compare_images(image_path, known_folder, unknown_folder):
    # get list of ".jpg" files in the "known" folder
    known_files = [file for file in os.listdir(known_folder) if file.endswith(".jpg")]

    for known_file in known_files:
        known_file_path = os.path.join(known_folder, known_file)
        # compare "sample.jpg" with each ".jpg" file in the "known" folder
        if file_compare(image_path, known_file_path):
            return known_file

    return None

def file_compare(file1, file2):
    # TODO maybe chose another method e.g. opencv
    # binary comparison
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()

if __name__ == "__main__":
    configure_logging()

    sample_file = "sample.jpg"
    known_folder = "known"
    unknown_folder = "unknown"

    if os.path.exists(sample_file):
        match = compare_images(sample_file, known_folder, unknown_folder)
        if match:
            logging.info(f"Match found: {match}")
            # remove the initial "sample.jpg" file
            os.remove(sample_file)

            # write the filename without extension to "result.txt"
            with open("result.txt", "w") as result_file:
                result_file.write(os.path.splitext(match)[0])
        else:
            timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
            new_unknown_file = f"unknown_{timestamp}.jpg"
            shutil.move(sample_file, os.path.join(unknown_folder, new_unknown_file))
            logging.error(f"No match found. Moved 'sample.jpg' to 'unknown/{new_unknown_file}'")
            # write a space to "result.txt" indicating no match
            with open("result.txt", "w") as result_file:
                result_file.write(" ")
    else:
        logging.error(f"No 'sample.jpg' found.")
    time.sleep(1)  # keep calm

