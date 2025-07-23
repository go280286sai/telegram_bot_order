import React, {useEffect, useState} from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import AdminCityModal from "./AdminCityModal";

export default function AdminCity() {
    const [content, setContent] = useState([]);
    const [formData, setFormData] = useState({});

    const fetchCities = async () => {
        try {
            const response = await fetch("http://localhost:8000/city/gets", {
                method: "GET",
                credentials: "include",
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            if (data.success) {
                setContent(data.data.cities);

                // Создаём локальное состояние для редактирования
                const initForm = {};
                data.data.cities.forEach(item => {
                    initForm[item.id] = {
                        name: item.name,
                        post_id:item.post_id
                    };
                });
                setFormData(initForm);
            }
        } catch (error) {
            await log("error", "cities", error);
        }
    };

    // Инициализация
    useEffect(() => {
        fetchCities();
    }, []);
    useEffect(() => {
        if (content.length > 0) {
            const dtInstance = new DataTable('#myTable2');
            return () => {
                dtInstance.destroy();
            };
        }
    }, [content]);
    // Обновление значения при вводе
    const handleChange = (id, field, newValue) => {
        setFormData(prev => ({
            ...prev,
            [id]: {
                ...prev[id],
                [field]: newValue
            }
        }));
    };

    const fetchUpdate = async (id) => {
        const {name, post_id} = formData[id];
        try {
            const response = await fetch(`http://localhost:8000/city/update/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({name, post_id})
            });
            const data = await response.json();
            if (data.success) {
                fetchCities();
            }
        } catch (error) {
            await log("error", "products", error);
        }
    };
    const fetchDelete = async (id) => {
        try {
            const response = await fetch(`http://localhost:8000/city/delete/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
            });
            const data = await response.json();
            if (data.success) {
                fetchCities();
            }
        } catch (error) {
            await log("error", "cities", error);
        }
    };
    return (
        <div>
            <h3>Cities</h3>
            <div className="btn btn-success mb-2 btn_with"
                 data-bs-toggle="modal"
                 data-bs-target="#addCity">Add item
            </div>
            <AdminCityModal/>
            <table id="myTable2" className="display table table-dark">
                <thead>
                <tr>
                    <th>Id</th>
                    <th>Name</th>
                    <th>Post Id</th>
                    <th>Update</th>
                    <th>Delete</th>
                </tr>
                </thead>
                <tbody>
                {content.map((item) => (
                    <tr key={item.id}>
                        <td>{item.id}</td>
                        <td>
                            <input
                                className="form-control form-control-sm"
                                value={formData[item.id]?.name || ""}
                                onChange={(e) => handleChange(item.id, "name", e.target.value)}
                            />
                        </td>
                        <td>
                            <input
                                type={"number"}
                                className="form-control form-control-sm"
                                value={formData[item.id]?.post_id || ""}
                                onChange={(e) => handleChange(item.id, "post_id", e.target.value)}
                            />
                        </td>
                        <td>
                            <button data-testid={"item_update"} className="btn btn-primary btn-sm" onClick={() => fetchUpdate(item.id)}>
                                Update
                            </button>
                        </td>
                        <td>
                            <button data-testid={"item_delete"} className="btn btn-danger btn-sm" onClick={() => fetchDelete(item.id)}>
                                Delete
                            </button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}
