import React, {useEffect, useState} from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import AdminOrderInvoiceModal from "./AdminOrderInvoiceModal";
import AdminOrderCommentModal from "./AdminOrderCommentlModal";
import AdminOrderViewModal from "./AdminOrderViewModal";
import {IoSearch, IoTime, IoTrophySharp} from "react-icons/io5";
import {AiOutlineDelete, AiTwotoneFileAdd} from "react-icons/ai";

export default function AdminOrders() {
    const [content, setContent] = useState([]);

    const fetchOrders = async () => {
        try {
            const response = await fetch("http://localhost:8000/order/gets", {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            if (data.success) {
                setContent(data.data.orders);
            }
        } catch (error) {
            await log("error", "orders", error);
        }
    };

    useEffect(() => {
        fetchOrders();
    }, []);
    useEffect(() => {
        if (content.length > 0) {
            const dtInstance = new DataTable('#myTable');
            return () => {
                dtInstance.destroy();
            };
        }
    }, [content]);
    const fetchDelete = async (id) => {
        try {
            const response = await fetch(`http://localhost:8000/order/delete/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
            });
            const data = await response.json();
            if (data.success) {
                window.location.reload();
            }
        } catch (error) {
            await log("error", "products", error);
        }
    };
    return (
        <div className={"row block_1 p-1"}>
            <table id="myTable" className="display table table-dark">
                <thead>
                <tr>
                    <th>Id</th>
                    <th>Products</th>
                    <th>User Id</th>
                    <th>Delivery</th>
                    <th>Total</th>
                    <th>Transaction</th>
                    <th>Status</th>
                    <th>Created</th>
                    <th>Invoice</th>
                    <th>Comment</th>
                    <th></th>
                    <th></th>
                </tr>
                </thead>
                <tbody>
                {content.map((item) => (
                    <tr key={item.id}>
                        <td>{item.id}</td>
                        <td>
                            {item.products}
                        </td>
                        <td>
                            {item.user}
                        </td>
                        <td>
                            {item.delivery}
                        </td>
                        <td>
                            {item.total}
                        </td>
                        <td>
                            {item.transaction_id}
                        </td>
                        <td>
                            {item.status ? (
                                <div className={"center-vertical"}>
                                    <button value={"Done"} className={"btn btn-link btn_gen"}
                                            disabled={true}>
                                        <IoTrophySharp className={"IoTrophySharp"} title={"Done"}/>
                                    </button>
                                </div>
                            ) : (
                                <div className={"center-vertical"}>
                                    <button
                                        value={"Wait"}
                                        className={"btn btn-link btn_gen"}
                                        data-bs-toggle="modal"
                                        data-bs-target="#SendInvoice"
                                        data-order-id={item.id}
                                        data-user-id={item.user}>
                                        <IoTime className={"IoTime"} title={"Wait"}/>
                                    </button>
                                </div>
                            )}
                        </td>
                        <td>
                            {item.created_at}
                        </td>
                        <td>
                            {item.invoice}
                        </td>
                        <td>
                            {item.comment ? (
                                <div>
                                    <small data-bs-toggle="modal"
                                           data-bs-target="#AddOrderComment"
                                           data-orders-id={item.id}>{item.comment}</small>
                                </div>
                            ) : (
                                <div className={"center-vertical"}>
                                    <button
                                        className={"btn btn-link btn_gen"}
                                        value={"Add"}
                                        title={"Add comment"}
                                        data-bs-toggle="modal"
                                        data-bs-target="#AddOrderComment"
                                        data-orders-id={item.id}>
                                        <AiTwotoneFileAdd className={"AiTwotoneFileAdd"}/>
                                    </button>
                                </div>
                            )}
                        </td>
                        <td>
                            <div className={"center-vertical"}>
                                <button
                                    className={"btn btn-link btn_gen"}
                                    value={"V"}
                                    data-bs-toggle="modal"
                                    data-bs-target="#AdminViewOrder"
                                    data-orders-id={item.id}>
                                    <IoSearch className={"IoSearch"} title={"View"}/>
                                </button>
                            </div>
                        </td>
                        <td>
                            <div className={"center-vertical"}>
                                <button data-testid={"item_delete"} className="btn btn-link btn_gen"
                                        onClick={() => fetchDelete(item.id)}>
                                    <AiOutlineDelete className={"AiOutlineDelete"} title={"Delete"}/>
                                </button>
                            </div>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
            <AdminOrderInvoiceModal/>
            <AdminOrderCommentModal/>
            <AdminOrderViewModal/>
        </div>
    );
}
