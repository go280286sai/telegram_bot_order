import React from "react";

export default function Contacts({ settings }) {

    return (
        <div className="row contacts">
            <strong><b className={"contact_title"}>Phone: </b>{settings.phone}</strong>
            <strong><b className={"contact_title"}>E-mail: </b>{settings.email}</strong>
            <strong><b className={"contact_title"}>Address: </b>{settings.address}</strong>
        </div>
    );
}
