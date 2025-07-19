import React, {useEffect, useState} from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import AdminProductsModal from "./AdminProductsModal";
import AdminOrderInvoiceModal from "./AdminOrderInvoiceModal";
import AdminOrderCommentModal from "./AdminOrderCommentlModal";
import AdminOrderViewModal from "./AdminOrderViewModal";

export default function AdminOrders() {
    const [content, setContent] = useState([]);

    const fetchProducts = async () => {
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

    // Инициализация
    useEffect(() => {
        fetchProducts();
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
                fetchProducts();
            }
        } catch (error) {
            await log("error", "products", error);
        }
    };
    return (
        <div className={"row block_1 p-1"}>

            <div className="btn btn-success mb-2 btn_with"
                 data-bs-toggle="modal"
                 data-bs-target="#addProducts">Add item
            </div>
            <AdminProductsModal/>
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
                    <th>View</th>
                    <th>Delete</th>
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
                            {item.status?(
                                <div>
                                    <input type="button" value={"Done"} className={"btn btn-success btn-sm"} disabled={true}/>
                                </div>
                            ):(
                                <div>
                                    <input type="button"
                                           value={"Wait"}
                                           className={"btn btn-danger btn-sm"}
                                           data-bs-toggle="modal"
                                           data-bs-target="#SendInvoice"
                                           data-order-id={item.id}
                                           data-user-id={item.user}
                                    />
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
                            {item.comment?(
                                <div>
                                    <small data-bs-toggle="modal"
                                           data-bs-target="#AddOrderComment"
                                           data-orders-id={item.id}>{item.comment}</small>
                                </div>
                            ):(
                                <div>
                                    <input
                                        type="button"
                                        className={"btn btn-success btn-sm"}
                                        value={"Add"}
                                        data-bs-toggle="modal"
                                        data-bs-target="#AddOrderComment"
                                        data-orders-id={item.id}/>
                                </div>
                            )}
                        </td>
                        <td>
                            <input
                                type="button"
                                className={"btn btn-success btn-sm"}
                                value={"V"}
                                data-bs-toggle="modal"
                                data-bs-target="#AdminViewOrder"
                                data-orders-id={item.id}/>
                        </td>
                        <td>
                            <button className="btn btn-danger btn-sm" onClick={() => fetchDelete(item.id)}>
                                Delete
                            </button>
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
