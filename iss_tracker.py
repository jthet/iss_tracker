from flask import Flask, request
import requests
import xmltodict
import math # NEED TO ADD SQRT TO SPEED CALC



app = Flask(__name__)


# Gets usefull date (only data -> stateVectors)
def get_data() -> list:
    """
    Retrieves the data from the nasa published ISS location coordinates, converts from XML to a dictionary, and returns the 
    Valuable data concering the ISS position and velocity at different times. 

    Route: None, only used to retreive data for other routes

    Args:
        None

    Returns:
        data (dict): the ISS stateVectors at different epochs
    """

    url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    response = requests.get(url)
    data = xmltodict.parse(response.text) # repsonse.text contains text xml Data
    return data['ndm']['oem']['body']['segment']['data']['stateVector']



# Base url, returns dict of all data
@app.route('/', methods = ['GET'])
def get_all() -> list:
    """
    Returns all epochs for the entire data set of the ISS state vectors. Decorated with the app route "<baseURL>/"

    Route: <baseURL>/

    Args:
        None

    Returns:
        dataSet (dict): Dictionary of all epochs and corresponding state Vectors of the ISS
    """
    return dataSet

@app.route('/epochs', methods = ['GET'])
def get_epochs() -> list:
    """
    Returns all the epochs in the data set, without the state Vectors. 
    
    Route: <baseURL>/epochs

    Args:
        None

    Returns:
        epochs (list): A list of all the epochs (time stamps) in the data set. 
    """

    all_epochs = []
    queried_epochs = []

    for d in dataSet:
        all_epochs.append(d['EPOCH'])

    # Testing query paramters
    try:    
        offset = int(request.args.get('offset', 0)) # default value is 0
    except ValueError:
        return "Error: query parameter 'offset' must be an integer\n", 404

    try:
        limit = int(request.args.get('limit', len(all_epochs) - offset))
    except ValueError:
        return "Error: query parameter 'limit' must be an integer\n", 404

    if limit > len(all_epochs) or offset > len(all_epochs) or (limit+offset) > len(all_epochs):
        return "Query Paramters out of bounds of data set\n"
  
    
    epoch_dict = {} 
    for i in range(limit):
        epoch_dict[offset+i+1] = all_epochs[offset + i]

    return epoch_dict

@app.route('/epochs/<epoch>', methods = ['GET']) 
def get_entry(epoch: str) -> dict:
    """
    Given an epoch, returns the state vectors associated with that specific epoch.
    Decorated with the app route "<baseURL>/epochs/<epoch>"

    Route: <baseURL>/epochs/<int:epoch>

    Args:
        epoch (string): returns a string representing the epoch entry index number as an int. 
            - Note: epoch is given as a string but is converted to and used as a integer to index a list. 

    Returns:
        data[int(epoch)] (dict): returns the given index "epoch" of the data list from the full data set 
    """
    # <int:epoch>  works too but used try block just to test functionality 
    try: 
        epoch = int(epoch)
    except ValueError:
        return "Error: Epoch number must be an integer\n", 404

    if epoch <= 0:
        return "Epoch number must be a positive index (cannot be 0)\n", 404
    
    if epoch > len(dataSet):
        return "Error: Epoch index out of data set range\n", 404 

    return dataSet[int(epoch)-1]

@app.route('/epochs/<epoch>/speed', methods = ['GET'])
def speed_calc(epoch: str) -> dict:
    """
    Given an epoch, returns the speed of the ISS at that specific epoch. 
    Speed is calculated from the X, Y, and Z velocities given in the data set. 
    
    Route: <baseURL>/epochs/<int:epoch>/speed

    Args:
        epoch (string): returns a string representing the epoch entry index number as an int. 
            - Note: epoch is given as a string but is converted to and used as a integer to index a list. 

    Returns:
        {"speed (km/s)" : speed} (dict): returns the speed of a given index "epoch"
    """
    try: 
        epoch = int(epoch)
    except ValueError:
        return "Error: Epoch number must be an integer\n", 404

    if epoch <= 0:
        return "Epoch number must be a positive index (cannot be 0)\n", 404
    
    if epoch > len(dataSet):
        return "Error: Epoch index out of data set range\n", 404

    veloList = get_velocity(epoch)
    speed = sum([float(i)**2 for i in veloList])
    return {"speed (km/s)" : sqrt(speed)}

@app.route('/epochs/<epoch>/position', methods = ['GET'])
def get_position(epoch: str) -> dict:
    """
    Given an epoch, returns the position of the ISS at that specific epoch. 
    Position is given as the the X, Y, and Z positional coordinates. 
    
    Route: <baseURL>/epochs/<int:epoch>/position

    Args:
        epoch (string): returns a string representing the epoch entry index number as an int. 
            - Note: epoch is given as a string but is converted to and used as a integer to index a list. 

    Returns:
        position (dict): returns the X, Y, and Z positional coordinates of a given index "epoch"
    """

    try: 
        epoch = int(epoch)
    except ValueError:
        return "Error: Epoch number must be an integer\n", 404

    if epoch <= 0:
        return "Epoch number must be a positive index (cannot be 0)\n", 404
    
    if epoch > len(dataSet):
        return "Error: Epoch index out of data set range\n", 404


    epoch_state = get_entry(epoch)
    position = {'X (km)': epoch_state['X']['#text'], 'Y (km)': epoch_state['Y']['#text'], 'Z (km)': epoch_state['Z']['#text']}
    return position

@app.route('/epochs/<epoch>/velocity', methods = ['GET']) # Really just need this func for speed calc but added app route anyway
def get_velocity(epoch: str) -> list:
    """
    Given an epoch, returns the velocity of the ISS at that specific epoch. 
    Velocity is given as the X, Y, and Z velocities. 

    Route: <baseURL>/epochs/<int:epoch>/velocity
    
    Args:
        epoch (string): returns a string representing the epoch entry index number as an int. 
            - Note: epoch is given as a string but is converted to and used as a integer to index a list. 

    Returns:
        velo (list): returns the X, Y, and Z velocity of a given index "epoch"
    """

    try: 
        epoch = int(epoch)
    except ValueError:
        return "Error: Epoch number must be an integer\n", 404

    if epoch <= 0:
        return "Epoch number must be a positive index (cannot be 0)\n", 404
    
    if epoch > len(dataSet):
        return "Error: Epoch index out of data set range\n", 404

    velo = [] # formatted as [X, Y, Z]
    epoch_state = get_entry(epoch)
    velo.append(epoch_state['X_DOT']['#text'])
    velo.append(epoch_state['Y_DOT']['#text'])
    velo.append(epoch_state['Z_DOT']['#text'])
    return velo

@app.route('/help', methods = ['GET'])
def get_help() -> str:
    """
    Returns a message of all the available routes and methods and how to use them 
    
    Route: <baseURL>/help

    Args:
        NONE

    Returns:
        help_message (string) : brief descriptions of all available routes and methods
    """

    list_of_functions = ['get_data', 'get_all', 'get_epochs', 'get_entry', 'speed_calc', 'get_position', 'get_velocity', 'get_help', 'delete_data', 'post_data']
    
    help_message = '\nHERE IS A HELP MESSAGE FOR EVERY FUNCTION/ROUTE IN "iss_tracker.py"\n\n'

    for func in list_of_functions:
        help_message = help_message + f'{func}:\n' + eval(func).__doc__ + '\n\n'

    return help_message

@app.route('/delete-data', methods = ['DELETE']) 
def delete_data() -> str:
    """
    Deletes all data from the data set
    
    Route: <baseURL>/delete-data

    Args:
        NONE

    Returns:
        (str) 'Data is deleted'
    """
    # USE: 'curl -X DELETE localhost:5000/post-data'
    global dataSet
    dataSet.clear()

    return 'Data is deleted\n'


@app.route('/post-data', methods = ['POST']) 
def post_data() -> str:
    """
    Restores the data to the ISS dictionary
    
    Route: <baseURL>/post-data

    Args:
        NONE

    Returns:
        (str) 'Data is posted'
    """
    # USE: 'curl -X POST localhost:5000/post-data'
    global dataSet
    dataSet = get_data()

    return "Data has been posted\n"


#dataSet = {} # global Variable
dataSet = get_data()
copyOfData = dataSet




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
