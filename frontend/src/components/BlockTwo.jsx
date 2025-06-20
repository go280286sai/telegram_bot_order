import React, { useEffect, useState } from "react";
import trash from "../assets/img/trash.png";

export default function BlockTwo() {
    const [products, setProducts] = useState([]);
    const addToCart = async (id) => {
        await fetch(`http://localhost:8000/cart/add/${id}`, {
            method: "POST",
            credentials: "include", // важно для работы с cookie
        });
        await fetchCart()
    };
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("http://localhost:8000/products");
                const data = await response.json();
                console.log("Полученные данные:", data);
                setProducts(data.products); // ← вот это ключевой момент
            } catch (error) {
                console.error("Ошибка при получении данных:", error);
            }
        };

        fetchData();
        fetchCart();
    }, []);
    const [cartItems, setCartItems] = useState([]);
    const increaseAmount = async (id) => {
        try {
            await fetch(`http://localhost:8000/cart/increase/${id}`, {
                method: "POST",
                credentials: "include",
            });
            fetchCart(); // обновить корзину после изменения
        } catch (error) {
            console.error("Ошибка при увеличении количества:", error);
        }
    };

    const decreaseAmount = async (id) => {
        try {
            await fetch(`http://localhost:8000/cart/decrease/${id}`, {
                method: "POST",
                credentials: "include",
            });
            fetchCart();
        } catch (error) {
            console.error("Ошибка при уменьшении количества:", error);
        }
    };

    const fetchCart = async () => {
        try {
            const response = await fetch("http://localhost:8000/cart", {
                method: "GET",
                credentials: "include",
            });
            const data = await response.json();
            console.log(data)
            setCartItems(data.cart); // Обновляем cart
        } catch (error) {
            console.error("Ошибка при получении данных:", error);
        }
    };

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
        <div className="row block_1">
            <div className="col-12">
                <table className="table table-info service">
                    <thead>
                    <tr>
                        <th scope="col">Id</th>
                        <th scope="col">Name</th>
                        <th scope="col">Description</th>
                        <th scope="col">Price</th>
                        <th scope="col">Action</th>
                    </tr>
                    </thead>
                    <tbody>
                    {products.map((product, index) => (
                        <tr key={product.id || index}>
                            <th scope="row">{product.id}</th>
                            <td>{product.name}</td>
                            <td>
                                <div className="accordion" id="productAccordion">
                                    <div className="accordion-item">
                                        <h2 className="accordion-header">
                                            <button
                                                className="accordion-button collapsed accordion_color"
                                                type="button"
                                                data-bs-toggle="collapse"
                                                data-bs-target={`#collapse${index}`}
                                                aria-expanded="false"
                                                aria-controls={`collapse${index}`}>
                                                Подробнее
                                            </button>
                                        </h2>
                                        <div
                                            id={`collapse${index}`}
                                            className="accordion-collapse collapse"
                                            data-bs-parent="#productAccordion">
                                            <div className="accordion-body">
                                                {product.description}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </td>
                            <td>
                                <strong className="price">${product.price}</strong>
                            </td>
                            <td>
                                <button className="btn btn-success" onClick={() => addToCart(product.id)}>Add to Cart
                                </button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>

            <div className="trash_mi">
                <div>
                    <div className="modal fade" id="cartModal" tabIndex="-1" aria-labelledby="cartModalLabel"
                         aria-hidden="true">
                        <div className="modal-dialog modal-lg">
                            <div className="modal-content">
                                <div className="modal-header">
                                    <h5 className="modal-title" id="cartModalLabel">Ваша корзина</h5>
                                    <button type="button" className="btn-close" data-bs-dismiss="modal"
                                            aria-label="Close"></button>
                                </div>
                                <div className="modal-body">
                                    <div className="table-responsive">
                                        <table className="table">
                                            <thead>
                                            <tr>
                                                <th>#</th>
                                                <th>Name</th>
                                                <th>Amount</th>
                                                <th>Max amounts</th>
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
                                                        <div className="input-group input-group-sm"
                                                             style={{width: "120px"}}>
                                                            <button
                                                                className="btn btn-outline-secondary"
                                                                type="button"
                                                                onClick={() => decreaseAmount(item.id)}
                                                                disabled={item.amount <= 1}>-</button>
                                                            <input
                                                                type="text"
                                                                className="form-control text-center"
                                                                value={item.amount}/>
                                                            <button
                                                                className="btn btn-outline-secondary"
                                                                type="button"
                                                                onClick={() => increaseAmount(item.id)}
                                                                disabled={item.amount === item.amounts}>+</button>
                                                        </div>
                                                    </td>
                                                    <td><input
                                                        type="text"
                                                        className="form-control text-center"
                                                        value={item.amounts}
                                                        readOnly={true}
                                                    /></td>
                                                    <td>{item.price.toFixed(2)} $</td>
                                                    <td>{(item.amount * item.price).toFixed(2)} $</td>
                                                    <td>
                                                        <button
                                                            className="btn btn-warning"
                                                            onClick={() => removeFromCart(item.id)}>
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

                    <div className="btn trash" data-bs-toggle="modal" data-bs-target="#cartModal">
                        <span className="badge text-bg-dark">{cartItems.length}</span><img src={trash} alt="Trash" title="Trash"/>
                    </div>
                </div>
            </div>
        </div>
    );
}
