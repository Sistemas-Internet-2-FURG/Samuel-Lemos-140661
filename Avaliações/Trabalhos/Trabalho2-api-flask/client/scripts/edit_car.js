// Pegar o ID do carro via URL (exemplo: edit_car.html?id=1)
const params = new URLSearchParams(window.location.search);
const carId = params.get("id");
//console.log(`id: ${carId}`)
if (!carId) {
    alert("Nenhum veículo especificado para edição!");
    window.location.href = "dashboard.html";
}

const API_BASE_URL = "http://localhost:5000";
const token = localStorage.getItem("token");

async function fetchCarDetails() {
    const response = await fetch(`${API_BASE_URL}/getCarById/${carId}`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (response.ok) {
        const car = await response.json();
        document.getElementById("car-name").value = car.name;
        document.getElementById("car-year").value = car.year;
        document.getElementById("car-description").value = car.description;
        //document.getElementById("car-type-id").value = car.type_id;
    } else {
        alert("Erro ao buscar os detalhes do carro.");
        window.location.href = "dashboard.html";
    }
}

fetchCarDetails();

document.getElementById("edit-car-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("car-name").value;
    const year = document.getElementById("car-year").value;
    const description = document.getElementById("car-description").value;
    //const type_id = document.getElementById("car-type-id").value;

    const response = await fetch(`${API_BASE_URL}/edit/${carId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ name, year, description })
    });

    if (response.ok) {
        alert("Veículo atualizado com sucesso!");
        window.location.href = "dashboard.html";
    } else {
        alert("Erro ao atualizar o veículo.");
    }
});
