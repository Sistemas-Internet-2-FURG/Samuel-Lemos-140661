document.getElementById("add-car-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const API_BASE_URL = "http://localhost:5000";
    const token = localStorage.getItem("token");

    const name = document.getElementById("car-name").value;
    const year = document.getElementById("car-year").value;
    const description = document.getElementById("car-description").value;
    const type_id = document.getElementById("car-type-id").value;

    const response = await fetch(`${API_BASE_URL}/new`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ name, year, description, type_id })
    });

    if (response.ok) {
        alert("Veículo cadastrado com sucesso!");
        window.location.href = "dashboard.html";
    } else {
        alert("Erro ao cadastrar o veículo.");
    }
});
