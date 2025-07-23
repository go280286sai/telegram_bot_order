import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import AdminAddSettingModal from "../components/admin/AdminAddSettingModal";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();
delete window.location;
window.location = {reload: jest.fn()};

describe("AdminAddSettingModal", () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it("submits form and reloads page on success", async () => {
        fetch.mockResolvedValueOnce({
            json: () => Promise.resolve({ success: true })
        });

        render(<AdminAddSettingModal />);

        fireEvent.change(screen.getByTestId("item_name"), {
            target: { value: "SettingName" }
        });
        fireEvent.change(screen.getByTestId("item_value"), {
            target: { value: "SettingValue" }
        });

        fireEvent.click(screen.getByText("Send"));

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(
                "http://localhost:8000/setting/create",
                expect.objectContaining({
                    method: "POST",
                    body: JSON.stringify({
                        name: "SettingName",
                        value: "SettingValue"
                    }),
                })
            );
            expect(window.location.reload).toHaveBeenCalled();
        });
    });

    it("logs error if submission fails", async () => {
        const log = require("../helps/logs.mjs");
        fetch.mockResolvedValueOnce({
            json: () => Promise.resolve({ success: false })
        });

        render(<AdminAddSettingModal />);
        fireEvent.change(screen.getByTestId("item_name"), {
            target: { value: "BrokenSetting" }
        });
        fireEvent.change(screen.getByTestId("item_value"), {
            target: { value: "ErrorValue" }
        });

        fireEvent.click(screen.getByText("Send"));

        await waitFor(() => {
            expect(log).toHaveBeenCalledWith(
                "error",
                "add new item setting error",
                expect.any(Object)
            );
        });
    });
});
