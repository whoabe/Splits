
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


#coords will be a dictionary with bounding box coordinates as key
#values will be the OCR text
coords={}

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
        # coords='bounds: {}'.format(','.join(vertices))

        #turns all coords into a tuple and puts them into a list
        # for vertex in text.bounding_poly.vertices:
        #     coords.append(tuple((vertex.x , vertex.y)))
            
        #takes coords of top left and bottom right, then put them in the tuple
        topleft = tuple((text.bounding_poly.vertices[0].x, text.bounding_poly.vertices[0].y))
        bottomright = tuple((text.bounding_poly.vertices[2].x, text.bounding_poly.vertices[2].y))
        box = tuple((topleft,bottomright))

        #only allowing boxes with less than 50 characters
        #arbitrarily decided that if a box contained more than 50 chars, it is the whole image.
        if len(text.description) > 50:
            coords[box] = "imagebox"
        else:
            coords[box] = text.description

detect_text('./Receipt Images/receipt6.jpg')
image = cv2.imread('./Receipt Images/receipt6.jpg')

#made a copy of the original image in case anything else needs to be done with it
original_image = image

#annotates image with rectangles. to access the text value, text=coords[coord]
for coord in coords:
    topleft = coord[0]
    bottomright = coord[1]
    # text = coords[coord]
    cv2.rectangle(image, topleft, bottomright, (0,255,0), 3)

print(coords)

cv2.imshow('Red dots', image)
cv2.waitKey(0)