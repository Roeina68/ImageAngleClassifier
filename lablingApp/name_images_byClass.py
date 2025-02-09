import os
import shutil
import cv2  # OpenCV for image resizing

def list_files_in_folder(folder_path, output_file):
    try:
        # Open the output file in write mode
        with open(output_file, 'w') as file:
            # Walk through the folder
            for root, dirs, files in os.walk(folder_path):
                for filename in files:
                    # Write each file name to the output file
                    file.write(f"{filename}\n")
        print(f"File names have been listed in {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")



class DroneImageProcessor:
    def __init__(self, base_path):
        self.base_path = base_path
        self.categories = ["horizontal", "diagonal", "vertical"]
        self.raw_folder = os.path.join(base_path, "visDrone/raw")  # Source images
        self.processed_folder = os.path.join(base_path, "visDrone/preprocessed")  # Resized images destination

        # Ensure preprocessed category folders exist
        for category in self.categories:
            os.makedirs(os.path.join(self.processed_folder, category), exist_ok=True)

    def resize_and_save_image(self, source_path, destination_path):
        """Resizes an image to 224x224 and saves it in the correct folder."""
        try:
            img = cv2.imread(source_path)
            if img is None:
                print(f"❌ Error: Could not read {source_path}. Skipping.")
                return
            resized_img = cv2.resize(img, (224, 224))
            cv2.imwrite(destination_path, resized_img)
            print(f"✅ Resized and saved {destination_path}")
        except Exception as e:
            print(f"❌ Error processing {source_path}: {e}")

    def process_images(self):
        """Reads `*_photos.txt`, resizes, and copies images to the correct folder."""
        for category in self.categories:
            label_file = os.path.join(self.processed_folder, category, f"{category}_photos.txt")
            category_folder = os.path.join(self.processed_folder, category)

            if not os.path.exists(label_file):
                print(f"⚠️ Warning: Label file {label_file} does not exist. Skipping {category}.")
                continue

            with open(label_file, 'r') as file:
                for line in file:
                    filename = line.strip()
                    source_path = os.path.join(self.raw_folder, filename)
                    destination_path = os.path.join(category_folder, filename)

                    if os.path.exists(source_path):
                        self.resize_and_save_image(source_path, destination_path)
                    else:
                        print(f"❌ File {filename} not found in raw folder.")

    def run(self):
        """Runs the image processing pipeline."""
        print("\n📌 Resizing and saving images...")
        self.process_images()
        print("\n🎉 Image processing complete!")


if __name__ == "__main__":

    #  Listing labeled images in files
    categories = ["horizontal", "diagonal", "vertical"]
    for c in categories:
        # Specify the folder path and output file name
        folder_path = f"C:/Projects/ElbitRuppin/data/visDrone/preprocessed/{c}"
        output_file = f"C:/Projects/ElbitRuppin/data/visDrone/preprocessed/{c}_photos.txt"
        # Call the function
        list_files_in_folder(folder_path, output_file)


    # #  Label and resize photos according to labling files
    # base_path = "C:/Projects/ElbitRuppin/data"
    # processor = DroneImageProcessor(base_path)
    # processor.run()