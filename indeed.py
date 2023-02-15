from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

url = 'https://www.indeed.com/'
driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()

time.sleep(2)

box = driver.find_element(By.XPATH, '//*[@id="text-input-what"]')
box.send_keys('data analyst')

time.sleep(1)

# For Remote Roles, otherwise it automatically searches by your current location.
location = driver.find_element(By.XPATH, '//*[@id="text-input-where"]')

for x in range(1,25):
    location.send_keys(Keys.BACK_SPACE)

location.send_keys('remote')

time.sleep(2)

driver.find_element(By.XPATH, '//*[@id="jobsearch"]/button').click()

df = pd.DataFrame({'Link': [''], 'Job Title': [''], 'Company':[''], 'Location':[''], 'Salary':[''], 'Date':['']})

while True:

    soup = BeautifulSoup(driver.page_source, 'lxml')

    postings = soup.find_all('div', class_= 'slider_container css-g7s71f eu4oa1w0')

    for post in postings:
        link = post.find('a', class_= 'jcs-JobTitle css-jspxzf eu4oa1w0').get('href')
        full_link = 'https://www.indeed.com' + link

        title = post.find('h2', class_='jobTitle').text

        try:
            company = post.find('span', class_= 'companyName').text
        except:
            company = 'n/a'

        date = post.find('span', class_= 'date').text
        if date == 'PostedToday':
            date = 'Today'
        if 'PostedPosted' in  date:
            date = date.replace('PostedPosted', '')
        if 'EmployerActive' in date:
            date = date.replace('EmployerActive', '')
        if date == 'PostedJust posted':
            date = 'Today'

        location = post.find('div', class_= 'companyLocation').text
        if '+' in location:
            location = location.split('+', 1)[0]

        try:
            salary = post.find('div', class_= 'metadata salary-snippet-container').text
        except:
            salary = 'n/a'

        df = df.append({'Link':full_link, 'Job Title':title, 'Company':company, 'Location':location, 'Salary':salary, 'Date':date},
                        ignore_index = True)

    try:
        button = soup.find('a', {'aria-label': 'Next Page'}).get('href')
        driver.get('https://www.indeed.com'+button)
        time.sleep(2)
    except:
        break


df = df.drop_duplicates()

df=df.drop(df.index[0])

df.to_csv(r'C:\Users\anais\Documents\Projects\IndeedScraper\da_jobs.csv', index=False)