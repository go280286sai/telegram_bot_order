import React, { useEffect, useState } from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import AdminAddSettingModal from "./AdminAddSettingModal";
import {
    AiOutlineInteraction,
    AiTwotoneFileAdd,
    AiOutlineDelete, AiFillCopy
} from "react-icons/ai";
export default function AdminSettings() {
    const [content, setContent] = useState([]);
    const [formData, setFormData] = useState({});

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
    useEffect(() => {
        fetchSetting();
    }, []);
    useEffect(() => {
        if (content.length > 0) {
            const dtInstance = new DataTable('#myTable');
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
                window.location.reload();
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
                window.location.reload();
            }
        } catch (error) {
            await log("error", "is_auth", error);
        }
    };
    const fetchAutoLoad = async () => {
        try {
            const response = await fetch("http://localhost:8000/setting/auto_create", {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
            });
            const data = await response.json();
            if (data.success) {
                window.location.reload();
            }
        } catch (error) {
            await log("error", "autoload error", error);
        }
    };
    return (
        <div className={"row block_1 p-1"}>
            <div className="mb-2 btn_with">
                <table>
                    <tbody>
                    <tr>
                        <td>
                            <button className={"btn btn-link btn_gen"} data-bs-toggle="modal"
                                    data-bs-target="#addSetting">
                                <AiTwotoneFileAdd className={"AiTwotoneFileAdd"} title={"Add"}/>
                            </button>
                        </td>
                        <td>
                            <button className={"btn btn-link btn_gen"} data-testid={"autoload"} onClick={()=> fetchAutoLoad()}>
                               <AiFillCopy className={"AiTwotoneFileAdd"} title={"Default"}/>
                            </button>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
            <AdminAddSettingModal/>
            <table id="myTable" className="display table table-dark">
                <thead>
                <tr>
                    <th>Id</th>
                    <th>Name</th>
                    <th>Value</th>
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
                                value={formData[item.id]?.value || ""}
                                onChange={(e) => handleChange(item.id, "value", e.target.value)}
                            />
                        </td>
                        <td>
                            <button data-testid={"item_update"} className="btn btn-link btn_gen" onClick={() => fetchUpdate(item.id)}>
                                <AiOutlineInteraction className={"AiOutlineInteraction"} title={"Update"}/>
                            </button>
                        </td>
                        <td>
                            <button data-testid={"item_delete"} className="btn btn-link btn_gen" onClick={()=>fetchDelete(item.id)}>
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
