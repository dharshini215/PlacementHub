// ==============================
// Full Name Validation
// ==============================

const fullName = document.getElementById("full_name");
const nameError = document.getElementById("nameError");

if (fullName && nameError) {

    fullName.addEventListener("input", function () {

        this.value = this.value.replace(/\s+/g, " ");

        if (this.value.length === 0) {

            nameError.innerHTML = "";
            fullName.classList.remove("is-invalid");

        }
        else if (!/^[A-Za-z ]+$/.test(this.value)) {

            nameError.innerHTML =
                "Only letters and spaces are allowed.";

            fullName.classList.add("is-invalid");

        }
        else if (this.value.trim().length < 3) {

            nameError.innerHTML =
                "Name must contain at least 3 characters.";

            fullName.classList.add("is-invalid");

        }
        else {

            nameError.innerHTML = "";
            fullName.classList.remove("is-invalid");

        }

    });

}


// ==============================
// Register Number Validation
// ==============================

const registerNumber =
    document.getElementById("register_number");

const registerError =
    document.getElementById("registerError");

if (registerNumber && registerError) {

    registerNumber.addEventListener("input", function () {

        this.value =
            this.value.toUpperCase().replace(/\s/g, "");

        const pattern =
            /^(\d{3}[A-Z]{2}\d{3}|\d{2}UG[A-Z]{3}\d{5})$/;

        if (this.value.length === 0) {

            registerError.innerHTML = "";
            registerNumber.classList.remove("is-invalid");

        }
        else if (!pattern.test(this.value)) {

            registerError.innerHTML =
                "Invalid Register Number format.";

            registerNumber.classList.add("is-invalid");

        }
        else {

            registerError.innerHTML = "";
            registerNumber.classList.remove("is-invalid");

        }

    });

}


// ==============================
// Email Validation
// ==============================

const email = document.getElementById("email");
const emailError = document.getElementById("emailError");

if (email && emailError) {

    email.addEventListener("input", function () {

        this.value =
            this.value.toLowerCase().replace(/\s/g, "");

        const pattern =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (this.value.length === 0) {

            emailError.innerHTML = "";
            email.classList.remove("is-invalid");

        }
        else if (!pattern.test(this.value)) {

            emailError.innerHTML =
                "Enter a valid Email Address.";

            email.classList.add("is-invalid");

        }
        else {

            emailError.innerHTML = "";
            email.classList.remove("is-invalid");

        }

    });

}


// ==============================
// Phone Number Validation
// ==============================

const phone = document.getElementById("phone");
const phoneError = document.getElementById("phoneError");

if (phone && phoneError) {

    phone.addEventListener("input", function () {

        // Allow only numbers
        this.value = this.value.replace(/\D/g, "");

        // Maximum 10 digits
        this.value = this.value.substring(0, 10);

        if (this.value.length === 0) {

            phoneError.innerHTML = "";
            phone.classList.remove("is-invalid");

        }
        else if (!/^[6-9]\d{9}$/.test(this.value)) {

            phoneError.innerHTML =
                "Enter a valid 10-digit Indian mobile number.";

            phone.classList.add("is-invalid");

        }
        else {

            phoneError.innerHTML = "";
            phone.classList.remove("is-invalid");

        }

    });

}


// ==============================
// CGPA Validation
// ==============================

const cgpa = document.getElementById("cgpa");
const cgpaError = document.getElementById("cgpaError");

if (cgpa && cgpaError) {

    cgpa.addEventListener("input", function () {

        const value = parseFloat(this.value);

        if (this.value === "") {

            cgpaError.innerHTML = "";
            cgpa.classList.remove("is-invalid");

        }
        else if (isNaN(value)) {

            cgpaError.innerHTML =
                "Enter a valid CGPA.";

            cgpa.classList.add("is-invalid");

        }
        else if (value < 0 || value > 10) {

            cgpaError.innerHTML =
                "CGPA must be between 0 and 10.";

            cgpa.classList.add("is-invalid");

        }
        else {

            cgpaError.innerHTML = "";
            cgpa.classList.remove("is-invalid");

        }

    });

}


// ==============================
// Password Validation
// Only runs on Register page
// ==============================

const password =
    document.getElementById("password");

const passwordError =
    document.getElementById("passwordError");

const passwordStrength =
    document.getElementById("passwordStrength");

if (password && passwordError && passwordStrength) {

    password.addEventListener("input", function () {

        const value = this.value;

        password.classList.remove("is-invalid");

        passwordError.innerHTML = "";
        passwordStrength.innerHTML = "";

        if (value.length === 0) {
            return;
        }

        if (value.length < 8) {

            passwordError.innerHTML =
                "Password must contain at least 8 characters.";

            password.classList.add("is-invalid");

            return;

        }

        let score = 0;

        if (/[A-Z]/.test(value)) score++;
        if (/[a-z]/.test(value)) score++;
        if (/[0-9]/.test(value)) score++;
        if (/[^A-Za-z0-9]/.test(value)) score++;

        if (score <= 2) {

            passwordStrength.innerHTML =
                "<span class='text-danger'>Weak Password</span>";

        }
        else if (score === 3) {

            passwordStrength.innerHTML =
                "<span class='text-warning'>Medium Password</span>";

        }
        else {

            passwordStrength.innerHTML =
                "<span class='text-success'>Strong Password</span>";

        }

    });

}


// ==============================
// Confirm Password Validation
// Only runs on Register page
// ==============================

const confirmPassword =
    document.getElementById("confirm_password");

const confirmPasswordError =
    document.getElementById("confirmPasswordError");

if (
    confirmPassword &&
    confirmPasswordError &&
    password
) {

    confirmPassword.addEventListener("input", function () {

        if (this.value.length === 0) {

            confirmPasswordError.innerHTML = "";
            confirmPassword.classList.remove("is-invalid");

        }
        else if (this.value !== password.value) {

            confirmPasswordError.innerHTML =
                "Passwords do not match.";

            confirmPassword.classList.add("is-invalid");

        }
        else {

            confirmPasswordError.innerHTML = "";
            confirmPassword.classList.remove("is-invalid");

        }

    });

}