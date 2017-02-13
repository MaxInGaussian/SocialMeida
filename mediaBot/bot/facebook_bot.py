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
        br_id = self._get_any_idle_br_id()
        shared_posts_class = "userContent"
        time_xpath = "div[3]/div[1]/div/div/div[2]/div/div/div[2]/div/span[3]/span/a/abbr"
        self._new_command(br_id, (self.GOTO, self.SHARE_URL+"%d"%(int(post_id))))
        last_loaded_posts = 0
        while(True):
            self.br_dict[br_id].execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            found, shared_posts = self._new_command(br_id, (self.CLASS, shared_posts_class))
            print('loaded', len(shared_posts), 'posts...')
            if(len(shared_posts) == last_loaded_posts):
                break
            last_loaded_posts = len(shared_posts)
        if(not found):
            print("shared post not found!")
        else:
            print("found", len(shared_posts),"shared posts!")
        self._idle_br(br_id)