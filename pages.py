from fastapi.responses import HTMLResponse
from typing import Mapping

def get_html(path: str, *args, status_code: int= 200, headers: Mapping[str, str]|None= None):
	value = open("pages/{}.html".format(path)).read()
	if len(args) > 0:
		value = value.format(*args)
	return HTMLResponse(value, status_code, headers)