# Glassdoor scraper

Get [Glassdoor's](https://www.glassdoor.com/index.htm) salary for a job title from a list of different locations. 

Get salary converted in US dollar for a specific job title in various locations as a [csv](https://docs.python.org/3/library/csv.html) file and plot the different locations' salary with [matplotlib](https://matplotlib.org/stable/) to determine where you can get the highest salary. 

# How to use the project 

You need a glassdoor account to use the project. The first step is to create a <code>user_credentials.json</code> file storing your user credentials

``` json
{
    "email": "your.email@youremail.com",
    "password": "your_password"
}
```

and a <code>locations.json</code> file storing the location you want get salary information from

``` json
{
    "locations": [
        "London",
        "Paris",
        "New York",
        "..."
    ]
}
```

Then, in order to create a new database, run the following code

``` python
from DatabaseHandler import DatabaseHandler
job_title = 'Data Engineer'
database = DatabaseHandler()
database.create(job_title=job_title)
database.fill(headless=True)
database.plot()
```

In order to open a already existing database, run the following code

``` python
from DatabaseHandler import DatabaseHandler
database = DatabaseHandler()
database.open("path/to/database.csv")
database.plot()
```

The results can be viewed as follow

![image](https://github.com/chagab/glassdoor_scraper/assets/28218716/a1403876-30d2-45b0-ae9b-834087dc5bf4)

