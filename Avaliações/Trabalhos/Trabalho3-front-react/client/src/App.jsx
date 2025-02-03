import "./App.css";
import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://localhost:5000";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [cars, setCars] = useState([]);
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [newCar, setNewCar] = useState({ name: "", year: "", description: "", type_id: "" });

  // Estados para edição
  const [editCar, setEditCar] = useState(null);
  const [editData, setEditData] = useState({ name: "", year: "", description: "" });

  useEffect(() => {
    if (token) fetchCars();
  }, [token]);

  const login = async () => {
    try {
      const res = await axios.post(`${API_URL}/login`, { name, password });
      setToken(res.data.token);
      localStorage.setItem("token", res.data.token);
    } catch (err) {
      alert("Falha no login");
    }
  };

  const register = async () => {
    try {
      await axios.post(`${API_URL}/register`, { name, password });
      alert("Usuário cadastrado! Faça login.");
    } catch (err) {
      alert("Erro ao cadastrar");
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken("");
    setCars([]);
  };

  const fetchCars = async () => {
    try {
      const res = await axios.get(`${API_URL}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setCars(res.data.cars);
    } catch (err) {
      alert("Erro ao buscar veículos");
    }
  };

  const addCar = async () => {
    try {
      await axios.post(`${API_URL}/new`, newCar, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchCars();
    } catch (err) {
      alert("Erro ao adicionar veículo");
    }
  };

  const startEdit = (car) => {
    setEditCar(car);
    setEditData({ name: car.name, year: car.year, description: car.description });
  };

  const handleEditChange = (e) => {
    setEditData({ ...editData, [e.target.name]: e.target.value });
  };

  const saveEdit = async () => {
    if (!editCar) return;
    try {
      await axios.post(`${API_URL}/edit/${editCar.id}`, editData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setEditCar(null);
      fetchCars(); // Atualiza a lista de veículos
    } catch (error) {
      console.error("Erro ao editar veículo:", error);
    }
  };

  const deleteCar = async (id) => {
    try {
      await axios.get(`${API_URL}/delete/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchCars();
    } catch (err) {
      alert("Erro ao excluir veículo");
    }
  };

  return (
    <div className="p-4">
      {!token ? (
        <div>
          <h2>Login</h2>
          <input placeholder="Nome" value={name} onChange={(e) => setName(e.target.value)} />
          <input type="password" placeholder="Senha" value={password} onChange={(e) => setPassword(e.target.value)} />
          <button onClick={login}>Login</button>
          <button onClick={register}>Registrar</button>
        </div>
      ) : (
        <div>
          <button onClick={logout}>Sair</button>
          <h2>Lista de Veículos</h2>
          <ul>
            {cars.map((car) => (
              <li key={car.id}>
                {car.name} - {car.year} - {car.type_name}
                <button onClick={() => startEdit(car)}>Editar</button>
                <button onClick={() => deleteCar(car.id)}>Deletar</button>
              </li>
            ))}
          </ul>
          <h3>Adicionar Veículo</h3>
          <input placeholder="Nome" onChange={(e) => setNewCar({ ...newCar, name: e.target.value })} />
          <input placeholder="Ano" onChange={(e) => setNewCar({ ...newCar, year: e.target.value })} />
          <input placeholder="Descrição" onChange={(e) => setNewCar({ ...newCar, description: e.target.value })} />
          <button onClick={addCar}>Adicionar</button>
        </div>
      )}

      {editCar && (
        <div>
          <h2>Editando: {editCar.name}</h2>
          <input type="text" name="name" value={editData.name} onChange={handleEditChange} placeholder="Nome do veículo" />
          <input type="number" name="year" value={editData.year} onChange={handleEditChange} placeholder="Ano do veículo" />
          <input type="text" name="description" value={editData.description} onChange={handleEditChange} placeholder="Descrição" />
          <button onClick={saveEdit}>Salvar</button>
          <button onClick={() => setEditCar(null)}>Cancelar</button>
        </div>
      )}
    </div>
  );
}
