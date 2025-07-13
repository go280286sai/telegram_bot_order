import React, {useEffect, useState} from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import AdminAddressModal from "./AdminAddressModal";

export default function AdminAddress() {
    const [content, setContent] = useState([]);
    const [formData, setFormData] = useState({});

    const fetchAddresses = async () => {
        try {
            const response = await fetch("http://localhost:8000/address/gets", {
                method: "GET",
                credentials: "include",
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            if (data.success) {
                setContent(data.data.addresses);

                // Создаём локальное состояние для редактирования
                const initForm = {};
                data.data.addresses.forEach(item => {
                    initForm[item.id] = {
                        name: item.name,
                        city_id:item.city_id
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
        fetchAddresses();
    }, []);
    useEffect(() => {
        if (content.length > 0) {
            const dtInstance = new DataTable('#myTable1');
            return () => {
                dtInstance.destroy();
            };
        }
    }, [content]);
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
        const {name, city_id} = formData[id];
        try {
            const response = await fetch(`http://localhost:8000/address/update/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({name, city_id})
            });
            const data = await response.json();
            if (data.success) {
                fetchAddresses();
            }
        } catch (error) {
            await log("error", "address", error);
        }
    };
    const fetchDelete = async (id) => {
        try {
            const response = await fetch(`http://localhost:8000/address/delete/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
            });
            const data = await response.json();
            if (data.success) {
                fetchAddresses();
            }
        } catch (error) {
            await log("error", "address", error);
        }
    };
    return (
        <div>
            <h3>Addresses</h3>
            <div className="btn btn-success mb-2"
                 data-bs-toggle="modal"
                 data-bs-target="#addAddress">Add item
            </div>
            <AdminAddressModal/>
            <table id="myTable1" className="display table table-dark">
                <thead>
                <tr>
                    <th>Id</th>
                    <th>Name</th>
                    <th>Address Id</th>
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
                                value={formData[item.id]?.city_id || ""}
                                onChange={(e) => handleChange(item.id, "city_id", e.target.value)}
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
