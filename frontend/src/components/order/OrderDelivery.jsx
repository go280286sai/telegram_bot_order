import React, {useEffect, useState} from "react";
import log from "../../helps/logs.mjs";
import OrderPay from "./OrderPay";

export default function OrderDelivery({total}) {
    const [deliveries, setDeliveries] = useState([]);
    const [delivery, setDelivery] = useState(null);
    const [statusDelivery, setStatusDelivery] = useState(false);
    const [formDelivery, setFormDelivery] = useState({id: ""});

    useEffect(() => {
        fetchCurrentDelivery();
        fetchAllDeliveries();
    }, []);

    const fetchAllDeliveries = async () => {
        try {
            const res = await fetch("http://localhost:8000/delivery/gets", {
                method: "GET",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
            });
            const data = await res.json();
            if (data.success) {
                setDeliveries(data.data.deliveries);
            }
        } catch (error) {
            await log("error", "fetchAllDeliveries", error);
        }
    };

    const fetchCurrentDelivery = async () => {
        try {
            const res = await fetch("http://localhost:8000/cart/delivery/get", {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
            });
            const data = await res.json();
            if (data.success) {
                setDelivery(data.data);
                setStatusDelivery(true);
            }
        } catch (error) {
            await log("error", "fetchCurrentDelivery", error);
        }
    };

    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormDelivery(prev => ({...prev, [name]: value}));
    };

    const handleSubmit = async () => {
        try {
            const res = await fetch(`http://localhost:8000/cart/delivery/create/${formDelivery.id}`, {
                method: "POST",
                credentials: "include",
            });
            const data = await res.json();
            if (data.success) {
                window.location.reload();
            } else {
                await log("error", "createDelivery", data);
            }
        } catch (error) {
            await log("error", "createDelivery", error);
        }
    };

    const deleteDelivery = async () => {
        try {
            const res = await fetch("http://localhost:8000/cart/delivery/delete", {
                method: "POST",
                credentials: "include",
            });
            const data = await res.json();
            if (data.success) {
                window.location.reload();
            } else {
                await log("error", "deleteDelivery", data);
            }
        } catch (error) {
            await log("error", "deleteDelivery", error);
        }
    };

    return (
        <div className="col-8">
            {!statusDelivery ? (
                <>
                    <div className="modal-body">
                        <div className="mb-3">
                            <label htmlFor="nameDelivery" className="form-label">Add delivery</label>
                            <select
                                className="form-select"
                                id="nameDelivery"
                                name="id"
                                value={formDelivery.id}
                                onChange={handleChange}
                                required
                            >
                                <option value="">Select delivery method</option>
                                {deliveries.map((item, index) => (
                                    <option key={index} value={item.delivery_id}>
                                        {item.post_name} {item.city_name} {item.address_name}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <div className="modal-footer">
                            <button
                                onClick={handleSubmit}
                                className="btn btn-primary"
                            >
                                Add Delivery
                            </button>
                        </div>
                    </div>
                </>
            ) : (
                <table className="table table-dark">
                    <tbody>
                    <tr>
                        <th>Post service</th>
                        <td>{delivery?.post_name}</td>
                    </tr>
                    <tr>
                        <th>City</th>
                        <td>{delivery?.city_name}</td>
                    </tr>
                    <tr>
                        <th>Address</th>
                        <td>{delivery?.address_name}</td>
                    </tr>
                    </tbody>
                </table>
            )}

            {statusDelivery && (
                <input
                    type="button"
                    value="Delete"
                    className="btn btn-danger mb-3"
                    onClick={deleteDelivery}
                />
            )}

            <OrderPay total={total}/>
            <br/>
            <input
                type="button"
                className="btn btn-success mt-3"
                value="To pay"
                data-bs-toggle="modal"
                data-bs-target="#to_pay"
            />

        </div>
    );
}
