import React from "react";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import AdminAddress from "../components/admin/AdminAddress";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();

describe("AdminAddress component", () => {
    const mockAddresses = [
        { id: 1, name: "Shevchenka St", city_id: 101 },
        { id: 2, name: "Independence Ave", city_id: 102 },
    ];

    afterEach(() => {
        jest.clearAllMocks();
        cleanup();
    });

    it("should fetch and render address list", async () => {
        fetch.mockResolvedValueOnce({
            json: () => Promise.resolve({
                success: true,
                data: { addresses: mockAddresses }
            })
        });

        render(<AdminAddress />);

        await waitFor(() => {
            expect(screen.getByDisplayValue("Shevchenka St")).toBeInTheDocument();
            // eslint-disable-next-line testing-library/no-wait-for-multiple-assertions
            expect(screen.getByDisplayValue("101")).toBeInTheDocument();
            // eslint-disable-next-line testing-library/no-wait-for-multiple-assertions
            expect(screen.getByDisplayValue("Independence Ave")).toBeInTheDocument();
            // eslint-disable-next-line testing-library/no-wait-for-multiple-assertions
            expect(screen.getByDisplayValue("102")).toBeInTheDocument();
        });
    });

    it("should call fetchUpdate when clicking Update button", async () => {
        fetch
            .mockResolvedValueOnce({ // fetchAddresses
                json: () => Promise.resolve({
                    success: true,
                    data: { addresses: mockAddresses }
                })
            })
            .mockResolvedValueOnce({ // fetchUpdate
                json: () => Promise.resolve({ success: true })
            });

        render(<AdminAddress />);
        await waitFor(() => {
            expect(screen.getByDisplayValue("Shevchenka St")).toBeInTheDocument();
            // eslint-disable-next-line testing-library/no-wait-for-multiple-assertions
            expect(screen.getByDisplayValue("101")).toBeInTheDocument();
            // eslint-disable-next-line testing-library/no-wait-for-multiple-assertions
            expect(screen.getByDisplayValue("Independence Ave")).toBeInTheDocument();
            // eslint-disable-next-line testing-library/no-wait-for-multiple-assertions
            expect(screen.getByDisplayValue("102")).toBeInTheDocument();
        });
        const updateButtons = await screen.findAllByTestId("btn_update");
        fireEvent.click(updateButtons[0]);

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining("/address/update/1"),
                expect.objectContaining({
                    method: "POST"
                })
            );
        });
    });

    it("should call fetchDelete when clicking Delete button", async () => {
        fetch
            .mockResolvedValueOnce({ // fetchAddresses
                json: () => Promise.resolve({
                    success: true,
                    data: { addresses: mockAddresses }
                })
            })
            .mockResolvedValueOnce({ // fetchDelete
                json: () => Promise.resolve({ success: true })
            });

        render(<AdminAddress />);

        const deleteButtons = await screen.findAllByTestId("btn_delete");
        fireEvent.click(deleteButtons[0]);

        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(
                expect.stringContaining("/address/delete/1"),
                expect.objectContaining({
                    method: "POST"
                })
            );
        });
    });
});
