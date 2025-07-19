import React, {useEffect, useState} from "react";
import log from "../../helps/logs.mjs";

export default function AdminOrderCommentModal(){
    const [formData, setFormData] = useState({
        body: "",
        toId: "",
    });

    useEffect(() => {
        const modalEl = document.getElementById('AddOrderComment');
        if (!modalEl) return;

        const handleShow = (event) => {
            const button = event.relatedTarget;
            const id = button.getAttribute('data-orders-id');
            setFormData(prev => ({
                ...prev,
                toId: id
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
            const response = await fetch(`http://localhost:8000/order/add_comment/${formData.toId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    body: formData.body
                }),
                credentials: "include"
            });
            const data = await response.json();
            if (data.success) {
                window.location.reload();
            } else {
                log("error", "add comment error", data);
            }
        } catch (error) {
            log("error", "add comment error", error);
        }
    };

    return (
        <div className="modal fade" id="AddOrderComment" tabIndex="-1" aria-labelledby="AddOrderComment" aria-hidden="true">
            <div className="modal-dialog">
                <form className="modal-content" onSubmit={handleSubmit}>
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="RecoverLabel">Add order comment</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div className="modal-body">
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
                        <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Exit</button>
                        <button type="submit" className="btn btn-primary">Send</button>
                    </div>
                </form>
            </div>
        </div>
    );
}
