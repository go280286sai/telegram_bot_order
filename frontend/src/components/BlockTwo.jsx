import React, {useEffect, useState, useMemo} from "react";
import log from "../helps/logs.mjs";
import {IoBagAdd, IoCardOutline, IoCart} from "react-icons/io5";
import {AiFillCheckSquare, AiOutlineDelete} from "react-icons/ai";

export default function BlockTwo() {
    const [showAlert, setShowAlert] = useState(false);
    const [products, setProducts] = useState([]);
    const [discount, setDiscount] = useState(0);
    const [totalBonus, setTotalBonus] = useState(0);
    const [formData, setFormData] = useState({promotion: ""});
    const [formDataBonus, setFormDataBonus] = useState({bonus: 0});
    const [cartItems, setCartItems] = useState([]);

    const total = useMemo(() => {
        let bonus = formDataBonus.bonus;
        if (bonus > totalBonus) {
            bonus = totalBonus;
        }

        const rawTotal = cartItems.reduce((sum, item) => sum + item.amount * item.price, 0);
        let result = rawTotal - (rawTotal * discount) / 100;

        if (result < bonus) {
            result = 0;
        } else {
            result -= bonus;
        }

        return result.toFixed(2);
    }, [cartItems, discount, formDataBonus.bonus, totalBonus]);

    const addToCart = async (id) => {
        try {
            await fetch(`http://localhost:8000/cart/increase/${id}`, {
                method: "POST",
                credentials: "include",
            });
            setShowAlert(true);
            setTimeout(() => setShowAlert(false), 3000);
            await fetchCart();
        } catch (error) {
            await log("error", "add to cart", error);
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
            setTotalBonus(result.data.bonus);
        } catch (error) {
            await log("error", "get all from carts", error);
        }
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

    const addDiscount = async () => {
        try {
            await fetch(`http://localhost:8000/cart/discount/add/${discount}`, {
                method: "POST",
                credentials: "include",
            });
        } catch (error) {
            await log("error", "apply discount", error);
        }
    };

    const handleDiscount = async (e) => {
        e.preventDefault();
        try {
            const res = await fetch("http://localhost:8000/setting/get/discount", {
                method: "GET",
                headers: {"Content-Type": "application/json"},
                credentials: "include",
            });
            const data = await res.json();
            if (data.success && data.data.settings.promotional === formData.promotion) {
                setDiscount(parseInt(data.data.settings.discount));
                addDiscount();
            } else {
                log("error", "Discount not found", data);
                alert("Discount not found");
            }
        } catch (error) {
            await log("error", "recover error", error);
        }
    };

    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData((prev) => ({...prev, [name]: value}));
    };

    const handleChangeBonus = (e) => {
        const {name, value} = e.target;
        setFormDataBonus((prev) => ({...prev, [name]: parseFloat(value) || 0}));
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
    const to_order = async (e) => {
        if(cartItems.length<=0){
            return
        }
        try {
            const bonus = formDataBonus.bonus <= totalBonus ? formDataBonus.bonus : totalBonus
            const response = await fetch("http://localhost:8000/cart/total_bonus", {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    total: total,
                    bonus: bonus
                })
            });
            const data = await response.json();
            if (data.success) {
                window.location.replace("/order");
            }
        } catch (error) {
            await log("error", "apply discount", error);
        }
    }
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
                    {products
                        .filter(product => product.amount > 0)
                        .map((product, index) => (
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
                                    <button
                                        type="button"
                                        className="btn btn-link btn_gen"
                                        data-testid={"add_to_cart"}
                                        onClick={() => addToCart(product.id)}>
                                        <IoBagAdd className={"IoBagAdd"} title={"Add to cart"}/>
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
                                                            <AiOutlineDelete className={"AiOutlineDelete"}
                                                                             title={"Remove"}/>
                                                        </button>
                                                    </td>
                                                </tr>
                                            ))}
                                            </tbody>
                                            <tfoot>
                                            <tr>
                                                <td colSpan="4" className="text-end">
                                                    <strong>Bonus: {totalBonus}</strong></td>
                                                <td colSpan="2">
                                                    <form onSubmit={handleDiscount}>
                                                        <table>
                                                            <tbody>
                                                            <tr>
                                                                <td>
                                                                    <input
                                                                        type="number"
                                                                        className="form-control"
                                                                        id="bonus"
                                                                        name="bonus"
                                                                        autoComplete="bonus"
                                                                        data-testid="promotion"
                                                                        value={formDataBonus.bonus}
                                                                        onChange={handleChangeBonus}
                                                                        required
                                                                    />
                                                                </td>
                                                            </tr>
                                                            </tbody>
                                                        </table>
                                                    </form>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td colSpan="4" className="text-end">
                                                    <strong>Promotion:</strong></td>
                                                <td colSpan="2">
                                                    <form onSubmit={handleDiscount}>
                                                        <table>
                                                            <tbody>
                                                            <tr>
                                                                <td><input
                                                                    type="text"
                                                                    className="form-control"
                                                                    id="promotion"
                                                                    name="promotion"
                                                                    autoComplete="login"
                                                                    data-testid="promotion"
                                                                    value={formData.promotion}
                                                                    onChange={handleChange}
                                                                    required
                                                                /></td>
                                                                <td>
                                                                    <button type="submit"
                                                                            className="btn btn-link btn_gen"
                                                                            data-testid={"promo_send"}>
                                                                        <AiFillCheckSquare
                                                                            className={"AiFillCheckSquare"}
                                                                            title={"Send"}/>
                                                                    </button>
                                                                </td>
                                                            </tr>
                                                            </tbody>
                                                        </table>
                                                    </form>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td colSpan="4" className="text-end">
                                                    <strong>Discount:</strong></td>
                                                <td colSpan="2"><strong
                                                    data-testid={"discountLabel"}>{discount} %</strong></td>
                                            </tr>
                                            <tr>
                                                <td colSpan="4" className="text-end"><strong>Total:</strong></td>
                                                <td colSpan="2"><strong data-testid="calculateTotal">{total} $</strong>
                                                </td>
                                            </tr>
                                            </tfoot>
                                        </table>
                                    </div>
                                </div>
                                <div className="modal-footer">
                                    <div className="btn btn-link btn_gen"><IoCardOutline className={"IoCardOutline"}
                                                                                         title={"To pay"}
                                                                                         onClick={to_order}/></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    {cartItems.length > 0 ? (
                        <div className="btn trash" data-bs-toggle="modal" data-bs-target="#cartModal">
                            <span className="badge text-bg-danger">{cartItems.length}</span>
                            <IoCart className={"IoCart"} title="Trash"/>
                        </div>
                    ) : (
                        <div className="btn trash">
                            <span className="badge text-bg-danger">{cartItems.length}</span>
                            <IoCart className={"IoCart"} title="Trash"/>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
