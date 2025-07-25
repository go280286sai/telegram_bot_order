import React, {useState} from "react";
import log from "../../helps/logs.mjs";
import 'draft-js/dist/Draft.css';
import {
    AiOutlineInteraction,
    AiOutlineRest,
    AiOutlineRightSquare,
    AiTwotoneFileAdd,
    AiTwotoneCloseSquare, AiFillCheckSquare
} from "react-icons/ai";

export default function AdminMailModal() {
    const [formData, setFormData] = useState({
        header: "",
        title: "",
        body: "",
    });
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        fetch("http://localhost:8000/template/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                header: formData.header,
                title: formData.title,
                body: formData.body
            }),
            credentials: "include"
        }).then(res => res.json())
            .then((data) => {
                if (data.success) {
                    window.location.reload()
                } else {
                    log("error", "add new item template error", data);
                }
            }).catch(data => log("error", "add new item template error", data));
    };
    return (
        <div className="modal fade" id="addTemplate" tabIndex="-1" aria-labelledby="addTemplate" aria-hidden="true">
            <div className="modal-dialog">
                <form className="modal-content" onSubmit={handleSubmit}>
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="ReviewLabel">Add new template</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div className="modal-body">
                        <div className="mb-3">
                            <label htmlFor="Header_item" className="form-label">Header</label>
                            <input
                                type="text"
                                className="form-control"
                                id="Header_item"
                                name="header"
                                autoComplete="header"
                                value={formData.header}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="Title_item" className="form-label">Title</label>
                            <input
                                type="text"
                                className="form-control"
                                id="Title_item"
                                name="title"
                                autoComplete="title"
                                value={formData.title}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="Body_item" className="form-label">Body</label>
                            <textarea cols="30" rows="10"
                                      className="form-control"
                                      id="Body_item"
                                      name="body"
                                      autoComplete="body"
                                      value={formData.body}
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
