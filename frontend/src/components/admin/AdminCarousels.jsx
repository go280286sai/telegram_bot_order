import React, { useEffect, useState } from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import AdminAddSettingModal from "./AdminAddSettingModal";
import AdminCarouselsModal from "./AdminCarouselsModal";

export default function AdminCarousels() {
    const [content, setContent] = useState([]);
    const [formData, setFormData] = useState({});

    // Загружаем данные
    const fetchCarousels = async () => {
        try {
            const response = await fetch("http://localhost:8000/front/carousel/gets", {
                method: "GET",
                credentials: "include",
                headers: { "Content-Type": "application/json" }
            });
            const data = await response.json();
            if (data.success) {
                setContent(data.data.carousels);

                // Создаём локальное состояние для редактирования
                const initForm = {};
                data.data.carousels.forEach(item => {
                    initForm[item.id] = {
                        title: item.title,
                        description: item.description,
                        image: item.image
                    };
                });
                setFormData(initForm);
            }
        } catch (error) {
            await log("error", "carousels", error);
        }
    };

    // Инициализация
    useEffect(() => {
            new DataTable('#myTable');
        fetchCarousels();
    }, []);

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

    // Отправка обновлений
    const fetchUpdate = async (id) => {
        const { title, description, image } = formData[id];
        try {
            const response = await fetch(`http://localhost:8000/front/carousel/update/${id}`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title, description, image })
            });
            const data = await response.json();
            if (data.success) {
                fetchCarousels();
            }
        } catch (error) {
            await log("error", "carousels", error);
        }
    };
    const fetchDelete = async (id) => {
        try {
            const response = await fetch(`http://localhost:8000/front/carousel/delete/${id}`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
            });
            const data = await response.json();
            if (data.success) {
                fetchCarousels();
            }
        } catch (error) {
            await log("error", "carousels", error);
        }
    };
    return (
        <div className={"row block_1 p-1"}>

            <div className="btn btn-success mb-2"
                 data-bs-toggle="modal"
                 data-bs-target="#addCarousels">Add item
            </div>
            <AdminCarouselsModal/>
            <table id="myTable" className="display table table-dark">
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Title</th>
                    <th>Description</th>
                    <th>Image</th>
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
                                value={formData[item.id]?.title || ""}
                                onChange={(e) => handleChange(item.id, "title", e.target.value)}
                            />
                        </td>
                        <td>
                            <input
                                className="form-control form-control-sm"
                                value={formData[item.id]?.description || ""}
                                onChange={(e) => handleChange(item.id, "description", e.target.value)}
                            />
                        </td>
                        <td>
                            <input
                                className="form-control form-control-sm"
                                value={formData[item.id]?.image || ""}
                                onChange={(e) => handleChange(item.id, "image", e.target.value)}
                            />
                        </td>
                        <td>
                            <button className="btn btn-primary btn-sm" onClick={() => fetchUpdate(item.id)}>
                                Update
                            </button>
                        </td>
                        <td>
                            <button className="btn btn-danger btn-sm" onClick={() => fetchDelete(item.id)}>
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
