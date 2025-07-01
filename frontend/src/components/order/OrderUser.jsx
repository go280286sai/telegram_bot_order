import React from "react";

export default function OrderUser({ user }){
    return(
        <div className={"col-8"}>
            <table className={"table table-dark"}>
                <tbody>
                <tr>
                    <th>Username</th>
                    <td>{user.username}</td>
                </tr>
                <tr>
                    <th>Email</th>
                    <td>{user.email}</td>
                </tr>
                <tr>
                    <th>Phone</th>
                    <td>{user.phone}</td>
                </tr>
                </tbody>
            </table>
        </div>
    )
}