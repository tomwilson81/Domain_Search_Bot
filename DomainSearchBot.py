from dataclasses import dataclass, replace
from re import search
import time
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service as ChromeService
import pandas as pd
import re
import numpy as np


@dataclass
class Task:
    name: str
    link: str

class DomainSearcher():
    def __init__(self) -> None:
        self.base_url = "https://www.google.co.uk"
        self.SEARCH_TEXT = "site:"
        self.COMMAND_OR_CONTROL = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        
    
    def get_domains(self):
        df = pd.read_csv('domain_search_input.csv')
        #print(df)
        websites = df['Website'].values.tolist()
        #print(websites)

        # search parameter for Google engine
        self.search_list = []
        for site in websites:
            self.search_name = self.SEARCH_TEXT + site
            self.search_list.append(self.search_name)
        #print(self.search_list)
        return self.search_list


    def get_google_result(self):
        self.get_domains()
        goog_search_name = self.search_list
        #print("Google search: " + str(goog_search_name) + '\n')
        self.driver.get(self.base_url)
        time.sleep(2)
        self.driver.find_element(By.ID, "L2AGLb").click()
        #self.driver.find_element(By.CLASS_NAME, "QS5gu sy4vM")
        time.sleep(3)

        self.current_google_result = []

        for item in goog_search_name: 
            searchbox = self.driver.find_element(By.NAME, "q")
            searchbox.click()
            searchbox.send_keys(Keys.COMMAND + "a")
            time.sleep(1)
            searchbox.send_keys(Keys.DELETE)
            searchbox.send_keys(item)
            time.sleep(1)
            searchbox.submit()
            time.sleep(2)
        
            google_result = self.driver.find_element(By.ID, "result-stats").text
            #print(google_result)
            
            updated_google_result = re.sub(",","", google_result)
            new_result = re.findall('[0-9]+', updated_google_result)
            #print(new_result)

            self.current_google_result.append(new_result[0])
        print(len(self.current_google_result))
        return self.current_google_result
        
        

    def update_csv_file(self):
        input_data = self.current_google_result
        print(input_data)

        # making data frame from the csv file 
        df = pd.read_csv('domain_search_input.csv')
        
        df['Size of Website (pages)'] = np.array(input_data)
        
        # writing  the dataframe to another csv file
        df.to_csv('domain_search_input_updated.csv', 
                        index = False)
                    
        print("Code Complete!!")
    
    
    def try_code(self):
        self.get_domains()
        self.get_google_result()
        self.update_csv_file()
        self.driver.quit()


if __name__ == '__main__':
    bot = DomainSearcher()
    bot.try_code()

