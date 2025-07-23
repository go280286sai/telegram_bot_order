import React from "react";
import {render, screen, fireEvent, waitFor, cleanup} from "@testing-library/react";
import AdminCity from "../components/admin/AdminCity";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();

describe("AdminCity component", () => {
    const mockCities = [
        {id: 1, name: "Kyiv", post_id: 101},
        {id: 2, name: "Lviv", post_id: 102}
    ];

    beforeEach(() => {
        fetch.mockResolvedValueOnce({
            json: () => Promise.resolve({
                success: true,
                data: {cities: mockCities}
            })
        });
    });

    afterEach(() => {
        jest.clearAllMocks();
        cleanup();
    });

    it("renders city inputs after fetch", async () => {
        render(<AdminCity/>);
        await waitFor(() => {
            expect(screen.getByDisplayValue("Kyiv")).toBeInTheDocument();
            expect(screen.getByDisplayValue("101")).toBeInTheDocument();
            expect(screen.getByDisplayValue("Lviv")).toBeInTheDocument();
            expect(screen.getByDisplayValue("102")).toBeInTheDocument();
        });
    });

    it("calls fetchUpdate when Update is clicked", async () => {
        fetch
            .mockResolvedValueOnce({ // refetch after update
                json: () => Promise.resolve({success: true, data: {cities: mockCities}})
            });
        render(<AdminCity/>);
        const item_update = await screen.findAllByTestId("item_update")
        await waitFor(() => {
            expect(item_update[0]).toBeInTheDocument();
        });

        fireEvent.click(item_update[0]);

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining("/city/update/1"),
                expect.objectContaining({
                    method: "POST",
                    body: JSON.stringify({name: "Kyiv", post_id: 101})
                })
            );
        });
    });

    it("calls fetchDelete when Delete is clicked", async () => {
        fetch
            .mockResolvedValueOnce({ // refetch after delete
                json: () => Promise.resolve({success: true, data: {cities: mockCities}})
            });
        render(<AdminCity/>);
        const item_delete = await screen.findAllByTestId("item_delete")

        await waitFor(() => {
            expect(item_delete[0]).toBeInTheDocument();
        });

        fireEvent.click(item_delete[0]);

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining("/city/delete/1"),
                expect.objectContaining({
                    method: "POST"
                })
            );
        });
    });
});
