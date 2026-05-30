document.addEventListener("DOMContentLoaded", async () => {
	const noLoggedInDiv = document.getElementById("nologgedin")
	const loggedInDiv = document.getElementById("loggedin")
	const usernameSpan = document.getElementById("username")
	const deleteBtn = document.getElementById("delete")

	const username = await fetch("/api/user/me").then(raw => raw.json())
	if (username != null) {
		usernameSpan.innerText = username
		loggedInDiv.hidden = false
	} else {
		noLoggedInDiv.hidden = false
	}

	deleteBtn.addEventListener("dblclick", async () => {
		await fetch("/api/user/me", {"method": "DELETE"})
		location.reload()
	})
})