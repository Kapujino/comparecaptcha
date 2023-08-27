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

def compare_images(image_path, known_folder):
    # traverse through subdirs
    for root, dirs, files in os.walk(known_folder):
        for file in files:
            #logging.info(f"file = {file}")
            # check if .jpg
            if file.lower().endswith(".jpg"):
                known_file_path = os.path.join(root, file)
                #logging.info(f"known_file_path = {known_file_path}")
                # compare images
                if file_compare(image_path, known_file_path):
                    # return folder name
                    return os.path.basename(root)
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
        match = compare_images(sample_file, known_folder)
        if match:
            logging.info(f"Match found: {match}")
            # remove the initial "sample.jpg" file
            os.remove(sample_file)

            # write the filename without extension to "result.txt"
            with open("result.txt", "w") as result_file:
                result_file.write(match)
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

