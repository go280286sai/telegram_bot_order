import React, {useEffect, useState} from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import {fetchAuth} from "./fetchAuth";
import AdminSendEmailModal from "./AdminSendEmailModal";
import {
    AiOutlineInteraction,
    AiOutlineMail, AiOutlineDelete
} from "react-icons/ai";
import {IoLockClosedSharp, IoLockOpen, IoReloadCircleSharp} from "react-icons/io5";

export default function AdminUsers() {
    const [content, setContent] = useState([]);
    const [formData, setFormData] = useState({});
    const fetchUsers = async () => {
        try {
            await fetchAuth();
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
                        bonus: item.bonus,
                        created_at: item.created_at.toString()
                    };
                });
                setFormData(initForm);
            }
        } catch (error) {
            await log("error", "users", error);
        }
    };

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
                await fetchUsers();
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
                await fetchUsers();
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
                await fetchUsers();
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
                    <th>First</th>
                    <th>Last</th>
                    <th>Bonus</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Comments</th>
                    <th></th>
                    <th></th>
                    <th>Status</th>
                    <th>Admin</th>
                    <th>Reset</th>
                    <th></th>
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
                        <td>{formData[item.id]?.bonus || ""}</td>
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
                            <div>
                                <button data-testid={"item_update"} className="btn btn-link btn_gen"
                                        onClick={() => fetchUpdate(item.id)}>
                                    <AiOutlineInteraction className={"AiOutlineInteraction"} title={"Update"}/>
                                </button>
                            </div>
                        </td>
                        <td>
                            <div>
                                <button
                                    className="btn btn-link btn_gen" data-bs-toggle="modal"
                                    data-bs-target="#SendEmail"
                                    data-user-id={item.id}
                                    data-user-email={formData[item.id]?.email || ""}>
                                    <AiOutlineMail className={"AiOutlineMail"} title={"Send email"}/></button>
                            </div>
                        </td>
                        <td>
                            {item.status ? (
                                <div className={"center-vertical"}>
                                    <button className={"btn btn-link btn_gen"} value={"Deactivate"}
                                            onClick={() => {
                                                fetchSetStatus(item.id, 0)
                                            }}>
                                        <IoLockOpen className={"IoLockOpen"} title={"Deactivate"}/></button>
                                </div>
                            ) : (
                                <div className={"center-vertical"}>
                                    <button className={"btn btn-link btn_gen"}
                                            value={"Active"}
                                            onClick={() => {
                                                fetchSetStatus(item.id, 1)
                                            }}>
                                        <IoLockClosedSharp className={"IoLockClosedSharp"} title={"Active"}/></button>
                                </div>
                            )}
                        </td>
                        <td>
                            {item.is_admin ? (
                                <div className={"center-vertical"}>
                                    <button className={"btn btn-link btn_gen"} value={"Deactivate"}
                                            onClick={() => {
                                                fetchSetAdminStatus(item.id, 0)
                                            }}>
                                        <IoLockOpen className={"IoLockOpen"} title={"Deactivate"}/></button>
                                </div>
                            ) : (
                                <div className={"center-vertical"}>
                                    <button className={"btn btn-link btn_gen"} value={"Active"}
                                            onClick={() => {
                                                fetchSetAdminStatus(item.id, 1)
                                            }}>
                                        <IoLockClosedSharp className={"IoLockClosedSharp"} title={"Active"}/></button>
                                </div>
                            )}
                        </td>
                        <td>
                            <div className={"center-vertical"}>
                                <button className={"btn btn-link btn_gen"} value={"Reset"}
                                        onClick={() => {
                                            fetchResetPassword(item.username, item.email)
                                        }}>
                                    <IoReloadCircleSharp className={"IoReloadCircleSharp"} title={"Reset password"}/>
                                </button>
                            </div>
                        </td>
                        <td>
                            <div className={"center-vertical"}>
                                <button className="btn btn-link btn_gen"
                                        onClick={() => fetchDelete(item.id)}>
                                    <AiOutlineDelete className={"AiOutlineDelete"} title={"Delete"}/>
                                </button>
                            </div>
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
