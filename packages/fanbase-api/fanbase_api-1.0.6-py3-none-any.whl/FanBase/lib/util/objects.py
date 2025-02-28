def _extract(response, path):
	keys = path.split(".")
	result = []
	for data in response["data"]:
		value = data
		try:
			for key in keys:
				if key.isdigit():
					key = int(key)
				value = value[key]
			result.append(value)
		except (KeyError, IndexError, TypeError):
			result.append(None)
	return result
	def __getattr__(self, key):
		return None
class MainFeed():
	def __init__(self, response):
		self.userIds = _extract(response, "uuid")
		self.postIds = _extract(response, "id")
		self.thumbnails = _extract(response, "attributes.media.0.thumbnail")
		self.usernames = _extract(response, "user.name")
		self.ids = _extract(response, "user.id")
		self.urls = _extract(response, "actions.share_url")
		self.media_types = _extract(response, "attributes.media.0.media_type")
		self.next_pageId = response.get("next_page_id")
		self.previous_pageId = response.get("previous_page_id")

class Login:
	def __init__(self, response):
		attributes = response["included"]["user"]["attributes"]
		self.token = response["data"]["access_token"]
		self.token_type = response["data"]["token_type"]
		self.refresh_token = response["data"]["refresh_token"]
		self.id = response["included"]["user"]["id"]
		self.dob = attributes.get("dob")
		self.email = attributes.get("email")
		self.username = attributes.get("name")
		self.real_name = attributes.get("realname")
		self.last_name = attributes.get("lastname")
		self.full_name = attributes.get("fullname")
		self.website = attributes.get("website")
		self.bio = attributes.get("bio")
		self.avatar = attributes.get("avatar")
		self.cover = attributes.get("cover")
		self.region = attributes.get("region")
		self.country = attributes.get("country")
		self.braze_external_id = attributes.get("braze_external_id")


class UserFeed():
	def __init__(self, response):
		self.media_types = _extract(response, "attributes.media.0.media_type")
		self.urls = _extract(response, "actions.share_url")
		self.thumbnails = _extract(response, "attributes.media.0.thumbnails")
		self.titles = _extract(response, ("attributes.title"))
		self.captions = _extract(response, ("attributes.caption"))
		self.postIds = response.get("id")