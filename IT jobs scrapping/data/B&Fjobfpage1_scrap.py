import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook

headers = {
    'Accept-Language': 'en-US,en;q=0.5'
}

#base_url = ""
url = ("https://www.timesjobs.com/candidate/job-search.html?searchType=Home_Search&from=submit&asKey=OFF&txtKeywords=&cboPresFuncArea=42")

response = requests.get(url, headers=headers)
source = response.text


soup_data = BeautifulSoup(source, 'html.parser')
# second_soup_data = BeautifulSoup(second_page,'html.parser')

pg1_divs = soup_data.find_all('li', class_="clearfix job-bx wht-shd-bx")
# first_div_inner_page = second_soup_data.find('li',class_="clearfix job-bx wht-shd-bx")  

page_1 = []
# company_name = first_div_inner_page.find('h3',class_="joblist-comp-name").text.strip()

for job in pg1_divs:
    job_title = job.find('h2').text.strip() 
    # print(job_title)
    company_name = job.find('h3', class_="joblist-comp-name").text.strip().replace('More Jobs', '').strip()
    # print(company_name)
    # job_details = job.find('ul', class_="top-jd-dtl clearfix").find_all('li')
    # experience = job_details[0].text.strip().replace('\n', '').replace('  ', ' ').replace('card_travel', '').strip()
    # experience = ' '.join(experience.split()) 
    # location = job_details[2].text.strip().replace('location_on', '').strip()
    job_details = job.find('ul', class_="top-jd-dtl clearfix").find_all('li')

    experience = job_details[0].text.strip().replace('\n', '').replace('  ', ' ').replace('card_travel', '').strip()
    experience = ' '.join(experience.split()) 
    # print(experience)

    link_tag = job.find('a', href=True)
    MEjob_url = link_tag['href']

    BFjob_detail_response = requests.get(MEjob_url, headers=headers)
    BFjob_detail_soup = BeautifulSoup(BFjob_detail_response.text, 'lxml')
        # location_li = itjob_detail_soup.find('ul', class_='top-jd-dtl clearfix').find_all('li')
        # location = location_li.text.strip().split(":")[1].strip()  if location_li else 'N/A'
        # print(location)
    location_li = BFjob_detail_soup.find('ul', class_='top-jd-dtl clearfix').find_all('li')
    if len(location_li) > 2:
        location = location_li[2].text.strip().replace('location_on', '').strip()
    else:
        location = 'N/A'
        
    package_li = BFjob_detail_soup.find('ul', class_='top-jd-dtl clearfix').find_all('li')
    if len(package_li) > 1:
        package = package_li[1].text.strip().replace('\n', '').replace('  ', ' ').strip()
    else:
        package = 'N/A'
    # location = job_details[2].text.strip().replace('location_on', '').strip()
    # print(location)
    # package = job_details.find[2].text.strip()
    # package = job_details[1].text.strip().split(":")[1].strip() if len(job_details) > 2 and ":" in job_details[2].text else "As per Industry Standards"
    
    # job_description_list_items = job.find('ul', class_="list-job-dtl clearfix").find_all('li')
    # job_description = ' '.join([li.text.strip() for li in job_description_list_items])
    job_description = job.find('ul', class_="list-job-dtl clearfix").find('li').text.strip().replace('Job Description:', '').replace('More Details', '').strip()
    # print(job_description)
    key_skill = job.find('span', class_="srp-skills").text.strip() 
    job_data = {
        "Job Title": job_title,
        "Company Name": company_name,
        "Package":package,
        "Experience": experience,
         "Location": location,
        "Job Description": job_description,
        "Key Skill": key_skill,
    }
    
    page_1.append(job_data)

df = pd.DataFrame(page_1)
df.to_excel("B&FJobsPage1_scrap.xlsx", index=False)

print("Data has been written to B&FITJobsPage1.xlsx")
