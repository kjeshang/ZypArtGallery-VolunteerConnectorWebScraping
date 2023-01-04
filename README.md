# ZypArtGallery-VolunteerConnectorWebScraping

## Description

This project was created to assist Zyp Art Gallery to retrieve volunteer application data. The platform Zyp Art Gallery used to receive, accept, and reject volunteer application data is the Volunteer Connector Portal. As Volunteer Connector does not have either an API or a feature to download the application data as CSV files, I took on the task to construct a simple web scraper that will retrieve the volunteer application data. Retrieving the volunteer application data would help the Analytics team construct visualizations to assist deriving volunteer application insights such as volunteer interest per month, as well as all open and complete applcations on a lifetime basis.

This project was developed using the Python programming language and the Pandas, Selenium, Time, and Datetime libraries. The Python version used was 3.10.1. The IDE used to construct the Python scripts for this project was Microsoft Visual Studio Code. The Windows version of the Chrome Web Driver was used to facilitate the automated actions of the web scraper. To successfully create and run this project, it was imperative to have an organization-level account through Zyp Art Gallery on the Volunteer Connector portal, as well as the Google Chrome Web Browser.

## Important Note

Please note that the scraped Volunteer Connector data and the Volunteer Connector login credentials are not provided to protect the privacy of the Zyp Art Gallery organization, as well as that of the past & current volunteer applicants.

## How the Project Works

The Python scripts and other related files are within the **ZypVolunteerConnector** project directory. Below is a breakdown of the files in the project directory, as well as descriptions of what each file is used for.

|File|Description|
|--|--|
|**loginCredentials** Python script|This Python script contains the user's Volunteer Connector login credentials (i.e., username and password). This script is used as a module in the actual web scraping script.|
|**chromedriver** Windows Executable file|The web driver file that is required to facilitate the web scraping using the Google Chrome Browser, which is required by the Selenium Python package. Therefore, the web driver is imported into the actual web scraping script and is dependency to utilize the Selenium package to perform web scraping.|
|**scrape** Python script|This is the Python script that performs the web scraping.|
|**data** directory|The directory where the scraped data is saved which is in the form of CSV files.|

Below is a list of steps that conceptually explain how the Python script is able to scrape the data from the Volunteer Connector portal, clean & transform the data into dataframes, and load the dataframes as CSV files to deliver to the Analytics team.

1. Setup
    * Import the required packages and _loginCredentials_ module.
    * Specifiy the URLs of the Volunteer Connector portal.
    * Define function to convert month name to month number.
2. Instantiate Web Driver
    * Import the Chrome web driver.
    * Instantiate the web driver using Selenium, which starts an automated Chrome Browser Window.
    * Maximize the browser window.
3. Log into Volunteer Connector Portal
    * Log into Volunteer Connector Portal, using the username and password provided by the _loginCredentials_ module, to access the Zyp Art Gallery volunteer application dashboard.
4. Scrape Home Data
    * Specify the total number of time periods (i.e., months) to retrieve data from the Volunteer Connector dashboard, which shows the Monthly Report.
    * Retrieve the month name, year, and month number of all avaialble time periods that is filterable on the Volunteer Connector dashbord.
    * Using the above to filter the dashboard by month name & year, and retrieve the following monthly metrics:
        * Time Period (i.e., month & year)
        * Number of Views (Total posting views)
        * Number of Volunteers (People on your team)
        * Number of Applications (People applied)
        * Engagement Rate of Volunteer of Actual/Prospective Applicants
    * Save time period and the monthly metrics in a dataframe.
    * Export the **_Monthly Report Data_** dataframe as a CSV file.
5. Scrape Open Application Data
    * Go to the Applications section of the Volunteer Connector portal.
    * Count the total number of pages containing pending applications.
    * For each page containing pending applications that has the status of either "New Application" or "In-Review", retreive the following data for each application:
        * Name (i.e., the name of the volunteer applicant)
        * Posting (i.e., the volunteer position)
        * Status (i.e., application status; "New Application" or "In-Review")
        * When (i.e., the amount of time that has passed since the applicant submitted the application)
    * Save the scraped data mentioned above in a dataframe.
    * Export the **_Open Application Data_** dataframe as a CSV file.
6. Scrape Completed Application Data
    * Go to the Applications section of the Volunteer Connector portal.
    * Count the total number of pages containing completed applications.
    * For each page containing completed applications that has the status of either "Application Withdrawn", or "Application Declined", "Application Approved", retreive the following data for each application:
        * Name (i.e., the name of the volunteer applicant)
        * Posting (i.e., the volunteer position)
        * Status (i.e., application status; "Application Withdrawn", "Application Declined", "Application Approved")
        * When (i.e., the amount of time that has passed since the applicant submitted the application)
        * Approved By (i.e., the person who made a decision regarding the volunteer application given that that the applicant did not withdraw their application)
    * Save the scraped data mentioned above in a dataframe.
    * Export the **_Completed Application Data_** dataframe as a CSV file.
7. Close the Driver
    * Close the web driver, in turn, completing web scraping of the Volunteer Connector data.

## Credits
> i.e., The References Section

Despite completing this project independently, I referred to the following online resources to learn about creating a web scraper using the Selenium package and addressed any programming challenge I faced.

* Python Programming
    * [Remove all whitespace in a string](https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string) - _StackOverflow_
    * [Check if String Contains a Substring in Python](https://able.bio/rhett/check-if-string-contains-a-substring-in-python--03jrtz1#:~:text=The%20simplest%20way%20to%20check,%3A%20print('Word%20found.)) - Rhett Trickett (able.io)
    * [How to strip a specific word from a string?](https://stackoverflow.com/questions/23669024/how-to-strip-a-specific-word-from-a-string) - _StackOverflow_
    * [pandas.DataFrame.to_csv](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html) - _Pandas Documentation_
* Web Driver Dependency
    * [Downloads](https://chromedriver.chromium.org/downloads) - _Chrome Driver - Web Driver for Chrome_
    * [How to find which version of Google Chrome you're currently using, and update it if needed](https://www.businessinsider.com/guides/tech/what-version-of-google-chrome-do-i-have) - Devon Delfino (Business Insider)
* Python & Web Scraping
    * [How to scrape a website which requires login using python and beautifulsoup?](https://stackoverflow.com/questions/23102833/how-to-scrape-a-website-which-requires-login-using-python-and-beautifulsoup) - _StackOverflow_
    * [How to Automate Login using Selenium in Python](https://www.thepythoncode.com/article/automate-login-to-websites-using-selenium-in-python) - Redouane Niboucha & Abdou Rockikz (PythonCode)
    * [Automate Login System using Selenium WebDriver in Python 2019](https://medium.com/analytics-vidhya/automate-login-system-using-selenium-webdriver-in-python-2019-8844718b06e) - Rahul Bhatt (Medium)
    * [Selenium with Python Tutorial: Getting started with Test Automation](https://www.browserstack.com/guide/python-selenium-to-run-web-automation-test) - Shaumik Daityari & Pradeep Krishnakumar (BrowserStack)
    * [Finding elements by class name with Selenium in Python](https://stackoverflow.com/questions/30002313/finding-elements-by-class-name-with-selenium-in-python) - _StackOverflow_
    * [AttributeError: 'WebDriver' object has no attribute 'find_element_by_xpath'](https://stackoverflow.com/questions/72754651/attributeerror-webdriver-object-has-no-attribute-find-element-by-xpath) - _StackOverflow_
    * [How to click button Selenium Python?](https://www.tutorialspoint.com/how-to-click-button-selenium-python#:~:text=We%20can%20click%20a%20button,is%20represented%20by%20button%20tagname.) - Debomita Bhattacharjee (TutorialsPoint)
    * [Selenium - get all child elements from div class](https://stackoverflow.com/questions/73223578/selenium-get-all-child-elements-from-div-class/73224247) - _StackOverflow_
    * [Python Selenium create loop to click through links on a page and press button on each new page](https://stackoverflow.com/questions/31361432/python-selenium-create-loop-to-click-through-links-on-a-page-and-press-button-on) - _StackOverflow_
    * [How to do loop with click() in selenium?](https://stackoverflow.com/questions/58717379/how-to-do-loop-with-click-in-selenium) - _StackOverflow_
    * [Web Scraping using Python and Selenium(XPATH)](https://medium.com/analytics-vidhya/web-scraping-using-python-and-selenium-xpath-f315f63ac229) - Shubham Pandey (Medium)
    * [How can I parse a website using Selenium and Beautifulsoup in python? [closed]](https://stackoverflow.com/questions/13960326/how-can-i-parse-a-website-using-selenium-and-beautifulsoup-in-python) - _StackOverflow_
    * [Pagination using Selenium Python](https://www.numpyninja.com/post/pagination-using-selenium-python) - rgupta190508 (Numpy Ninja)
    * [How to Maximize window in chrome using webDriver (python)](https://stackoverflow.com/questions/12211781/how-to-maximize-window-in-chrome-using-webdriver-python) - _StackOverflow_