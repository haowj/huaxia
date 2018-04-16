#!/usr/bin/python
#-*- coding: utf-8 -*-
import tornado.web
from handler.base import BaseHandler
from common.function import not_need_login, hash
from tornado import gen
class Login(BaseHandler):
    def initialize(self):
        BaseHandler.initialize(self)
    def get(self):
        print(self.db.execute("SELECT VERSION()"))
        self.write("chunk")
      
class LoginHandler(BaseHandler):
	def initialize(self):
		BaseHandler.initialize(self)
		self.topbar = 'login'

	@not_need_login
	def prepare(self):
		BaseHandler.prepare(self)

	def get(self):
		self.render("login.htm")

	@tornado.web.asynchronous
	@gen.coroutine
	def post(self):
		try:
			username = self.get_body_argument('username', default="")
			password = self.get_body_argument('password', default="")
			remember = self.get_body_argument('remember', default = "off")
			
			# check captcha
			captcha = self.get_body_argument("captcha", default="")
			if self.settings["captcha"]["login"] and not Captcha.check(captcha, self):
				self.custom_error("验证码错误")

			user = yield self.db.member.find_one({"username": username})
			check = yield self.backend.submit(hash.verify, password, user.get("password"))
			if check and user["power"] >= 0:
				session = self.set_session(user)
				if remember == "on":
					cookie_json = json.dumps(session)
					self.set_secure_cookie("user_info", cookie_json, expires_days = 30, httponly = True)
				yield self.db.member.find_and_modify({"username": username},{
					"$set": {
						"logintime": time.time(),
						"loginip": self.get_ipaddress()
					}
				})
				self.redirect("/")
			else:
				assert False
		except tornado.web.Finish:
			pass
		except:
			import traceback
			print(traceback.print_exc())
			self.custom_error("用户名或密码错误或账号被禁用", jump = "/login")  