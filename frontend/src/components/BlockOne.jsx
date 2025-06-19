import React from "react";
import Social from "./Social";

export default function BlockOne() {
    return (
        <div className="row block_1">
            <div className="col-5">
                <div className={"logo_img"} title={"Sonic Farm"}></div>
            </div>
            <div className="col-5 block_top">
                <h1 className={"title_h1"}>Exclusive Items</h1>
                <p className={"title_pre"}>We offer farm construction, auto shield, exclusive skins, pirate search, and more at unbeatable
                    prices. Upgrade your experience now!</p>
                <Social/>
            </div>
        </div>
    );
}
