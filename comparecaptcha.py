#!/usr/bin/python3

import os
import time
import shutil
import logging
import cv2
from PIL import Image
import numpy as np

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
                logging.info(f"PATH: known_file_path = {known_file_path}")
                # compare images
                if file_compare(image_path, known_file_path):
                    # return folder name
                    return os.path.basename(root)
    return None

# simple binary compare
def binary_file_compare(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()

# compare with opencv
def file_compare(image1_path, image2_path):
    # TODO make it nice
    # unify image
    # to avoid errors with different image types
    try:
        image1_orig = Image.open(image1_path)
        image1_new = image1_orig.resize(image1_orig.size)
        # convert to numpy array and specify data type
        image1_array = np.array(image1_new, dtype=np.uint8)
        image2_orig = Image.open(image2_path)
        image2_new = image2_orig.resize(image2_orig.size)
        # convert to numpy array and specify data type
        image2_array = np.array(image2_new, dtype=np.uint8)

    except Exception as e:
        print(f"Error resizing image: {e}")

    try:
        # load image after np.array and convert RGB to BGR
        image1 = cv2.cvtColor(image1_array, cv2.COLOR_RGB2BGR)
        image2 = cv2.cvtColor(image2_array, cv2.COLOR_RGB2BGR)
    except Exception as e:
        logging.error(f"Error loading images: {e}")
        return False

    # check if images were loaded successfully
    if image1 is None:
        logging.error(f"Error loading image1: {image1_path}")
        return False
    if image2 is None:
        logging.error(f"Error loading image2: {image2_path}")
        return False

    # compute the Mean Squared Error (MSE)
    mse = ((image1 - image2) ** 2).mean()

    # threshold for similarity
    similarity_threshold = 20  # lower value = more equal, higher value = more diff

    # compare the MSE with the threshold
    if mse < similarity_threshold:
        logging.info(f"Images are similar. image1: {image1_path} and image2: {image2_path}")
        return True
    else:
        logging.info(f"Images are not similar. image1: {image1_path} and image2: {image2_path}")
        logging.info(f"MSE: {mse}")
        return False


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

