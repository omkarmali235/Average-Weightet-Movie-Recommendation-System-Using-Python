# song-recommeder
> *"A simple song recommender using python and GUI using Tkinter."*

## Table of Contents
* [Installation](#installation)
* [Data](#data)
* [Usage](#usage)
* [Examples](#examples)

### Installation
##### 1. Download the repository

Clone the base repository onto your desktop with `git` as follows:
```console
$ git clone https://github.com/omkarmali235/Movie-Recommendation-System-Using-Python
```

``

### Data 

We will use subset of **5000 TMDB Dataset**. It is a mixture of movies from various websites with the rating that users gave after watching the movie.<br>
It contains of two files, ***tmdb_5000_credits.csv*** and ***tmdb_5000_movies.csv***<br> 
The ***tmdb_5000_credits.csv*** contains *movie_id*,*title*,*cast*,*crew*<br>
The ***tmdb_5000_movies.csv*** contains *budget*,*genres*,*homepage*,*id*,*keywords*,*original_language*,*original_title*,*overview*,*popularity*,*production_companies*, *production_countries*,*release_date*,*revenue*,*runtime*,*spoken_languages*,*status*,*tagline*,*title*,*vote_average*,*vote_count*<br>
<br> 

Get the data as follows: 

```console
$ wget https://www.kaggle.com/tmdb/tmdb-movie-metadata

```

### Usage

To launch the app, launch it as follows:

```console
$ python index.py
```
![](/Screenshots/GUI.png)

### Examples
#### *When the application Starts?*
![](/FirstWindow.png)


#### *Recommendations to the Iron Man Movie?*
![](/Reccomendation.png)



