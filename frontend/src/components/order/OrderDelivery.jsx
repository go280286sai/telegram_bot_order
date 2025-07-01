import React, {useEffect, useState} from "react";
import log from "../../helps/logs.mjs";

export default function OrderDelivery({delivery}) {
    useEffect(() =>{
        console.log(delivery)
    }, [])
    const [formDelivery, setFormDelivery] = useState({
        name: "",
        city: "",
        address: ""
    });
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormDelivery(prev => ({...prev, [name]: value}));
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        fetch("http://localhost:8000/cart/delivery", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: formDelivery.name,
                city: formDelivery.city,
                address: formDelivery.address
            }),
            credentials: "include"
        }).then(res => res.json())
            .then((data) => {
                if (data.success) {
                    window.location.reload()
                } else {
                    log("error", "login error", data);
                }
            }).catch(data => log("error", "login error", data));
    };

    return (
        <div className={"col-8"}>
            {delivery === false ? (<div>
                <form className="modal-content" onSubmit={handleSubmit}>
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="loginLabel">Add delivery</h1>
                    </div>
                    <div className="modal-body">
                        <div className="mb-3">
                            <label htmlFor="nameDelivery" className="form-label">Select Post</label>
                            <input
                                type="text"
                                className="form-control"
                                id="nameDelivery"
                                name="name"
                                autoComplete="name"
                                value={formDelivery.name}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="cityDelivery" className="form-label">Select city</label>
                            <input
                                type="text"
                                className="form-control"
                                id="cityDelivery"
                                name="city"
                                autoComplete="city"
                                value={formDelivery.city}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="addressDelivery" className="form-label">Select address</label>
                            <input
                                type="text"
                                className="form-control"
                                id="addressDelivery"
                                name="address"
                                autoComplete="current-password"
                                value={formDelivery.address}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    </div>
                    <div className="modal-footer">
                        <button type="submit" className="btn btn-primary">Add Delivery</button>
                    </div>
                </form>
            </div>) : (

                <table className={"table table-dark"}>
                    <tbody>
                    <tr>
                        <th>Post service</th>
                        <td>{delivery.name}</td>
                    </tr>
                    <tr>
                        <th>City</th>
                        <td>{delivery.city}</td>
                    </tr>
                    <tr>
                        <th>Address</th>
                        <td>{delivery.address}</td>
                    </tr>
                    </tbody>
                </table>

            )}
        </div>
    )
}