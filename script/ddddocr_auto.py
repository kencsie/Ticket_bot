import ddddocr
import csv

# CSV output path
csv_file_path = "../Data/outputs.csv"

# Create an OCR object
ocr = ddddocr.DdddOcr()

# Open the CSV file in append mode
with open(csv_file_path, "w", newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Path", "Ground_truth"])

    # Process each image
    for idx in range(0, 5000):
        image_path = f"../Data/Pics/Ndhu/captcha{idx}.jpg"

        # Open and read the image
        with open(image_path, "rb") as file:
            image = file.read()

        # Perform OCR on the image
        result = ocr.classification(image)

        # Write the image filename and OCR result to the CSV file
        writer.writerow([image_path, result])

