document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault(); // prevent form from refreshing page

    const form = e.target;

    const data = {
        username: form.username.value,
        password: form.password.value
    };

    try {
        const response = await fetch("/login", {  // match Flask route
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            window.location.href = "/dashboard-page";  // your dashboard route
        } else {
            document.getElementById("error").innerText = result.error;
        }
    } catch (err) {
        document.getElementById("error").innerText = "Server error, try again!";
    }
});
