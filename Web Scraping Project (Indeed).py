#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
from random import randint
from time import sleep


# In[ ]:


job_title = []
company_name = []
salary = []
frequency = []
page_numbers = ['https://uk.indeed.com/jobs?q=project+manager&l=United+Kingdom&fromage=10&start=10']
location = []


# In[ ]:


# Where all data is taken from accompanying tags
def results_card(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find(class_="jobsearch-ResultsList css-0")

    #find job title using span and only if parent is an <a> tag
    title = div.find_all("span")
    for job in title:
        parent = job.parent
        if parent.name == "a" and job.string != None:
            job_title.append(job.string)

        company = div.find_all(class_="companyName")
        for comp in company:
            company_name.append(comp.string)

        items = soup.find_all("td", class_="resultContent")
        for item in items:
            salary_string(item)

        company_locations = div.find_all(class_="companyLocation")
        for loc in company_locations:
            location.append(loc.string)
        


def salary_string(item):
    item = str(item.text)
    if "£" not in item:
        salary.append(0)
    else:
        item = item.split("£")
        item = item[1:]
        if item[-1] > item[0]:
            item = item[0] + item[1]
            salary_split(item)
        else:
            item = item[0]
            salary_split(item)
        

def salary_split(item):
    item = item.split("a", 1)
    item = str(item)
    item = item.split("-")
    item = item[-1]
    item = item.replace(" ", "")
    item = item.replace(",", "")
    salary.append(item)


# In[ ]:


i = 0
while i < 5:
    url = page_numbers[i]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    pagination = soup.find(class_="mosaic-zone")
    
    a_tag = pagination.find_all("li")
    for href in a_tag:
        href = href.get('href')
        href = "https://uk.indeed.com" + href
        if href not in page_numbers:
            page_numbers.append(href)


    results_card(url)

    sleep(randint(3,5))

    i +=1
    sleep(1)
    
    

 


# In[ ]:


df = pd.DataFrame(list(zip(job_title, company_name, salary, frequency, location)),
               columns =['Title', 'Company Name', 'JD Salary', 'Frequency','Location'])


# In[ ]:





# In[ ]:


writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer)
writer.save()

