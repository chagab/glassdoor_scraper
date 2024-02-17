# Glassdoor scraper

Get salaries for a job title in various locations of the world.

Choose a job title you are interested in and input a list of locations as a [json](https://docs.python.org/3/library/json.html) file to know how much this job pays over there. A [selenium](https://www.selenium.dev/) bot will automatically fetch the information from [Glassdoor](https://www.glassdoor.com/index.htm) and store the results in [csv](https://docs.python.org/3/library/csv.html) database. Finally, you can plot the results with [matplotlib](https://matplotlib.org/stable/) to determine where you can get the highest salary. 

![image](https://github.com/chagab/glassdoor_scraper/assets/28218716/a1403876-30d2-45b0-ae9b-834087dc5bf4)

All the salaries are converted in US dollar. If the result is empty, there are no information about the job title at the given location on Glassdoor.

*This code was tested in the US. In other regions of the world (Europe for instance), it crashes due to cookie preferences pop-ups.*

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

Then, in order to create a new database of salaries, run the following code

``` python
from DatabaseHandler import DatabaseHandler
job_title = 'Data Engineer' # as an example
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
