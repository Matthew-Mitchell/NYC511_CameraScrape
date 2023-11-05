import requests
from bs4 import BeautifulSoup
import glob
import os
import time
import sys

def get_pdf_links():
    url = "https://www.nyc.gov/site/nypd/stats/traffic-data/traffic-data-collision.page"
    response = requests.get(url)
    if response.status_code == 200:
        html_doc = response.content
        soup = BeautifulSoup(html_doc, 'html.parser')
        links = soup.find_all('a')
        named_links = [(link.get_text(), link.get('href'))for link in links if ".pdf" in link.get('href')]
        base_url = "https://www.nyc.gov/"
        named_links = [(name.strip("(PDF)"), base_url + relative_url) for name, relative_url in named_links]
        return named_links

    else:
        print("Error retrieving base page. Status code: {}".format(response.status_code))

def download_pdf(url, filename=None):
    assert url[-4:] == ".pdf", "Warning url does not appear to be a pdf file."
    if filename:
        pass
    else:
        filename = url.split("/")[-1]
        
    #Request PDF File
    response = requests.get(url)
    if response.status_code != 200:
        print("Response not successful. Status code: {}".format(response.status_code))
        return None
    if os.path.isfile(filename):
        overwrite = input("File: {} already exists. Do you wish to overwrite? (Y/N)".format(filename))
        if overwrite:
            print("Overwriting file. Saving to: {}".format(filename))
            with open(filename, 'wb') as f:
                f.write(response.content)
    else:
        with open(filename, 'wb') as f:
            f.write(response.content)

def run():
    named_links = get_pdf_links()
    for name, url in named_links:
        filename = "{base}{extension}".format(base=name, extension='.pdf')
        sys.stdout.write("\rDownloading: {}".format(filename))
        download_pdf(url, filename=filename)
        time.sleep(3)

if __name__ == '__main__':
    run()