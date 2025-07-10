import React from "react";

export default function adminHeader(){
    return(
        <div className={"row block_1"}>
            <div className={"header_menu"}>
                <ul>
                    <li><a href="">Users</a></li>
                    <li><a href="">Products</a></li>
                    <li><a href="">Deliveries</a></li>
                    <li><a href="">Orders</a></li>
                    <li><a href="">Mailing</a></li>
                    <li><a href="">Predict</a></li>
                    <li><a href="">Reviews</a></li>
                    <li><a href="">Carousels</a></li>
                    <li><a href="/admin/settings">Settings</a></li>
                </ul>
            </div>
        </div>
    )
}