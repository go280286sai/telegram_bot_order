import React, {useEffect, useState} from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import AdminPost from "./AdminPost";
import AdminCity from "./AdminCity";
import AdminAddress from "./AdminAddress";

export default function AdminDelivery() {
    const [content, setContent] = useState([]);

    const fetchDelivery = async () => {
        try {
            const response = await fetch("http://localhost:8000/delivery/gets", {
                method: "GET",
                credentials: "include",
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            if (data.success) {
                setContent(data.data.deliveries);
            }
        } catch (error) {
            await log("error", "deliveries", error);
        }
    };

    useEffect(() => {
        fetchDelivery();
    }, []);

    useEffect(() => {
        if (content.length > 0) {
            const dtInstance = new DataTable('#myTable');
            return () => {
                dtInstance.destroy();
            };
        }
    }, [content]);

    return (
        <div className="row block_1 p-1">
            <table id="myTable" className="display table table-dark">
                <thead>
                <tr>
                    <th>Post</th>
                    <th>City</th>
                    <th>Address</th>
                </tr>
                </thead>
                <tbody>
                {content.map((item, index) => (
                    <tr key={index}>
                        <td>{item.post_name}</td>
                        <td>{item.city_name}</td>
                        <td>{item.address_name}</td>
                    </tr>
                ))}
                </tbody>
            </table>
            <AdminPost/>
            <AdminCity/>
            <AdminAddress/>
        </div>

    );
}
