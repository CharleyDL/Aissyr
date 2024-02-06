import dagshub
import mlflow
import cv2
import numpy as np

# dagshub.init("my-first-repo", "CharleyDL", mlflow=True)
# mlflow.start_run()

# # train your model...

# mlflow.log_param("parameter name ", "value")
# mlflow.log_metric("metric name", 1)

# mlflow.end_run()

# Import necessary libraries
# Load the image
image = cv2.imread("/Users/charley.dlebarbier/Documents/Dev/VSCode/Projects/projet_NeoAIssyr/notebook_model/data/train_images/K01057.jpg")

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to create a binary image
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find contours in the binary image
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate over the contours
for contour in contours:
    # Calculate the contour area
    area = cv2.contourArea(contour)

    # Filter out small contours
    if area > 50:
        # Draw a bounding rectangle around the contour
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Display the image with detected glyphs
cv2.imshow("Glyph Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
