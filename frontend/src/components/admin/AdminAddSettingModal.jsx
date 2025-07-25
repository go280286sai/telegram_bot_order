import React, {useState} from "react";
import log from "../../helps/logs.mjs";
import {AiFillCheckSquare, AiTwotoneCloseSquare} from "react-icons/ai";

export default function AdminAddSettingModal() {
    const [formData, setFormData] = useState({
        name: "",
        value: "",
    });
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        fetch("http://localhost:8000/setting/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: formData.name,
                value: formData.value
            }),
            credentials: "include"
        }).then(res => res.json())
            .then((data) => {
                if (data.success) {
                    window.location.reload()
                } else {
                    log("error", "add new item setting error", data);
                }
            }).catch(data => log("error", "add new item setting error", data));
    };
    return (
        <div className="modal fade" id="addSetting" tabIndex="-1" aria-labelledby="addSetting" aria-hidden="true">
            <div className="modal-dialog">
                <form className="modal-content" onSubmit={handleSubmit}>
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="RecoverLabel">Add new item setting</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div className="modal-body">
                        <div className="mb-3">
                            <label htmlFor="name_item" className="form-label">Name</label>
                            <input
                                data-testid={"item_name"}
                                type="text"
                                className="form-control"
                                id="name_item"
                                name="name"
                                autoComplete="name"
                                value={formData.name}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="value_item" className="form-label">Value</label>
                            <input
                                data-testid={"item_value"}
                                type="text"
                                className="form-control"
                                id="value_item"
                                name="value"
                                autoComplete="value"
                                value={formData.value}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    </div>
                    <div className="modal-footer">
                        <button type="button" className="btn btn-link btn_gen" data-bs-dismiss="modal">
                             <AiTwotoneCloseSquare className={"AiTwotoneCloseSquare"} title={"Exit"}/>
                        </button>
                        <button type="submit" className="btn btn-link btn_gen">
                            <AiFillCheckSquare className={"AiFillCheckSquare"} title={"Send"}/>
                        </button>
                    </div>
                </form>
            </div>

        </div>
    )
}