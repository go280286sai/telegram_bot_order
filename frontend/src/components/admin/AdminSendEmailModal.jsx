import React, {useEffect, useState} from "react";
import log from "../../helps/logs.mjs";
import {AiFillCheckSquare, AiTwotoneCloseSquare} from "react-icons/ai";

export default function AdminSendEmailModal() {
    const [formData, setFormData] = useState({
        header: "",
        title: "",
        body: "",
        toId: "",
        toEmail: ""
    });

    useEffect(() => {
        const modalEl = document.getElementById('SendEmail');
        if (!modalEl) return;

        const handleShow = (event) => {
            const button = event.relatedTarget;
            const id = button.getAttribute('data-user-id');
            const email = button.getAttribute('data-user-email');
            setFormData(prev => ({
                ...prev,
                toId: id,
                toEmail: email
            }));
        };
        modalEl.addEventListener('show.bs.modal', handleShow);
        return () => {
            modalEl.removeEventListener('show.bs.modal', handleShow);
        };
    }, []);

    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`http://localhost:8000/user/send_email/${formData.toId}/${formData.toEmail}`, {
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
            });
            const data = await response.json();
            if (data.success) {
                alert("Done");
            } else {
                log("error", "send email user error", data);
            }
        } catch (error) {
            log("error", "send email user error", error);
        }
    };

    return (
        <div className="modal fade" id="SendEmail" tabIndex="-1" aria-labelledby="SendEmail" aria-hidden="true">
            <div className="modal-dialog">
                <form className="modal-content" onSubmit={handleSubmit}>
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="RecoverLabel">Send email</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div className="modal-body">
                        <div className="mb-3">
                            <label htmlFor="header_item" className="form-label">Header</label>
                            <input
                                type="text"
                                className="form-control"
                                id="header_item"
                                name="header"
                                autoComplete="title"
                                value={formData.header}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="title_item" className="form-label">Title</label>
                            <input
                                type="text"
                                className="form-control"
                                id="title_item"
                                name="title"
                                autoComplete="title"
                                value={formData.title}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="body_item" className="form-label">Body</label>
                            <input
                                type="text"
                                className="form-control"
                                id="body_item"
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
    );
}
