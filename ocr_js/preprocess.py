import io
import sys
import cv2
import base64
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

imagePath = sys.argv[1]


def ndarray_to_image_string(numpy_array):
    # Convert NumPy array to PIL Image
    image = Image.fromarray(numpy_array)

    # Create an in-memory byte stream
    image_stream = io.BytesIO()

    # Save the PIL Image to the byte stream in PNG format
    image.save(image_stream, format="PNG")

    # Get the byte stream value as a base64-encoded string
    image_string = base64.b64encode(image_stream.getvalue()).decode("utf-8")

    return image_string


def areaFilter(minArea, inputImage):
    # Perform an area filter on the binary blobs:
    (
        componentsNumber,
        labeledImage,
        componentStats,
        componentCentroids,
    ) = cv2.connectedComponentsWithStats(inputImage, connectivity=4)

    # Get the indices/labels of the remaining components based on the area stat
    # (skip the background component at index 0)
    remainingComponentLabels = [
        i for i in range(1, componentsNumber) if componentStats[i][4] >= minArea
    ]

    # Filter the labeled pixels based on the remaining labels,
    # assign pixel intensity to 255 (uint8) for the remaining pixels
    filteredImage = np.where(
        np.isin(labeledImage, remainingComponentLabels) == True, 255, 0
    ).astype("uint8")

    return filteredImage


# Read image
inputImage = cv2.imread(imagePath)

# Conversion to CMYK (just the K channel):
# Convert to float and divide by 255:
imgFloat = inputImage.astype(np.float64) / 255.0

# Calculate channel K:
kChannel = 1 - np.max(imgFloat, axis=2)

# Convert back to uint 8:
kChannel = (255 * kChannel).astype(np.uint8)

# Threshold image:
binaryThresh = 130
_, binaryImage = cv2.threshold(kChannel, binaryThresh, 255, cv2.THRESH_BINARY)

# Filter small blobs:
minArea = 100
binaryImage = areaFilter(minArea, binaryImage)

# Use a little bit of morphology to clean the mask:
# Set kernel (structuring element) size:
kernelSize = 3
# Set morph operation iterations:
opIterations = 2
# Get the structuring element:
morphKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelSize, kernelSize))
# Perform closing:
binaryImage = cv2.morphologyEx(
    binaryImage,
    cv2.MORPH_CLOSE,
    morphKernel,
    None,
    None,
    opIterations,
    cv2.BORDER_REFLECT101,
)

cv2.imwrite("./thres.jpg", binaryImage)

sys.stdout.write(ndarray_to_image_string(binaryImage))
