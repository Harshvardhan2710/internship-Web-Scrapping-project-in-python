import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook


headers = {
    'Accept-Language': 'en-US,en;q=0.5'
}
base_url ="https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&postWeek=60&searchType=Home_Search&cboPresFuncArea=28&sequence="
url_lst = [base_url + str(i) + "&startPage=1" for i in range(1,361)]
all_lst = []
for val in url_lst:
    response = requests.get(val).text
    converted_data = BeautifulSoup(response, 'lxml')
    all_page_div = converted_data.find_all('li', class_="clearfix job-bx wht-shd-bx")
    for item in all_page_div:
        job_title = item.find('h2').text.strip() 
        company_name = item.find('h3', class_="joblist-comp-name").text.strip()
        
        job_details = item.find('ul', class_="top-jd-dtl clearfix").find_all('li')
        experience = job_details[0].text.strip().replace('\n', '').replace('  ', ' ').replace('card_travel', '').strip() 
        experience = ' '.join(experience.split())

        link_tag = item.find('a', href=True)
        MEjob_url = link_tag['href']

        MEjob_detail_response = requests.get(MEjob_url, headers=headers)
        MEjob_detail_soup = BeautifulSoup(MEjob_detail_response.text, 'lxml')
        # location_li = itjob_detail_soup.find('ul', class_='top-jd-dtl clearfix').find_all('li')
        # location = location_li.text.strip().split(":")[1].strip()  if location_li else 'N/A'
        # print(location)
        location_li = MEjob_detail_soup.find('ul', class_='top-jd-dtl clearfix').find_all('li')
        if len(location_li) > 2:
            location = location_li[2].text.strip().replace('location_on', '').strip()
        else:
            location = 'N/A'
        
        package_li = MEjob_detail_soup.find('ul', class_='top-jd-dtl clearfix').find_all('li')
        if len(package_li) > 1:
            package = package_li[1].text.strip().replace('\n', '').replace('  ', ' ').strip()
        else:
            package = 'N/A'
        # location = job_details[1].text.strip().split(":")[1].strip() if len(job_details) > 1 and ":" in job_details[1].text else "N/A"
        # package = job_details[2].text.strip().split(":")[1].strip() if len(job_details) > 2 and ":" in job_details[2].text else "As per Industry Standards"

        # job_description = item.find('ul', class_="list-job-dtl clearfix").find('li').text.strip().replace('Job Description:', '').replace('More Details', '').strip() 
        job_description_div = MEjob_detail_soup.find('div', class_='jd-desc job-description-main')
        if len(job_description_div) > 1:
            job_description = job_description_div.text.strip().replace('Job Description:', '')
        else:
            job_description = 'N/A'
        
        key_skill = item.find('span', class_="srp-skills").text.strip()

        job_data = {
            "Job Title": job_title,
            "Company Name": company_name,
            "Experience": experience,
            "Package": package,
            "Location": location,
            "Job Description": job_description,
            "Key Skill": key_skill,
        }
        
        all_lst.append(job_data)

pg1_df = pd.DataFrame(all_lst)  
pg1_df.to_excel("M&EJobswebsite_scrap.xlsx", index=False)

print("Data has been written to M&EJobswebsite_scrap.xlsx")