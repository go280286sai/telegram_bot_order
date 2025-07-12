import React, {useState, useEffect} from "react";
import one from "../assets/img/carusel/1.webp"
import two from "../assets/img/carusel/2.webp"
import three from "../assets/img/carusel/3.webp"
import four from "../assets/img/carusel/4.webp"
import five from "../assets/img/carusel/5.webp"
import six from "../assets/img/carusel/1.webp"
import seven from "../assets/img/carusel/2.webp"
import eight from "../assets/img/carusel/3.webp"
import nine from "../assets/img/carusel/4.webp"
import ten from "../assets/img/carusel/5.webp"
import log from "../helps/logs.mjs";
export default function Carousel() {
    const mapImages = {
        "1": one,
        "2": two,
        "3": three,
        "4": four,
        "5": five,
        "6": six,
        "7": seven,
        "8": eight,
        "9": nine,
        "10": ten
    }
    const [images, setImages] = useState([])
    useEffect(() => {
        const fetchCarousel = async () => {
            try {
                const response = await fetch("http://localhost:8000/front/carousel/gets", {
                    method: "GET",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json"
                    }
                });
                const result = await response.json();
                if (result.data) {
                    setImages(result.data.carousels);
                }
            } catch (error) {
                await log("error", "carousels", error);
            }
        };
        fetchCarousel();
    }, []);
    return (
        <div className="row block_1">
            <div id="carouselExampleDark" className="carousel carousel-dark slide service" data-bs-ride="carousel">

                {/* Индикаторы */}
                <div className="carousel-indicators">
                    {images.map((item, index) => (
                        <button
                            type="button"
                            data-bs-target="#carouselExampleDark"
                            data-bs-slide-to={index}
                            className={index === 0 ? "active" : ""}
                            aria-current={index === 0 ? "true" : undefined}
                            aria-label={`Slide ${index + 1}`}
                            key={item.id || index}
                        ></button>
                    ))}
                </div>

                {/* Слайды */}
                <div className="carousel-inner">
                    {images.map((item, index) => (
                        <div
                            className={`carousel-item ${index === 0 ? "active" : ""}`}
                            data-bs-interval="10000"
                            key={item.id || index}
                        >
                            <img
                                src={mapImages[item.id?.toString()]}
                                className="d-block w-100"
                                alt={`slide-${item.id}`}
                            />
                            <div className="carousel-caption d-none d-md-block">
                                <h5 className="rekl_h5">{item.title}</h5>
                                <p className="rekl_p">{item.description}</p>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Навигация */}
                <button className="carousel-control-prev" type="button" data-bs-target="#carouselExampleDark"
                        data-bs-slide="prev">
                    <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span className="visually-hidden">Previous</span>
                </button>
                <button className="carousel-control-next" type="button" data-bs-target="#carouselExampleDark"
                        data-bs-slide="next">
                    <span className="carousel-control-next-icon"  aria-hidden="true"></span>
                    <span className="visually-hidden">Next</span>
                </button>
            </div>
        </div>

    )
}