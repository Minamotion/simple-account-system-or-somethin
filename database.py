from random import randint

class User:
	username: str
	password: str
	authkey: str
	def __init__(self, username: str, password: str):
		self.username = username
		self.password = password
		self.authkey = ""
	def __str__(self):
		return "{}:{}".format(self.username, self.authkey)

users: list[User]= []
pswdcsv_path = "database/pswd.csv"

def generate_unique_key() -> str:
	key: str= ""
	while any(userb.authkey == key for userb in users) or key == "":
		chars: list[str]= "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"
		for _ in range(randint(8, 32)):
			key += chars[randint(0, len(chars) -1)]
	return key

with open(pswdcsv_path) as file:
	table = file.read()
	for row in table.split("\n"):
		if len(row) == 0: continue
		info = row.split(":")
		user = User(info[0], info[1])
		user.authkey = generate_unique_key()
		users.append(user)
	file.close()