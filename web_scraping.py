from selenium import webdriver
from bs4 import BeautifulSoup
import time, csv, requests

START_URL = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("../../../Downloads/chromedriver")
browser.get(START_URL)

time.sleep(10)

headers = ["Name", "Light_years_from_earth", "Planet_mass", "Stellar_magnitude", "Discovery_date", "hyperlink", "Planet_type", "Planet_Radius", "Orbital_Radius", "Orbital_Period", "Eccentricity"]
planet_data = []
new_planet_data = []
final_planet_data = []

def scrap():
    for i in range(0, 428):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for ul_tag in soup.find_all("ul", attrs = {"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            #store data in row
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tag = li_tag[0]
            temp_list.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    # with open("scraper_2.csv", "w") as f:
    #     csvwriter = csv.writer(f)
    #     csvwriter.writerow(headers)
    #     csvwriter.writerows(planet_data)

def scrap_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_planet_data.append(temp_list)
    except:
        time.sleep(1)
        scrap_more_data(hyperlink)

scrap()

for data in planet_data:
    scrap_more_data(data[5])

for index, data in enumerate(planet_data):
    final_planet_data.append(data + final_planet_data[index])
    print(f"{index+1} page done to")

for index, data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [elem.replace("\n", "")for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data+new_planet_data_element)

with open("scraper_3.csv", "w")as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)


