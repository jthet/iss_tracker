# ISS Tracker 
### Overview: 
This project contains files that build an API of data from International Space Station, posted by NASA. This API can be used to access different information concerning the ISS, including positional and time data along with comments from NASA.

### Data:
The data used in this project is a XML file that contains information on the state Vectors of the ISS at different epochs (points in time). The data can be viewed here: [ISS Public Data](https://spotthestation.nasa.gov/trajectory_data.cfm).

The Data is read in as XML and converted to a python dictionary with the module `xmltodict`

### Scripts:

`iss_tracker.py`:
Flask application for querying the ISS position and velocity. The application should loads in the data mentioned above and provides flask routes for a user to digest the data and find specific data points and values associated with specific data points.
The routes and returns are as follows:


| Route         | Return        | 
| ------------- |:-------------:| 
| `/`     | returns full data set | 
| `/epochs`       | returns all epochs in the data set      |
| `/epochs/<int:epoch>`  | returns all the data (state vectors) associated with a specific epoch      |
| `/epochs/<int:epoch>/position`  | returns the positional coordinates of a specific epoch     |
| `/epochs/<int:epoch>/velocity`  | returns the velocity of a specific epoch        |
| `/epochs/<int:epoch>/speed`  | returns the speed of a specific epoch      |
| `/help`  | Return help text (as a string) that briefly describes each route     |
| `/delete-data`  | Delete all data from the dictionary object |
| `/post-data`  | Reload the dictionary object with data from the web |
| `/comment`  | Return ‘comment’ list object from ISS data |
| `/header`  | Return ‘header’ dict object from ISS data |
| `/metadata`  | Return ‘metadata’ dict object from ISS data |
| `/epochs/<epoch>/location`| Return latitude, longitude, altitude, and geoposition for given Epoch |
| `/now`  | Return latitude, longitude, altidue, and geoposition for Epoch that is nearest in time |


** Note: <epoch> takes in an integer value, corresponding to the index of the epoch (i.e. the first epoch in the data set is epoch = 1)




`Dockerfile`: Text document that contains the commands to assemble the iss_tracker Docker image that is used to produce the Docker container when ran. 
 
`docker-compose.yml`: YAML file that automates deployment of the flask App.
 
`config.yaml`: YAML file that allows configurations of flask app deployment, in particular, turning "Debug" mode on/off.
 
`tester_script.sh`: bash script that executes all routes in `iss_tracker.py` and outputs the stdout and stderr output in the `tester_script_output.txt` and `tester_script_stderr.txt` files, respectively. This script also can take in a specific <epoch> input and is used to test the flask app for errors and to confirm errors are handled. 

## Instructions and Installation:

### Preferred Method: Use docker-compose file to automate containerized deployment. 
 
 To use the `docker-compose.yml` file, execute the following command:

 ```
 $ docker-compose up
 Starting iss_tracker_flask-app_1 ... done
Attaching to iss_tracker_flask-app_1
flask-app_1  |  * Serving Flask app 'iss_tracker'
flask-app_1  |  * Debug mode: off
flask-app_1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
flask-app_1  |  * Running on all addresses (0.0.0.0)
flask-app_1  |  * Running on http://127.0.0.1:5000
flask-app_1  |  * Running on http://172.22.0.2:5000
flask-app_1  | Press CTRL+C to quit
 ```

 This will open a container running the flask app. To enter the container find the container ID or container name with:
 ```
 $ docker ps
 CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS          PORTS                                       NAMES
ab819371ad36   jthet/iss_tracker:1.0   "python3 iss_tracker…"   29 minutes ago   Up 14 seconds   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   iss_tracker_flask-app_1
 ```
 
 Use the container ID to enter into the container, from which you can access the flask app API:
 ```
 $ docker exec -it iss_tracker_flask-app_1 /bin/bash
 root@ab819371ad36:
 ```
 Skip to the "Using the Flask app" section to use the flask app. 

 
### Method 2: Use Existing Docker Image:

To use the existing Docker Image run the following commands:
```
$ docker pull jthet/iss_tracker:1.0
...
$ docker run -it --rm -p 5000:5000 jthet/iss_tracker:1.0
```
This will open the flask app. 
Skip to the "Using the Flask app" section to use the flask app. 

### Method 3: Build a new image from Dockerfile:
To build a new image from the existing Dockerfile, execute the following commands:
Note: Dockerfile must be in the current directory when this command is executed.
```
$ docker build -t <dockerhubusername>/<code>:<version> .
```
Example:
```
$ docker build -t jthet/iss_tracker:1.0 .
Sending build context to Docker daemon  203.3kB
Step 1/9 : FROM python:3.8.10
 ---> a369814a9797
Step 2/9 : RUN pip3 install Flask==2.2.2
 ---> Using cache
 ---> d61f67c8565f
Step 3/9 : RUN pip3 install requests==2.22.0
 ---> Using cache
 ---> 3490f259e389
Step 4/9 : RUN pip3 install xmltodict==0.13.0
 ---> Using cache
 ---> 8e6a6a6b8aee
Step 5/9 : RUN pip3 install geopy==2.3.0
 ---> Using cache
 ---> 99ccc7bab631
Step 6/9 : RUN pip3 install PyYAML==6.0
 ---> Using cache
 ---> 5a0813d68822
Step 7/9 : COPY iss_tracker.py /iss_tracker.py
 ---> Using cache
 ---> 7a3dd4153e1c
Step 8/9 : COPY config.yaml /config.yaml
 ---> Using cache
 ---> 4ae29c585d99
Step 9/9 : CMD ["python3", "iss_tracker.py"]
 ---> Using cache
 ---> 2339fda107e3
Successfully built 2339fda107e3
Successfully tagged jthet/iss_tracker:1.0
```

Check the image was built with `$ docker images`:
```
$ docker images
REPOSITORY                 TAG        IMAGE ID       CREATED              SIZE
jthet/iss_tracker        1.0        2883079fad18   About a minute ago   928MB
```
Run the image with the following:
```
$ docker run -it --rm -p 5000:5000 jthet/iss_tracker:hw05
 * Serving Flask app 'iss_tracker'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 108-861-049
```
This will open the flask app in the current directory.
Skip to the "Using the Flask app" section to use the flask app.

### Method 4: Running the Flask App directly
 
To run the flask App directly, execute the command ` $ flask --app iss_tracker run `:
 ```
 $ flask --app iss_tracker run 
 * Serving Flask app 'iss_tracker'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 108-861-049
 ```
 This will open the flask app in the current directory.
 Skip to the "Using the Flask app" section to use the flask app.
 

## Using the Flask app
After completing any of methods from the "instructions and installation" section you should see the following output prompt:

```
$ docker run -it --rm -p 5000:5000 jthet/iss_tracker:hw05
 * Serving Flask app 'iss_tracker'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 108-861-049
```
 
 

Each route can be accessed with the following:
```
$ curl localhost:5000/ [ROUTE]
```


All of the routes and example output are shown below.

Route: `/`
```
$ curl localhost:5000/
              .
              .
              .
 {
    "EPOCH": "2023-063T12:00:00.000Z",
    "X": {
      "#text": "2820.04422055639",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "5.0375825820999403",
      "@units": "km/s"
    },
    "Y": {
      "#text": "-5957.89709645725",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "0.78494316057540003",
      "@units": "km/s"
    },
    "Z": {
      "#text": "1652.0698653803699",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "-5.7191913150960803",
      "@units": "km/s"
    }
  }
]
```


Route: `/epochs`
```
$ curl localhost:5000/epochs
              .
              .
              .
  "2023-063T11:43:00.000Z",
  "2023-063T11:47:00.000Z",
  "2023-063T11:51:00.000Z",
  "2023-063T11:55:00.000Z",
  "2023-063T11:59:00.000Z",
  "2023-063T12:00:00.000Z"
]
```

Route: `/epochs/<int:epoch>`
```
$ curl localhost:5000/epochs/1

{
  "EPOCH": "2023-048T12:04:00.000Z",
  "X": {
    "#text": "-5998.4652356788401",
    "@units": "km"
  },
  "X_DOT": {
    "#text": "-2.8799691318087701",
    "@units": "km/s"
  },
  "Y": {
    "#text": "391.26194859011099",
    "@units": "km"
  },
  "Y_DOT": {
    "#text": "-5.2020406581448801",
    "@units": "km/s"
  },
  "Z": {
    "#text": "-3164.26047476555",
    "@units": "km"
  },
  "Z_DOT": {
    "#text": "4.8323394499086101",
    "@units": "km/s"
  }
}
```


Route: `/epochs/1/position`
```
$ curl localhost:5000/epochs/1/position
{
  "X (km)": "-5998.4652356788401",
  "Y (km)": "391.26194859011099",
  "Z (km)": "-3164.26047476555"
}
```

Route: `/epochs/1/velocity`
```
$ curl localhost:5000/epochs/1/velocity
[
  "-2.8799691318087701",
  "-5.2020406581448801",
  "4.8323394499086101"
]
```


Route: `/epochs/1/speed`
```
$ curl localhost:5000/epochs/1/speed
{
  "speed (km/s)": 58.70695376830683
}
```

Route: `/help`
```
$ curl localhost:5000/help

HERE IS A HELP MESSAGE FOR EVERY FUNCTION/ROUTE IN "iss_tracker.py"

get_data:

    Retrieves the data from the nasa published ISS location coordinates, converts from XML to a dictionary, and returns the 
    Valuable data concering the ISS position and velocity at different times. 

    Route: None, only used to retreive data for other routes

    Args:
        None

    Returns:
        data (dict): the ISS stateVectors at different epochs
    

get_all:

    Returns all epochs for the entire data set of the ISS state vectors. Decorated with the app route "<baseURL>/"

    Route: <baseURL>/

    Args:
        None

    Returns:
        dataSet (dict): Dictionary of all epochs and corresponding state Vectors of the ISS
 .
 .
 .
 (Help messages for all routes will be shown in actual execution. For brevity the entire message is excluded)
```

Route: `/delete-data` (Must use `-X DELETE` tag)
```
$ curl -X DELETE localhost:5000/delete-data
Data is deleted
```

Route: `/post-data` (Must use `-X POST` tag)
```
$ curl -X POST localhost:5000/post-data
Data is posted
```

Route: `/comment`
```
$ curl localhost:5000/comment
[
  "Units are in kg and m^2",
  "MASS=473291.00",
  "DRAG_AREA=1421.50",
  "DRAG_COEFF=2.80",
  "SOLAR_RAD_AREA=0.00",
  "SOLAR_RAD_COEFF=0.00",
  "Orbits start at the ascending node epoch",
  "ISS first asc. node: EPOCH = 2023-03-08T12:50:10.295 $ ORBIT = 2617 $ LAN(DEG) = 108.61247",
  "ISS last asc. node : EPOCH = 2023-03-23T11:58:44.947 $ ORBIT = 2849 $ LAN(DEG) = 32.65474",
  "Begin sequence of events",
  "TRAJECTORY EVENT SUMMARY:",
  null,
  "|       EVENT        |       TIG        | ORB |   DV    |   HA    |   HP    |",
  "|                    |       GMT        |     |   M/S   |   KM    |   KM    |",
  "|                    |                  |     |  (F/S)  |  (NM)   |  (NM)   |",
  "=============================================================================",
  "GMT067 Reboost        067:19:47:00.000             0.6     428.1     408.4",
  "(2.0)   (231.1)   (220.5)",
  null,
  "Crew05 Undock         068:22:00:00.000             0.0     428.7     409.6",
  "(0.0)   (231.5)   (221.2)",
  null,
  "SpX27 Launch          074:00:30:00.000             0.0     428.3     408.7",
  "(0.0)   (231.2)   (220.7)",
  null,
  "SpX27 Docking         075:12:00:00.000             0.0     428.2     408.6",
  "(0.0)   (231.2)   (220.6)",
  null,
  "=============================================================================",
  "End sequence of events"
]
```

Route: `/header`
```
$ curl localhost:5000/header
{
  "CREATION_DATE": "2023-067T21:02:49.080Z",
  "ORIGINATOR": "JSC"
}
```
 
Route: `/metadata`
```
$ curl localhost:5000/metadata
{
  "CENTER_NAME": "EARTH",
  "OBJECT_ID": "1998-067-A",
  "OBJECT_NAME": "ISS",
  "REF_FRAME": "EME2000",
  "START_TIME": "2023-067T12:00:00.000Z",
  "STOP_TIME": "2023-082T12:00:00.000Z",
  "TIME_SYSTEM": "UTC"
}
```
 
Route: `/epochs/<epoch>/location`
```
$ curl localhost:5000/epochs/1/location
{
  "Altitude": 426.6207371384162,
  "Geoposition": "Over the Ocean",
  "Latitude": 11.029159199242079,
  "Longitude": -57.867905190541975
}
```
 
Route: `/now`
```
$ curl localhost:5000/now
{
  "closest epoch": "2023-068T23:12:00.000Z",
  "location": {
    "Altitude": 416.2149196401033,
    "Geoposition": "Urschendorf, Gemeinde St. Egyden am Steinfeld, Bezirk Neunkirchen, Lower Austria, 2731, Austria",
    "Latitude": 47.78779872268547,
    "Longitude": 16.09248383193608
  },
  "seconds from now": 95.75182104110718,
  "speed (km/s)": 7.666928348002811,
  "velocity (km/s) (X, Y, Z)": [
    "-0.32898806323843999",
    "-7.3943941991672402",
    "1.9991227013311601"
  ]
}
```

### Query Parameters
The route `/epochs` has 2 query paramaters: "limit" and "offset" 

The offset query parameter should offset the start point by an integer. For example, `offset=0` would begin printing at the first Epoch, `offset=1` would begin printing at the second Epoch, etc. The limit query parameter controls how many results are returned. For example `limit=10` would return 10 Epochs, `limit=100` would return 100 Epochs, etc. Putting them together, the route `/epochs?limit=20&offset=50` would return Epochs 51 through 70 (20 total).

Example:
```
$ curl 'localhost:5000/epochs?limit=4&offset=20'
{
  "21": "2023-055T13:20:00.000Z",
  "22": "2023-055T13:24:00.000Z",
  "23": "2023-055T13:28:00.000Z",
  "24": "2023-055T13:32:00.000Z"
}
```
