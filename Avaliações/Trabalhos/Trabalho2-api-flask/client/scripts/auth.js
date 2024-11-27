const API_BASE_URL = "http://localhost:5000";

document.getElementById("login-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("login-name").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, password })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.token);
        window.location.href = "dashboard.html";
    } else {
        alert("Login falhou!");
    }
});
