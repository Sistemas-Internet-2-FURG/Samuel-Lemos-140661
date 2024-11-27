const API_BASE_URL = "http://localhost:5000";
const token = localStorage.getItem("token");

async function fetchCarTypes() {

    const response = await fetch(`${API_BASE_URL}/getTypes`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (response.ok) {
        const data = await response.json();
        const select = document.getElementById("car-type-id");

        data.car_types.forEach(carType => {
            const option = document.createElement("option");
            option.value = carType.id;
            option.textContent = carType.name;
            select.appendChild(option);
        });
    } else {
        alert("Erro ao buscar tipos de carros.");
    }
}

fetchCarTypes();
