"""
Author:AMJADHKHAN CA
Date: 13/12/2019
Purpose:Program for Scraping Instagram profile details and last posted post details
Modules used: datetime,json,requests,bs4,sys
"""
import requests
import json
import sys
from datetime import datetime
from bs4 import BeautifulSoup
from random import choice

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

USER_AGENTS = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']
class InstagramScraper:
    def __init__(self, url, user_agents=None):
        self.url = url
        self.user_agents = user_agents

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(USER_AGENTS)

    def __request_url(self):
        try:
            response = requests.get(
                        self.url,
                        headers={'User-Agent': self.__random_agent()})
            response.raise_for_status()
        except requests.HTTPError:
            raise requests.HTTPError('Received non-200 status code.')
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response.text
    @staticmethod
    def extract_json(html):
        global soup
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')      
        return json.loads(raw_string)
        
    
    def page_metrics(self):
        results = {}
        try:
            response = self.__request_url()
            json_data = self.extract_json(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        except Exception as e:
            raise e
        else:
            for key, value in metrics.items():
                if key == 'biography':
                    results[key]=value
                if key == 'full_name':
                    results[key]=value
                if key != 'edge_owner_to_timeline_media':
                    if value and isinstance(value, dict):
                        value = value['count']
                        # print(value)
                        results[key] = value
        data = soup.find_all('meta', attrs={'property': 'og:description'
                             })
        text = data[0].get('content').split()
        user = '%s %s %s' % (text[-3], text[-2], text[-1])
        results["user"]=user

        return results
    def post_metrics(self):
        results = []
        try:
            response = self.__request_url()
            json_data = self.extract_json(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node,dict):
                    results.append(node)
        return results
    def get_images(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(self.url)
        time.sleep(1)
        log_btn=browser.find_element_by_xpath("//a[contains(text(),'Log In')]")
        log_btn.click()
        time.sleep(1)
        fb_login=browser.find_element_by_xpath("//span[contains(text(),'Log in with Facebook')]")
        fb_login.click()
        time.sleep(2)
        username = browser.find_element_by_name("email")
        username.send_keys('amjadhkhan.ga3@iiitmk.ac.in')
        time.sleep(0.5)
        password = browser.find_element_by_name('pass')
        password.send_keys('Apple@12345')
        time.sleep(0.5)
        sign_in_button = browser.find_element_by_xpath("//button[contains(@id, 'loginbutton')]")
        sign_in_button.click()
        time.sleep(4)
        browser.get(self.url)
        elem = browser.find_element_by_tag_name("body")

        no_of_pagedowns = 30
        while no_of_pagedowns:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            no_of_pagedowns-=1
            post_elems = browser.find_elements_by_class_name("FFVAD")
        print("------------POSTD IMAGES ------------------")
        for post in post_elems:
            img_link=post.get_attribute("srcset")
            img_link=img_link[:-4]
            print(img_link)
        browser.quit()

account = input("Enter the profile Name You want to scrap :")
url = "https://www.instagram.com/"+account+"/?hl=en"

# // Initiate a scraper object and call one of the methods.
instagram = InstagramScraper(url)
post_metrics = instagram.post_metrics()
page_metrics = instagram.page_metrics()

for m in post_metrics:
    i_id = str(m['id'])
    i_post_time = datetime.fromtimestamp(m['taken_at_timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    i_likes = int(m['edge_liked_by']['count'])
    i_comments = int(m['edge_media_to_comment']['count'])
    i_media = m['display_url']
    i_video = bool(m['is_video'])
print("-------------------USER DETAILS------------------------")
print("User :",page_metrics['user'])
print("Followers:",page_metrics['edge_followed_by'])
print("Following :",page_metrics['edge_follow'])
print("Biography :",page_metrics['biography'])


print("----------------------LAST POST DETAILS-----------------")
print("POST ID:",i_id)
print("POST DATE AND TIME:",i_post_time)
print("LIKES:",i_likes)
print("COMMENTS:",i_comments)
print("MEDIA URL:",i_media)
print("IS THAT A VIDEO:",i_video)

images = instagram.get_images()








