import React, {useState} from "react";
import log from "../../helps/logs.mjs";

export default function OrderPay({total}){
    const [error, setError] = useState("")
    const [formData, setFormData] = useState({
        cardNumber: "",
        cardMonth: "",
        cardYear: "",
        cardKey: "",
    });
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };
    const date = new Date();
    const currentData = date.getFullYear();
    const fetchTransactionSuccess = async (transaction) => {
        try {
            const res = await fetch("http://localhost:8000/order/create", {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    transaction: transaction,
                    cardTotal: total
                }),
            });
            const data = await res.json();
            if (data['success']) {
               window.location.replace("/")
            }
        } catch (error) {
            await log("error", "fetchCurrentDelivery", error);
        }
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        if(parseInt(formData.cardNumber).toString().length!==16){
            setError("Number card error");
            return
        }
        if(formData.cardMonth<=0 || formData.cardMonth>12){
            setError("Number month error");
            return
        }
        if(currentData>(2000+parseInt(formData.cardYear))){
            setError("Number year error");
            return
        }
        if(parseInt(formData.cardKey).toString().length!==3 || isNaN(parseInt(formData.cardKey))){
            setError("Number secret key error");
            return
        }
        fetch("http://localhost:8000/order/pay", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                cardTotal:total,
                cardNumber: formData.cardNumber,
                cardMonth: formData.cardMonth,
                cardYear: formData.cardYear,
                cardKey: formData.cardKey
            }),
            credentials: "include"
        }).then(res => res.json())
            .then((data) => {
                if (data.success) {
                    const transaction = data["data"]["transaction_id"];
                    fetchTransactionSuccess(transaction)
                    // window.location.reload()
                } else {
                    log("error", "login error", data);
                    setError("Incorrect username or password")
                }
            }).catch(data => log("error", "login error", data));
    };
    return (
        <div className="modal fade" id="to_pay" tabIndex="-1" aria-labelledby="loginLabel" aria-hidden="true">
            <div className="modal-dialog">
                <form className="modal-content" onSubmit={handleSubmit}>
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="loginLabel">Payment by card</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body">
                        <p className={"error"}>{error}</p>
                        <form>
                            <div className="mb-3">
                                <label htmlFor="cardNumber" className="form-label">Card Number</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    id="cardNumber"
                                    name="cardNumber"
                                    placeholder="1234567890123456"
                                    maxLength="16"
                                    value={formData.cardNumber}
                                    onChange={handleChange}
                                    required
                                />
                            </div>

                            <div className="row">
                                <div className="col-md-6 mb-3">
                                    <label htmlFor="cardMonth" className="form-label">Expiry Month</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="cardMonth"
                                        name="cardMonth"
                                        placeholder="MM"
                                        maxLength="2"
                                        value={formData.cardMonth}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>

                                <div className="col-md-6 mb-3">
                                    <label htmlFor="cardYear" className="form-label">Expiry Year</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="cardYear"
                                        name="cardYear"
                                        placeholder="YY"
                                        maxLength="2"
                                        value={formData.cardYear}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                            </div>

                            <div className="mb-3">
                                <label htmlFor="cvv" className="form-label">CVV</label>
                                <input
                                    type="password"
                                    className="form-control"
                                    id="cardKey"
                                    name="cardKey"
                                    placeholder="•••"
                                    maxLength="3"
                                    value={formData.cardKey}
                                    onChange={handleChange}
                                    required
                                />
                            </div>
                        </form>
                    </div>
                    <div className="modal-footer">
                        <button type="submit" className="btn btn-primary">Pay</button>
                        <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Exit</button>
                    </div>
                </form>
            </div>
        </div>
    )
}