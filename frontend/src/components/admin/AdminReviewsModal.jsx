import React, {useState} from "react";
import log from "../../helps/logs.mjs";
import {AiFillCheckSquare, AiTwotoneCloseSquare} from "react-icons/ai";

export default function AdminReviewsModal(){
    const [formData, setFormData] = useState({
        name: "",
        text: "",
        gender: ""
    });
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        fetch("http://localhost:8000/review/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: formData.name,
                text: formData.text,
                gender: formData.gender
            }),
            credentials: "include"
        }).then(res => res.json())
            .then((data) => {
                if (data.success) {
                    window.location.reload()
                } else {
                    log("error", "add new item review error", data);
                }
            }).catch(data => log("error", "add new item review error", data));
    };
    return (
        <div className="modal fade" id="addReviews" tabIndex="-1" aria-labelledby="addReviews" aria-hidden="true">
           <div className="modal-dialog">
                <form className="modal-content" onSubmit={handleSubmit}>
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="ReviewLabel">Add new item review</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div className="modal-body">
                        <div className="mb-3">
                            <label htmlFor="Name_item" className="form-label">Name</label>
                            <input
                                type="text"
                                className="form-control"
                                id="Name_item"
                                name="name"
                                autoComplete="name"
                                value={formData.name}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="text_item" className="form-label">Text</label>
                            <input
                                type="text"
                                className="form-control"
                                id="text_item"
                                name="text"
                                autoComplete="text"
                                value={formData.text}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="gender_item" className="form-label">Gender</label>
                            <input
                                type="number"
                                className="form-control"
                                id="gender_item"
                                name="gender"
                                autoComplete="gender"
                                value={formData.gender}
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