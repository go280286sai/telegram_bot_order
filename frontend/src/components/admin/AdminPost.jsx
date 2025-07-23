import React, {useEffect, useState} from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import AdminPostsModal from "./AdminPostsModal";

export default function AdminPost() {
    const [content, setContent] = useState([]);
    const [formData, setFormData] = useState({});

    const fetchPosts = async () => {
        try {
            const response = await fetch("http://localhost:8000/post/gets", {
                method: "GET",
                credentials: "include",
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            if (data.success) {
                setContent(data.data.posts);

                // Создаём локальное состояние для редактирования
                const initForm = {};
                data.data.posts.forEach(item => {
                    initForm[item.id] = {
                        name: item.name
                    };
                });
                setFormData(initForm);
            }
        } catch (error) {
            await log("error", "products", error);
        }
    };

    // Инициализация
    useEffect(() => {
        fetchPosts();
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
        const {name} = formData[id];
        try {
            const response = await fetch(`http://localhost:8000/post/update/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({name})
            });
            const data = await response.json();
            if (data.success) {
                fetchPosts();
            }
        } catch (error) {
            await log("error", "products", error);
        }
    };
    const fetchDelete = async (id) => {
        try {
            const response = await fetch(`http://localhost:8000/post/delete/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
            });
            const data = await response.json();
            if (data.success) {
                fetchPosts();
            }
        } catch (error) {
            await log("error", "products", error);
        }
    };
    return (
        <div>
            <h3>Post service</h3>
            <div className="btn btn-success mb-2 btn_with"
                 data-bs-toggle="modal"
                 data-bs-target="#addPosts">Add item
            </div>
            <AdminPostsModal/>
            <table id="myTable3" className="display table table-dark">
                <thead>
                <tr>
                    <th>Id</th>
                    <th>Name</th>
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
