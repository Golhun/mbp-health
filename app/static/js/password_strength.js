document.addEventListener("DOMContentLoaded", function () {
	const passwordInput = document.getElementById("password");
	const confirmPasswordInput = document.getElementById("confirm_password");
	const requirements = document.getElementById("password-requirements");
	const strengthBar = document.getElementById("password-strength");
	const showPasswordCheckbox = document.getElementById("show-password");

	if (passwordInput) {
		passwordInput.addEventListener("focus", function () {
			requirements.style.display = "block";
		});

		passwordInput.addEventListener("blur", function () {
			if (!passwordInput.value) {
				requirements.style.display = "none";
			}
		});

		passwordInput.addEventListener("keyup", function () {
			checkPasswordStrength(passwordInput.value);
		});
	}

	if (showPasswordCheckbox) {
		showPasswordCheckbox.addEventListener("change", function () {
			const type = showPasswordCheckbox.checked ? "text" : "password";
			passwordInput.type = type;
			confirmPasswordInput.type = type;
		});
	}

	function checkPasswordStrength(password) {
		let strength = 0;

		const requirementsList = [
			{
				regex: /.{6,}/,
				element: document.getElementById("length-requirement"),
			},
			{
				regex: /[a-z]+/,
				element: document.getElementById("lowercase-requirement"),
			},
			{
				regex: /[A-Z]+/,
				element: document.getElementById("uppercase-requirement"),
			},
			{
				regex: /[0-9]+/,
				element: document.getElementById("number-requirement"),
			},
			{
				regex: /[\W]+/,
				element: document.getElementById("special-requirement"),
			},
		];

		requirementsList.forEach((item) => {
			if (item.regex.test(password)) {
				item.element.classList.add("text-green-500");
				item.element.classList.remove("text-red-500");
				item.element.innerHTML = `<i class="fas fa-check"></i> ${item.element.dataset.text}`;
				strength++;
			} else {
				item.element.classList.add("text-red-500");
				item.element.classList.remove("text-green-500");
				item.element.innerHTML = `<i class="fas fa-times"></i> ${item.element.dataset.text}`;
			}
		});

		strengthBar.innerHTML = "";
		if (strength < 2) {
			strengthBar.innerHTML =
				'<span class="text-red-500"><i class="fas fa-times"></i> Weak</span>';
		} else if (strength < 4) {
			strengthBar.innerHTML =
				'<span class="text-yellow-500"><i class="fas fa-exclamation"></i> Medium</span>';
		} else {
			strengthBar.innerHTML =
				'<span class="text-green-500"><i class="fas fa-check"></i> Strong</span>';
		}
	}
});
