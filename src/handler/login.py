#!/usr/bin/python
#-*- coding: utf-8 -*-
import tornado.web


class Login(tornado.web.RequestHandler):
    def get(self):
        self.write("chunk")