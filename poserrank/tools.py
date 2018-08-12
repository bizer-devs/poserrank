import json
from json import JSONEncoder


class ModelEncoder(JSONEncoder):
	"""
	A bare-bones JSONEncoder that emulates JSONEncoder, but attempts to call `serializeable` first.  All models should
	have this method defined, allowing them to
	"""

	def default(self, obj):
		"""
		WTF, why doesn't JSONEncoder already try str(obj) ??
		"""
		try:
			return obj.serializeable()
		except AttributeError:
			pass

		try:
			return JSONEncoder.default(self, obj)
		except TypeError:
			return str(obj)


# WARNING: Deprecated
def dictifyUser(user):
	"""
	Returns a dictionary of the information contained in a user object, so that
	this data can be stored in the session.  Also removes sensitive information
	(e.g. passwords) and unserializable items (e.g. complex objects).
	"""
	userDict = user.__dict__  # make dictionary
	removeList = []  # can't change size of list during iteration
	for key in userDict:  # loop through each item, deleting if not serializable
		try:
			json.dumps(
				userDict[key])  # note that we throw this serialization away; it's just to see if we can serialize it
		except TypeError:
			removeList.append(key)

	for key in removeList:
		del userDict[key]

	del userDict['password']
	return userDict
