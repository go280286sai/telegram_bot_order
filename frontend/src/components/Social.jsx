import React from "react";
import telegram from "../assets/img/telegram.png"
import viber from "../assets/img/viber.png"
import whatsapp from "../assets/img/whatsap.png"
export default function Social(){

    return(
        <div className={"social"}>
            <ul className="d-flex justify-content-around align-items-center list-unstyled">
                <li><a href="" className={"a_hover"}><img src={telegram} alt="Telegram" title={"Telegram"}/></a></li>
                <li><a href="" className={"a_hover"}><img src={viber} alt="Viber" title={"Viber"}/></a></li>
                <li><a href="" className={"a_hover"}><img src={whatsapp} alt="WhatsApp" title={"WhatsApp"}/></a></li>
            </ul>
        </div>
    )
}