import React, { useState, useEffect } from "react";
import trash from "../assets/img/trash.png";

export default function Trash() {
    const [cartItems, setCartItems] = useState([]);

    const fetchData = async () => {
        try {
            const response = await fetch("http://localhost:8000/cart", {
                method: "GET",
                credentials: "include",
            });
            const data = await response.json();
            console.log("Полученные данные:", data);
            setCartItems(data.cart); // Обновляем cart
        } catch (error) {
            console.error("Ошибка при получении данных:", error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const calculateTotal = () => {
        return cartItems
            .reduce((sum, item) => sum + item.amount * item.price, 0)
            .toFixed(2);
    };

    const removeFromCart = async (id) => {
        try {
            await fetch(`http://localhost:8000/cart/remove/${id}`, {
                method: "POST",
                credentials: "include",
            });
            // После удаления обновляем корзину
            setCartItems((prev) => prev.filter((item) => item.id !== id));
        } catch (error) {
            console.error("Ошибка при удалении товара:", error);
        }
    };

    return (
        <div>
            <div className="modal fade" id="cartModal" tabIndex="-1" aria-labelledby="cartModalLabel" aria-hidden="true">
                <div className="modal-dialog modal-lg">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h5 className="modal-title" id="cartModalLabel">Ваша корзина</h5>
                            <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div className="modal-body">
                            <div className="table-responsive">
                                <table className="table">
                                    <thead>
                                    <tr>
                                        <th>#</th>
                                        <th>Name</th>
                                        <th>Amount</th>
                                        <th>Price</th>
                                        <th>Total</th>
                                        <th></th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {cartItems.map((item, index) => (
                                        <tr key={item.id}>
                                            <td>{index + 1}</td>
                                            <td>{item.name}</td>
                                            <td>
                                                <div className="input-group input-group-sm" style={{ width: "120px" }}>
                                                    <button className="btn btn-outline-secondary" type="button">-</button>
                                                    <input
                                                        type="text"
                                                        className="form-control text-center"
                                                        value={item.amount}
                                                    />
                                                    <button className="btn btn-outline-secondary" type="button">+</button>
                                                </div>
                                            </td>
                                            <td>{item.price.toFixed(2)} $</td>
                                            <td>{(item.amount * item.price).toFixed(2)} $</td>
                                            <td>
                                                <button
                                                    className="btn btn-warning"
                                                    onClick={() => removeFromCart(item.id)}
                                                >
                                                    Remove
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                    </tbody>
                                    <tfoot>
                                    <tr>
                                        <td colSpan="4" className="text-end"><strong>Итого:</strong></td>
                                        <td colSpan="2"><strong>{calculateTotal()} $</strong></td>
                                    </tr>
                                    </tfoot>
                                </table>
                            </div>
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">
                                Продолжить покупки
                            </button>
                            <button type="button" className="btn btn-success">Оформить заказ</button>
                        </div>
                    </div>
                </div>
            </div>

            <div className="btn btn-primary trash" data-bs-toggle="modal" data-bs-target="#cartModal">
                <img src={trash} alt="Корзина" />
            </div>
        </div>
    );
}
