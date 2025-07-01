import React, {useEffect, useState} from "react";
import log from "../../helps/logs.mjs";
import Register from "../Register";
import Login from "../Login";
import OrderCart from "./OrderCart";
import OrderUser from "./OrderUser";
import OrderDelivery from "./OrderDelivery";

export default function Order(){
    const [cartItems, setCartItems] = useState([]);
    const [user, setUser] = useState({
        "user":
            {
                "username": "None",
                "email": "None",
                "phone": "None",
                "status": false
            }
    });
    const [delivery, setDelivery] = useState([])
    const [statusDelivery, setStatusDelivery] = useState(false)
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
                if (data.data) {
                    setUser(data.data);
                    setStatusUser(true);
                    fetchCart()
                }
            } catch (error) {
                await log("error", "is_auth", error);
            }
        };
        fetchUser();
    }, []);

    const fetchCart = async () => {
        try {
            const response = await fetch("http://localhost:8000/cart", {
                method: "POST",
                credentials: "include",
            });
            const result = await response.json();
            setCartItems(result.data.cart);
        } catch (error) {
            await log("error", "get all from carts", error);
        }
    };
    return (
        <div className={"row block_1"}>
            <div className={"order"}>
                <h2>Checkout</h2>
                {statusUser?(
                    <div>
                        <OrderUser user={user}/>
                        <OrderCart items={cartItems}/>
                        <OrderDelivery delivery={statusDelivery}/>
                    </div>
                ):(
                    <div>
                        <>
                        <p>Please sign up or log in to complete your order.</p>
                        <Register/>
                        <Login/>
                        <button type="button" className="btn btn-primary m-1" data-bs-toggle="modal"
                                data-bs-target="#login">Login</button>
                        <button type="button" className="btn btn-primary m-1" data-bs-toggle="modal"
                                data-bs-target="#register">Register</button>
                        </>
                    </div>
                )}
                <a href="/"><div className={"btn btn-dark mt-5"}>Exit</div></a>
            </div>

        </div>
    )
}