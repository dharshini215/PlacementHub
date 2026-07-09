// ==========================================
// Full Name Validation
// ==========================================

const fullName = document.getElementById("full_name");
const nameError = document.getElementById("nameError");

if (fullName) {

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
                "Name must contain at least 3 letters.";

            fullName.classList.add("is-invalid");

        }

        else {

            nameError.innerHTML = "";
            fullName.classList.remove("is-invalid");

        }

    });

}


// ==========================================
// Phone Number Validation
// ==========================================

const phone = document.getElementById("phone");
const phoneError = document.getElementById("phoneError");

if (phone) {

    phone.addEventListener("input", function () {

        this.value = this.value.replace(/\D/g, "");

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


// ==========================================
// CGPA Validation
// ==========================================

const cgpa = document.getElementById("cgpa");
const cgpaError = document.getElementById("cgpaError");

if (cgpa) {

    cgpa.addEventListener("input", function () {

        let value = parseFloat(this.value);

        if (this.value.length === 0) {

            cgpaError.innerHTML = "";
            cgpa.classList.remove("is-invalid");

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