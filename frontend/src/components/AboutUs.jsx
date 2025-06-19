import React from "react";
import woman from "../assets/img/women.webp";
import man from "../assets/img/man.webp";

export default function AboutUs() {
    return (
        <div className="row">
            <div id="carouselExampleAutoplaying" className="carousel slide" data-bs-ride="carousel">
                <div className="carousel-inner">

                    <div className="carousel-item active">
                        <div className="about_us d-flex flex-column align-items-center justify-content-center text-center" style={{ minHeight: "300px" }}>
                            <div className="d-flex align-items-center gap-4">
                                <img src={man} alt="Client" />
                                <div>
                                    <p>Пожалуй, сложный человек, но работает на все 100%! Спасибо за отличную работу!</p>
                                    <h5>Senor Oso</h5>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="carousel-item">
                        <div className="about_us d-flex flex-column align-items-center justify-content-center text-center" style={{ minHeight: "300px" }}>
                            <div className="d-flex align-items-center gap-4">
                                <img src={man} alt="Client" />
                                <div>
                                    <p>Excellente gestion des fermes. Travailler avec vous est un vrai plaisir. Moins de souci pour moi — je recommande Sonic sans hésiter !</p>
                                    <h5>Djo</h5>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="carousel-item">
                        <div className="about_us d-flex flex-column align-items-center justify-content-center text-center" style={{ minHeight: "300px" }}>
                            <div className="d-flex align-items-center gap-4">
                                <img src={woman} alt="Client" />
                                <div>
                                    <p>Быстрый сервис, хорошие цены, приятное общение — за пару месяцев сотрудничества только плюсы!</p>
                                    <h5>Angel</h5>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>

                <button className="carousel-control-prev" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="prev">
                    <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span className="visually-hidden">Previous</span>
                </button>

                <button className="carousel-control-next" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="next">
                    <span className="carousel-control-next-icon" aria-hidden="true"></span>
                    <span className="visually-hidden">Next</span>
                </button>
            </div>
        </div>
    );
}
