import os, re, sys, time
import datetime as dt
import pandas as pd
import numpy as np
from .bot import Bot
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

class FacebookBot(Bot):
    
    LOGIN_URL = 'https://www.facebook.com/'
    SHARE_URL = "https://www.facebook.com/shares/view?id="
    
    def __init__(self, browser="phantomjs", verbose=True):
        super(FacebookBot, self).__init__(browser, verbose=verbose)
        self.clr_str = lambda str: re.sub(re.compile('\W'), '', str)
    
    def login(self, usr, pwd):
        br_id = self._get_any_idle_br_id()
        self._new_command(br_id, (self.GOTO, self.LOGIN_URL))
        logged_in = not self._new_command(br_id, (self.ID, "login_form"))[0]
        if(logged_in):
            self.br_dict[br_id].save_screenshot('login_status.png')
            self._idle_br(br_id)
            return
        elem = self._new_command(br_id, (self.ID, "email"))[1][0]
        elem.send_keys(usr)
        elem = self._new_command(br_id, (self.ID, "pass"))[1][0]
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        facebookLogo = "/html/body/div/div[1]/div/div/div/div[1]/div/h1/a"
        self.br_dict[br_id].save_screenshot('login_status.png')
        self._idle_br(br_id)

    def fetch_shared_posts_by_post_id(self, post_id):
        shared_posts_header = ['share_time', 'user_name', 'user_link',
            'post_content', 'post_link', 'num_likes']
        shared_posts_dict = {attr:{} for attr in shared_posts_header}
        br_id = self._get_any_idle_br_id()
        shared_posts_class = "fbUserContent"
        user_name_class = "fwb"
        post_link_xpath = "div[1]/div[3]/div[1]/div/div/div[2]/div/div/div[2]/div/span[3]/span/a"
        share_tme_xpath = "div[1]/div[3]/div[1]/div/div/div[2]/div/div/div[2]/div/span[3]/span/a/abbr"
        post_content_xpath = "div[1]/div[3]/div[2]"
        num_likes_class = "_4arz"
        self._new_command(br_id, (self.GOTO, self.SHARE_URL+"%d"%(int(post_id))))
        all_shared_posts = []
        last_loaded_posts = 0
        while(True):
            self.br_dict[br_id].execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            found, shared_posts = self._new_command(br_id, (self.CLASS, shared_posts_class))
            print('loaded', len(shared_posts), 'posts...')
            all_shared_posts = shared_posts
            if(len(shared_posts) == last_loaded_posts):
                break
            last_loaded_posts = len(shared_posts)
        self._idle_br(br_id)
        if(len(all_shared_posts) == 0):
            print("shared post not found!")
            return None
        ind = 0
        for shared_post in all_shared_posts:
            share_time = post.find_element_by_xpath(share_tme_xpath)
            shared_posts_dict['share_time'][ind] = share_time.text
            user_name = post.find_element_by_class_name(user_name_class)
            shared_posts_dict['user_name'][ind] = user_name.text
            user_link = user_name.find_element_by_tag_name("a")
            shared_posts_dict['user_link'][ind] = user_link.get_attribute('href')
            post_content = post.find_element_by_xpath(post_content_xpath)
            shared_posts_dict['post_content'][ind] = post_content.text
            post_link = post.find_element_by_xpath(post_link_xpath)
            shared_posts_dict['post_link'][ind] = post_link.get_attribute('href')
            num_likes = post.find_element_by_xpath(num_likes_class)
            shared_posts_dict['num_likes'][ind] = num_likes.text
            ind += 1
        return pd.DataFrame(shared_posts_dict)