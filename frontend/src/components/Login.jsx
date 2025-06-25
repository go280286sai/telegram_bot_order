import React, {useState} from "react";

export default function Login() {
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
            credentials: "include" // если используешь cookie или сессию
        }).then(res => res.json())
            .then((data) => {
                if (data.data.user_id) {
                    window.location.reload()
                } else {
                    console.log(data)
                }

            }).catch(data => console.log(data));
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
                            <label htmlFor="username" className="form-label">Username</label>
                            <input type="text" className="form-control" id="username" name="username"
                                   value={formData.username} onChange={handleChange} required/>
                        </div>
                        <div className="mb-3">
                            <label htmlFor="password" className="form-label">Password</label>
                            <input type="password" className="form-control" id="password" name="password"
                                   value={formData.password} onChange={handleChange} required/>
                        </div>
                    </div>
                    <div className="modal-footer">
                        <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Exit</button>
                        <button type="submit" className="btn btn-primary">Login</button>
                    </div>
                </form>
            </div>
        </div>
    );
}
