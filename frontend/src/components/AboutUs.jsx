import React, { useState, useEffect } from "react";
import woman from "../assets/img/women.webp";
import man from "../assets/img/man.webp";
import log from "../helps/logs.mjs";

export default function AboutUs() {
    const [reviews, setReviews] = useState([]);
    const avatar = {
        0: woman,
        1: man
    };
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("http://localhost:8000/review/reviews");
                const result = await response.json();
                setReviews(result?.data?.reviews || []);
            } catch (error) {
                await log("error", "get reviews", error);
            }
        };
        fetchData();
    }, []);
    return (
        <div className="row block_1">
            <div id="carouselExampleAutoplaying" className="carousel slide" data-bs-ride="carousel">
                <div className="carousel-inner">
                    {reviews.length > 0 ? (
                        reviews.map((item, index) => (
                            <div
                                className={`carousel-item ${index === 0 ? "active" : ""}`}
                                key={index}>
                                <div
                                    className="about_us d-flex flex-column align-items-center
                                    justify-content-center text-center"
                                    style={{ minHeight: "300px" }}>
                                    <div className="d-flex align-items-center gap-4">
                                        <img
                                            src={avatar[item.gender] || man}
                                            alt={`${item.name}'s avatar`}
                                        />
                                        <div className={"about_us_text"}>
                                            <p>{item.text}</p>
                                            <h5>{item.name}</h5>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))
                    ) : (
                        <div className="carousel-item active">
                            <div
                                className="about_us d-flex flex-column align-items-center
                                justify-content-center text-center"
                                style={{ minHeight: "300px" }}>
                                <p className="reviews">There are no reviews yet</p>
                            </div>
                        </div>
                    )}
                </div>
                <button className="carousel-control-prev"
                        type="button"
                        data-bs-target="#carouselExampleAutoplaying"
                        data-bs-slide="prev">
                    <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span className="visually-hidden">Previous</span>
                </button>
                <button className="carousel-control-next"
                        type="button"
                        data-bs-target="#carouselExampleAutoplaying"
                        data-bs-slide="next">
                    <span className="carousel-control-next-icon" aria-hidden="true"></span>
                    <span className="visually-hidden">Next</span>
                </button>
            </div>
        </div>
    );
}
