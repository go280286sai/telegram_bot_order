import React from "react";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import AdminAddressModal from "../components/admin/AdminAddressModal";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();
delete window.location
window.location = {reload: jest.fn()};
describe("AdminAddressModal component", () => {
    afterEach(() => {
        jest.clearAllMocks();
        cleanup();
    });

    it("submits valid form data and reloads page on success", async () => {
        fetch.mockResolvedValueOnce({
            json: () => Promise.resolve({ success: true })
        });

        render(<AdminAddressModal />);
        fireEvent.change(screen.getByTestId("item_name"), {
            target: { value: "Test Street" }
        });

        fireEvent.change(screen.getByTestId("item_city"), {
            target: { value: "202" }
        });

        fireEvent.click(screen.getByText("Send"));

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(
                "http://localhost:8000/address/create",
                expect.objectContaining({
                    method: "POST",
                    body: JSON.stringify({ name: "Test Street", city_id: "202" }),
                })
            );
            // eslint-disable-next-line testing-library/no-wait-for-multiple-assertions
            expect(window.location.reload).toHaveBeenCalled();
        });
    });

    it("logs error if form submission fails", async () => {
        const mockLog = require("../helps/logs.mjs");
        fetch.mockResolvedValueOnce({
            json: () => Promise.resolve({ success: false })
        });

        render(<AdminAddressModal />);
        fireEvent.change(screen.getByTestId("item_name"), {
            target: { value: "Fail Street" }
        });

        fireEvent.change(screen.getByTestId("item_city"), {
            target: { value: "999" }
        });

        fireEvent.click(screen.getByText("Send"));

        await waitFor(() => {
            expect(mockLog).toHaveBeenCalledWith(
                "error",
                "add new item address error",
                expect.any(Object)
            );
        });
    });
});
