import React, {useState} from "react";
import log from "../../helps/logs.mjs";
import {AiFillCheckSquare, AiTwotoneCloseSquare} from "react-icons/ai";

export default function AdminCarouselsModal(){
    const [formData, setFormData] = useState({
        title: "",
        description: "",
        image: ""
    });
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        fetch("http://localhost:8000/front/carousel/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: formData.title,
                description: formData.description,
                image: formData.image
            }),
            credentials: "include"
        }).then(res => res.json())
            .then((data) => {
                if (data.success) {
                    window.location.reload()
                } else {
                    log("error", "add new item carousel error", data);
                }
            }).catch(data => log("error", "add new item carousel error", data));
    };
    return (
        <div className="modal fade" id="addCarousels" tabIndex="-1" aria-labelledby="addSetting" aria-hidden="true">
           <div className="modal-dialog">
                <form className="modal-content" onSubmit={handleSubmit}>
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="RecoverLabel">Add new item carousel</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div className="modal-body">
                        <div className="mb-3">
                            <label htmlFor="title_item" className="form-label">Title</label>
                            <input
                                type="text"
                                className="form-control"
                                id="title_item"
                                name="title"
                                autoComplete="title"
                                value={formData.title}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="description_item" className="form-label">Description</label>
                            <input
                                type="text"
                                className="form-control"
                                id="description_item"
                                name="description"
                                autoComplete="description"
                                value={formData.description}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="image_item" className="form-label">Image</label>
                            <input
                                type="text"
                                className="form-control"
                                id="image_item"
                                name="image"
                                autoComplete="image"
                                value={formData.image}
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