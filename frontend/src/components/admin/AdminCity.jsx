import React, {useEffect, useState} from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import AdminCityModal from "./AdminCityModal";
import {AiOutlineDelete, AiOutlineInteraction, AiTwotoneFileAdd} from "react-icons/ai";

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
                const initForm = {};
                data.data.cities.forEach(item => {
                    initForm[item.id] = {
                        name: item.name,
                        post_id: item.post_id
                    };
                });
                setFormData(initForm);
            }
        } catch (error) {
            await log("error", "cities", error);
        }
    };
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
                window.location.reload();
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
                window.location.reload();
            }
        } catch (error) {
            await log("error", "cities", error);
        }
    };
    return (
        <div>
            <h3>Cities</h3>
            <div className={"center-vertical"}>
                <button className="btn btn-link mb-2 btn_with"
                        style={{border: "none", background: "none"}}
                        data-bs-toggle="modal"
                        data-bs-target="#addCity">
                    <AiTwotoneFileAdd className={"AiTwotoneFileAdd"} title={"Add city"}/>
                </button>
            </div>
            <AdminCityModal/>
            <table id="myTable2" className="display table table-dark">
                <thead>
                <tr>
                    <th>Id</th>
                    <th>Name</th>
                    <th>Post Id</th>
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
                                type={"number"}
                                className="form-control form-control-sm"
                                value={formData[item.id]?.post_id || ""}
                                onChange={(e) => handleChange(item.id, "post_id", e.target.value)}
                            />
                        </td>
                        <td>
                            <div className={"center-vertical"}>
                                <button data-testid={"item_update"} className="btn btn-link"
                                        style={{border: "none", background: "none"}}
                                        onClick={() => fetchUpdate(item.id)}>
                                    <AiOutlineInteraction className={"AiOutlineInteraction"} title={"Update"}/>
                                </button>
                            </div>

                        </td>
                        <td>
                            <div className={"center-vertical"}>
                                <button data-testid={"item_delete"} className="btn btn-danger btn-sm"
                                        onClick={() => fetchDelete(item.id)}
                                        style={{border: "none", background: "none"}}>
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
