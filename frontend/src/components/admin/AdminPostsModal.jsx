import React, {useState} from "react";
import log from "../../helps/logs.mjs";
import {AiFillCheckSquare, AiTwotoneCloseSquare} from "react-icons/ai";

export default function AdminPostsModal() {
    const [formData, setFormData] = useState({
        name: ""
    });
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };
    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch("http://localhost:8000/post/create", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: formData.name
                }),
                credentials: "include"
            });

            const data = await response.json();

            if (data.success) {
                window.location.reload();
            } else {
                await log("error", "add new item post error", data);
            }
        } catch (error) {
            await log("error", "add new item post error", error);
        }
    };

    return (
        <div className="modal fade" id="addPosts" tabIndex="-1" aria-labelledby="addPosts" aria-hidden="true">
            <div className="modal-dialog">
                <form className="modal-content" onSubmit={handleSubmit}>
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="ReviewLabel">Add new item post</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body">
                        <div className="mb-3">
                            <label htmlFor="Name_item" className="form-label">Name</label>
                            <input
                                type="text"
                                className="form-control"
                                id="Name_item"
                                name="name"
                                autoComplete="name"
                                value={formData.name}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    </div>
                    <div className="modal-footer">
                        <button type="button" className="btn btn-link btn_gen" data-bs-dismiss="modal">
                            <AiTwotoneCloseSquare className={"AiTwotoneCloseSquare"} title={"Exit"}/>
                        </button>
                        <button type="submit" className="btn btn-link btn_gen">
                            <AiFillCheckSquare className={"AiFillCheckSquare"} title={"Send"}/>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}
