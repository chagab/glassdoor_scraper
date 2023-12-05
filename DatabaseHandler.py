import os
import csv


class DatabaseHandler():

    def __init__(self, database_directory="./database"):
        self.database_directory = database_directory

    def create_database(self, job_title, locations) -> None:
        self.locations = locations
        self.job_title = job_title

        database_name = f"database-{job_title.replace(' ', '_').lower()}.csv"
        database_path = os.path.join(
            self.database_directory,
            database_name
        )

        if not os.path.exists(database_path):
            with open(database_path, "w", newline='') as database:
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
                for location in locations:
                    row = [location] + (len(columns_name) - 1) * ['']
                    database_writer.writerow(row)
