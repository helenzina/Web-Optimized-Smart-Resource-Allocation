const password = document.querySelector("#password");
const passwordToggle = document.querySelector(".toggle");

passwordToggle.addEventListener('click', () => {
    if (password.type === "password") {
        password.type = "text";
        passwordToggle.classList.remove("bi-eye-slash");
        passwordToggle.classList.add("bi-eye");
    } else {
        password.type = "password";
        passwordToggle.classList.remove("bi-eye");
        passwordToggle.classList.add("bi-eye-slash");
    }
});
