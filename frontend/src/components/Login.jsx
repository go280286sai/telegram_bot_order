import React, {useState} from "react";
import log from "../helps/logs.mjs";

export default function Login() {
    const [recovery, setRecovery] = useState(true)
    const [error, setError] = useState("")
    const [formData, setFormData] = useState({
        username: "",
        password: "",
    });
    const [formRecover, setFormRecover] = useState({
        user: "",
        email: "",
    });
    const toggleRecover = () =>{
        if(recovery !== !recovery){
            setRecovery(!recovery)
        }
    }
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };
    const exit= () => {
        setRecovery(true)
    }
    const handleSubmit = (e) => {
        e.preventDefault();
        if(formData.username.trim() === "" || formData.password.trim() === ""){
            alert("Login or password error");
            return;
        }
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
                if (data.data.success) {
                    window.location.reload();
                } else {
                    log("error", "login error", data);
                    setError("Incorrect username or password")
                }
            }).catch(data => log("error", "login error", data));
    };

    const handleRecovery = (e) => {
        const {name, value} = e.target;
        setFormRecover(prev => ({...prev, [name]: value}));
    };

    const handleSubmitRecovery = (e) => {
        e.preventDefault();
        fetch("http://localhost:8000/user/recovery", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: formRecover.user,
                email: formRecover.email
            }),
            credentials: "include"
        }).then(res => res.json())
            .then((data) => {
                if (data.success) {
                    setRecovery(true)
                } else {
                    log("error", "recover error", data);
                    window.location.reload();
                }
            }).catch(data => log("error", "recover error", data));
    };

    return (
        <div className="modal fade" id="login" tabIndex="-1" aria-labelledby="loginLabel" aria-hidden="true">
            {recovery ? <div className="modal-dialog">
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
                    <p className={"error"}>{error}</p>
                    <div className="modal-footer">
                        <button className="btn btn-primary" type="button" onClick={toggleRecover} title={"recover_password"}>
                            Recover password
                        </button>
                        <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Exit</button>
                        <button type="submit" className="btn btn-primary" title={"Login"}>Login</button>
                    </div>
                </form>
            </div> : <div className="modal-dialog">
            <form className="modal-content" onSubmit={handleSubmitRecovery}>
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="RecoverLabel">Recover password</h1>

                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>

                    </div>

                    <div className="modal-body">
                        <div className="mb-3">
                            <label htmlFor="user_id" className="form-label">Input you username</label>
                            <input
                                type="text"
                                className="form-control"
                                id="user_id"
                                name="user"
                                autoComplete="user"
                                value={formRecover.user}
                                onChange={handleRecovery}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="email_id" className="form-label">Input you Email</label>
                            <input
                                type="email"
                                className="form-control"
                                id="email_id"
                                name="email"
                                autoComplete="current-password"
                                value={formRecover.email}
                                onChange={handleRecovery}
                                required
                            />
                        </div>
                    </div>
                    <div className="modal-footer">
                        <button type="button" className="btn btn-secondary" onClick={exit}>Exit</button>
                        <button type="submit" className="btn btn-primary" title={"btn_recover"}>Send</button>
                    </div>
                </form>
            </div>}

        </div>
    );
}
