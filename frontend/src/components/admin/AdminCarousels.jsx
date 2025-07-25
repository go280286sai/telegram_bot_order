import React, {useEffect, useState} from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import AdminCarouselsModal from "./AdminCarouselsModal";
import {AiOutlineDelete, AiOutlineInteraction, AiTwotoneFileAdd} from "react-icons/ai";

export default function AdminCarousels() {
    const [content, setContent] = useState([]);
    const [formData, setFormData] = useState({});
    const fetchCarousels = async () => {
        try {
            const response = await fetch("http://localhost:8000/front/carousel/gets", {
                method: "GET",
                credentials: "include",
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            if (data.success) {
                setContent(data.data.carousels);
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
    useEffect(() => {
        fetchCarousels();
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
        const {title, description, image} = formData[id];
        try {
            const response = await fetch(`http://localhost:8000/front/carousel/update/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({title, description, image})
            });
            const data = await response.json();
            if (data.success) {
                window.location.reload();
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
                headers: {"Content-Type": "application/json"},
            });
            const data = await response.json();
            if (data.success) {
                window.location.reload();
            }
        } catch (error) {
            await log("error", "carousels", error);
        }
    };
    return (
        <div className={"row block_1 p-1"}>
<div className={"center-vertical"}>
    <button className="btn btn-link mb-2 btn_with btn_gen"
                 data-bs-toggle="modal"
                 data-bs-target="#addCarousels">
        <AiTwotoneFileAdd className={"AiTwotoneFileAdd"} title={"Add item"}/>
    </button>
</div>
            <AdminCarouselsModal/>
            <table id="myTable" className="display table table-dark">
                <thead>
                <tr>
                    <th>Id</th>
                    <th>Title</th>
                    <th>Description</th>
                    <th>Image</th>
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
                            <button data-testid={"item_update"} className="btn btn-link btn_gen"
                                    onClick={() => fetchUpdate(item.id)}>
                                <AiOutlineInteraction className={"AiOutlineInteraction"} title={"Update"}/>
                            </button>
                        </td>
                        <td>
                            <button data-testid={"item_delete"} className="btn btn-link btn_gen"
                                    onClick={() => fetchDelete(item.id)}>
                                <AiOutlineDelete className={"AiOutlineDelete"} title={"Delete"}/>
                            </button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}
