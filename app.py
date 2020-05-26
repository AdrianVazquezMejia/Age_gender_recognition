import argparse
import cv2
import numpy as np

from handle_models import handle_hc, preprocessing
from inference import Network

GENDER= ["Female", "Male"]


def get_args():
    '''
    Gets the arguments from the command line.
    '''

    parser = argparse.ArgumentParser("Basic Edge App with Inference Engine")
    # -- Create the descriptions for the commands

    c_desc = "CPU extension file location, if applicable"
    d_desc = "Device, if not CPU (GPU, FPGA, MYRIAD)"
    i_desc = "The location of the input image"
    m_desc = "The location of the model XML file"

    # -- Add required and optional groups
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # -- Create the arguments
    required.add_argument("-i", help=i_desc, required=True)
    required.add_argument("-m", help=m_desc, required=True)
    optional.add_argument("-d", help=d_desc, default="CPU")
    args = parser.parse_args()

    return args



def create_output_image(image, output, width,heigth):
        # Get the age and gender from their lists
        age = output[0]
        genre = GENDER[output[1]]
        # Scale the output text by the image shape
        scaler = max(int(image.shape[0] / 1000), 1)
        # Write the text of color and type onto the image
        image = cv2.putText(image, 
            "Age: {}, Gender: {}".format(age, genre), 
            (25 * scaler, 50 * scaler), cv2.FONT_HERSHEY_SIMPLEX, 
            1 * scaler, (255, 255, 255), 3 * scaler)
        image = cv2.resize(image,(width,heigth))
        return image


def perform_inference(args):
    '''
    Performs inference on an input image, given a model.
    '''
    # Create a Network for using the Inference Engine
    inference_network = Network()  
    # Load the model in the network, and obtain its input shape    
    n, c, h, w = inference_network.load_model(args.m, args.d)
    ### TODO: Get and open video capture
        #Check for CAM, image or video
    if args.i == 'CAM':
        input_stream = 0
    cap = cv2.VideoCapture(input_stream)
    if input_stream :
        cap.open(args.input)
    #cap.open(args.i)
    width = int(cap.get(3))
    height = int(cap.get(4))
    # The second argument should be `cv2.VideoWriter_fourcc('M','J','P','G')`
    # on Mac, and `0x00000021` on Linux
    out = cv2.VideoWriter('out.mp4', 0x00000021, 30, (width,height))
    while cap.isOpened():
        flag, frame = cap.read()
        if not flag:
            break
        key_pressed = cv2.waitKey(60)
    # Read the input image
    ### TODO: Preprocess the input image
        preprocessed_image = preprocessing(frame, h, w)
    # Perform asynchronous inference on the image
        inference_network.async_inference(preprocessed_image)
        #TODO: process the output image
        output_func = handle_hc
        if inference_network.wait() == 0:
            # Obtain the output of the inference request
            output = inference_network.extract_output()
            # Draw the output mask onto the input
            processed_output = output_func(output, frame.shape)
            # Create an output image based on network
            output_image = create_output_image(frame, processed_output,width,height)
            # Save down the resulting image
            out.write(output_image)
            cv2.imshow("fram",output_image)      
        if key_pressed == 27:
            break
    # Release the capture and destroy any OpenCV windows
    out.release()
    cap.release()
    cv2.destroyAllWindows()
    
def main():
    args = get_args()
    perform_inference(args)
'''
python app.py -i "input_video.mp4" -m "model_directory/age-gender-recognition-0013.xml" -c "/opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so"
'''

if __name__ == "__main__":
    main()
