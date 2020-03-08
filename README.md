# Age_gender_recognition
Using OpenVINO toolkit to deploy an app that can recognize age and gender of a human face

The input is a mp4 video, and the output is a mp4 video with text indicating the age and gender of the person in the video.

The arguments are

    c_desc = "CPU extension file location, if applicable"
    d_desc = "Device, if not CPU (GPU, FPGA, MYRIAD)"
    i_desc = "The location of the input"
    m_desc = "The location of the model XML file"
    
    if argument "i" is equal to "0" then the input is the webcam.
    
    ESC to break the processing

example of command 

python app.py -i "input_video.mp4" -m "model_directory/age-gender-recognition-0013.xml" 
-c "/opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so"
