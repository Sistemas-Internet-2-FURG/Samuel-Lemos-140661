const API_BASE_URL = "http://localhost:5000";
const token = localStorage.getItem("token");

async function fetchCars() {
    const response = await fetch(`${API_BASE_URL}/`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (response.ok) {
        const data = await response.json();
        const carList = document.getElementById("car-list");
        carList.innerHTML = "";
        data.cars.forEach(car => {
            const carDiv = document.createElement("div");
            carDiv.classList.add("car-item");

            carDiv.innerHTML = `
                <p><strong>Nome:</strong> ${car.name}</p>
                <p><strong>Ano:</strong> ${car.year}</p>
                <p><strong>Descrição:</strong> ${car.description || "N/A"}</p>
                <p><strong>Tipo:</strong> ${car.type_name}</p>
                <button class="edit-button" data-id="${car.id}">Editar</button>
                <button class="delete-button" data-id="${car.id}">Excluir</button>
            `;

            carList.appendChild(carDiv);
        });

        document.querySelectorAll(".edit-button").forEach(button => {
            button.addEventListener("click", (e) => {
                const carId = e.target.getAttribute("data-id");
                window.location.href = `edit_car.html?id=${carId}`;
            });
        });

        document.querySelectorAll(".delete-button").forEach(button => {
            button.addEventListener("click", async (e) => {
                const carId = e.target.getAttribute("data-id");
                
                const response = await fetch(`${API_BASE_URL}/delete/${carId}`, {
                    headers: { "Authorization": `Bearer ${token}` }
                });

                if (response.ok) {
                    alert("Veículo deletado com sucesso!");
                    window.location.href = "dashboard.html";
                } else {
                    alert("Erro ao deletar o veículo.");
                }
            })
        })
    } else {
        alert("Erro ao buscar os veículos.");
    }
}

fetchCars();

document.getElementById("logout").addEventListener("click", () => {
    localStorage.removeItem("token");
    window.location.href = "index.html";
});
