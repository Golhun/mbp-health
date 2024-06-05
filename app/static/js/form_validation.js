document.addEventListener("DOMContentLoaded", function () {
	const form = document.querySelector("form");
	const passwordInput = document.getElementById("password");
	const confirmPasswordInput = document.getElementById("confirm_password");

	if (form) {
		form.addEventListener("submit", function (event) {
			if (passwordInput.value !== confirmPasswordInput.value) {
				event.preventDefault();
				alert("Passwords do not match!");
			}
		});
	}
});
