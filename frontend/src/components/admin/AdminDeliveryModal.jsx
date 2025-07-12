import React, {useEffect, useState} from "react";
import log from "../../helps/logs.mjs";

export default function AdminDeliveryModal(){
    const [formData, setFormData] = useState({
        post: "",
        city: "",
        address: "",
    });
    const [selectPost, setSelectPost] = useState([])
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
    const fetchPost = async () => {
        try {
            const response = await fetch("http://localhost:8000/post/gets", {
                method: "GET",
                credentials: "include",
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            if (data.success) {
                setSelectPost(data.data.posts);
                console.log(data.data.posts)
            }
        } catch (error) {
            await log("error", "deliveries", error);
        }
    };
    useEffect(()=>{
        fetchPost();
    }, [])
    return (
        <div className="modal fade" id="addDelivery" tabIndex="-1" aria-labelledby="addProducts" aria-hidden="true">
           <div className="modal-dialog">
                <form className="modal-content" onSubmit={handleSubmit}>
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="ReviewLabel">Add new item delivery</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div className="modal-body">
                        <div className="mb-3">
                            <select className="form-select" aria-label="Default select example">
                                <option selected>Open this select menu</option>
                                <option value="1">One</option>
                                <option value="2">Two</option>
                                <option value="3">Three</option>
                            </select>
                            {/*<label htmlFor="Name_item" className="form-label">Post</label>*/}
                            {/*<input*/}
                            {/*    type="text"*/}
                            {/*    className="form-control"*/}
                            {/*    id="Name_item"*/}
                            {/*    name="name"*/}
                            {/*    autoComplete="name"*/}
                            {/*    value={formData.name}*/}
                            {/*    onChange={handleChange}*/}
                            {/*    required*/}
                            {/*/>*/}
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