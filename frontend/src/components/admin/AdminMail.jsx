import React, {useEffect, useState} from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import AdminMailModal from "./AdminMailModal";
import {
    AiFillCheckSquare,
    AiOutlineDelete,
    AiOutlineInteraction, AiOutlineMail,
    AiTwotoneFileAdd
} from "react-icons/ai";

export default function AdminMail() {
    const [content, setContent] = useState([]);
    const [formData, setFormData] = useState({});

    const fetchTemplates = async () => {
        try {
            const response = await fetch("http://localhost:8000/template/gets", {
                method: "GET",
                credentials: "include",
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            if (data.success) {
                setContent(data.data.templates);
                const initForm = {};
                data.data.templates.forEach(item => {
                    initForm[item.id] = {
                        header: item.header,
                        title: item.title,
                        body: item.body
                    };
                });
                setFormData(initForm);
            }
        } catch (error) {
            await log("error", "template", error);
        }
    };

    useEffect(() => {
        fetchTemplates();
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
        const {title, header, body} = formData[id];
        try {
            const response = await fetch(`http://localhost:8000/template/update/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({title, header, body})
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
            const response = await fetch(`http://localhost:8000/template/delete/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
            });
            const data = await response.json();
            if (data.success) {
                window.location.reload();
            }
        } catch (error) {
            await log("error", "templates", error);
        }
    };
    const fetchSendUsers = async (id) => {
        try {
            const response = await fetch(`http://localhost:8000/template/send_users/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
            });
            const data = await response.json();
            if (data.success) {
                window.location.reload();
            }
        } catch (error) {
            await log("error", "templates", error);
        }
    };
    const fetchSendSubscribers = async (id) => {
        try {
            const response = await fetch(`http://localhost:8000/subscriber/send_subscribers/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
            });
            const data = await response.json();
            if (data.success) {
                window.location.reload();
            }
        } catch (error) {
            await log("error", "templates", error);
        }
    };
    return (
        <div className={"row block_1 p-1"}>
            <div className="mb-2 btn_with">
                <button className={"btn btn-link btn_gen"} data-bs-toggle="modal" data-bs-target="#addTemplate">
                    <AiTwotoneFileAdd  className={"AiTwotoneFileAdd"} title={"Add template"}/>
                </button>
            </div>
            <AdminMailModal/>
            <table id="myTable" className="display table table-dark">
                <thead>
                <tr>
                    <th>Id</th>
                    <th>Header</th>
                    <th>Title</th>
                    <th>Body</th>
                    <th>Send users</th>
                    <th>Subscribers</th>
                    <th></th>
                    <th></th>
                </tr>
                </thead>
                <tbody>
                {content.map((item) => (
                    <tr key={item.id}>
                        <td>{item.id}</td>
                        <td>
                            <textarea
                                name="" id="" cols="5" rows="5"
                                className="form-control form-control-sm"
                                value={formData[item.id]?.header || ""}
                                onChange={(e) => handleChange(item.id, "header", e.target.value)}
                            />
                        </td>
                        <td>
                            <textarea
                                name="" id="" cols="5" rows="5"
                                className="form-control form-control-sm"
                                value={formData[item.id]?.title || ""}
                                onChange={(e) => handleChange(item.id, "title", e.target.value)}
                            />
                        </td>
                        <td>
                            <textarea
                                name="" id="" cols="10" rows="5"
                                className="form-control form-control-sm"
                                value={formData[item.id]?.body || ""}
                                onChange={(e) => handleChange(item.id, "body", e.target.value)}
                            />
                        </td>
                        <td>
                            <button type="button" className="btn btn-link btn_gen" onClick={() => fetchSendUsers(item.id)}
                                    data-testid="item_send_user">
                                <AiOutlineMail className={"AiOutlineMail"} title={"Send email users"}/>
                            </button>
                        </td>
                        <td>
                            <button type="button" className="btn btn-link btn_gen" onClick={() => fetchSendSubscribers(item.id)}
                                    data-testid="item_send_subscriber">
                                <AiOutlineMail className={"AiOutlineMail"} title={"Send subscribers"}/>
                            </button>
                        </td>
                        <td>
                            <button type="button" className="btn btn-link btn_gen" onClick={() => fetchUpdate(item.id)} data-testid="item_update">
                                <AiOutlineInteraction className={"AiOutlineInteraction"} title={"Update"}/>
                            </button>
                        </td>
                        <td>
                            <button type="button" className="btn btn-link btn_gen" onClick={() => fetchDelete(item.id)}
                                    data-testid="item_delete">
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
