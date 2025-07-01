import React, {useEffect, useState} from "react";
import Social from "./Social";
import Register from "./Register";
import Login from "./Login";
import Profile from "./Profile";
import log from "../helps/logs.mjs"

export default function BlockOne() {
    const [user, setUser] = useState({
        "user":
            {
                "username": "None",
                "email": "None",
                "phone": "None",
                "status": false
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
                    setStatusUser(true);
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
                <div className={"logo_img"} title={"Sonic Farm"}></div>
            </div>
            <div className="col-5 block_top">
                <Register/>
                <Login/>
                <Profile user={user}/>
                {statusUser === true ? (
                    <div className="text-end register">
                        <button className="btn btn-primary" type="button" data-bs-toggle="offcanvas"
                                data-bs-target="#profile"
                                aria-controls="staticBackdrop">
                            Profile
                        </button>
                        | <button type="button" className="btn btn-primary" onClick={logout}>Logout
                    </button>
                    </div>
                ) : (
                    <div className="text-end register">
                        <button type="button" className="btn btn-primary" data-bs-toggle="modal"
                                data-bs-target="#login">Login
                        </button>
                        | <button type="button" className="btn btn-primary" data-bs-toggle="modal"
                                  data-bs-target="#register">Register
                    </button>
                    </div>
                )}
                <h1 className={"title_h1"}>Exclusive Items</h1>
                <p className={"title_pre"}>We offer farm construction, auto shield, exclusive skins, pirate search, and
                    more at unbeatable
                    prices. Upgrade your experience now!</p>
                <Social/>
            </div>
        </div>
    );
}
