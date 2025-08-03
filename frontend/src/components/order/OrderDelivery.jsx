import React, {useEffect, useState} from "react";
import log from "../../helps/logs.mjs";
import OrderPay from "./OrderPay";
import OrderDeliveryModal from "./OrderDeliveryModal";
import {IoWallet} from "react-icons/io5";
import {AiFillTruck, AiOutlineDelete} from "react-icons/ai";

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
                            <div className="btn btn-link mb-2 btn_gen"
                                 data-bs-toggle="modal"
                                 data-bs-target="#addDelivery">
                                <AiFillTruck className={"AiFillTruck "} title={"Add delivery"}/>
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
                    <button
                        value="Delete"
                        className="btn btn-link mb-3 btn_gen"
                        onClick={deleteDelivery}
                        data-testid={"deleteDelivery"}>
                        <AiOutlineDelete className={"AiOutlineDelete"} title={"Delete"}/>
                    </button>

                    <OrderPay total={total}/>
                    <br/>
                    <button
                        className="btn btn-link mt-3 btn_gen"
                        value="To pay"
                        data-bs-toggle="modal"
                        data-bs-target="#to_pay">
                        <IoWallet className={"IoWallet"} title={"To pay"}/>
                    </button>
                </>
            )}
        </div>
    );
}
