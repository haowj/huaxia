#!/usr/bin/python
#-*- coding: utf-8 -*-


class BaseHandler(object):
    def initialize(self):
        self.db = self.settings.get("database")
        self.backend = self.settings.get("thread_pool")
        self.flash = self.flash(self)
        self.topbar = "home"
        
    def flash(self):
        pass
    