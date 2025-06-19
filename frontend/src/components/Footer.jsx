import React from "react";
import Social from "./Social";
import AboutUs from "./AboutUs";

export default function Footer() {
    return (
        <div className={"row block_1"}>
            <div className={"row service"}>
                <div className={"col-7"}>
                    <AboutUs/>
                </div>
                <div className={"col-5"}>
                    <Social/>
                    <form action="" method="post">
                        <div className={"mb-2"}>
                            <label htmlFor="exampleFormControlInput1" className={"form-label"}>Subscriber</label>
                            <input type="email" className={"form-control"} id="exampleFormControlInput1"
                                   placeholder="name@example.com"/>
                        </div>
                        <div>
                            <input type="submit" className={"btn btn-dark"} value="Submit"/>
                        </div>
                    </form>

                </div>
            </div>
        </div>
    )
}