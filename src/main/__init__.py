#!/usr/bin/python
#-*- coding: utf-8 -*-
import tornado.httpserver
import tornado.web
import tornado.ioloop
import os
import sys
import yaml
import motor
from tornado.options import options, define

tornado.options.define("port", default=8888, help="Run server on a specific port", type=int)
tornado.options.define("host", default="localhost", help="Run server on a specific host")
tornado.options.define("url", default=None, help="Url to show in HTML")
tornado.options.define("config", default="./config.yaml", help="config file's full path")
tornado.options.parse_command_line()

if not tornado.options.options.url:
    tornado.options.options.url = "http://%s:%d" % (tornado.options.options.host, tornado.options.options.port)

setting = {
           "base_url": tornado.options.options.url,
           "config_filename": tornado.options.options.config,
           "session": {
                    "driver": "redis",
                    "driver_settings": {
                        "host": "localhost",
                        "port": 6379,
                        "db": 1
                    },
                    "force_persistence": False,
                    "cache_driver": True,
                    "cookie_config": {
                        "httponly": True
                    },
                },
           }


config = {}
try:
    with open(setting["config_filename"], "r") as fin:
        config = yaml.load(fin)
    for k, v in config["global"].items():
        setting[k] = v
    if "session" in config:
        setting["session"]["driver_settings"] = config["session"]
except:
    print("cannot found config.yaml file")
    sys.exit(0)
    

# mongodb connection
# format: mongodb://user:pass@host:port/
# database name: minos

try:
    client = motor.MotorClient(config["database"]["config"])
    database = client[config["database"]["db"]]
    setting["database"] = database
except:
    print("cannot connect mongodb, check the config.yaml") 
    sys.exit(0)
    
    
application = tornado.web.Application(
                                      [(r'/', 'handler.login.Login'),
                                       ]
                                      ,**setting)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
