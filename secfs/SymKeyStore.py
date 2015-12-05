from cryptography.fernet import Fernet

def asymm_encryption(key, data):
	# TODO: Actually implement
	return data

class SymKeyStore:
	
	def __init__(self, users, groups):
		"""
		users: a dict with key: user (prinicpal that is a user)
		and value: public key

		groups: d dict with key: group (prinicpal that is a group)
		and value: list of users (prinicpal that is a user)
		"""
		# print("SymKeyStore.input_users: {}, type: {}".format(input_users, type(input_users)))
		# self.users = {}
		self.users = {u: asymm_encryption(Fernet.generate_key(), users[u]) for u in users}
		# for u in input_users:
		# 	self.users[u] = asymm_encryption(Fernet.generate_key(), input_users[u])

		self.groups = {}
		for g in groups:
			group_key = Fernet.generate_key()
			self.groups[g] = {u: asymm_encryption(group_key, users[u]) for u in groups[g]}
