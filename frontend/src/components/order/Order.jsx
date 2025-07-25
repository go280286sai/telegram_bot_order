import React, {useEffect, useState} from "react";
import log from "../../helps/logs.mjs";
import Register from "../Register";
import Login from "../Login";
import OrderCart from "./OrderCart";
import OrderUser from "./OrderUser";
import {AiTwotoneCloseSquare} from "react-icons/ai";

export default function Order() {
    const [user, setUser] = useState({
        "user":
            {
                "username": "None",
                "email": "None",
                "phone": "None",
                "status": false
            }
    });

    const [statusUser, setStatusUser] = useState(null)

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await fetch("http://localhost:8000/user/is_auth", {
                    method: "POST",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json"
                    }
                });
                const data = await response.json();
                if (data['success']) {
                    if (data.data.first_name === null || data.data.last_name === null){
                        alert("The name or surname cannot be empty. Edit profile");
                        window.location.replace("/");
                    }
                    setUser(data.data);
                    if(data.data.status){
                        setStatusUser(true);
                    }
                }
            } catch (error) {
                await log("error", "is_auth", error);
            }
        };
        fetchUser();
    }, []);


    return (
        <div className={"row block_1"}>
            <div className={"order"}>
                <h2>Checkout</h2>
                {statusUser ? (
                    <div>
                        <OrderUser user={user}/>
                        <OrderCart/>
                    </div>
                ) : (
                    <div>
                        <>
                            <p>Please sign up or log in to complete your order.</p>
                            <Register/>
                            <Login/>
                            <button type="button" className="btn btn-primary m-1" data-bs-toggle="modal"
                                    data-bs-target="#login">Login
                            </button>
                            <button type="button" className="btn btn-primary m-1" data-bs-toggle="modal"
                                    data-bs-target="#register">Register
                            </button>
                        </>
                    </div>
                )}
                <a href="/">
                    <div className={"btn btn-link mt-5 btn_gen"}><AiTwotoneCloseSquare className={"AiTwotoneCloseSquareMain"} title={"Exit"}/> </div>
                </a>
            </div>

        </div>
    )
}