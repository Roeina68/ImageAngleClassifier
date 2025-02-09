import os


def count_images_in_directory(directory):
    """
    Counts the total number of image files in a directory (including subdirectories).
    Considers only image file extensions: .jpg, .jpeg, .png, .bmp, .tiff.
    """
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
    total_count = sum(
        len([f for f in files if os.path.splitext(f)[1].lower() in image_extensions])
        for _, _, files in os.walk(directory)
    )
    return total_count


def count_files_in_subdirectories(parent_dir):
    """
    Returns a sorted dictionary where keys are subdirectories of parent_dir
    and values are the percentage of total files in each subdirectory.
    """
    results = {}
    total_files = count_images_in_directory(parent_dir)  # Count only images

    for entry in os.scandir(parent_dir):
        if entry.is_dir():
            subdir_path = entry.path
            file_count = count_images_in_directory(subdir_path)
            results[subdir_path] = file_count

    # Convert counts to percentages and sort in descending order
    if total_files > 0:
        results = {subdir: (count / total_files) * 100 for subdir, count in results.items()}
        results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))

    return results, total_files


if __name__ == "__main__":
    raw_directory = r"C:\Projects\ElbitRuppin\data\visDrone\raw"
    preprocessed_directory = r"C:\Projects\ElbitRuppin\data\visDrone\preprocessed"

    if not os.path.exists(raw_directory) or not os.path.exists(preprocessed_directory):
        print("One or both specified directories do not exist.")
    else:
        # Count images in raw and preprocessed datasets
        total_raw_images = count_images_in_directory(raw_directory)
        total_preprocessed_images = count_images_in_directory(preprocessed_directory)

        # Get percentages for subdirectories in the preprocessed dataset
        file_percentages, preprocessed_image_count = count_files_in_subdirectories(preprocessed_directory)

        # Display the percentage of images in each preprocessed subfolder
        print("\n### Preprocessed Image Distribution ###")
        for subdir, percentage in file_percentages.items():
            print(f"{subdir}: {percentage:.2f}% of preprocessed images")

        # Calculate overall preprocessing percentage
        if total_raw_images > 0:
            overall_percentage = (total_preprocessed_images / total_raw_images) * 100
            print(f"\n### Overall Preprocessing Statistics ###")
            print(f"Total raw images: {total_raw_images}")
            print(f"Total preprocessed images: {total_preprocessed_images}")
            print(f"Percentage of raw images that were preprocessed: {overall_percentage:.2f}%")
        else:
            print("No images found in the raw dataset.")
