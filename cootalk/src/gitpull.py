#! /usr/bin/python 

from gittle import Gittle
import os

class Ger_gitfile(object):




    def __init__(self,repo_path,repo_url):
        self.repo_path = repo_path
        self.repo_url = repo_url

    def clone(self):
        if not os.listdir(self.repo_path):
            repo = Gittle.clone(self.repo_url, self.repo_path)
