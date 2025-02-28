def login_headers(data):
	return {
		"Host": "app.fanbase.app",
		"platform": "android",
		"accept": "apllication/json",
		"app-version": "3.13.0",
		"user-agent": "Android_Fanbase/3.13.0",
		"accept-language": "en-GB",
		"client-id": "959",
		"client-secret": "tpdTByeeuaG4NRuEDKX4iJzrOHQfjHGCHkYDpiWW",
		"content-type": "apllication/json; charset=UTF-8",
		"content-length": str(len(str(data))),
		"accept-encoding": "gzip"
	}
def headers(token, data=None):
	
	headers = {"Host": "app.fanbase.app",
		"platform": "android",
		"accept": "apllication/json",
		"app-version": "3.13.0",
		"user-agent": "Android_Fanbase/3.13.0",
		"accept-language": "en-GB",
		"authorization": token,
		"content-type": "apllication/json; charset=UTF-8",
		"accept-encoding": "gzip"
	}
	if data:
		headers["content-length"] = str(len(str(data)))
	return headers