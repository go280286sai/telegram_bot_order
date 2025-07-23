import React from "react";
import {render, screen, waitFor, cleanup} from "@testing-library/react";
import OrderCart from "../components/order/OrderCart";

global.fetch = jest.fn();
jest.mock("../helps/logs.mjs", () => jest.fn());
jest.mock("../components/order/OrderDelivery", () => () => (
    <div data-testid="delivery_modal">Delivery Placeholder</div>
));

describe("OrderCart component", () => {
    afterEach(() => {
        jest.clearAllMocks();
        cleanup();
    });

    it("Get order cart", async () => {
        fetch.mockResolvedValueOnce({
            json: () =>
                Promise.resolve({
                    success: true,
                    data: {
                        cart: [
                            {
                                id: 1,
                                name: "Name1",
                                amount: 2,
                                amounts: 5,
                                price: 20.0,
                                description: "description"
                            }
                        ]
                    }
                })
        });

        render(<OrderCart/>);
        expect(await screen.findByText("Name1")).toBeInTheDocument();
        expect(await screen.findByText("2")).toBeInTheDocument();
        expect(await screen.findByText("20.00 $")).toBeInTheDocument();
        const totals = await screen.findAllByText("40.00 $")
        for (let total of totals) {
            expect(total).toBeInTheDocument();
        }
        expect(await screen.findByTestId("delivery_modal")).toBeInTheDocument();
    });
});
