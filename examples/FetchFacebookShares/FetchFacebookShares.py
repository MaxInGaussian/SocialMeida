"""
Data Bot for Social Media
Github: https://github.com/MaxInGaussian/mediaBot
Author: Max W. Y. Lam [maxingaussian@gmail.com]
"""

import os, sys
import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt

try:
    from mediaBot import FacebookBot
except:
    print("Trying to call directly from source...")
    from sys import path
    path.append("../../")
    from mediaBot import FacebookBot
    print("done.")

fb_bot = FacebookBot()
fb_bot.login("ericwowo2003@gmail.com", "3002owowcire")
fb_bot.fetch_shared_posts_by_post_id(10154223184020772)