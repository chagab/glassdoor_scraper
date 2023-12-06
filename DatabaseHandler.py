import os
import csv
import json
import regex as re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from GlassdoorBot import GlassdoorBot
from currency_code import CurrencyCode
from currency_converter import CurrencyConverter
from selenium.common.exceptions import TimeoutException


class UnkownMultiplier(Exception):
    pass


class DatabaseHandler():

    def __init__(self, database_directory="./database") -> None:
        self.database_directory = database_directory

    def get_locations(self) -> list[str]:
        with open("locations.json") as json_file:
            return json.load(json_file)["locations"]

    def create(self, job_title, locations=None) -> None:
        if locations is None:
            self.locations = self.get_locations()
        else:
            self.locations = locations

        self.job_title = job_title

        database_name = f"database-{job_title.replace(' ', '_').lower()}.csv"
        self.database_path = os.path.join(
            self.database_directory,
            database_name
        )

        if not os.path.exists(self.database_path):
            with open(self.database_path, "w", newline='') as database:
                database_writer = csv.writer(database)
                columns_name = [
                    "City",
                    "Job title",
                    "Min salary (local currency)",
                    "Max salary (local currency)",
                    "per",
                    "Min salary (usd/y)",
                    "Max salary (usd/y)",
                    "Average salary (usd/y)"
                ]
                database_writer.writerow(columns_name)
                for location in self.locations:
                    row = [location] + (len(columns_name) - 1) * ['']
                    database_writer.writerow(row)

    def fill(self, user_credential_path="user_credentials.json", headless=True) -> None:
        # check if there are empty rows in the database
        db = pd.read_csv(self.database_path)
        has_empty_cells = np.any(pd.isna(db['Job title']))
        locations = db['City']

        while has_empty_cells:
            # update the database after every crash
            db = pd.read_csv(self.database_path)
            with open(user_credential_path) as json_file:
                user_credential = json.load(json_file)
                bot = GlassdoorBot(
                    email=user_credential['email'],
                    password=user_credential['password'],
                    headless=headless
                )

            try:
                bot.open_glassdoor()
                for i, location in enumerate(locations):

                    # If the row is empty
                    if pd.isna(db.at[i, 'Job title']):
                        description = self.job_title, location
                        salary_details = bot.get_salary_details(*description)
                        job_title, city, salary_range = salary_details

                        min_salary, max_salary = salary_range.split(' - ')
                        frequency = max_salary[-2:]
                        max_salary = max_salary[:-3].replace(' ', '')
                        min_salary = min_salary.replace(' ', '')

                        if frequency == 'yr':
                            mult = 1
                        elif frequency == 'mo':
                            mult = 12
                        else:
                            raise UnkownMultiplier("Error: Unknown multiplier")

                        min_salary_usdy = self.to_usd(min_salary) * mult
                        max_salary_usdy = self.to_usd(max_salary) * mult
                        min_max = [min_salary_usdy, max_salary_usdy]
                        mean_salary_usdy = np.mean(min_max)

                        # update the database
                        db.at[i, 'Job title'] = job_title
                        db.at[i, 'Min salary (local currency)'] = min_salary
                        db.at[i, 'Max salary (local currency)'] = max_salary
                        db.at[i, 'per'] = frequency
                        db.at[i, 'Min salary (usd/y)'] = min_salary_usdy
                        db.at[i, 'Max salary (usd/y)'] = max_salary_usdy
                        db.at[i, 'Average salary (usd/y)'] = mean_salary_usdy

                        # save the database
                        db.to_csv(self.database_path, index=False)

                        # update the looping condition
                        has_empty_cells = np.any(pd.isna(db['Job title']))

            except TimeoutException:
                bot.driver.close()

    @staticmethod
    def to_usd(currency_string) -> float:
        # currency_string = currency_string.replace(' ', '')
        multiplier = currency_string[-1]

        # Match everything before a digit
        currency = re.search(r'^[^\d]*', currency_string).group()
        currency = CurrencyCode.get_code(currency)

        # Match a group of digits
        amount = re.search(r'(\d+)', currency_string).group()
        amount = int(amount)

        if multiplier == 'K':
            amount *= 1e3
        elif multiplier == 'M':
            amount *= 1e6
        else:
            raise UnkownMultiplier("Error: Unknown multiplier")

        try:
            currency_converter = CurrencyConverter()
            return currency_converter.convert(amount, currency, 'USD')
        except:
            return 0.0

    def plot(self) -> None:
        database = pd.read_csv(self.database_path, usecols=[0, 1, 5, 6, 7])
        database = database.sort_values(
            'Average salary (usd/y)', ascending=False)

        profession = database['Job title'][0]

        plt.close('all')

        num_bar, _ = database.shape
        x = range(num_bar)

        plt.figure()
        plt.suptitle(f'{profession} salaries around the world')
        plt.bar(
            x, database['Max salary (usd/y)'],
            color='lightblue', label='max'
        )
        plt.bar(
            x, database['Min salary (usd/y)'],
            color='dodgerblue', label='min'
        )
        plt.plot(
            x, database['Average salary (usd/y)'],
            'ro-', label='average'
        )
        plt.axhline(y=100e3, color='red')
        plt.legend()
        plt.xticks(x, database['City'], rotation=90)
        plt.ylabel('Salary (USD)')
        plt.tight_layout()
        plt.show()
