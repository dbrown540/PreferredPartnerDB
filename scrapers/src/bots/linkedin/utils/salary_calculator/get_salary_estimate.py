import logging
import random
import time
from typing import List
from datetime import datetime

import pandas as pd
from pandas import DataFrame
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementNotInteractableException,
    ElementClickInterceptedException
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from ...scripts.linkedinbot import BaseManager  # pylint: disable=relative-beyond-top-level
from ....webdriver.webdriver_manager import WebDriverManager
from .....database.scripts.database_manager import DatabaseManager, LinkedInDatabaseManager  # pylint: disable=relative-beyond-top-level

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")


class SalaryScraper(BaseManager):
    def __init__(self, webdriver_manager: WebDriverManager, database_manager: DatabaseManager) -> None:
        super().__init__(webdriver_manager, database_manager)

    def access_salary_website(self):
        self.driver.get("https://www.salary.com/")

    def type_job_title(self, job_title):
        try:
            job_title_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "trafficdrivertad-worth-jobtitle_input"))
            )
            job_title_input.send_keys(job_title)
        except NoSuchElementException:
            raise Exception('Unable to find the job title input element')

    def type_location(self, location):
        try:
            location_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "trafficdrivertad-worth-location_input"))
            )
            location_input.send_keys(location)
        except NoSuchElementException:
            raise Exception('Unable to find the job title input element')

    def click_search_button(self):
        search_button = self.driver.find_element(
            By.CSS_SELECTOR, "a.btn.border-greenneon.bg-greenneon[onclick='submitJobTitleForTrafficDriverTypeaheadForm(this)']"
        )
        search_button.click()

    def click_first_result(self):
        top_result = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "a-color.font-semibold.margin-right10"))
        )
        if top_result:
            print("Found the top result.", top_result.text)
        top_result.click()

    def click_salary_and_bonus(self):
        salary_and_bonus_button = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'div-tabs')]/a[text()='Salary + Bonus']"))
        )
        if salary_and_bonus_button:
            print(salary_and_bonus_button.get_attribute("href"))
        else:
            print("Could not find the salary and bonus button")

    def extract_median_income(self):
        median_salary = self.wait.until(
            EC.presence_of_element_located((By.ID, "top_salary_value"))
        ).text
        return float(median_salary)

    def wrapper(self):
        self.access_salary_website()
        self.type_job_title("Data Scientist")
        self.type_location("Baltimore, MD")
        self.click_search_button()
        self.click_first_result()
        self.click_salary_and_bonus()
        median_salary = self.extract_median_income()
        print(median_salary)
        time.sleep(5)


class SalaryCalculator:
    current_date = datetime.now()

    def __init__(self, salary: float, start_date: str, end_date: str) -> None:
        self.salary = salary,
        self.start_date = start_date,
        self.end_date = end_date,
        self.inflation = 0.03  #  3% per year
        self.current_year = self.current_date.year

    def generate_list_of_years(self):
        # Extract the years
        start_date_year = int(self.start_date[0][:4])
        end_date_year = int(self.end_date[0][:4])
        if end_date_year > start_date_year:
            return list(range(start_date_year, end_date_year + 1))
        return [start_date_year]

    def calculate_pre_taxed_salary(self, year):
        pre_taxed_income = self.salary[0] / ((1 + self.inflation) ** (self.current_year - year))  # Only calculates for 1 year. Expected input comes from a  member of list_of_years
        return pre_taxed_income


class FederalTaxCalculator(SalaryCalculator):
    def __init__(self, salary: float, start_date: str, end_date: str) -> None:
        super().__init__(salary, start_date, end_date)

    def clean_federal_tax_csv(self, df: DataFrame, cols=['Married Filing Jointly Salary', 'Married Filing Separately Salary', 'Single Filer Salary', 'Head of Household Salary']) -> DataFrame:
        # Create a copy of the DataFrame
        df = df.copy()

        # Remove na rows
        df = df.dropna(how='all')

        # Iterate over DataFrame columns
        for col in cols:
            # Check if the column contains strings
            if df[col].dtype == 'object':
                # Use regular expression to remove '$' and ',' characters, then convert to float
                df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)

        # Convert the year column to integers
        if 'Year' in df.columns:
            df['Year'] = df['Year'].astype(int)

        # Function to convert percentages to fractions
        def convert_percentage_to_fraction(df, substring):
            # Get the columns containing the specified substring
            relevant_columns = [col for col in df.columns if substring in col]

            # Iterate over relevant columns and convert percentages to fractions
            for col in relevant_columns:
                # Convert percentage string to float
                df[col] = df[col].str.rstrip('%').astype(float) / 100.0

            return df

        # Convert percentages to fractions for columns containing the substring "(Rates/Brackets)"
        df = convert_percentage_to_fraction(df, "(Rates/Brackets)")

        return df

    def filter_by_year(self, df, year):
        return df[df['Year'] == year]

    def locate_tax_bracket(self, df: DataFrame, salary):
        tax_brackets = {
            "Married Filing Jointly": None,
            "Married Filing Separately": None,
            "Single Filer": None,
            "Head of Household": None
        }
        print("SALARY: ", salary)

        highest_brackets = {
            'Married Filing Jointly': df['Married Filing Jointly (Rates/Brackets)'].iloc[-1],
            'Married Filing Separately': df['Married Filing Separately (Rates/Brackets)'].iloc[-1],
            'Single Filer': df['Single Filer (Rates/Brackets)'].iloc[-1],
            'Head of Household': df['Head of Household (Rates/Brackets)'].iloc[-1]
        }

        prev_row = None  # Initialize prev_row to None

        for index, row in df.iterrows():
            if salary < row['Married Filing Jointly Salary']:
                if prev_row is not None:
                    tax_brackets['Married Filing Jointly'] = prev_row['Married Filing Jointly (Rates/Brackets)']
                else:
                    tax_brackets['Married Filing Jointly'] = 0.1  # Default value if no previous row found
                break  # Exit the loop once the tax bracket is found
            prev_row = row
        else:
            tax_brackets['Married Filing Jointly'] = highest_brackets['Married Filing Jointly']


        prev_row = None  # Reset prev_row for the next loop

        for index, row in df.iterrows():
            if salary < row['Single Filer Salary']:
                if prev_row is not None:
                    tax_brackets['Single Filer'] = prev_row['Single Filer (Rates/Brackets)']
                else:
                    tax_brackets['Single Filer'] = 0.1  # Default value if no previous row found
                break  # Exit the loop once the tax bracket is found
            prev_row = row
        else:
            tax_brackets['Single Filer'] = highest_brackets['Single Filer']

        prev_row = None  # Reset prev_row for the next loop

        for index, row in df.iterrows():
            if salary < row['Head of Household Salary']:
                if prev_row is not None:
                    tax_brackets['Head of Household'] = prev_row['Head of Household (Rates/Brackets)']
                else:
                    tax_brackets['Head of Household'] = 0.1  # Default value if no previous row found
                break  # Exit the loop once the tax bracket is found
            prev_row = row
        else:
            tax_brackets['Head of Household'] = highest_brackets['Head of Household']

        prev_row = None  # Reset prev_row for the next loop

        for index, row in df.iterrows():
            if salary < row["Married Filing Separately Salary"]:
                if prev_row is not None:
                    tax_brackets['Married Filing Separately'] = prev_row['Married Filing Separately (Rates/Brackets)']
                else:
                    tax_brackets['Married Filing Separately'] = 0.1  # Default value if no previous row found
                break  # Exit the loop once the tax bracket is found
            prev_row = row
        else:
            tax_brackets['Married Filing Separately'] = highest_brackets['Married Filing Separately']

        return tax_brackets

    def calcalate_federal_tax(self, year: int, federal_income_tax_data='scrapers//src//bots//linkedin//utils//salary_calculator//federal_income_tax_date.csv'):
        df = pd.read_csv(federal_income_tax_data)
        df = self.clean_federal_tax_csv(df)
        df = self.filter_by_year(df, year)
        print("SALARY ", self.salary[0])
        tax_bracket = self.locate_tax_bracket(df, self.salary[0])
        print(tax_bracket)
        print(df.head(10))


# Example usage
calc = SalaryCalculator(100, '2015-09-09', '2020-10-02')
fedcalc = FederalTaxCalculator(100, '2015-09-09', '2020-10-02')
list_of_years = calc.generate_list_of_years()
print(list_of_years)
pretaxed_vals = []
for year in list_of_years:
    pretaxed_val = calc.calculate_pre_taxed_salary(year)
    rouded_pretaxed_val = round(pretaxed_val, 2)
    pretaxed_vals.append(rouded_pretaxed_val)
print(pretaxed_vals)
fedcalc.calcalate_federal_tax(2023)
