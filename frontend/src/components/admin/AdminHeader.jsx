import React from "react";

export default function adminHeader(){
    return(
        <div className={"row block_1"}>
            <div className={"header_menu"}>
                <ul>
                    <li><a href="">Users</a></li>
                    <li><a href="/admin/products">Products</a></li>
                    <li><a href="/admin/delivery">Deliveries</a></li>
                    <li><a href="">Orders</a></li>
                    <li><a href="">Mailing</a></li>
                    <li><a href="">Predict</a></li>
                    <li><a href="/admin/reviews">Reviews</a></li>
                    <li><a href="/admin/carousels">Carousels</a></li>
                    <li><a href="/admin/settings">Settings</a></li>
                </ul>
            </div>
        </div>
    )
}