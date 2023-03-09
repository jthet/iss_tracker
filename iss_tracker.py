from flask import Flask, request
import requests
import xmltodict
import math 
from geopy.geocoders import Nominatim
import time
import yaml



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

# Gets full data set (inlcudes comments, headers, etc.)
def get_full_dataSet():
    """
    Retrieves the complete data sete from the nasa published ISS location coordinates, converts from XML to a dictionary, and returns the 
    full NASA data set 

    Route: None, only used to retreive data for other routes

    Args:
        None

    Returns:
        data (dict): the the entire NASA data set
    """

    url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    response = requests.get(url)
    data = xmltodict.parse(response.text) # repsonse.text contains text xml Data
    return data

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
    global dataSet
    if not dataSet:
        return "Data Set is empty \n"
    return dataSet

@app.route('/epochs', methods = ['GET'])
def get_epochs() -> list:
    """
    Returns all the epochs in the data set, without the state Vectors. 
    
    Route: <baseURL>/epochs
        Optional Route: '<baseURL>/epochs?limit=<some_Int>&offset=<some_Int>'

    Args:
        None

    Returns:
        epochs (list): A list of all the epochs (time stamps) in the data set. 
    """
    global dataSet
    if not dataSet:
        return "Data Set is empty \n"
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
    global dataSet
    if not dataSet:
        return "Data Set is empty \n"
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
    global dataSet
    if not dataSet:
        return "Data Set is empty \n"
    try: 
        epoch = int(epoch)
    except ValueError:
        return "Error: Epoch number must be an integer\n", 404

    if epoch <= 0:
        return "Epoch number must be a positive index (cannot be 0)\n", 404
    
    if epoch > len(dataSet):
        return "Error: Epoch index out of data set range\n", 404

    veloList = get_velocity(epoch)
    speed = math.sqrt(sum([float(i)**2 for i in veloList]))
    return {"speed (km/s)" : speed}

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
    global dataSet
    if not dataSet:
        return "Data Set is empty \n"
    try: 
        epoch = int(epoch)
    except ValueError:
        return "Error: Epoch number must be an integer\n", 404

    if epoch <= 0:
        return "Epoch number must be a positive index (cannot be 0)\n", 404
    
    if epoch > len(dataSet):
        return "Error: Epoch index out of data set range\n", 404


    epoch_state = get_entry(epoch)
    position = {'X': epoch_state['X']['#text'], 'Y': epoch_state['Y']['#text'], 'Z': epoch_state['Z']['#text']}
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
    global dataSet
    if not dataSet:
        return "Data Set is empty \n"
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
    
    list_of_functions = ['get_data', 'get_all', 'get_epochs', 'get_entry', 'speed_calc', 'get_position', 'get_velocity', 'get_help', 'delete_data', 'post_data', 'get_comment', 'get_header', 'get_metadata', 'get_location', 'recent_data']
    
    help_message = '\nHERE IS A HELP MESSAGE FOR EVERY FUNCTION/ROUTE IN "iss_tracker.py"\n\n'

    for func in list_of_functions:
        help_message = help_message + f'{func}:\n' + eval(func).__doc__
        if func == 'get_epochs':
            help_message = help_message + "\n    This function has query parameters 'limit' and 'offset' that affect the output by \n    changing the number of returned epochs and the starting point of the first returned epoch"
        help_message = help_message + '\n\n'

    return help_message

@app.route('/delete-data', methods = ['DELETE']) 
def delete_data() -> str:
    """
    Deletes all data from the data set
    
    Route: <baseURL>/delete-data
        example: 'curl -X DELETE localhost:5000/delete-data'

    Args:
        NONE

    Returns:
        (str) 'Data is deleted'
    """
    # USE: 'curl -X DELETE localhost:5000/post-data'

    try:
        global dataSet
        dataSet.clear()
    except Exception:
        return "Error: Data was not able to be deleted\n", 404

    return 'Data is deleted\n'

@app.route('/post-data', methods = ['POST']) 
def post_data() -> str:
    """
    Restores the data to the ISS dictionary
    
    Route: <baseURL>/post-data
        example 'curl -X POST localhost:5000/post-data'

    Args:
        NONE

    Returns:
        (str) 'Data is posted'
    """
    # USE: 'curl -X POST localhost:5000/post-data'
    try:
        global dataSet
        dataSet = get_data()
    except Exception:
        return "Error: Data was not able to be posted\n", 404

    return "Data has been posted\n", 200

@app.route('/comment', methods = ['GET']) 
def get_comment() -> list:
    """
    Returns the ‘comment’ list object from the ISS data
    
    Route: <baseURL>/comment

    Args:
        NONE

    Returns:
        (list) comments: All the comments in the data set
    """

    try:
        global fullSet
        comments = fullSet['ndm']['oem']['body']['segment']['data']['COMMENT']
    except KeyError as e:
        return f'Key Error in Dict Key {e}: No Comments exist in DataSet\n', 404
    except Exception:
        return "Unknown Error\n", 418

    return comments, 200

@app.route('/header', methods = ['GET']) 
def get_header() -> list:
    """
    Returns the ‘header’ dictionary object from the ISS data
    
    Route: <baseURL>/header

    Args:
        NONE

    Returns:
        header (list): the ‘header’ dictionary object from the ISS data
    """
    try:
        global fullSet
        header = fullSet['ndm']['oem']['header']
    except KeyError as e:
        return f'Key Error in Dict Key {e}: No Headers exist in DataSet\n', 404
    except Exception:
        return "Unknown Error\n", 418
        
    return header, 200

@app.route('/metadata', methods = ['GET']) 
def get_metadata() -> list:
    """
    Returns the 'metadata' dictionary object from the ISS data
    
    Route: <baseURL>/metadata

    Args:
        NONE

    Returns:
        metadata (list): the 'metadata' dictionary object from the ISS data
    """
    try:
        global fullSet
        metadata = fullSet['ndm']['oem']['body']['segment']['metadata']
    except KeyError as e:
        return f'Key Error in Dict Key {e}: No metadata exist in DataSet\n', 404
    except Exception:
        return "Unknown Error\n", 418
        
    return metadata, 200

@app.route('/epochs/<epoch>/location', methods = ['GET'])
def get_location(epoch: str) -> dict:
    '''
    Returns latitude, longitude, altitude, and geoposition for a given epoch.

    Route: <baseURL>/epochs/<epoch>/location

    Args: 
        epoch (string): returns a string representing the epoch entry index number as an int. 
            - Note: epoch is given as a string but is converted to and used as a integer to index a list.

    Returns:
        outputDict (dict): A dictionary of the latitude, longitude, altitude, and geoposition of the given epoch. 

    '''
    
    global dataSet
    MEAN_EARTH_RADIUS = 6371 # km
    

    if not dataSet:
        return "Data Set is empty \n"

    try:    
        epoch = int(epoch)
    except ValueError:
        return "Error: Epoch number must be an integer\n", 404

    if epoch <= 0:
        return "Epoch number must be a positive index (cannot be 0)\n", 404
    
    if epoch > len(dataSet):
        return "Error: Epoch index out of data set range\n", 404
    

    # Getting variables
    # position data
    epochPosition = get_position(epoch)
    x = float(epochPosition['X'])
    y = float(epochPosition['Y'])
    z = float(epochPosition['Z'])

    # Time data
    epochData = get_entry(epoch)
    epochTime = epochData["EPOCH"] # Gives string represeting data time, we will indx string for hour and minutes data
    hrs = int(epochTime[9] + epochTime[10])
    mins = int(epochTime[12] + epochTime[13])

    # Calculation
    lat = math.degrees(math.atan2(z, math.sqrt(x**2 + y**2)))                
    lon = math.degrees(math.atan2(y, x)) - ((hrs-12)+(mins/60))*(360/24) + 24
    alt = math.sqrt(x**2 + y**2 + z**2) - MEAN_EARTH_RADIUS     

    geocoder = Nominatim(user_agent='iss_tracker')
    geoloc = geocoder.reverse((lat, lon), zoom=20, language='en')
    
    try:
        geoPos = geoloc.address
    except AttributeError:
        geoPos = "Over the Ocean"
    finally:
        outputDict = {"Latitude": lat, "Longitude": lon, "Altitude": alt, "Geoposition": geoPos}

    return outputDict

@app.route('/now', methods = ['GET'])
def recent_data() -> dict:
    '''
    Return latitude, longitude, altitude, and geoposition for Epoch that is nearest in time

    Route: '<baseURL>/now'

    Args:
        NONE

    Returns:
        outputDict (dict): a dictionary containing the latitude, longitude, altitude, and geoposition
        for the most recent Epoch.
        
        outputDict Format:
            {
                "closest epoch": ------, 
                "seconds from now": -----, 
                "location": -----,
                "speed (km/s)": -----,
                "velocity (km/s) (X, Y, Z)": ------
            }
    '''
    
    global dataSet
    MEAN_EARTH_RADIUS = 6371 #km
    current_time = time.time() # gives present time in seconds since unix epoch
    smallest_dif = 100000000000 # arbitrary big number


    if not dataSet:
        return "Data Set is empty \n"

    epoch_index_counter = 0
    for epoch in dataSet:
        epoch_index_counter += 1
        time_epoch = time.mktime(time.strptime(epoch['EPOCH'][:-5], '%Y-%jT%H:%M:%S'))        # gives epoch (eg 2023-058T12:00:00.000Z) time in seconds since unix epoch
        dif = current_time - time_epoch
        if dif < smallest_dif:
            smallest_dif = dif
            closest_epoch = epoch
            closest_epoch_index = epoch_index_counter

    epoch_now = get_entry(closest_epoch_index)
    
    outputDict = {"closest epoch": epoch_now["EPOCH"], 
    "seconds from now": smallest_dif, 
    "location": get_location(closest_epoch_index),
    "speed (km/s)": speed_calc(closest_epoch_index)['speed (km/s)'],
    "velocity (km/s) (X, Y, Z)": get_velocity(closest_epoch_index)
    }

    return outputDict

def get_config():
    default_config = {"debug": True}
    try:
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Couldn't load the config file; details: {e}")
    # if we couldn't load the config file, return the default config
    return default_config

# Global Variables
dataSet = get_data()
fullSet = get_full_dataSet()




if __name__ == '__main__':
    config = get_config()
    if config.get('debug', True):
        app.run(debug=True, host='0.0.0.0')
    else:
        app.run(host='0.0.0.0')
