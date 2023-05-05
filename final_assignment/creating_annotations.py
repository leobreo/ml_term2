from PIL import Image, ImageDraw
import os

def read_coordinates_from_file(file_path):
    with open(file_path, "r") as f:
        line = f.readline().strip()
        
        if not line:  # If the file is empty
            return 0, 0, 0, 0
        else:
            values = line.split()
            if len(values) == 5:
                _, n1, n2, n3, n4 = map(float, values)
                return n1, n2, n3, n4
            else:
                print(f"Warning: Unexpected number of values in the file {file_path}")
                return 0, 0, 0, 0

def draw_rectangle_on_image(input_image_path, output_image_path, normalized_coordinates, interpretation):
    # Open the image
    image = Image.open(input_image_path)
    width, height = image.size

    # Convert normalized coordinates based on the interpretation
    n1, n2, n3, n4 = normalized_coordinates
    # ... (same as before, no changes needed in this part) ...

    if interpretation == 1: # x_center, y_center, width, height
        x1, y1 = int((n1 - n3/2) * width), int((n2 - n4/2) * height)
        x2, y2 = int((n1 + n3/2) * width), int((n2 + n4/2) * height)
    elif interpretation == 2: # y_center, x_center, height, width
        x1, y1 = int((n2 - n4/2) * width), int((n1 - n3/2) * height)
        x2, y2 = int((n2 + n4/2) * width), int((n1 + n3/2) * height)
    elif interpretation == 3: # x1, y1, x2, y2
        x1, y1 = int(n1 * width), int(n2 * height)
        x2, y2 = int(n3 * width), int(n4 * height)
    elif interpretation == 4: # y1, x1, y2, x2
        x1, y1 = int(n2 * width), int(n1 * height)
        x2, y2 = int(n4 * width), int(n3 * height)
    elif interpretation == 5: # x_center, y_center, x2, y2
        x1, y1 = int((n1 - n3) * width), int((n2 - n4) * height)
        x2, y2 = int(n3 * width), int(n4 * height)
    elif interpretation == 6: # x1, y1, x2, y2 (absolute)
        x1, y1 = int(n1 * width), int(n2 * height)
        x2, y2 = int(n3 * width), int(n4 * height)
    elif interpretation == 7: # y1, x1, y2, x2 (absolute)
        x1, y1 = int(n2 * width), int(n1 * height)
        x2, y2 = int(n4 * width), int(n3 * height)
        
    coordinates = (x1, y1, x2, y2)

    # Create an ImageDraw object
    draw = ImageDraw.Draw(image)

    # Draw the rectangle on the image
    draw.rectangle(coordinates, outline="red", width=3)

    # Save the image with the rectangle
    image.save(output_image_path)


if __name__ == "__main__":
    image_folder = "/Users/leonardbrenk/Downloads/obj/"
    txt_folder = "/Users/leonardbrenk/Downloads/obj/"
    output_folder = "/Users/leonardbrenk/Documents/03 Education/02 Uni/02 Master/Semester 2/01 ML/ml_term2/final_assignment/data/annotated"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for img_index in range(1, 10001):  # Process the first 2000 images
        input_image_path = os.path.join(image_folder, f"image_{img_index}.jpg")
        txt_file_path = os.path.join(txt_folder, f"image_{img_index}.txt")

        if os.path.exists(input_image_path) and os.path.exists(txt_file_path):
            normalized_coordinates = read_coordinates_from_file(txt_file_path)
            output_image_path = os.path.join(output_folder, f"output_image_{img_index}.jpg")
            draw_rectangle_on_image(input_image_path, output_image_path, normalized_coordinates, 1)
            print(f"Processed image {img_index}")
        else:
            print(f"Image {img_index} or its corresponding text file not found")
