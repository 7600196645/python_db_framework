document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("PatientForm");
    const errorDisplay = document.getElementById("error");

    form.addEventListener("submit", function (e) {
        const name = form.elements["name"].value.trim();
        const age = form.elements["age"].value.trim();
        const email = form.elements["email"].value.trim();

        if (name === "" || age === "" || email === "") {
            e.preventDefault();
            errorDisplay.textContent = "All fields are required.";
        } else if (isNaN(age) || age <= 0) {
            e.preventDefault();
            errorDisplay.textContent = "Please enter a valid age.";
        } else {
            errorDisplay.textContent = "";
        }
    });
});
