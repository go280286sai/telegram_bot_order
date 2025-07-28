import React, {useEffect, useState} from "react";
import log from "../../helps/logs.mjs";
import {AiTwotoneCloseSquare} from "react-icons/ai";
import {IoPrint} from "react-icons/io5";

export default function AdminOrderViewModal() {
    const [content, setContent] = useState({
        products: [],
        user: {},
        delivery: {}
    });
    const fetchOrder = async (id) => {
        try {
            const response = await fetch(`http://localhost:8000/order/get_view/${id}`, {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                }
            });
            const data = await response.json();
            if (data.success) {
                setContent(data.data);
            }
        } catch (error) {
            await log("error", "is_auth", error);
        }
    };

    useEffect(() => {
        const modalEl = document.getElementById('AdminViewOrder');
        if (!modalEl) return;

        const handleShow = (event) => {
            const button = event.relatedTarget;
            const id = button.getAttribute('data-orders-id');
            fetchOrder(id);
        };
        modalEl.addEventListener('show.bs.modal', handleShow);
        return () => {
            modalEl.removeEventListener('show.bs.modal', handleShow);
        };
    }, []);
    const printInvoice = () => {
        const printContents = document.getElementById("invoiceContent").innerHTML;
        const originalContents = document.body.innerHTML;
        document.body.innerHTML = printContents;
        window.print();
        document.body.innerHTML = originalContents;
        window.location.reload(); // reload page after print
    };

    return (
        <div className="modal fade" id="AdminViewOrder" tabIndex="-1" aria-labelledby="AdminViewOrder"
             aria-hidden="true">
            <style>
                {`
    @media print {
      body * {
        visibility: hidden;
      }
      #invoiceContent, #invoiceContent * {
        visibility: visible;
      }
      #invoiceContent {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
      }
      .no-print {
        display: none !important;
      }
    }
  `}
            </style>


            <div className="modal-dialog modal-lg">
                <div className="modal-content" id="invoiceContent">
                    <div id={"printableArea"}>
                        <div className="modal-header">
                            <h5 className="modal-title" id="invoiceModalLabel">Purchase invoice</h5>
                            <button type="button" className="btn-close" data-bs-dismiss="modal"
                                    aria-label="Закрыть"></button>
                        </div>
                        <div className="modal-body">
                            <p><strong>Order Id:</strong> {content.id}</p>
                            <p><strong>Created:</strong> {content.created}</p>

                            <table className="table table-bordered">
                                <thead>
                                <tr>
                                    <th>Product/Service</th>
                                    <th>Amount</th>
                                    <th>Price</th>
                                    <th>Total</th>
                                </tr>
                                </thead>
                                <tbody>
                                {content.products.map((value, index) => (
                                    <tr key={index}>
                                        <td>{value.name}</td>
                                        <td>{value.amount}</td>
                                        <td>{value.price}</td>
                                        <td>{value.amount * value.price}</td>
                                    </tr>
                                ))}
                                </tbody>
                                <tfoot>
                                <tr>
                                    <th colSpan="3">Bonus</th>
                                    <th>{content.bonus}</th>
                                </tr>
                                <tr>
                                    <th colSpan="3">Discount</th>
                                    <th>{content.discount}</th>
                                </tr>
                                <tr>
                                    <th colSpan="3">Total</th>
                                    <th>{content.total}</th>
                                </tr>
                                </tfoot>
                            </table>
                            <p><strong>Recipient:</strong> {content.user.first_name} {content.user.last_name}</p>
                            <p>
                                <strong>Address:</strong> {content.delivery.post_name}, {content.delivery.city_name}, {content.delivery.address_name}
                            </p>
                            <p><strong>Invoice:</strong> {content.invoice}</p>
                        </div>
                    </div>
                    <div className="modal-footer no-print">
                        <button type="button" className="btn btn-link btn_gen" data-bs-dismiss="modal">
                            <AiTwotoneCloseSquare className={"AiTwotoneCloseSquare"} title={"Exit"}/>
                        </button>
                        <button className="btn btn-link btn_gen"
                                onClick={printInvoice}>
                            <IoPrint className={"IoPrint"} title={"Print"}/>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
