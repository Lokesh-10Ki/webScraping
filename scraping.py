import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

def main():
    HOME_URL = "https://cado.eservices.gov.nl.ca/CadoInternet/Main.aspx"
    REQUEST_URL = "https://cado.eservices.gov.nl.ca/CadoInternet/Company/CompanyNameNumberSearch.aspx"
    DATA_FILE_NAME = "CADO-Company-Search-Data"
    company_name_keyword_1 = ""
    company_name_keyword_2 = ""

    company_name_keyword_1 = input(
        "Enter the first keyword to search or the company name: ")
    company_name_keyword_2 = input(
        "Enter the second keyword to search or the company name: ")

    REQUEST_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "cado.eservices.gov.nl.ca",
        "Origin": "https://cado.eservices.gov.nl.ca",
        "Referer": "https://cado.eservices.gov.nl.ca/CadoInternet/Company/CompanyNameNumberSearch.aspx",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "sec-ch-ua-platform": "Windows"
    }

    # Initialize session and fetch the page content
    session = requests.Session()

    response = session.get(HOME_URL, headers=REQUEST_HEADERS)
    # use bs4 ot find the viewstate value

    soup = BeautifulSoup(response.content, "lxml")
    viewstate = soup.find('input', {'name': '__VIEWSTATE'})
    VIEWSTATE = viewstate["value"]
    print(VIEWSTATE)

    PAYLOAD = {
        "__VIEWSTATE": VIEWSTATE,
        "txtNameKeywords1": company_name_keyword_1 if company_name_keyword_1 else "",
        "txtNameKeywords2": company_name_keyword_2 if company_name_keyword_2 else "",
        "txtCompanyNumber": "",
        "btnSearch.x:": 38,
        "btnSearch.y:": 14,
    }


    response = session.post(
        url=REQUEST_URL, data=PAYLOAD, headers=REQUEST_HEADERS)
    
    with open(file=DATA_FILE_NAME+'.html', mode="w", encoding="utf-8") as file:
        file.write(response.content.decode("utf-8"))
    print("Data saved to file: "+DATA_FILE_NAME+'.html')

    html_content = BeautifulSoup(response.content, "lxml") 
  

    # table = html_content.find('table', {'id': 'tableSearchResults'})
    table = html_content.find('table', attrs={'id': 'tableSearchResults'})
    table = table.find('table')
    table=table.find('table')
    print(table)
    td_tags = table.find_all('td')


    # Extract the text from each td tag
    texts = [td.text.strip() for td in td_tags]

    # remove the newlines and spaces from texts
    texts = [text for text in texts if text]

    #remove the last element from the list
    texts.pop()

    print(texts)

    # for text in texts:
        # print(text)

    #convert the texts into a dataframe
    

    # print(df)
    rows = [texts[i:i+5] for i in range(0, len(texts), 5)]
    # Write the rows to a CSV file

    df = pd.DataFrame(rows)

    print(df)

    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


if __name__ == "__main__":
    main()
