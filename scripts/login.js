const password = document.querySelector("#password");
const passwordToggle = document.querySelector(".toggle");

passwordToggle.addEventListener('click', () => {
    if (password.type === "password") {
        password.type = "text";
        passwordToggle.classList.remove("bi-eye");
        passwordToggle.classList.add("bi-eye-slash");
    } else {
        password.type = "password";
        passwordToggle.classList.remove("bi-eye-slash");
        passwordToggle.classList.add("bi-eye");
    }
});

const login = document.querySelector("#login");
const loginText = document.querySelector(".login_text")
const username = document.querySelector("#username");
const form = document.querySelector("#loginForm");
const inputs = document.querySelectorAll(".inputs");
const personIcon = document.querySelector(".bi-person-fill");
const lockIcon = document.querySelector(".bi-lock-fill");
const toggle = document.querySelector(".toggle");

login.addEventListener('click', (event) => {
    event.preventDefault();

    const existingInvalidUsername = document.querySelector("#invalid-username");
    const existingInvalidPassword = document.querySelector("#invalid-password");

    if (existingInvalidUsername) existingInvalidUsername.remove();
    if (existingInvalidPassword) existingInvalidPassword.remove();

    let validUsername = true;
    let validPassword = true;

    resetIconPositions();

    if (username.value === "") {
        const invalidUsername = document.createElement("div");
        invalidUsername.classList.add("invalid-feedback");
        invalidUsername.setAttribute("id", "invalid-username");
        invalidUsername.textContent = "Πληκτρολογήστε το όνομα φοιτητή.";
        username.parentElement.appendChild(invalidUsername);
        username.classList.add("invalid");

        personIcon.style.top = "40%";
        lockIcon.style.top = "55%";
        toggle.style.top = "55%";
        validUsername = false;
    } else {
        validUsername = matchUsernamePattern();
    }

    if (password.value === "") {
        const invalidPassword = document.createElement("div");
        invalidPassword.classList.add("invalid-feedback");
        invalidPassword.setAttribute("id", "invalid-password");
        invalidPassword.textContent = "Πληκτρολογήστε τον κωδικό πρόσβασης.";
        password.parentElement.appendChild(invalidPassword);
        password.classList.add("invalid");

        toggle.style.top = "40%"; 
        lockIcon.style.top = "40%"; 
        personIcon.style.top = username.classList.contains("invalid") ? "40%" : "55%";
        validPassword = false;
    } else {
        password.classList.remove("invalid");
    }

    if (!validUsername || !validPassword) {
        inputs.forEach((inputDiv) => {
            inputDiv.style.flexDirection = "column";
        });

    } else {

        inputs.forEach((inputDiv) => {
            inputDiv.style.flexDirection = "";
        });

        loginText.textContent = "";
        login.classList.add("login_loading");

        setTimeout(() => {
            form.submit();
        }, 2000);
    }
});


function resetIconPositions() {
    personIcon.style.top = "45%";
    lockIcon.style.top = "45%";
    toggle.style.top = "50%";
}

function matchUsernamePattern() {
    const pattern = /^[a-zA-Z0-9]+$/;
    if (!pattern.test(username.value)) {
        const usernameNotMatched = document.createElement("div");
        usernameNotMatched.classList.add("invalid-feedback");
        usernameNotMatched.setAttribute("id", "invalid-username");
        usernameNotMatched.textContent = "Το όνομα φοιτητή δεν είναι έγκυρο.";
        username.parentElement.appendChild(usernameNotMatched);
        username.classList.add("invalid");

        personIcon.style.top = username.classList.contains("invalid") ? "40%" : "55%";
        lockIcon.style.top = username.classList.contains("invalid") ? "55%" : "40%";
        toggle.style.top = lockIcon.style.top; 

        return false;
    } else {
        username.classList.remove("invalid");
    }

    return true;
}