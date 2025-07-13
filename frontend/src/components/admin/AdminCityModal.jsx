import React, {useState} from "react";
import log from "../../helps/logs.mjs";

export default function AdminCityModal(){
    const [formData, setFormData] = useState({
        name: "",
        post_id: ""
    });
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        fetch("http://localhost:8000/city/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: formData.name,
                post_id: formData.post_id
            }),
            credentials: "include"
        }).then(res => res.json())
            .then((data) => {
                if (data.success) {
                    window.location.reload()
                } else {
                    log("error", "add new item city error", data);
                }
            }).catch(data => log("error", "add new item city error", data));
    };
    return (
        <div className="modal fade" id="addCity" tabIndex="-1" aria-labelledby="addCity" aria-hidden="true">
           <div className="modal-dialog">
               <form className="modal-content" onSubmit={handleSubmit}>
                   <div className="modal-header">
                       <h1 className="modal-title fs-5" id="ReviewLabel">Add new city</h1>
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
                   </div>
                   <div className="modal-body">
                       <div className="mb-3">
                           <label htmlFor="post_id_item" className="form-label">Post Id</label>
                           <input
                               type="number"
                               className="form-control"
                               id="post_id_item"
                               name="post_id"
                               autoComplete="post_id"
                               value={formData.post_id}
                               onChange={handleChange}
                               required
                           />
                       </div>
                   </div>
                   <div className="modal-footer">
                       <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Exit</button>
                       <button type="submit" className="btn btn-primary">Send</button>
                   </div>
               </form>
           </div>
        </div>
    )
}