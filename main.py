from controller import Controller

mainController = Controller()

# Input Configuration
mainController.inputConfig()

# API Call
output = mainController.apiCall(
    image_url='https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/faces.jpg')

# Output Configuration
mainController.outputDisplay(output)
