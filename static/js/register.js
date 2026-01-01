document.getElementById("registerForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const form = e.target;

    const data = {
        first_name: form.first_name.value,
        last_name: form.last_name.value,
        father_name: form.father_name.value,
        age: form.age.value,
        username: form.username.value,
        password: form.password.value,
        confirm_password: form.confirm_password.value
    };

    try {
        const response = await fetch("/register", {  // must match Flask route
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            alert("Registered successfully!");
            window.location.href = "/login";  // redirect to login page
        } else {
            document.getElementById("error").innerText = result.error;
        }
    } catch (err) {
        document.getElementById("error").innerText = "Server error, try again!";
        console.error(err);
    }
});
