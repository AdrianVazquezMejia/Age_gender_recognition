import cv2
import numpy as np



def handle_hc(output, input_shape):
    '''
    Handles the output of the age- genre recognition model.
    Returns gender and age
    '''
    # TODO 1: Extract the blobs
    
    age= output['age_conv3'].flatten()
    genre = output['prob'].flatten()
    # TODO 2: Resize this output 
    age_pred = int(age*100);
    genre_pred = np.argmax(genre)

    return age_pred, genre_pred




def preprocessing(input_image, height, width):
    '''
    Given an input image, height and width:
    - Resize to width and height
    - Transpose the final "channel" dimension to be first
    - Reshape the image to add a "batch" of 1 at the start 
    '''
    image = np.copy(input_image)
    image = cv2.resize(image, (width, height))
    image = image.transpose((2,0,1))
    image = image.reshape(1, 3, height, width)

    return image
