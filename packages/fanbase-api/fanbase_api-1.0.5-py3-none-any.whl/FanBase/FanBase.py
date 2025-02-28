import requests
from .lib.util import headers
from .lib.util.objects import *


class fanbase:
	BASE_URL = "https://app.fanbase.app"

	def __init__(self):
		self.login_headers = headers.login_headers
		self.headers = headers.headers
		self.token = ""
		self.session = requests.Session()

	def login(self, user: str, password: str):
		data = {"user": user, "password": password}
		response = self.session.post(f"{self.BASE_URL}/api/v2/oauth/login", headers=self.login_headers(data), json=data)
		
		if response.status_code == 200:
			login = Login(response.json())
			self.token = f"{login.token_type} {login.token}"
			return login
		raise Exception(response.json())

	def send_message(self, userId: str, content: str, message_type: str = "text"):
		data = {"message_text": content, "message_type": message_type}
		response = self.session.post(f"{self.BASE_URL}/dm/conversations/{userId}/messages", headers=self.headers(self.token, data), json=data)
		if response.status_code not in range(200, 300):
			raise Exception(response.json())

	def get_main_feed(self, pageId: str = None):
		url = f"{self.BASE_URL}/api/v4/feed/main-v3"
		if pageId:
			url += f"?page_id={pageId}"
		response = self.session.get(url, headers=self.headers(self.token))
		if response.status_code == 200:
			return MainFeed(response.json())
		raise Exception(response.json())

	def comment_in_post(self, postId: int, comment: str, post_type):
		data = {"comment": comment}
		post_type = "posts" if post_type=="post" else "flickz/videos"
		response = self.session.post(f"{self.BASE_URL}/api/v2/{post_type}/{postId}/comments", headers=self.headers(self.token, data), json=data)
		if response.status_code not in range(200, 300):
			raise Exception(response.json())

	def like(self, postId: int, post_type):
		post_type = "posts" if post_type=="post" else "flickz/videos"
		response = self.session.post(f"{self.BASE_URL}/api/v2/{post_type}/{postId}/liked", headers=self.headers(self.token))
		if response.status_code not in range(200, 300):
			raise Exception(response.json())

	def get_user_feed(self, userId: str, pageId: str = None):
		url = f"{self.BASE_URL}/api/v4/feed/user/{userId}/exclusive"
		if pageId:
			url += f"?page_id={pageId}"
		response = self.session.get(url, headers=self.headers(self.token))
		if response.status_code == 200:
			return UserFeed(response.json())
		raise Exception(response.json())