import os
import datetime
from PIL import Image

preprocessed_list_path = r"C:\Projects\ElbitRuppin\data\visDrone\raw\preprocessed_images.txt"   # List preprocessed images

# Define classes
raw_images_dir = r"C:\Projects\ElbitRuppin\data\visDrone\raw"
output_dir = r"C:\Projects\ElbitRuppin\data\visDrone\preprocessed"
categories = ["horizontal", "diagonal", "vertical"]

#  Init images lists - track what images don't need preprocessing
preprocessed_images = []
new_preprocessed_images = []

# Image size
target_size = (224, 224)

# Get a list of all image files from all subdirectories
def get_all_images(base_dir):
    image_files = []
    # Load preprocessed images, stripping newlines
    if os.path.exists(preprocessed_list_path):
        with open(preprocessed_list_path, "r") as file:
            preprocessed_images = {line.strip() for line in file.readlines()}
    else:
        preprocessed_images = set()

    # Walk through all subdirectories and find new images
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith((".jpg", ".png", ".jpeg")) and os.path.basename(file) not in preprocessed_images:
                image_files.append(os.path.join(root, file))
    return image_files

images = get_all_images(raw_images_dir)
current_index = 0

def tag_image(category):
    global current_index
    img_path = images[current_index]

    dest_path = os.path.join(output_dir, category, os.path.basename(img_path))

    with Image.open(img_path) as img:
        img_resized = img.resize(target_size)
        img_resized.save(dest_path)


    current_index += 1
