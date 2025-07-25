import React, {useEffect, useState} from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import AdminPostsModal from "./AdminPostsModal";
import {AiOutlineDelete, AiOutlineInteraction, AiTwotoneFileAdd} from "react-icons/ai";

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
                window.location.reload();
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
                window.location.reload();
            }
        } catch (error) {
            await log("error", "products", error);
        }
    };
    return (
        <div>
            <h3>Post service</h3>
            <div className={"center-vertical"}>
                <button className="btn btn-link mb-2 btn_with btn_gen"
                        data-bs-toggle="modal"
                        data-bs-target="#addPosts">
                    <AiTwotoneFileAdd className={"AiTwotoneFileAdd"} title={"Add item"}/>
                </button>
            </div>
            <AdminPostsModal/>
            <table id="myTable3" className="display table table-dark">
                <thead>
                <tr>
                    <th>Id</th>
                    <th>Name</th>
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
