#!/usr/bin/python
#-*- coding: utf-8 -*-
import tornado.httpserver
import tornado.web
import tornado.ioloop
import os
import sys
import yaml
import motor
import pymysql
from tornado.options import options, define

tornado.options.define("port", default=8888, help="Run server on a specific port", type=int)
tornado.options.define("host", default="localhost", help="Run server on a specific host")
tornado.options.define("url", default=None, help="Url to show in HTML")
tornado.options.define("config", default="./config.yaml", help="config file's full path")
tornado.options.parse_command_line()

BASE_ID = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_ID)

if not tornado.options.options.url:
    tornado.options.options.url = "http://%s:%d" % (tornado.options.options.host, tornado.options.options.port)

setting = {
           "base_url": tornado.options.options.url,
           "template_path": "template",
           "static_path": "static",
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

# config file
config = {}
try:
    with open(setting["config_filename"], "r") as fin:
        config = yaml.load(fin)
    for k, v in config["database"].items():
        setting[k] = v
    if "session" in config:
        setting["session"]["driver_settings"] = config["session"]
except:
    print("cannot found config.yaml file")
    sys.exit(0)

    
try:
    client = pymysql.connect(setting["config"],setting["user"],setting["password"],setting["db"])
    database = client.cursor()
    setting["database"] = database
except:
    print("cannot connect mysql, check the config.yaml")
    sys.exit(0)  
     
application = tornado.web.Application(
                                      [(r'/', 'handler.login.Login'),
                                       (r'/log', 'handler.login.LoginHandler')
                                       ]
                                      ,**setting)

if __name__ == "__main__":
    try:
        application.listen(tornado.options.options.port)
        tornado.ioloop.IOLoop.instance().start()
    except:
        import traceback
        print(traceback.print_exc())
    finally:
        sys.exit(0)
    
