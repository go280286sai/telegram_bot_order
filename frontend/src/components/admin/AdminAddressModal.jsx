import React, {useState} from "react";
import log from "../../helps/logs.mjs";

export default function AdminAddressModal(){
    const [formData, setFormData] = useState({
        name: "",
        city_id: ""
    });
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        fetch("http://localhost:8000/address/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: formData.name,
                city_id: formData.city_id
            }),
            credentials: "include"
        }).then(res => res.json())
            .then((data) => {
                if (data.success) {
                    window.location.reload()
                } else {
                    log("error", "add new item address error", data);
                }
            }).catch(data => log("error", "add new item address error", data));
    };
    return (
        <div className="modal fade" id="addAddress" tabIndex="-1" aria-labelledby="addAddress" aria-hidden="true">
           <div className="modal-dialog">
               <form className="modal-content" onSubmit={handleSubmit}>
                   <div className="modal-header">
                       <h1 className="modal-title fs-5" id="ReviewLabel">Add new address</h1>
                       <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                   </div>

                   <div className="modal-body">
                       <div className="mb-3">
                           <label htmlFor="Name_item" className="form-label" >Name</label>
                           <input
                               data-testid={"item_name"}
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
                           <label htmlFor="city_id_item" className="form-label">City Id</label>
                           <input
                               data-testid={"item_city"}
                               type="number"
                               className="form-control"
                               id="city_id_item"
                               name="city_id"
                               autoComplete="city_id"
                               value={formData.city_id}
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