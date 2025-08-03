import React, {useEffect, useState} from "react";
import Social from "./Social";
import Register from "./Register";
import Login from "./Login";
import Profile from "./Profile";
import log from "../helps/logs.mjs";

export default function BlockOne({settings}) {
    const [user, setUser] = useState({
        "user":
            {
                "username": "None",
                "email": "None",
                "phone": "None",
                "status": false,
                "bonus": 0
            }
    });
    const [statusUser, setStatusUser] = useState(false)
    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await fetch("http://localhost:8000/user/is_auth", {
                    method: "POST",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json"
                    }
                });
                const data = await response.json();
                if (data.data) {
                    setUser(data.data);
                    if (data.success) {
                        setStatusUser(true);
                    }
                }
            } catch (error) {
                await log("error", "is_auth", error);
            }
        };
        fetchUser();
    }, []);

    const logout = async () => {
        try {
            const response = await fetch("http://localhost:8000/user/logout", {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                }
            });
            const data = await response.json();
            if (data.data) {
                setStatusUser(false);
            }
        } catch (error) {
            await log("error", "is_auth", error);
        }
    }
    return (
        <div className="row block_1">
            <div className="col-5">
                <div className={"logo_img"} title={settings.title}></div>
            </div>
            <div className="col-5 block_top">
                <Register/>
                <Login/>
                <Profile user={user}/>
                {statusUser === true ? (
                    <div className="text-end register auth">
                        <strong data-bs-toggle="offcanvas"
                                data-bs-target="#profile"
                                aria-controls="staticBackdrop"
                                data-testid={"profile_title_mock"}>Profile</strong>
                        <strong className={"auth"}>|</strong>
                        <strong className={"auth"} onClick={logout} data-testid={"logout_title_mock"}>Logout</strong>
                    </div>
                ) : (
                    <div className="text-end register auth">
                        <strong data-bs-toggle="modal"
                                data-bs-target="#login" title={"login_modal"}
                                data-testid={"login_title_mock"}>Login</strong>
                        <strong className={"auth"}>|</strong>
                        <strong data-bs-toggle="modal"
                                data-bs-target="#register" className={"auth"}
                                data-testid={"register_title_mock"}>Register</strong>
                    </div>
                )}
                <h1 className={"title_h1"}>{settings.title}</h1>
                <p className={"title_pre"}>{settings.description}</p>
                <Social settings={settings}/>
            </div>
        </div>
    );
}
