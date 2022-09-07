# Setup ---------------------------------------------------------------
from loginCredentials import login
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime

website = 'https://www.volunteerconnector.org/organizations/';
login_url = website + 'login';
passowrd_url = website + 'auth/password?next='
organization_dashboard = website + '2927/dashboard/';
organization_applications = website + '2927/applications/';

def getMonthNumber(month_name):
    month_num = datetime.strptime(month_name, '%B').month
    if month_num < 10:
        return str(0)+str(month_num);
    else:
        return str(month_num);

# Instantiate Web Driver -----------------------------------------------
driver = webdriver.Chrome("chromedriver");

driver.set_window_size(1024, 600);
driver.maximize_window();

# Log into Volunteer Connector -----------------------------------------
time.sleep(3);
driver.get(login_url);
print(driver.current_url);
driver.find_element("id","email").send_keys(login['username']);
driver.find_element("name","submit").click();

time.sleep(3);
print(driver.current_url);
driver.find_element("id","password").send_keys(login['password']);
password_xpath = '//*[@id="content"]/section[2]/div/article/form/div[2]/button';
driver.find_element("xpath", password_xpath).click();

time.sleep(3);
print(driver.current_url);

# Scrape Home Data -----------------------------------------------------

numMonths = 34; # MANUALLY EDIT THIS PARAMETER

def getHomeData(numMonths):
    timePeriod_raw = [];
    for month in driver.find_elements("xpath",'//*[@id="id_month"]'):
        # print(month.text);
        timePeriod_raw.append(month.text);

    numMonths = len(timePeriod_raw[0].split("\n"));

    timePeriod = [];
    count = 0;
    for month in timePeriod_raw[0].split("\n"):
        if count >= numMonths:
            break;
        else:
            perMonthData = {
                'option':count,
                'time_period':month.strip(),
                'year':month.strip().split(" ")[1],
                'month_number':getMonthNumber(month.strip().split(" ")[0]),
                'xpath':'//*[@id="id_month"]/option['+str(count)+']'
            };
            timePeriod.append(perMonthData);
            count += 1;
    time_df = pd.DataFrame(timePeriod);

    monthlyReportMetric = [
        # Monthly Report - Views (Total posting views)
        {
            'metric':'Views',
            'xpath':'//*[@id="content"]/div/div/div[2]/section/div[5]/div[1]/div/span[2]'
        },
        # Monthly Report - Volunteers (People on your team)
        {
            'metric':'Volunteers',
            'xpath':'//*[@id="content"]/div/div/div[2]/section/div[5]/div[2]/div/span[2]'
        },
        # Monthly Report - Applications (People applied)
        {
            'metric':'Applications',
            'xpath':'//*[@id="content"]/div/div/div[2]/section/div[5]/div[3]/div/span[2]'
        },
        # What's happening this week - Engagement of your volunteers have an upcoming oppurtunity
        {
            'metric':'Engagment',
            'xpath':'//*[@id="content"]/div/div/div[2]/section/div[3]/div[2]/div/div/div[1]/div/div/span'
        }
    ];

    data = [];
    for i in time_df.index:
        row = [];
        time.sleep(10);
        driver.get(organization_dashboard + "?month=" + str(time_df.loc[i, 'year']) + "-" + str(time_df.loc[i, 'month_number']));
        print(driver.current_url);
        row.append(time_df.loc[i, 'time_period']);
        for elem in monthlyReportMetric:
            row.append(driver.find_element("xpath", elem.get('xpath')).text);
        print(row);
        data.append(row);

    labels = ['Time Period'];
    for elem in monthlyReportMetric:
        labels.append(elem.get('metric'));

    home_df = pd.DataFrame(data, columns=labels);
    return home_df;

home_df = getHomeData(numMonths);
home_df.to_csv("data/ZypVolunteerConnector_MonthlyReportData.csv", index=False);
print("Volunteer Connector Monthly Report Data Extraction Complete!");

# Scrape Open Application Data --------------------------------------------
time.sleep(3);
driver.get(organization_applications);    

def getOpenApplicationData():
    pages = [];
    for page in driver.find_elements("xpath",'//*[@id="content"]/div/div/div[2]/article/nav/ul'):
        pages.append(page.text);
    totalPages = int(pages[0].split("\n")[len(pages[0].split("\n"))-1]);

    labels = ["Name","Posting","Status","When"];
    openApplicationStatus = ["New Application","In Review"];

    data = [];
    for i in range(totalPages):
        time.sleep(10);
        driver.get(organization_applications + 'page-' + str(i+1));
        print(driver.current_url);

        rawApplicationData = [];
        for info in driver.find_element("xpath",'//*[@id="content"]/div/div/div[2]/article/section[2]').text.split("\n"):
            rawApplicationData.append(info)

        numApplications = 0;
        for elem in rawApplicationData:
            countStatus = False;
            for status in openApplicationStatus:
                if status in elem:
                    countStatus = True;
                    numApplications += 1;
                    break;
        print(numApplications);
        
        for j in range(numApplications):
            row = [];
            applicantData = driver.find_element("xpath",'//*[@id="content"]/div/div/div[2]/article/section[2]/div['+str(j+2)+']').text.split("\n");
            for k in range(len(applicantData)):
                row.append(applicantData[k]);
            print(row)
            data.append(row);

    openApp_df = pd.DataFrame(data, columns=labels);

    return openApp_df;

openApp_df = getOpenApplicationData();
openApp_df.to_csv("data/ZypVolunteerConnector_OpenApplicationData.csv", index=False);
print("Volunteer Connector Open Application Data Extraction Complete!");

# Scrape Completed Application Data ---------------------------------------
time.sleep(3);
driver.get(organization_applications);  

time.sleep(3);
driver.find_element("xpath",'//*[@id="content"]/div/div/div[2]/article/form/section/div[1]/div/div/label[4]').click();

organization_applications_completed_ending = str(driver.current_url).split("?")[1];

def getCompletedApplicationData():
    pages = [];
    for page in driver.find_elements("xpath",'//*[@id="content"]/div/div/div[2]/article/nav/ul'):
        pages.append(page.text);
    totalPages = int(pages[0].split("\n")[len(pages[0].split("\n"))-1]);

    labels = ["Name","Posting","Status","When","Approved By"];
    completedApplicationStatus = ["Application Withdrawn","Application Declined","Application Approved"];

    data = [];
    for i in range(totalPages):
        time.sleep(10);
        driver.get(organization_applications + 'page-' + str(i+1) + '?' + organization_applications_completed_ending);
        print(driver.current_url);

        rawApplicationData = [];
        for info in driver.find_element("xpath",'//*[@id="content"]/div/div/div[2]/article/section[2]').text.split("\n"):
            rawApplicationData.append(info)

        numApplications = 0;
        for elem in rawApplicationData:
            countStatus = False;
            for status in completedApplicationStatus:
                if status in elem:
                    countStatus = True;
                    numApplications += 1;
                    break;
        print(numApplications);
        
        for j in range(numApplications):
            row = [];
            applicantData = driver.find_element("xpath",'//*[@id="content"]/div/div/div[2]/article/section[2]/div['+str(j+2)+']').text.split("\n");
            for k in range(len(applicantData)):
                row.append(applicantData[k]);
            if len(applicantData) == 4:
                row.append("");
            print(row);
            data.append(row);
        
        completedApp_df = pd.DataFrame(data, columns=labels);

    return completedApp_df;

completedApp_df = getCompletedApplicationData();
completedApp_df.to_csv("data/ZypVolunteerConnector_CompletedApplicationData.csv", index=False);
print("Volunteer Connector Completed Application Data Extraction Complete!");

# Close Driver ------------------------------------------------------------
driver.close()