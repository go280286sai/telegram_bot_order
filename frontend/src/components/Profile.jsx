import React, {useState, useEffect} from "react";
import log from "../helps/logs.mjs";
import {AiFillCheckSquare, AiOutlineInteraction} from "react-icons/ai";

export default function Profile(props) {
    const [orders, setOrders] = useState([]);
    const [formData, setFormData] = useState({
        password: "",
        confirmPassword: ""
    });

    const [formDataUser, setFormDataUser] = useState({
        first_name: "",
        last_name: ""
    });
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };
    const handleChangeUser = (e) => {
        const {name, value} = e.target;
        setFormDataUser(prev => ({...prev, [name]: value}));
    };
    const handleSubmit = (e) => {
        e.preventDefault();

        if (formData.password !== formData.confirmPassword) {
            alert("Passwords do not match.");
            return;
        }
        if (formData.password === "") {
            alert("Passwords not be empty");
            return;
        }

        fetch("http://localhost:8000/user/update_profile", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({
                idx: props.user.id,
                password: formData.password,
            })
        })
            .then(res => res.json())
            .then(data => {
                if (data['success']) {
                    alert("Password is update")
                    window.location.reload();
                } else {
                    alert("Error update password");
                    log("error", "Error update password", data)
                }
            })
    };

    const handleSubmitUser = (e) => {
        e.preventDefault();

        if (formDataUser.first_name.length===0 || formDataUser.last_name.length===0) {
            alert("First name or last name not is empty");
            return;
        }
        fetch("http://localhost:8000/user/add_contact_profile", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({
                idx: props.user.id,
                first_name: formDataUser.first_name,
                last_name: formDataUser.last_name
            })
        })
            .then(res => res.json())
            .then(data => {
                if (data.data.success) {
                    alert("Profile is update")
                    window.location.reload();
                } else {
                    alert("Error update profile");
                    log("error", "Error update profile", data)
                }
            })
            .catch(err => {
                log("error", "Error update profile", err)
            });
    };

    const fetchUser = async () => {
        try {
            const response = await fetch("http://localhost:8000/order/get_orders_user", {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                }
            });
            const result = await response.json();
            if (Array.isArray(result.data.orders)) {
                setOrders(result.data.orders);
            } else {
                log("error","Error format data:", result.data.orders);
            }
        } catch (error) {
            log("error", "Error get orders users", error)
        }
    };
    const fetchDeleteAccount = async () => {
        try {
            const response = await fetch("http://localhost:8000/user/delete_user", {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                }
            });
            const result = await response.json();
            if (result.success) {
                alert("To confirm account deletion, please check your email");
            } else {
                log("error","Error format data:", result.error);
            }
        } catch (error) {
            log("error", "Error get orders users", error)
        }
    };
    useEffect(() => {
        fetchUser();
    }, []);
    return (
        <div>
            <div className={"offcanvas offcanvas-start"} data-bs-backdrop="static" tabIndex="-1" id="profile"
                 aria-labelledby="staticBackdropLabel">
                <div className={"offcanvas-header"}>
                    <h5 className={"offcanvas-title"} id="staticBackdropLabel">Profile</h5>
                    <button type="button" className={"btn-close"} data-bs-dismiss="offcanvas"
                            aria-label="Close"></button>
                </div>
                <div className={"offcanvas-body"}>
                    <div>
                        {props.user.status ? (
                            <>
                                <table className={"table table-dark"}>
                                    <tbody>
                                    <tr>
                                        <th>Username</th>
                                        <td>{props.user.username}</td>
                                    </tr>
                                    <tr>
                                        <th>First name</th>
                                        <td>{props.user.first_name}</td>
                                    </tr>
                                    <tr>
                                        <th>Last name</th>
                                        <td>{props.user.last_name}</td>
                                    </tr>
                                    <tr>
                                        <th>Email</th>
                                        <td>{props.user.email}</td>
                                    </tr>
                                    <tr>
                                        <th>Phone</th>
                                        <td>{props.user.phone}</td>
                                    </tr>
                                    </tbody>
                                </table>
                                <table className={"table table-dark"}>
                                    <thead>
                                    <tr>
                                        <th>Id</th>
                                        <th>Total</th>
                                        <th>Status</th>
                                        <th>Create</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {orders.map((order, index) => (
                                        <tr key={order.id || index}>
                                            <td>{order.id}</td>
                                            <td>{parseFloat(order.total)}</td>
                                            <td>{order.status === 0 ? "Wait" : "Done"}</td>
                                            <td>{order.created_at}</td>
                                        </tr>
                                    ))}
                                    </tbody>
                                </table>
                                <button onClick={fetchUser} className={"btn btn-link btn_gen"}>
                                    <AiOutlineInteraction className={"AiOutlineInteractionDark"} title={"update"}/>
                                </button>
                                <div className={"form-style"}>
                                    <div className="mb-3">
                                        <label htmlFor="first_name" className="form-label">First name</label>
                                        <input type="text" className="form-control" id="first_name" name="first_name"
                                               value={formDataUser.first_name} onChange={handleChangeUser}/>
                                    </div>
                                    <div className="mb-3">
                                        <label htmlFor="last_name" className="form-label">Last name</label>
                                        <input type="text" className="form-control" id="last_name"
                                               name="last_name"
                                               value={formDataUser.last_name} onChange={handleChangeUser}/>
                                    </div>
                                </div>
                                <button type="submit" title={"first_last_name"} className="btn btn-link"
                                        onClick={handleSubmitUser}>
                                    <AiFillCheckSquare className={"AiFillCheckSquare"} title={"Save"}/>
                                </button>
                                <div className={"form-style"}>
                                    <div className="mb-3">
                                        <label htmlFor="password" className="form-label">New password</label>
                                        <input type="password" className="form-control" id="password" name="password"
                                               value={formData.password} onChange={handleChange}/>
                                    </div>
                                    <div className="mb-3">
                                        <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
                                        <input type="password" className="form-control" id="confirmPassword"
                                               name="confirmPassword"
                                               value={formData.confirmPassword} onChange={handleChange}/>
                                    </div>
                                </div>
                                <button type="submit" className="btn btn-link btn_gen" data-testid={"password_save"}
                                        onClick={handleSubmit}>
                                    <AiFillCheckSquare className={"AiFillCheckSquare"} title={"Save"}/>
                                </button>
                            </>
                        ) : (<p className={"lock"}>Your account has been suspended. For more information, please
                            contact support.</p>)}
                    </div>
                    <div>
                        <button className={"btn btn-dark mt-2"} data-testid={"delete_account"}
                        onClick={fetchDeleteAccount}>Delete account</button>
                    </div>
                </div>

            </div>
        </div>
    )
}