import requests
import re
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

    # viewstate = soup.find('input', {'name': '__VIEWSTATE'})
    # VIEWSTATE = viewstate["value"]
    # print(VIEWSTATE)

    VIEWSTATE = re.findall(r'<input.*?value="(.*?)\"',str(response.content))[0]
    print(VIEWSTATE)
    print("***********************************************")

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


    table_record = re.findall(
        r'<a\s+id="rptCompanyNameSearch.*?\>(.*?)\<.*?StatusItem\"\>(.*?)\<.*?CompanyNumberText\"\>([^\<]*)\<.*?"110"\>(.*?)\<.*?DateItem"\>(.*?)\<', str(response.content))
    print(table_record)


    table_dict=[]
    for i in table_record:
        data={}
        data['Company Name'] = i[0]
        data['Status'] = i[1]
        data['Company Number'] = i[2]
        data['Type'] = i[3]
        data['Date'] = i[4]
        
        table_dict.append(data)
        print(data)

    print(table_dict)

    #convert the table_dict to a pandas dataframe
    df = pd.DataFrame(table_dict)
    print(df)
    df.to_csv('regex.csv', index=False)
    print("Data saved to file : regex.csv")




if __name__ == "__main__":
    main()
