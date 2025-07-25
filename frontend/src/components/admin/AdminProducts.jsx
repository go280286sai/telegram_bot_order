import React, {useEffect, useState} from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import AdminProductsModal from "./AdminProductsModal";
import {
    AiOutlineDelete,
    AiOutlineInteraction,
    AiTwotoneFileAdd
} from "react-icons/ai";

export default function AdminProducts() {
    const [content, setContent] = useState([]);
    const [formData, setFormData] = useState({});

    const fetchProducts = async () => {
        try {
            const response = await fetch("http://localhost:8000/product/products", {
                method: "GET",
                credentials: "include",
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            if (data.success) {
                setContent(data.data.products);
                const initForm = {};
                data.data.products.forEach(item => {
                    initForm[item.id] = {
                        name: item.name,
                        description: item.description,
                        amount: item.amount,
                        service: item.service.toString(),
                        price: item.price,
                    };
                });
                setFormData(initForm);
            }
        } catch (error) {
            await log("error", "products", error);
        }
    };

    useEffect(() => {
        fetchProducts();
    }, []);
    useEffect(() => {
        if (content.length > 0) {
            const dtInstance = new DataTable('#myTable');
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
        const {name, description, amount, service, price} = formData[id];
        try {
            const response = await fetch(`http://localhost:8000/product/update/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({name, description, amount, service, price})
            });
            const data = await response.json();
            if (data.success) {
                window.location.reload();
            }
        } catch (error) {
            await log("error", "products", error);
        }
    };
    const fetchDelete = async (id) => {
        try {
            const response = await fetch(`http://localhost:8000/product/delete/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
            });
            const data = await response.json();
            if (data.success) {
                window.location.reload();
            }
        } catch (error) {
            await log("error", "products", error);
        }
    };
    return (
        <div className={"row block_1 p-1"}>
            <div className={"center-vertical"}>
                <button className="btn btn-link mb-2 btn_with btn_gen"
                        data-bs-toggle="modal"
                        data-bs-target="#addProducts">
                    <AiTwotoneFileAdd className={"AiTwotoneFileAdd"} title={"Add product"}/>
                </button>
            </div>
            <AdminProductsModal/>
            <table id="myTable" className="display table table-dark">
                <thead>
                <tr>
                    <th>Id</th>
                    <th>Name</th>
                    <th>Description</th>
                    <th>Amount</th>
                    <th>Service</th>
                    <th>Price</th>
                    <th></th>
                    <th></th>
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
                                value={formData[item.id]?.description || ""}
                                onChange={(e) => handleChange(item.id, "description", e.target.value)}
                            />
                        </td>
                        <td>
                            <input
                                type={"number"}
                                className="form-control form-control-sm"
                                value={formData[item.id]?.amount || ""}
                                onChange={(e) => handleChange(item.id, "amount", e.target.value)}
                            />
                        </td>
                        <td>
                            <input
                                type={"number"}
                                className="form-control form-control-sm"
                                value={formData[item.id]?.service || ""}
                                onChange={(e) => handleChange(item.id, "service", e.target.value)}
                            />
                        </td>
                        <td>
                            <input
                                type={"number"}
                                className="form-control form-control-sm"
                                value={formData[item.id]?.price || ""}
                                onChange={(e) => handleChange(item.id, "price", e.target.value)}
                            />
                        </td>
                        <td>
                            <div className={"center-vertical"}>
                                <button data-testid={"item_update"} className="btn btn-link btn_gen"
                                        onClick={() => fetchUpdate(item.id)}>
                                    <AiOutlineInteraction className={"AiOutlineInteraction"} title={"Update"}/>
                                </button>
                            </div>
                        </td>
                        <td>
                            <div className={"center-vertical"}>
                                <button data-testid={"item_delete"} className="btn btn-link btn_gen"
                                        onClick={() => fetchDelete(item.id)}>
                                    <AiOutlineDelete className={"AiOutlineDelete"} title={"Delete"}/>
                                </button>
                            </div>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}
