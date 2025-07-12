import React, {useEffect, useState} from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import AdminAddSettingModal from "./AdminAddSettingModal";
import AdminCarouselsModal from "./AdminCarouselsModal";
import AdminReviewsModal from "./AdminReviewsModal";
import AdminProductsModal from "./AdminProductsModal";
import AdminDeliveryModal from "./AdminDeliveryModal";

export default function AdminDelivery() {
    const [content, setContent] = useState([]);
    const [formData, setFormData] = useState({});

    const fetchDelivery = async () => {
        try {
            const response = await fetch("http://localhost:8000/delivery/gets", {
                method: "GET",
                credentials: "include",
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            if (data.success) {
                setContent(data.data.deliveries);
                const initForm = {};
                data.data.deliveries.forEach(item => {
                    initForm[item.id] = {
                        post_id: item.post_name,
                        city_id: item.city_name,
                        address_id: item.address_name
                    };
                });
                setFormData(initForm);
            }
        } catch (error) {
            await log("error", "deliveries", error);
        }
    };

    // Инициализация
    useEffect(() => {
        new DataTable('#myTable');
        fetchDelivery();
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
    const fetchDelete = async (id) => {
        try {
            const response = await fetch(`http://localhost:8000/delivery/delete/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
            });
            const data = await response.json();
            if (data.success) {
                fetchDelivery();
            }
        } catch (error) {
            await log("error", "deliveries", error);
        }
    };
    return (
        <div className={"row block_1 p-1"}>

            <div className="btn btn-success mb-2"
                 data-bs-toggle="modal"
                 data-bs-target="#addDelivery">Add item
            </div>
            <AdminDeliveryModal/>
            <table id="myTable" className="display table table-dark">
                <thead>
                <tr>
                    <th>Id</th>
                    <th>Post</th>
                    <th>City</th>
                    <th>Address</th>
                    <th>Delete</th>
                </tr>
                </thead>
                <tbody>
                {content.map((item) => (
                    <tr key={item.delivery_id}>
                        <td>{item.delivery_id}</td>
                        <td>
                            <input
                                type={"text"}
                                className="form-control form-control-sm"
                                value={formData[item.id]?.post_id || ""}
                                onChange={(e) => handleChange(item.id, "post_id", e.target.value)}
                            />
                        </td>
                        <td>
                            <input
                                type={"text"}
                                className="form-control form-control-sm"
                                value={formData[item.id]?.city_id || ""}
                                onChange={(e) => handleChange(item.id, "city_id", e.target.value)}
                            />
                        </td>
                        <td>
                            <input
                                type={"text"}
                                className="form-control form-control-sm"
                                value={formData[item.id]?.address_id || ""}
                                onChange={(e) => handleChange(item.id, "address_id", e.target.value)}
                            />
                        </td>
                        <td>
                            <button className="btn btn-danger btn-sm" onClick={() => fetchDelete(item.delivery_id)}>
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
