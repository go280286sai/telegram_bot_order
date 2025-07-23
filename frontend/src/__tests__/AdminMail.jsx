import React from "react";
import {render, screen, fireEvent, waitFor, cleanup} from "@testing-library/react";
import AdminMail from "../components/admin/AdminMail";

jest.mock("../helps/logs.mjs", () => jest.fn());
global.fetch = jest.fn();
delete window.location
window.location = {reload: jest.fn()};

describe("AdminMail component", () => {
    const mockTemplates = [
        {id: 1, header: "Promo", title: "Summer Sale", body: "Up to 50% off!"},
        {id: 2, header: "Update", title: "New Products", body: "Check out our new arrivals"}
    ];

    beforeEach(() => {
        fetch.mockResolvedValueOnce({
            json: () => Promise.resolve({
                success: true,
                data: {templates: mockTemplates}
            })
        });


    });

    afterEach(() => {
        jest.clearAllMocks();
        cleanup();
    });

    it("renders templates after fetch", async () => {
        render(<AdminMail/>);
        await waitFor(() => {
            expect(screen.getByDisplayValue("Promo")).toBeInTheDocument();
            expect(screen.getByDisplayValue("Summer Sale")).toBeInTheDocument();
            expect(screen.getByDisplayValue("Up to 50% off!")).toBeInTheDocument();
        });

        expect(screen.getByDisplayValue("Update")).toBeInTheDocument();
        expect(screen.getByDisplayValue("New Products")).toBeInTheDocument();
        expect(screen.getByDisplayValue("Check out our new arrivals")).toBeInTheDocument();
    });

    it("updates a template when Update is clicked", async () => {
        fetch
            .mockResolvedValueOnce({json: () => Promise.resolve({success: true, data: {templates: mockTemplates}})})
            .mockResolvedValueOnce({
                json: () => Promise.resolve({
                    success: true,
                    data: {templates: mockTemplates}
                })
            });
        render(<AdminMail/>);
        const item_update = await screen.findAllByTestId("item_update");
        fireEvent.click(item_update[0]);

        await waitFor(() => {
            const calls = fetch.mock.calls;
            const updateCall = calls.find(([url]) => url.includes("/template/update/1"));
            const [, options] = updateCall;
            const parsedBody = JSON.parse(options.body);

            expect(parsedBody).toEqual({
                header: "Promo",
                title: "Summer Sale",
                body: "Up to 50% off!"
            });

            expect(options.method).toBe("POST");
        });

    });

    it("sends to users and reloads", async () => {
        fetch.mockResolvedValueOnce({json: () => Promise.resolve({success: true})});
        render(<AdminMail/>);
        const item_send = await screen.findAllByTestId("item_send_user");
        fireEvent.click(item_send[0]);

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining("/template/send_users/1"),
                expect.objectContaining({method: "POST"})
            );
            expect(window.location.reload).toHaveBeenCalled();
        });
    });

    it("sends to subscribers and reloads", async () => {
        fetch.mockResolvedValueOnce({json: () => Promise.resolve({success: true})});
        render(<AdminMail/>);
        const item_send = await screen.findAllByTestId("item_send_subscriber")
        fireEvent.click(item_send[0]);

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining("/subscriber/send_subscribers/1"),
                expect.objectContaining({method: "POST"})
            );
            expect(window.location.reload).toHaveBeenCalled();
        });
    });

    it("deletes a template and reloads", async () => {
        fetch.mockResolvedValueOnce({json: () => Promise.resolve({success: true})});
        render(<AdminMail/>);
        const item_delete = await screen.findAllByTestId("item_delete")

        fireEvent.click(item_delete[0]);

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining("/template/delete/1"),
                expect.objectContaining({method: "POST"})
            );
            expect(window.location.reload).toHaveBeenCalled();
        });
    });
});
