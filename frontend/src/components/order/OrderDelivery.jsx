import React, {useEffect, useState} from "react";
import log from "../../helps/logs.mjs";
import OrderPay from "./OrderPay";
import OrderDeliveryModal from "./OrderDeliveryModal";

export default function OrderDelivery({total}) {
    const [delivery, setDelivery] = useState(null);
    const [statusDelivery, setStatusDelivery] = useState(false);

    useEffect(() => {
        fetchCurrentDelivery();
    }, []);


    const fetchCurrentDelivery = async () => {
        try {
            const res = await fetch("http://localhost:8000/cart/delivery/get", {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
            });
            const data = await res.json();
            console.log(data)
            if (data.success) {
                setDelivery(data.data);
                setStatusDelivery(true);
            }
        } catch (error) {
            await log("error", "fetchCurrentDelivery", error);
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
                        <div className="modal-footer">
                            <OrderDeliveryModal/>
                            <div className="btn btn-success mb-2"
                                 data-bs-toggle="modal"
                                 data-bs-target="#addDelivery">Add item
                            </div>
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
                <>
                <input
                    type="button"
                    value="Delete"
                    className="btn btn-danger mb-3"
                    onClick={deleteDelivery}
                />

                    <OrderPay total={total}/>
                    <br/>
                    <input
                        type="button"
                        className="btn btn-success mt-3"
                        value="To pay"
                        data-bs-toggle="modal"
                        data-bs-target="#to_pay"
                    />

</>
            )}



        </div>
    );
}
