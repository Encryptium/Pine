const registerEmailInput = document.getElementById("email");

const registerUsernameInput = document.getElementById("username");

registerEmailInput.addEventListener('keyup', e => {
	if (!registerEmailInput.checkValidity()) {
		return;
	}

	fetch(`/api/v1/register/check-email?string=${registerEmailInput.value}`)
	.then(response => {
		if (response.status !== 200) {
			console.log("Couldn't establish connection to server.");
			return;
		}

		response.json()
			.then(data => {
				if (data.status == "success") {
					registerEmailInput.classList.remove("invalid");
					registerEmailInput.classList.add("valid");
					registerEmailInput.title = data.message;
				} else {
					registerEmailInput.classList.remove("valid");
					registerEmailInput.classList.add("invalid");
					registerEmailInput.title = data.message;
				}
			});
	});
});

registerUsernameInput.addEventListener('keyup', e => {
	fetch(`/api/v1/register/check-username?string=${registerUsernameInput.value}`)
	.then(response => {
		if (response.status !== 200) {
			console.log("Couldn't establish connection to server.");
			return;
		}

		response.json()
			.then(data => {
				if (data.status == "success") {
					registerUsernameInput.classList.remove("invalid");
					registerUsernameInput.classList.add("valid");
					registerUsernameInput.title = data.message;
				} else {
					registerUsernameInput.classList.remove("valid");
					registerUsernameInput.classList.add("invalid");
					registerUsernameInput.title = data.message;
				}
			});
	});
});