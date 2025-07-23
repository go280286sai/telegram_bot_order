import React from "react";

export default function GoogleMaps({ settings }){

    return (
        <div>
            <iframe
                title={"google-maps"}
                src={settings.map}
                width="600" height="200"
                allowFullScreen="" loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"></iframe>
        </div>
    )
}