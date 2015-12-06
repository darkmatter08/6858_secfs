from cryptography.fernet import Fernet
import secfs.crypto
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend

class SymKeyStore:
	
	def __init__(self, users, groups):
		"""
		users: a dict with key: user (prinicpal that is a user)
		and value: public key

		groups: d dict with key: group (prinicpal that is a group)
		and value: list of users (prinicpal that is a user)
		"""
		for u in users:
			users[u] = load_pem_public_key(users[u], backend=default_backend())
		self.users = {u: secfs.crypto.encrypt_asym(users[u], Fernet.generate_key()) for u in users}

		self.groups = {}
		for g in groups:
			group_key = Fernet.generate_key()
			self.groups[g] = {u: secfs.crypto.encrypt_asym(users[u], group_key) for u in groups[g]}

		print("SymKeyStore: users: {}\n groups: {}".format(users, groups))
