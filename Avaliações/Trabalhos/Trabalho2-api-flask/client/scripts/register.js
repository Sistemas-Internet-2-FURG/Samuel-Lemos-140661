const API_BASE_URL = "http://localhost:5000";

document.getElementById("register-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("register-name").value;
    const password = document.getElementById("register-password").value;

    const response = await fetch(`${API_BASE_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, password })
    });

    if (response.ok) {
        alert("Registro bem-sucedido!");
        window.location.href = "index.html";
    } else {
        alert("Falha no registro!");
    }
});