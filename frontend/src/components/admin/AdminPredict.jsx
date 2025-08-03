import React, {useEffect, useState} from "react";
import DataTable from 'datatables.net-dt';
import log from "../../helps/logs.mjs";
import img_1 from "../../assets/img/predict_components.png";
import img_2 from "../../assets/img/predict_forecast.png";
import {IoArrowRedoCircleSharp} from "react-icons/io5";

export default function AdminPredict() {
    const [content, setContent] = useState([]);
    const [formData, setFormData] = useState({
        id: ""
    });
    const handleChange = (e) => {
        const {name, value} = e.target;
        setFormData(prev => ({...prev, [name]: value}));
    };
    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch(`http://localhost:8000/order/get_predict/${formData.id}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({id: formData.id}),
                credentials: "include"
            });

            const data = await response.json();

            if (data.success && data.data.predict !== null) {
                setContent(data.data.predict);
            } else {
                await log("error", "add new item post error", data);
                alert("There is insufficient data for analysis.");
            }
        } catch (error) {
            await log("error", "add new item post error", error);
        }
    };

    useEffect(() => {
        if (content.length > 0) {
            const dtInstance = new DataTable('#myTable');
            return () => {
                dtInstance.destroy();
            };
        }
    }, [content]);


    return (
        <div className={"row block_1 p-1"}>
            <h3>Get predict</h3>
            <div className="mb-3">
                <label htmlFor="term_item" className="form-label">Term</label>
                <form className="modal-content" onSubmit={handleSubmit} style={{width: '10%'}}>
                    <table>
                        <tbody>
                        <tr>
                            <td><input
                                type="text"
                                className="form-control"
                                id="term_item"
                                name="id"
                                autoComplete="id"
                                value={formData.id}
                                onChange={handleChange}
                                required
                            /></td>
                            <td>
                                <button type="submit" className="btn btn-link btn_gen">
                                    <IoArrowRedoCircleSharp className={"IoArrowRedoCircleSharp "} title={"Ok"}/>
                                </button>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </form>
            </div>
            <table id="myTable" className="display table table-dark">
                <thead>
                <tr>
                    <th>Date</th>
                    <th>Predict</th>
                    <th>Predict lower</th>
                    <th>Predict upper</th>
                </tr>
                </thead>
                <tbody>
                {content.map((item) => (
                    <tr key={item.id}>
                        <td>{item.ds}</td>
                        <td>
                            {item.yhat}
                        </td>
                        <td>
                            {item.yhat_lower}
                        </td>
                        <td>
                            {item.yhat_upper}
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
            <div className={"img_predict"}>
                <img src={img_1} alt=""/>
            </div>
            <div className={"img_predict"}>
                <img src={img_2} alt=""/>
            </div>
        </div>
    );
}
