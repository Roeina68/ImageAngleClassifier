import os

raw_images_dir = r"C:\Projects\ElbitRuppin\Data\visDrone\raw"

# Check if the directory exists
if not os.path.exists(raw_images_dir):
    print(f"Error: Directory {raw_images_dir} does not exist!")

# List all image files
image_files = [f for f in os.listdir(raw_images_dir) if f.endswith((".jpg", ".png", ".jpeg"))]

if image_files:
    print(f"Found {len(image_files)} images in {raw_images_dir}:")
    print(image_files[:10])  # Print first 10 images
else:
    print("No images found in the directory!")
