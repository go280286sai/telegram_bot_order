import React, { useEffect, useState } from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import AdminAddSettingModal from "./AdminAddSettingModal";

export default function AdminSettings() {
    const [content, setContent] = useState([]);
    const [formData, setFormData] = useState({});

    // Загружаем данные
    const fetchSetting = async () => {
        try {
            const response = await fetch("http://localhost:8000/setting/gets", {
                method: "GET",
                credentials: "include",
                headers: { "Content-Type": "application/json" }
            });
            const data = await response.json();
            if (data.success) {
                setContent(data.data.settings);

                // Создаём локальное состояние для редактирования
                const initForm = {};
                data.data.settings.forEach(item => {
                    initForm[item.id] = {
                        name: item.name,
                        value: item.value
                    };
                });
                setFormData(initForm);
            }
        } catch (error) {
            await log("error", "is_auth", error);
        }
    };

    // Инициализация
    useEffect(() => {
            new DataTable('#myTable');
        fetchSetting();
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
        const { name, value } = formData[id];
        try {
            const response = await fetch(`http://localhost:8000/setting/update/${id}`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, value })
            });
            const data = await response.json();
            if (data.success) {
                fetchSetting();
            }
        } catch (error) {
            await log("error", "is_auth", error);
        }
    };
    const fetchDelete = async (id) => {
        try {
            const response = await fetch(`http://localhost:8000/setting/delete/${id}`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
            });
            const data = await response.json();
            if (data.success) {
                fetchSetting();
            }
        } catch (error) {
            await log("error", "is_auth", error);
        }
    };
    return (
        <div className={"row block_1 p-1"}>

            <div className="btn btn-success mb-2"
                 data-bs-toggle="modal"
                 data-bs-target="#addSetting">Add item
            </div>
            <AdminAddSettingModal/>
            <table id="myTable" className="display table table-dark">
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Name</th>
                    <th>Value</th>
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
                                className="form-control form-control-sm"
                                value={formData[item.id]?.value || ""}
                                onChange={(e) => handleChange(item.id, "value", e.target.value)}
                            />
                        </td>
                        <td>
                            <button className="btn btn-primary btn-sm" onClick={() => fetchUpdate(item.id)}>
                                Update
                            </button>
                        </td>
                        <td>
                            <button className="btn btn-danger btn-sm" onClick={()=>fetchDelete(item.id)}>
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
