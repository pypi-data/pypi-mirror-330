#importing the necessary libraries
from requests import get
from SECedgarpyExceptions import ErrorFoundWhileGETRequest

#defining the global Variables to be used
HEAD ={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"}
URL_FORM = "https://www.sec.gov/Archives/edgar/data/" 



#to filter out and get only the 10-k reports
def filterfunc(a: list) -> bool:
    if(a[0] == "10-K"):
        return True
    else:
        return False 

#to extract the url using the CIK which is passed into the func
def extract10Kurl(cikval: str) -> list:

    listofforms = []
    urllist = []

    url = f"https://data.sec.gov/submissions/CIK{cikval}.json"
    
    resp = get(url, timeout=5000, headers=HEAD)
    
    data = resp.json()

    ticker = str(data["tickers"][0]).lower()
    CIK = str(data["cik"])
    dataform = data["filings"]["recent"]

    for subzip in zip (dataform["form"], dataform["accessionNumber"] , dataform["reportDate"]):
        
        listofforms.append(list(subzip))

    finalarr = list(filter(filterfunc, listofforms))
        
    for elt in finalarr:
        elt[1] = str(elt[1]).replace("-","")
        elt[2] = str(elt[2]).replace("-","")

    for finelt in finalarr:
        newurl = URL_FORM + CIK + "/" + finelt[1] + "/"+ ticker + "-" + finelt[2] + ".htm"
        urllist.append(newurl)
      
    return urllist

#to convert the URL to direct xlsx Files
def URLtoXLSX(URLlist: list[str]) -> list:
    
    for urlelt in URLlist:
        urlelt = urlelt[:-17] + "Financial_Report.xlsx"
    
    return URLlist

