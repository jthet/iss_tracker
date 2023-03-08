# Homework 5: "Undone (The Sweater Container)" 
### Scenario: The API you developed for the ISS positional and velocity data (in homework 04) is a great start! But, there are many improvements we could make in order to make the API more useful. And, we can use some smart software engineering & design strategies to make our app more portable.
#### Objective: Gain familiarity with flask and containers. 

### Data:
The data for this homework set is a XML file that contains information on the state Vectors of the ISS at different epochs (points in time). The data can be viewed here: [ISS Public Data](https://spotthestation.nasa.gov/trajectory_data.cfm).

The Data is read in as XML and converted to a python dictionary with the module `xmltodict`

### Scripts:

`iss_tracker.py`:
Flask application for querying the ISS position and velocity. The application should loads in the data mentioned above and provides flask routes for a user to digest the data and find specific data points and values associated with specific data points.
The routes and returns are as follows


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


** Note: epoch takes in an integer value, corresponding to the index of the epoch (i.e. the first epoch in the data set is epoch = 1)




`Dockerfile`: Text document that contains the commands to assemble the iss_tracker Docker image that is used to produce the Docker container when ran. 

### Instructions and Installation:
#### Method 1: Use Existing Docker Image:

To use the existing Docker Image run the following commands:
```
$ docker pull jthet/iss_tracker:hw05
...
$ docker run -it --rm -p 5000:5000 jthet/iss_tracker:hw05
```
This will open the flask app. Skip to step 2 of method 2 below to see how to use the flask app. 

#### Method 2: Build a new image from Dockerfile:
To build a new image from the existing Dockerfile, execute the following commands:
Note: Dockerfile must be in the current directory when this command is executed.
```
$ docker build -t <dockerhubusername>/<code>:<version> .
```
Example:
```
$ docker build -t jthet/iss_tracker:hw05 .
Sending build context to Docker daemon   16.9kB
Step 1/6 : FROM python:3.8.10
 ---> a369814a9797
Step 2/6 : RUN pip3 install Flask==2.2.2
 ---> Using cache
 ---> d61f67c8565f
Step 3/6 : RUN pip3 install requests==2.22.0
 ---> Using cache
 ---> 3490f259e389
Step 4/6 : RUN pip3 install xmltodict==0.13.0
 ---> Using cache
 ---> 8e6a6a6b8aee
Step 5/6 : COPY iss_tracker.py /iss_tracker.py
 ---> Using cache
 ---> e724bf1387c1
Step 6/6 : CMD ["python3", "iss_tracker.py"]
 ---> Using cache
 ---> 4a86216dceea
Successfully built 4a86216dceea
Successfully tagged jthet/iss_tracker:hw05
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
```
This will open the flask app in a new container.

### Running the Flask App

#### After the container is built and the Flask app is running:
This should output the following prompt:

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

#### Using the Flask app
Each route can be accesd with the following:
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



