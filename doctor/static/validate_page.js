
function validateDoctorForm() {
    const form = document.forms["doctorForm"];
    const email = form["email"].value.trim();
    const phone = form["phone"].value.trim();

    const emailPattern = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
    const phonePattern = /^[0-9]{10}$/;

    if (!emailPattern.test(email)) {
        alert("Please enter a valid email address.");
        return false;
    }

    if (!phonePattern.test(phone)) {
        alert("Phone number must be exactly 10 digits.");
        return false;
    }

    return true;
}
