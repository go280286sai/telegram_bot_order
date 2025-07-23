import React, { useEffect, useState } from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import AdminReviewsModal from "./AdminReviewsModal";

export default function AdminReviews() {
    const [content, setContent] = useState([]);
    const [formData, setFormData] = useState({});

    const fetchReviews = async () => {
        try {
            const response = await fetch("http://localhost:8000/review/reviews", {
                method: "GET",
                credentials: "include",
                headers: { "Content-Type": "application/json" }
            });
            const data = await response.json();
            if (data.success) {
                setContent(data.data.reviews);

                // Создаём локальное состояние для редактирования
                const initForm = {};
                data.data.reviews.forEach(item => {
                    initForm[item.id] = {
                        name: item.name,
                        text: item.text,
                        gender: item.gender.toString()
                    };
                });
                setFormData(initForm);
            }
        } catch (error) {
            await log("error", "reviews", error);
        }
    };

    // Инициализация
    useEffect(() => {
        fetchReviews();
    }, []);
    useEffect(() => {
        if (content.length > 0) {
            const dtInstance = new DataTable('#myTable3');
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
        const { name, text, gender } = formData[id];
        try {
            const response = await fetch(`http://localhost:8000/review/update/${id}`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, text, gender })
            });
            const data = await response.json();
            if (data.success) {
                fetchReviews();
            }
        } catch (error) {
            await log("error", "reviews", error);
        }
    };
    const fetchDelete = async (id) => {
        try {
            const response = await fetch(`http://localhost:8000/review/delete/${id}`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
            });
            const data = await response.json();
            if (data.success) {
                fetchReviews();
            }
        } catch (error) {
            await log("error", "reviews", error);
        }
    };
    return (
        <div className={"row block_1 p-1"}>

            <div className="btn btn-success mb-2 btn_with"
                 data-bs-toggle="modal"
                 data-bs-target="#addReviews">Add item
            </div>
            <AdminReviewsModal/>
            <table id="myTable" className="display table table-dark">
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Name</th>
                    <th>Text</th>
                    <th>Gender</th>
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
                                value={formData[item.id]?.text || ""}
                                onChange={(e) => handleChange(item.id, "text", e.target.value)}
                            />
                        </td>
                        <td>
                            <input
                                type={"number"}
                                className="form-control form-control-sm"
                                value={formData[item.id]?.gender || ""}
                                onChange={(e) => handleChange(item.id, "gender", e.target.value)}
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
