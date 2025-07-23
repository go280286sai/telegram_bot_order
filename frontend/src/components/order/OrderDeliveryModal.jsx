import React, {useEffect, useState} from "react";
import log from "../../helps/logs.mjs";

export default function OrderDeliveryModal() {
    const [formData, setFormData] = useState({
        post: "",
        city: "",
        address: "",
    });
    const [selectPost, setSelectPost] = useState([]);
    const [selectCity, setSelectCity] = useState([]);
    const [selectAddress, setSelectAddress] = useState([]);

    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData((prev) => ({...prev, [name]: value}));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        fetch("http://localhost:8000/cart/delivery/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                post_id: formData.post,
                city_id: formData.city,
                address_id: formData.address
            }),
            credentials: "include"
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.success) {
                    window.location.reload();
                } else {
                    log("error", "add new item product error", data);
                }
            })
            .catch((data) => log("error", "add new item product error", data));
    };

    const fetchPost = async () => {
        try {
            const response = await fetch("http://localhost:8000/post/gets", {
                method: "GET",
                credentials: "include",
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            if (data.success) {
                setSelectPost(data.data.posts);
            }
        } catch (error) {
            await log("error", "deliveries", error);
        }
    };

    const fetchCity = async (postId) => {
        try {
            const response = await fetch(`http://localhost:8000/city/get/${postId}`, {
                method: "GET",
                credentials: "include",
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            if (data.success) {
                setSelectCity(data.data.cities);
            }
        } catch (error) {
            await log("error", "cities", error);
        }
    };

    const fetchAddress = async (cityId) => {
        try {
            const response = await fetch(`http://localhost:8000/address/get/${cityId}`, {
                method: "GET",
                credentials: "include",
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            if (data.success) {
                setSelectAddress(data.data.addresses);
            }
        } catch (error) {
            await log("error", "address", error);
        }
    };

    useEffect(() => {
        fetchPost();
    }, []);

    useEffect(() => {
        if (formData.post) {
            fetchCity(formData.post);
            setFormData(prev => ({
                ...prev,
                city: "",
                address: ""
            }));
            setSelectAddress([]);
        }
    }, [formData.post]);

    useEffect(() => {
        if (formData.city) {
            fetchAddress(formData.city);
            setFormData(prev => ({
                ...prev,
                address: ""
            }));
        } else {
            setSelectAddress([]);
        }
    }, [formData.city]);

    return (
        <div className="modal fade" id="addDelivery" tabIndex="-1" aria-labelledby="addProducts" aria-hidden="true">
            <div className="modal-dialog">
                <form className="modal-content" onSubmit={handleSubmit}>
                    <div className="modal-header">
                        <h1 className="modal-title fs-5" id="ReviewLabel">Add new item delivery</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <div className="modal-body">
                        <div className="mb-3">
                            <label htmlFor="Post_item" className="form-label">Post</label>
                            <select
                                data-testid={"post_input"}
                                className="form-select"
                                name="post"
                                value={formData.post}
                                onChange={handleChange}
                                required>
                                <option value="">Select post</option>
                                {selectPost.map((value) => (
                                    <option value={value.id} key={value.id}>{value.name}</option>
                                ))}
                            </select>
                        </div>

                        <div className="mb-3">
                            <label htmlFor="City_item" className="form-label">City</label>
                            <select
                                className="form-select"
                                name="city"
                                value={formData.city}
                                onChange={handleChange}
                                required
                                disabled={!selectCity.length}>
                                <option value="">Select city</option>
                                {selectCity.map((value) => (
                                    <option value={value.id} key={value.id}>{value.name}</option>
                                ))}
                            </select>
                        </div>

                        <div className="mb-3">
                            <label htmlFor="Address_item" className="form-label">Address</label>
                            <select
                                className="form-select"
                                name="address"
                                value={formData.address}
                                onChange={handleChange}
                                required
                                disabled={!selectAddress.length}>
                                <option value="">Select address</option>
                                {selectAddress.map((value) => (
                                    <option value={value.id} key={value.id}>{value.name}</option>
                                ))}
                            </select>
                        </div>
                    </div>
                    <div className="modal-footer">
                        <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Exit</button>
                        <button type="submit" className="btn btn-primary">Send</button>
                    </div>
                </form>
            </div>
        </div>
    );
}
