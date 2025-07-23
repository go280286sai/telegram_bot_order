import React from "react";
import { render, screen } from "@testing-library/react";
import Contacts from "../components/Contacts";

const mockSettings = {
    phone: "+380000000",
    email: "admin@admin.com",
    address: "Main street"
}

describe("Contact component",  () => {
    it('Get elements', async() => {
        render(<Contacts settings={mockSettings}/>)
        const phone = await screen.findByText(mockSettings.phone)
        expect(phone).toBeInTheDocument();
        const email = await screen.findByText(mockSettings.email);
        expect(email).toBeInTheDocument();
        const address = await screen.findByText(mockSettings.address)
        expect(address).toBeInTheDocument();
    });
});
