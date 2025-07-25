import React from "react";
import {render, screen, fireEvent, waitFor} from "@testing-library/react";
import Footer from "../components/Footer";

// Мокаем зависимости
jest.mock("../helps/logs.mjs", () => jest.fn());

jest.mock("../components/GoogleMaps", () => () => <div data-testid="google-maps"/>);
jest.mock("../components/Contacts", () => () => <div data-testid="contacts"/>);

global.fetch = jest.fn();

const mockSettings = {
    map: "https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d18786.52658104362!2d14.429132556912391!3d50.052595026866626!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f1"
    , email: "test@example.com"
};

describe("Footer component", () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });


    it("submits valid email and displays success", async () => {
        fetch.mockResolvedValueOnce({
            json: () => Promise.resolve({success: true})
        });

        render(<Footer settings={mockSettings}/>);
        const input = screen.getByPlaceholderText("example@example.com");
        const button = screen.getByTestId("submit");

        fireEvent.change(input, {target: {value: "user@example.com"}});
        fireEvent.click(button);
        const success = await screen.findByText("Ok")
        expect(success).toBeInTheDocument();

    });
});
