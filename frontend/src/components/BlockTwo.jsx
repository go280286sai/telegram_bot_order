import React, {useEffect, useState} from "react";
import log from "../helps/logs.mjs";
import {IoBagAdd, IoCardOutline, IoCart} from "react-icons/io5";
import {AiOutlineDelete} from "react-icons/ai";
export default function BlockTwo() {
    const [showAlert, setShowAlert] = useState(false);
    const [products, setProducts] = useState([]);
    const addToCart = async (id) => {
        try {
            await fetch(`http://localhost:8000/cart/increase/${id}`, {
                method: "POST",
                credentials: "include",
            })
            setShowAlert(true);
            setTimeout(() => setShowAlert(false), 3000);
            await fetchCart();
        } catch (error) {
            await log("error", "add to cart", error);
        }
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("http://localhost:8000/product/products");
                const result = await response.json();
                setProducts(result.data.products);
            } catch (error) {
                await log("error", "get products", error);
            }
        };

        fetchData();
        fetchCart();
    }, []);
    const [cartItems, setCartItems] = useState([]);

    const decreaseAmount = async (id) => {
        try {
            await fetch(`http://localhost:8000/cart/decrease/${id}`, {
                method: "POST",
                credentials: "include",
            });
            fetchCart();
        } catch (error) {
            await log("error", "decrease into cart", error);
        }
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
            setCartItems((prev) => prev.filter((item) => item.id !== id));
        } catch (error) {
            await log("error", "remove from cart", error);
        }
    };
    return (
        <div className="row block_1">
            <div className="col-12">
                {showAlert && (
                    <div className="alert alert-primary alert-dismissible fade show mt-3" role="alert">
                        Add to cart success!
                        <button type="button" className="btn-close" onClick={() => setShowAlert(false)}></button>
                    </div>
                )}
                <table className="table table-borderless service">
                    <thead>
                    <tr>
                        <th scope="col">№</th>
                        <th scope="col">Name</th>
                        <th scope="col">Description</th>
                        <th scope="col">Price</th>
                        <th scope="col"></th>
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
                                                Details
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

                                <button type="button" className="btn btn-link btn_gen" data-testid={"add_to_cart"}
                                        onClick={() => addToCart(product.id)}>
                                    <IoBagAdd className={"IoBagAdd"} title={"Add to cart"} />
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
                                    <h5 className="modal-title" id="cartModalLabel">Your cart</h5>
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
                                                    <td data-testid={"modal_name"}>{item.name}</td>
                                                    <td>
                                                        <div className="input-group input-group-sm"
                                                             style={{width: "120px"}}>
                                                            <button
                                                                className="btn btn-outline-secondary"
                                                                type="button"
                                                                onClick={() => decreaseAmount(item.id)}
                                                                disabled={item.amount === 1}>-
                                                            </button>
                                                            <input
                                                                type="text"
                                                                className="form-control text-center"
                                                                value={item.amount}/>
                                                            <button
                                                                className="btn btn-outline-secondary"
                                                                type="button"
                                                                onClick={() => addToCart(item.id)}
                                                                disabled={item.amount >= item.amounts}>+
                                                            </button>
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
                                                            className="btn btn-link btn_gen"
                                                            onClick={() => removeFromCart(item.id)}>
                                                            <AiOutlineDelete className={"AiOutlineDelete" } title={"Remove"}/>
                                                        </button>
                                                    </td>
                                                </tr>
                                            ))}
                                            </tbody>
                                            <tfoot>
                                            <tr>
                                                <td colSpan="4" className="text-end"><strong>Total:</strong></td>
                                                <td colSpan="2"><strong data-testid={"calculateTotal"}>{calculateTotal()} $</strong></td>
                                            </tr>
                                            </tfoot>
                                        </table>
                                    </div>
                                </div>
                                <div className="modal-footer">
                                    <a href="/order"><div className="btn btn-link btn_gen"><IoCardOutline className={"IoCardOutline"} title={"To pay"}/></div></a>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="btn trash" data-bs-toggle="modal" data-bs-target="#cartModal">
                        <span className="badge text-bg-danger">{cartItems.length}</span>
                        <IoCart className={"IoCart"} title="Trash"/>
                    </div>
                </div>
            </div>
        </div>
    );
}
