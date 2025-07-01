import React, {useState} from "react";
import log from "../helps/logs.mjs";

export default function Login() {
    const [error, setError] = useState("")
    const [formData, setFormData] = useState({
        username: "",
        password: "",
    });
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        fetch("http://localhost:8000/user/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: formData.username,
                password: formData.password
            }),
            credentials: "include"
        }).then(res => res.json())
            .then((data) => {
                if (data.success) {
                    window.location.reload()
                } else {
                    log("error", "login error", data);
                    setError("Incorrect username or password")
                }
            }).catch(data => log("error", "login error", data));
    };

    return (
        <div className="modal fade" id="login" tabIndex="-1" aria-labelledby="loginLabel" aria-hidden="true">
            <div className="modal-dialog">
                <form className="modal-content" onSubmit={handleSubmit}>
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="loginLabel">Login</h1>

                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>

                    </div>
                    <div className="modal-body">
                        <div className="mb-3">
                            <label htmlFor="loginUsername" className="form-label">Username</label>
                            <input
                                type="text"
                                className="form-control"
                                id="loginUsername"
                                name="username"
                                autoComplete="login"
                                value={formData.username}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="LoginPassword" className="form-label">Password</label>
                            <input
                                type="password"
                                className="form-control"
                                id="LoginPassword"
                                name="password"
                                autoComplete="current-password"
                                value={formData.password}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    </div>
                    <div className="modal-footer">
                        <p className={"error"}>{error}</p>
                        <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Exit</button>
                        <button type="submit" className="btn btn-primary">Login</button>
                    </div>
                </form>
            </div>
        </div>
    );
}
