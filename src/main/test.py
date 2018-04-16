#!/usr/bin/python
#-*- coding: utf-8 -*-
import yaml
impoort
config = {}
setting = dict()
try:
    with open("config.yaml", "r") as fin:
        config = yaml.load(fin)
    for k, v in config["database"].items():
        setting[k] = v
except:
    print("cannot found config.yaml file")
    sys.exit(0)

print(config,setting)