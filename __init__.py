from fastapi import FastAPI
from starlette.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from .pages import *
from .database import *

app: FastAPI = FastAPI(docs_url="/d", redoc_url=None)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

#region [Pages Endpoint]
@app.get("/")
def home_page():
	usernames: list[str] = []
	for user in users:
		usernames.append(user.username)
	return get_html("home", usernames)

@app.get("/login")
def login_page():
	return get_html("forms/login")

@app.get("/signin")
def login_page():
	return get_html("forms/signin")

@app.exception_handler(HTTPException)
def whoopsie(_, exception: HTTPException):
	response = get_html("error", exception.status_code, exception.detail, status_code=exception.status_code, headers=exception.headers)
	return response

#endregion
#region [API Endpoint]
#region [API User Endpoint]
@app.get("/api/user/me")
def api_user_me(request: Request):
	key = request.cookies.get("auth")
	if key is None:
		return
	for user in users:
		if key == user.authkey:
			return user.username
	return

@app.post("/api/user/me")
async def api_user_me(request: Request):
	response = get_html("success", "Logged in!")

	form = await request.form()
	username: str= form.get("username")
	password: str= form.get("password")

	my_user: User= None

	for user in users:
		if user.username == username:
			my_user = user
	if my_user == None:
		raise HTTPException(403, "Wrong login!")
	else:
		if password != my_user.password:
			raise HTTPException(403, "Wrong login!")
	
	response.set_cookie("auth", my_user.authkey, secure=True)
	return response

@app.delete("/api/user/me")
def api_user_me(request: Request):
	response = get_html("success", "Deleted account!")
	key = request.cookies.get("auth")
	if key is None:
		return response
	for user in users:
		if key == user.authkey:
			users.remove(user)
			table: list[str]= []
			with open(pswdcsv_path, "r") as file:
				table = file.readlines()
				file.close()
			with open(pswdcsv_path, "w") as file:
				for item in table:
					info = item.split(":")
					if info[0] == user.username:
						continue
					file.write(item)
				file.close()
	response.delete_cookie("auth")
	return response

@app.post("/api/user/new")
async def api_user_new(request: Request):
	response = get_html("success", "Created account!")

	form = await request.form()
	username: str= form.get("username")
	password: str= form.get("password")

	if any(user.username == username for user in users):
		raise HTTPException(403, "Username already in use")

	my_user: User = User(username, password)
	my_user.authkey = generate_unique_key()
	users.append(my_user)
	with open(pswdcsv_path, "a") as file:
		file.write("\n{}:{}".format(username, password))
		file.close()
	
	response.set_cookie("auth", my_user.authkey, secure=True)
	return response

@app.get("/api/user/logout")
def api_user_logout():
	response = get_html("success", "Logged out!")
	response.delete_cookie("auth")
	return response
#endregion
#region [API Endpoint]

#endregion
#endregion