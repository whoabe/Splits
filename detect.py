
import io
import os
import cv2
import numpy as np

# # Imports the Google Cloud client library
# from google.cloud import vision
# from google.cloud.vision import types

# # Instantiates a client
# client = vision.ImageAnnotatorClient()

# # The name of the image file to annotate
# file_name = os.path.join(
#     os.path.dirname(__file__),
#     'receipt2.jpg')

# # Loads the image into memory
# with io.open(file_name, 'rb') as image_file:
#     content = image_file.read()

# image = types.Image(content=content)

# # Performs label detection on the image file
# response = client.label_detection(image=image)
# labels = response.label_annotations

# print('Labels:')
# for label in labels:
#     print(label.description)

# 

coords=[] 
def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        # textdesc = '\n"{}"'.format(text.description)
        # print(textdesc)

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        for vertex in text.bounding_poly.vertices:
            coords.append(tuple((vertex.x , vertex.y)))
        # coords='bounds: {}'.format(','.join(vertices))
    print(coords)

detect_text('./receipt6.jpg')

for i in range(0,4):
    coords.pop(0)

image = cv2.imread('./receipt6.jpg')
original_image = image
for coord in coords:
    topleft = coords[0]
    bottomright = coords[2]
    coords.pop(0)
    coords.pop(0)
    coords.pop(0)
    coords.pop(0)
    if (coords[0][0] > 300 & coords[0][0] < 500):  
        cv2.rectangle(image, topleft, bottomright, (0,255,0), 3)

# for coord in coords:
#     cv2.circle(image,coord, 5, (0,0,255), -1)

cv2.imshow('Red dots', image)
cv2.waitKey(0)