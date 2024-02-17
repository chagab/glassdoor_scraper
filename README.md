# Glassdoor scraper

Get salaries for a job title in various locations of the world.

Choose a job title you are interested in and input a list of locations as a [json](https://docs.python.org/3/library/json.html) file to know how much this job pays over there. A [selenium](https://www.selenium.dev/) bot will automatically fetch the information from [Glassdoor](https://www.glassdoor.com/index.htm) and store the results in [csv](https://docs.python.org/3/library/csv.html) database. Finally, you can plot the results with [matplotlib](https://matplotlib.org/stable/) to determine where you can get the highest salary. 

![data_scientist](https://github.com/chagab/glassdoor_scraper/assets/28218716/5096c8e5-6d8a-4d8e-bb3c-79496d35e809)

All the salaries are converted in US dollar. If the result is empty, there are no information about the job title at the given location on Glassdoor.

*This code was tested in the US. In other regions of the world (Europe for instance), it crashes due to cookie preferences pop-ups that are not taken into account yet.*

# How to use the project 

You need a glassdoor account to use the project.

First, clone the project. Next, create a <code>user_credentials.json</code> file storing your Glassdoor account user credentials as follow

``` json
{
    "email": "your.email@youremail.com",
    "password": "your_glassdoor_password"
}
```
It is important that this file is stored in the project folder with the correct name (more precisely <code>user_credentials.json</code>). The code will automatically load the user credentials from this file and will otherwise crash if it is stored somewhere else.

Then create a <code>locations.json</code> file storing the location you want get salary information from

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
Same as for the previous file, it is important that the file is stored in the project folder with the correct file name. 

Then, in order to create a new database of salaries, run the following code

``` python
from DatabaseHandler import DatabaseHandler
job_title = 'Data Engineer' # as an example
database = DatabaseHandler()
database.create(job_title=job_title)
database.fill(headless=True)
database.plot()
```

This will create a Chrome web browser page scraper that connect to your glassdoor account and fetch the required data. If you want to see the web page, you can change the <code>headless</code> argument to False. After a few fetches, glassdoor detects that the request is done by a bot which will close the browser and start a new one. 

While browsing, the scraper will create a <code>database</code> folder where a csv file named <code>database-your_job_title.csv</code> will store the results. If the program crashes and you re-run it, it will start from the first empty location.

In order to open a already existing database, run the following code

``` python
from DatabaseHandler import DatabaseHandler
database = DatabaseHandler()
database.open("path/to/database.csv")
database.plot()
```
