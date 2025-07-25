import React from "react";
import AdminPost from "./AdminPost";
import AdminCity from "./AdminCity";
import AdminAddress from "./AdminAddress";

export default function AdminDelivery() {
    return (
        <div className="row block_1 p-1">
            <AdminPost/>
            <AdminCity/>
            <AdminAddress/>
        </div>
    );
}
