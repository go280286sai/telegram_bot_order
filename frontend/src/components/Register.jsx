import React, { useState } from "react";
import log from "../helps/logs.mjs";
import {AiFillCheckSquare, AiTwotoneCloseSquare} from "react-icons/ai";

export default function Register() {
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        phone: "",
        password: "",
        confirmPassword: ""
    });
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (formData.password !== formData.confirmPassword) {
            alert("Passwords do not match.");
            return;
        }
        fetch("http://localhost:8000/user/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: formData.username,
                password: formData.password,
                email: formData.email,
                phone: formData.phone}),
            credentials: "include"
        }).then(res => res.json())
            .then((data) => {
                if (data.success) {
                    window.location.reload();
                } else {
                    log("error", "register error", data);
                    alert("Register is error");
                }
            }).catch(data => log("error", "login error", data));
    };

    return (
        <div className="modal fade" id="register" tabIndex="-1" aria-labelledby="registerLabel" aria-hidden="true">
            <div className="modal-dialog">
                <form className="modal-content" onSubmit={handleSubmit}>
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="registerLabel">Register new user</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body">
                        <div className="mb-3">
                            <label htmlFor="username" className="form-label">Username</label>
                            <input type="text" className="form-control" id="username" name="username"
                                   autoComplete="new-login"
                                   value={formData.username} onChange={handleChange} required/>
                        </div>
                        <div className="mb-3">
                            <label htmlFor="email" className="form-label">Email address</label>
                            <input type="email" className="form-control" id="email" name="email"
                                   value={formData.email} onChange={handleChange} required/>
                        </div>
                        <div className="mb-3">
                            <label htmlFor="phone" className="form-label">Phone number</label>
                            <input type="tel" className="form-control" id="phone" name="phone"
                                   value={formData.phone} onChange={handleChange} required/>
                        </div>
                        <div className="mb-3">
                            <label htmlFor="password" className="form-label">Password</label>
                            <input type="password" className="form-control" id="password" name="password"
                                   autoComplete="new-password"
                                   value={formData.password} onChange={handleChange} required/>
                        </div>
                        <div className="mb-3">
                            <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
                            <input type="password" className="form-control" id="confirmPassword" name="confirmPassword"
                                   autoComplete="new-password"
                                   value={formData.confirmPassword} onChange={handleChange} required/>
                        </div>
                    </div>
                    <strong className={"error"}>After registration, confirm your email.</strong>
                    <div className="modal-footer">
                        <button type="button" className="btn btn-link btn_gen" data-bs-dismiss="modal">
                            <AiTwotoneCloseSquare className={"AiTwotoneCloseSquare"} title={"Exit"}/>
                        </button>
                        <button type="submit" className="btn btn-link btn_gen" title={"register"}>
                            <AiFillCheckSquare className={"AiFillCheckSquare"} title={"Send"}/>
                        </button>
                    </div>

                </form>
            </div>

        </div>
    );
}
