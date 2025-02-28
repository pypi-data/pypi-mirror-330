from .FanBase import fanbase
import requests
import os
version = "1.0.5"
newest = requests.get("https://pypi.org/pypi/fanbase-api/json").json()["info"]["version"]
if version != newest:
	print("There is a new version! ")
	answer = input("download it [y/n]")
	if answer.lower() == "n":
		pass
	else:
		os.system("pip install fanbase-api -U")
		exit()