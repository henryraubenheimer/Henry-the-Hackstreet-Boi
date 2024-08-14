import os
from PIL import Image

# Directories
images_dir = "train/images"
labels_dir = "train/labels"
cropped_dir = "train/cropped_images"

# Create the cropped images directory if it doesn't exist
os.makedirs(cropped_dir, exist_ok=True)

# Function to read crop coordinates from a label file
def read_crop_coordinates(label_path, image_width, image_height):
    with open(label_path, 'r') as file:
        for line in file:
            if line.startswith('0'):  # Find the first line that starts with '0'
                # Assuming the format is: 0 x y width height (normalized)
                parts = line.strip().split()
                if len(parts) >= 5:  # Ensure there are enough parts for coordinates
                    # Extract and convert normalized values
                    x = float(parts[1]) * image_width
                    y = float(parts[2]) * image_height
                    width = float(parts[3]) * image_width
                    height = float(parts[4]) * image_height

                    # Calculate the top-left and bottom-right coordinates
                    left = int(x - width / 2)
                    top = int(y - height / 2)
                    right = int(x + width / 2)
                    bottom = int(y + height / 2)
                    return left, top, right, bottom
    return None  # Return None if no valid line is found

# Iterate over all images in the images directory
for image_name in os.listdir(images_dir):
    if image_name.endswith(".jpg"):  # Adjust this if your images have a different extension
        # Paths to the image and corresponding label
        image_path = os.path.join(images_dir, image_name)
        label_path = os.path.join(labels_dir, image_name.replace('.jpg', '.txt'))

        # Ensure the label file exists
        if os.path.exists(label_path):
            # Load the image
            image = Image.open(image_path)
            image_width, image_height = image.size

            # Read the crop coordinates
            coordinates = read_crop_coordinates(label_path, image_width, image_height)
            
            if coordinates:  # If valid coordinates were found
                left, top, right, bottom = coordinates

                # Crop the image
                cropped_image = image.crop((left, top, right, bottom))

                # Save the cropped image to the cropped_images directory
                cropped_image_path = os.path.join(cropped_dir, image_name)
                cropped_image.save(cropped_image_path)

                print(f"Cropped and saved: {cropped_image_path}")
            else:
                print(f"No valid coordinates found in: {label_path}")
        else:
            print(f"Label file not found for: {image_name}")
