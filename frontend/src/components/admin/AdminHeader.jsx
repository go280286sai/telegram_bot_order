import React, {useEffect} from "react";
import {fetchAuth} from "./fetchAuth";

export default function AdminHeader(){

    useEffect(() => {
        fetchAuth();
    }, []);
    return(
        <div className={"row block_1"}>
            <div className={"header_menu"}>
                <ul>
                    <li><a href="/admin/users">Users</a></li>
                    <li><a href="/admin/products">Products</a></li>
                    <li><a href="/admin/delivery">Deliveries</a></li>
                    <li><a href="/admin/orders">Orders</a></li>
                    <li><a href="/admin/mailing">Mailing</a></li>
                    <li><a href="/admin/predict">Predict</a></li>
                    <li><a href="/admin/reviews">Reviews</a></li>
                    <li><a href="/admin/carousels">Carousels</a></li>
                    <li><a href="/admin/settings">Settings</a></li>
                </ul>
            </div>
        </div>
    )
}