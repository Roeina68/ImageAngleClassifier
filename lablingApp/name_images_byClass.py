import os

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

categories = ["horizontal", "diagonal", "vertical"]
for c in categories:
# Specify the folder path and output file name
    folder_path = f"C:/Projects/ElbitRuppin/data/visDrone/preprocessed/{c}"
    output_file = f"C:/Projects/ElbitRuppin/data/visDrone/preprocessed/{c}_photos.txt"
    # Call the function
    list_files_in_folder(folder_path, output_file)
