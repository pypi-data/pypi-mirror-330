#importing necessary modules
from requests import get
from bs4 import BeautifulSoup
from SECedgarpyExceptions import ErrorFoundWhileGETRequest, ExtractionError
from SECedgarpyProcessing import HEAD
import pandas as pd

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

#to get all the necessary CIK for the sp500.csv
def CIKExtractor() -> list:
    companyList = []
    
    try:
        response = get(url, timeout=5000, headers=HEAD)

        if (response.status_code == 404):
            raise FileNotFoundError

        elif(response.status_code != 200):
            raise ErrorFoundWhileGETRequest

        else:
            soup = BeautifulSoup(response.content, 'html.parser')

            table = soup.find('table', {'id': 'constituents'})

            if table is None:
                raise ValueError

            rows = table.find_all('tr')[1:] 

            for row in rows:
                cells = row.find_all('td')
                if len(cells) > 0:
                    companyName = cells[1].text.strip()
                    cik = cells[6].text.strip()
                    companyList.append((companyName, cik))

    except FileNotFoundError as fnf:
        print(fnf)
    except ErrorFoundWhileGETRequest as e:
        print(f"GET request error: {e}")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return companyList

#Function which gets all the S&P top 500 info in the form of an CSV
def GetAllSP500CSV():

    try:
        tables = pd.read_html(url)

        if not tables:
            raise ExtractionError("No tables found on the Wikipedia page.")

        sp500_table = tables[0]

        sp500_table.to_csv("sp500_companies.csv", index=False)
        print("S&P 500 companies data saved to sp500_companies.csv successfully.")

    except ExtractionError as e:
        print(f"Extraction error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")