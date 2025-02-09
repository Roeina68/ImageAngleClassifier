import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import datetime
import math

# Paths
raw_images_dir = r"C:\Projects\ElbitRuppin\data\visDrone\raw"
output_dir = r"C:\Projects\ElbitRuppin\data\visDrone\preprocessed"
log_file_path = r"C:\Projects\ElbitRuppin\data\tagging_log.txt"
debug_log_file_path = r"C:\Projects\ElbitRuppin\data\debug_log.txt"  # Separate debug log
preprocessed_list_path = r"C:\Projects\ElbitRuppin\data\visDrone\raw\preprocessed_images.txt"   # List preprocessed images

#  Init images lists - track what images don't need preprocessing
preprocessed_images = []
new_preprocessed_images = []

# Image size
target_size = (224, 224)

# Define classes
categories = ["horizontal", "diagonal", "vertical"]

# Create output directories for categories
for category in categories:
    os.makedirs(os.path.join(output_dir, category), exist_ok=True)

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

#  Load image to UI
def load_image():
    global current_index, img_label
    if current_index >= len(images):
        tk.Label(root, text="Tagging Complete!", font=("Helvetica", 16)).pack()
        return
    img_path = images[current_index]
    img = Image.open(img_path).resize((400, 400))  # Resize for display

    # Draw the 3x3 grid overlay
    overlay = img.copy()
    draw = ImageDraw.Draw(overlay)
    width, height = overlay.size
    for i in range(1, 3):  # Add vertical and horizontal lines
        draw.line((i * width // 3, 0, i * width // 3, height), fill="red", width=2)
        draw.line((0, i * height // 3, width, i * height // 3), fill="red", width=2)

    img_tk = ImageTk.PhotoImage(overlay)
    img_label.config(image=img_tk)
    img_label.image = img_tk

#  Tag (and resize )image to its class directory
def tag_image(category):
    global current_index
    img_path = images[current_index]
    log_entry = f"{datetime.datetime.now()}: {labeler_name} tagged {os.path.basename(img_path)} -> {category}\n"

    if debug_mode:
        log_entries.append(log_entry)
        if category == "horizontal":
            taggedNum[0] += 1
        elif category == "diagonal":
            taggedNum[1] += 1
        else:
            taggedNum[2] += 1
    else:
        dest_path = os.path.join(output_dir, category, os.path.basename(img_path))

        with Image.open(img_path) as img:
            img_resized = img.resize(target_size)
            img_resized.save(dest_path)

        new_preprocessed_images.append(os.path.basename(img_path) + "\n")
        log_entries.append(log_entry)
        if category == "horizontal":
            taggedNum[0] += 1
        elif category == "diagonal":
            taggedNum[1] += 1
        else:
            taggedNum[2] += 1

    current_index += 1
    load_image()

#  Stop labeling process and close program (writes to log)
def stop_labeling():
    totalLabels = sum(taggedNum)
    log_entries.append(f"{datetime.datetime.now()}: {labeler_name} has stopped labeling session\n")
    log_entries.append(f"Total images labeled: {totalLabels}, Horizontal: {taggedNum[0]}, Diagonal: {taggedNum[1]}, Vertical: {taggedNum[2]}\n")
    if totalLabels > 0:
        log_entries.append(f"Percentages: Horizontal: {taggedNum[0] / totalLabels * 100:.2f}%, "
                           f"Diagonal: {taggedNum[1] / totalLabels * 100:.2f}%, "
                           f"Vertical: {taggedNum[2] / totalLabels * 100:.2f}%\n")
    else:
        log_entries.append("Percentages: No images labeled during this session.\n")
    log_file = debug_log_file_path if debug_mode else log_file_path
    with open(log_file, "a") as f:
        f.writelines(log_entries)
    with open(preprocessed_list_path,"a") as f:
        f.writelines(new_preprocessed_images)
    root.quit()
    exit()

#  Set labeler for logs
def set_labeler(name):
    global labeler_name
    labeler_name = name
    labeler_selection.destroy()  # Close the labeler selection window
    root.deiconify()  # Show the main window after selecting labeler
    log_entries.append(f"{datetime.datetime.now()}: {labeler_name} has started labeling session\n")
    root.deiconify()  # Show the main window after selecting labeler
    load_image()  # Start loading images

#  Calc angle by manual distances
def calculate_tilt():
    try:
        distance = float(distance_entry.get())
        height = float(height_entry.get())
        angle = math.degrees(math.atan(height / distance))
        result_label.config(text=f"Calculated Tilt: {angle:.2f}°")
    except ValueError:
        result_label.config(text="Invalid Input")

images = get_all_images(raw_images_dir)
current_index = 0
log_entries = []
debug_mode = False
labeler_name = ""

# Create GUI
root = tk.Tk()
root.title("Image Tagging Tool with Tilt Calculation")

# Ask if debug mode
debug_mode = tk.messagebox.askyesno("Debug Mode", "Enable debug mode?")

# Ask for labeler's name using predefined options
labeler_name = tk.StringVar()

if __name__ == "__main__":
    taggedNum = [0,0,0]

    labeler_selection = tk.Toplevel(root)
    labeler_selection.title("Select Labeler")
    tk.Label(labeler_selection, text="Select your name:", font=("Helvetica", 14)).pack(pady=10)

    for name in ["Roei", "Yael"]:
        tk.Button(labeler_selection, text=name, command=lambda n=name: set_labeler(n)).pack(padx=10, pady=5)

    # Frame for Image Tagging and Calculation UI
    main_frame = tk.Frame(root)
    main_frame.pack()

    # Left frame for image tagging
    image_frame = tk.Frame(main_frame)
    image_frame.pack(side="left", padx=10)

    img_label = tk.Label(image_frame)
    img_label.pack()

    # Right frame for tilt calculation
    tilt_frame = tk.Frame(main_frame)
    tilt_frame.pack(side="right", padx=10)

    distance_label = tk.Label(tilt_frame, text="Distance from focal point (m):")
    distance_label.pack()
    distance_entry = tk.Entry(tilt_frame)
    distance_entry.pack()

    height_label = tk.Label(tilt_frame, text="Camera height (m):")
    height_label.pack()
    height_entry = tk.Entry(tilt_frame)
    height_entry.pack()

    # Add buttons for categories
    for category in categories:
        btn = tk.Button(root, text=category.capitalize(), command=lambda c=category: tag_image(c))
        btn.pack(side="left", padx=5, pady=5)
    calc_button = tk.Button(tilt_frame, text="Calculate Tilt", command=calculate_tilt)
    calc_button.pack()
    result_label = tk.Label(tilt_frame, text="Calculated Tilt: ")
    result_label.pack()

    # Add Stop Labeling button
    stop_button = tk.Button(root, text="Stop Labeling", command=stop_labeling)
    stop_button.pack(side="left", padx=5, pady=5)

    root.withdraw()  # Hide main window until labeler is selected
    root.mainloop()