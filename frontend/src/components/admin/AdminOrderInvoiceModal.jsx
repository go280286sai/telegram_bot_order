import React, {useEffect, useState} from "react";
import log from "../../helps/logs.mjs";

export default function AdminOrderInvoiceModal(){
    const [formData, setFormData] = useState({
        body: "",
        userId:"",
        orderId: ""
    });

    useEffect(() => {
        const modalEl = document.getElementById('SendInvoice');
        if (!modalEl) return;

        const handleShow = (event) => {
            const button = event.relatedTarget;
            const id_order = button.getAttribute('data-order-id');
            const id_user = button.getAttribute('data-user-id');
            setFormData(prev => ({
                ...prev,
                userId: id_user,
                orderId: id_order
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
            const response = await fetch(`http://localhost:8000/order/send_invoice/${formData.userId}/${formData.orderId}`,
                {
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
                log("error", "send invoice user error", data);
            }
        } catch (error) {
            console.log(formData.orderId, formData.userId)
            log("error", "send email invoice error", error);
        }
    };

    return (
        <div className="modal fade" id="SendInvoice" tabIndex="-1" aria-labelledby="SendInvoice" aria-hidden="true">
            <div className="modal-dialog">
                <form className="modal-content" onSubmit={handleSubmit}>
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="RecoverLabel">Send email</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div className="modal-body">
                        <div className="mb-3">
                            <label htmlFor="body_item" className="form-label">Invoice</label>
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
