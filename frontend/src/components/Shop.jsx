import React, { useState, useEffect } from "react";
import BlockTwo from "./BlockTwo";
import Trash from "./Trash";

export default function Shop() {
    const [cartItems, setCartItems] = useState([]);

    const fetchCart = async () => {
        try {
            const response = await fetch("http://localhost:8000/cart", {
                method: "GET",
                credentials: "include",
            });
            const data = await response.json();
            setCartItems(data.cart);
        } catch (error) {
            console.error("Ошибка при получении корзины:", error);
        }
    };

    useEffect(() => {
        fetchCart();
    }, []);

    return (
        <div>
            <BlockTwo fetchCart={fetchCart} />
            <Trash cartItems={cartItems} setCartItems={setCartItems} />
        </div>
    );
}
