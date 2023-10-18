# Flask Simple API

## Description

This simple Flask API was made for test purposes only. It allows user to search for some movie data, that is automatically added to the database when you first run the API. As it is not servered up, it is recomended to run in debug mode.

## Model Definition
The database used for it was SQLite.  

This API presents only one model, defined by:  

```
class MovieModel():
    id: Integer PRIMARY KEY
    year:  INTEGER NOT NULL
    title: STRING UNIQUE
    studios : STRING NOT NULL
    producers : STRING NOT NULL
    winner = STRING
```

As it is implemented in Python, a simple ```to_dict()``` function was implemented:  

```
  def to_dict(self):
      return {
          'id': self.id,
          'year': self.year,
          'title': self.title,
          'studios':self.studios,
          'producers':self.producers,
          'winner': self.winner if self.winner else ''
      }
```

## Routes
The MovieModel presents presents routes that cover 3 common HTTP requests(GET,POST,DELETE). (*PUT requests were not necessary)  

As it recommended to run in debug mode, it will use the user's localhost server and default port 5000, so routes will always have ```http://localhost:5000``` as base url.  


### GET ALL MOVIES
```/api/movies/allMovies``` -> Returns a list of all movies documents with full object infos.  

### GET MOVIE
```/api/movies/<id>``` -> Returns the full movie document the matches the <id> from the url.  

### POST MOVIE
```/api/movies``` -> Receives 1 object and post into the database.  

### DELETE MOVIE
```/api/movies/<id>``` -> Deletes the document that matchs the <id> from url.  

### GET THE PRODUCERS WITH LONGEST AND SHORTEST GAP THAT OBTAINED TWO AWARDS
```/api/movies/projection``` -> Projects an data object that brings the refered information.  

Data Object format:  

```
{
  "min": [
    {
      "producer": "Producer 1",
      "interval": 1,
      "previousWin": 2008,
      "followingWin": 2009
    },
    {
    "producer": "Producer 2",
    "interval": 1,
    "previousWin": 2018,
    "followingWin": 2019
    }
  ],
  "max": [
    {
      "producer": "Producer 1",
      "interval": 99,
      "previousWin": 1900,
      "followingWin": 1999
    },
    {
      "producer": "Producer 2",
      "interval": 99,
      "previousWin": 2000,
      "followingWin": 2099 
    }
  ]
}
```

## How to run it
I personally recommend you use a unique Python environment to execute the code, so you are certain that the dependencies version are supported.  

Create you environment with you prefered tool, that run:  

```pip install requirements.txt```  

It should install everything you need.  

Now, to execute it, just run:  
```flask run```  
To run in Debug mode, try instead:  
```flask run --debug```

It will automatically post the csv documents from the movielist.csv file inside the context.  
**NOTE:** If you want to change the movielist.csv file, just replace it and rename it equally to the original.  

Now, you are free to explore any request by any prefered tool, like Postman,Insomnia, etc.
