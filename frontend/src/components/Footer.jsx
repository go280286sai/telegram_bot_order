import React, {useState} from "react";
import log from "../helps/logs.mjs";
import Contacts from "./Contacts";
import GoogleMaps from "./GoogleMaps";

export default function Footer({ settings }) {
    const [info, setInfo] = useState("")
    const [formData, setFormData] = useState({
        email: "",
    });
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        fetch("http://localhost:8000/subscriber/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: formData.email,
            }),
            credentials: "include"
        }).then(res => res.json())
            .then((data) => {
                if (data.success) {
                    setInfo("Ok")
                } else {
                    log("error", "login error", data);
                    setInfo("Incorrect email")
                }
            });
    };
    return (
        <div className={"row block_1"}>
            <div className={"row service"}>
                <div className={"col-7"}>
                <GoogleMaps settings={settings}/>
                </div>
                <div className={"col-5"}>
                    <form action="" method="post">
                        <div className={"mb-2"}>
                            <label htmlFor="exampleFormControlInput1" className={"form-label"}>Subscriber</label>
                            <input
                                type="email"
                                className="form-control"
                                id="email"
                                name="email"
                                placeholder="example@example.com"
                                value={formData.email}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div>
                            <input type="submit" className={"btn btn-dark"} value="Submit" onClick={handleSubmit}/>
                        </div>
                        <strong className={"success"}>{info}</strong>
                    </form>
                    <Contacts settings={settings}/>
                </div>
            </div>
        </div>
    )
}