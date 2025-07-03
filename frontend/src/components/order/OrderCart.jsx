import React, {useEffect, useState} from "react";
import OrderDelivery from "./OrderDelivery";
import log from "../../helps/logs.mjs";

export default function OrderCart(){
    const [cartItems, setCartItems] = useState([]);
    const calculateTotal = () => {
        return cartItems
            .reduce((sum, item) => sum + item.amount * item.price, 0)
            .toFixed(2);
    };
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
    useEffect(()=>{
        fetchCart();
    }, [])
    return(
        <div className={"col-8"}>
                <table className="table table-dark">
                    <thead>
                    <tr>
                        <th>#</th>
                        <th>Name</th>
                        <th>Amount</th>
                        <th>Price</th>
                        <th>Total</th>
                    </tr>
                    </thead>
                    <tbody>
                    {cartItems.map((item, index) => (
                        <tr key={item.id}>
                            <td>{index + 1}</td>
                            <td>{item.name}</td>
                            <td>
                                <div className="input-group">
                                    {item.amount}
                                </div>
                            </td>
                            <td>{item.price.toFixed(2)} $</td>
                            <td>{(item.amount * item.price).toFixed(2)} $</td>
                        </tr>
                    ))}
                    </tbody>
                    <tfoot>
                    <tr>
                        <td colSpan="4" className="text-end"><strong>Total:</strong></td>
                        <td colSpan="2"><strong>{calculateTotal()} $</strong></td>
                    </tr>
                    </tfoot>
                </table>
            <OrderDelivery total={calculateTotal()}/>
        </div>
    )
}