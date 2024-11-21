import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging


logging.basicConfig(level=logging.INFO)


class LLMAgent:
    def __init__(self):
        self.tasks = []
        

    def add_task(self, task_type, task_data):
        task = {"type": task_type, "data": task_data}
        self.tasks.append(task)
        logging.info(f"Task added: {task_type}")
        

    def process_tasks(self):
        for task in self.tasks:
            if task['type'] == "scrape_homicide":
                self.scrape_homicide_statistics(task['data'])
            elif task['type'] == "other_non_crime_task":
                self.handle_non_crime_task(task['data'])
            else:
                logging.warning(f"Unknown task type: {task['type']}")
    
  
    def scrape_homicide_statistics(self, city_urls):
        homicide_data = []
        for city, url in city_urls.items():
            logging.info(f"Scraping data for {city}...")
            data = self.scrape_homicide_data(url)
            if data:
                homicide_data.extend(data)
        
        
        self.display_data(homicide_data)
    

    def scrape_homicide_data(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        homicide_data = []
        
       
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                cols = row.find_all('td')
                if len(cols) > 1:
                    year = cols[0].text.strip()
                    homicides = cols[1].text.strip()
                    homicide_data.append({'Year': year, 'Homicides': homicides, 'City': url.split('/')[-1]})
        
        return homicide_data
    
 
    def display_data(self, homicide_data):
        if homicide_data:
            df = pd.DataFrame(homicide_data)
            st.write("Homicide Statistics Table:")
            st.write(df)
        else:
            logging.warning("No homicide data found.")
    
   
    def handle_non_crime_task(self, task_data):
        logging.info(f"Processing non-crime task: {task_data}")


import streamlit as st

def main():
   
    agent = LLMAgent()
    
    st.title("LLM Agent for Homicide Statistics and Other Tasks")
    
  
    st.write("Please provide the URLs for homicide statistics of New York, New Orleans, and Los Angeles:")
    url_ny = st.text_input("New York URL", "")
    url_no = st.text_input("New Orleans URL", "")
    url_la = st.text_input("Los Angeles URL", "")
    
  
    if st.button("Extract Homicide Data"):
        if url_ny and url_no and url_la:
            city_urls = {
                'New York': url_ny,
                'New Orleans': url_no,
                'Los Angeles': url_la
            }
            
         
            agent.add_task('scrape_homicide', city_urls)
            
           
            agent.process_tasks()
        else:
            st.error("Please provide URLs for all three cities.")

if _name_ == '_main_':
    main()