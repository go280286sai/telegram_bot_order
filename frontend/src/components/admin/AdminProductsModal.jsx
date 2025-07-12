import React, {useState} from "react";
import log from "../../helps/logs.mjs";

export default function AdminProductsModal(){
    const [formData, setFormData] = useState({
        name: "",
        description: "",
        amount: "",
        price: "",
        service: ""
    });
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        fetch("http://localhost:8000/product/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: formData.name,
                description: formData.description,
                amount: formData.amount,
                price: formData.price,
                service: formData.service
            }),
            credentials: "include"
        }).then(res => res.json())
            .then((data) => {
                if (data.success) {
                    window.location.reload()
                } else {
                    log("error", "add new item product error", data);
                }
            }).catch(data => log("error", "add new item product error", data));
    };
    return (
        <div className="modal fade" id="addProducts" tabIndex="-1" aria-labelledby="addProducts" aria-hidden="true">
           <div className="modal-dialog">
                <form className="modal-content" onSubmit={handleSubmit}>
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="ReviewLabel">Add new item product</h1>
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
                        <div className="mb-3">
                            <label htmlFor="description_item" className="form-label">Description</label>
                            <input
                                type="text"
                                className="form-control"
                                id="description_item"
                                name="description"
                                autoComplete="description"
                                value={formData.description}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="amount_item" className="form-label">Amount</label>
                            <input
                                type="number"
                                className="form-control"
                                id="amount_item"
                                name="amount"
                                autoComplete="amount"
                                value={formData.amount}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="price_item" className="form-label">Price</label>
                            <input
                                type="number"
                                className="form-control"
                                id="price_item"
                                name="price"
                                autoComplete="price"
                                value={formData.price}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="service_item" className="form-label">Service</label>
                            <input
                                type="number"
                                className="form-control"
                                id="service_item"
                                name="service"
                                autoComplete="service"
                                value={formData.service}
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
    )
}