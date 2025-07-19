import React, {useEffect, useState} from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import {fetchAuth} from "./fetchAuth";
import AdminSendEmailModal from "./AdminSendEmailModal";

export default function AdminUsers() {
    const [content, setContent] = useState([]);
    const [formData, setFormData] = useState({});


    const fetchUsers = async () => {
        try {
            fetchAuth();
            const response = await fetch("http://localhost:8000/user/gets", {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            if (data.success) {
                setContent(data.data.users);
                const initForm = {};
                data.data.users.forEach(item => {
                    initForm[item.id] = {
                        username: item.username,
                        email: item.email,
                        phone: item.phone,
                        status: item.status,
                        comments: item.comments,
                        is_admin: item.is_admin,
                        first_name: item.first_name,
                        last_name: item.last_name,
                        created_at: item.created_at.toString()
                    };
                });
                setFormData(initForm);
            }
        } catch (error) {
            await log("error", "users", error);
        }
    };

    // Инициализация
    useEffect(() => {
        fetchUsers();
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
        const {username, email, phone, comments, first_name, last_name} = formData[id];
        try {
            const response = await fetch("http://localhost:8000/user/update", {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({username, email, phone, comments, first_name, last_name})
            });
            const data = await response.json();
            if (data.success) {
                fetchUsers();
            }
        } catch (error) {
            await log("error", "users", error);
        }
    };
    const fetchSetStatus = async (id, stat) => {
        try {
            const response = await fetch(`http://localhost:8000/user/set_status/${id}/${stat}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
            });
            const data = await response.json();
            if (data.success) {
                fetchUsers();
            }
        } catch (error) {
            await log("error", "users", error);
        }
    };
    const fetchResetPassword = async (username, email) => {
        try {
            const response = await fetch("http://localhost:8000/user/recovery/", {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    username: username,
                    email: email
                })
            });
            const data = await response.json();
            if (data.success) {
                alert("Done");
            }
        } catch (error) {
            await log("error", "users", error);
        }
    };
    const fetchSetAdminStatus = async (id, stat) => {
        try {
            const response = await fetch(`http://localhost:8000/user/set_status_admin/${id}/${stat}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
            });
            const data = await response.json();
            if (data.success) {
                fetchUsers();
            }
        } catch (error) {
            await log("error", "users", error);
        }
    };
    const fetchDelete = async (id) => {
        try {
            const response = await fetch(`http://localhost:8000/user/delete/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
            });
            const data = await response.json();
            if (data.success) {
                window.location.reload();
            }
        } catch (error) {
            await log("error", "users", error);
        }
    };
    return (
        <div className={"row block_1 p-1"}>
            <table id="myTable" className="display table table-dark">
                <thead>
                <tr>
                    <th>Id</th>
                    <th>Name</th>
                    <th>First name</th>
                    <th>Last name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Comments</th>
                    <th>Update</th>
                    <th>Send email</th>
                    <th>Status</th>
                    <th>Is admin</th>
                    <th>Reset password</th>
                    <th>Delete</th>
                    <th>Created</th>
                </tr>
                </thead>
                <tbody>
                {content.map((item) => (
                    <tr key={item.id}>
                        <td>{item.id}</td>
                        <td>
                            <input
                                type={"text"}
                                className="form-control form-control-sm"
                                value={formData[item.id]?.username || ""}
                                onChange={(e) => handleChange(item.id, "username", e.target.value)}
                            />
                        </td>
                        <td>
                            <input
                                type={"text"}
                                className="form-control form-control-sm"
                                value={formData[item.id]?.first_name || ""}
                                onChange={(e) => handleChange(item.id, "first_name", e.target.value)}
                            />
                        </td>
                        <td>
                            <input
                                type={"text"}
                                className="form-control form-control-sm"
                                value={formData[item.id]?.last_name || ""}
                                onChange={(e) => handleChange(item.id, "last_name", e.target.value)}
                            />
                        </td>
                        <td>
                            <input
                                type={"text"}
                                className="form-control form-control-sm"
                                value={formData[item.id]?.email || ""}
                                onChange={(e) => handleChange(item.id, "email", e.target.value)}
                            />
                        </td>
                        <td>
                            <input
                                type={"text"}
                                className="form-control form-control-sm"
                                value={formData[item.id]?.phone || ""}
                                onChange={(e) => handleChange(item.id, "phone", e.target.value)}
                            />
                        </td>
                        <td>
                            <textarea
                                className="form-control form-control-sm"
                                value={formData[item.id]?.comments || ""}
                                onChange={(e) => handleChange(item.id, "comments", e.target.value)}
                                id="floatingTextarea"></textarea>
                        </td>
                        <td>
                            <button className="btn btn-primary btn-sm" onClick={() => fetchUpdate(item.id)}>
                                Update
                            </button>
                        </td>
                        <td>
                            <div className="btn btn-success btn-sm"
                                 data-bs-toggle="modal"
                                 data-bs-target="#SendEmail"
                                 data-user-id={item.id}
                                 data-user-email={formData[item.id]?.email || ""}
                            >Send
                            </div>

                        </td>
                        <td>
                            {item.status ? (
                                <div>
                                    <input type="button" className={"btn btn-danger btn-sm"} value={"Deactive"}
                                           onClick={() => {
                                               fetchSetStatus(item.id, 0)
                                           }}/>
                                </div>
                            ) : (
                                <div>
                                    <input type="button" className={"btn btn-success btn-sm"} value={"Active"}
                                           onClick={() => {
                                               fetchSetStatus(item.id, 1)
                                           }}/>
                                </div>
                            )}
                        </td>
                        <td>
                            {item.is_admin ? (
                                <div>
                                    <input type="button" className={"btn btn-danger btn-sm"} value={"Deactive"}
                                           onClick={() => {
                                               fetchSetAdminStatus(item.id, 0)
                                           }}/>
                                </div>
                            ) : (
                                <div>
                                    <input type="button" className={"btn btn-success btn-sm"} value={"Active"}
                                           onClick={() => {
                                               fetchSetAdminStatus(item.id, 1)
                                           }}/>
                                </div>
                            )}
                        </td>
                        <td>
                            <div>
                                <input type="button" className={"btn btn-success btn-sm"} value={"Reset"}
                                       onClick={() => {
                                           fetchResetPassword(item.username, item.email)
                                       }}/>
                            </div>
                        </td>
                        <td>
                            <button className="btn btn-danger btn-sm" onClick={() => fetchDelete(item.id)}>
                                Delete
                            </button>
                        </td>
                        <td>
                            {item.created_at}
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
            <AdminSendEmailModal/>
        </div>
    );
}
