import requests                   
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook
import time
headers = {
    'Accept-Language': 'en-US,en;q=0.5'
}
time.sleep(5)

div_data = []
respond = requests.get("https://www.timesjobs.com/candidate/job-search.html?searchType=Home_Search&from=submit&asKey=OFF&txtKeywords=&cboPresFuncArea=35",headers=headers)
source  = respond.text

soup_data = BeautifulSoup(source,'html.parser')

second_page = requests.get("https://www.timesjobs.com/job-detail/software-engineer-required-in-abroad-exotic-expert-solutions-llp-netherlands-singapore-null-null-null-2-to-7-yrs-jobid-IfPAxwp4HL1zpSvf__PLUS__uAgZw==&source=srp").text
second_soup_data = BeautifulSoup(second_page,'html.parser')
first_div_inner_page = second_soup_data.find('div',class_="jd-header wht-shd-bx")  

first_div = soup_data.find('li',class_="clearfix job-bx wht-shd-bx")    

company_name = first_div_inner_page.find('h1',class_ = 'jd-job-title').text.strip()
# print(company_name)
job_title = first_div_inner_page.find('h2').text.strip()
# print(job_title)
details_list = first_div_inner_page.find('ul', class_='top-jd-dtl clearfix').find_all('li')
    
experience = details_list[0].text.strip().replace('\n', '').replace('  ', ' ').replace('card_travel', '').strip()
experience = ' '.join(experience.split()) 
package = details_list[1].text.strip().replace('\n', '').replace('  ', ' ')
# print(experience)
# print(package)
location = details_list[2].text.strip().replace('location_on', '').strip()
# print(location)

job_description_container = second_soup_data.find('div', class_='jd-desc job-description-main')
if job_description_container:
    job_description_list_items = job_description_container.find('ul').find_all('li')
    job_description = ' '.join([li.text.strip() for li in job_description_list_items])
# print(job_description)


key_skills_container = second_soup_data.find_all('span', class_='jd-skill-tag')
key_skills = ', '.join([skill.text.strip() for skill in key_skills_container])
# print(key_skills)



first_div_product = {
    'Job_title': job_title,
    'Company_name': company_name,
    'Experience': experience,
    'Package': package,
    'Location':location,
    'Job_Description': job_description,
    'Key_Skills': key_skills
      
}
div_data.append(first_div_product)
# print(div_data) 

df = pd.DataFrame(div_data)
df.to_excel("itjobfirst_div1.xlsx")