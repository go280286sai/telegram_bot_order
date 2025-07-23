import React from "react";
import {render, screen, waitFor, cleanup, fireEvent} from "@testing-library/react";
import OrderDelivery from "../components/order/OrderDelivery";

global.fetch = jest.fn();
jest.mock("../helps/logs.mjs", () => jest.fn());
jest.mock("../components/order/OrderPay", () => () => (
    <div data-testid="pay_modal">Pay Placeholder</div>
));
jest.mock("../components/order/OrderDeliveryModal", () => () => (
    <div data-testid="orderDeliveryModal_modal">OrderDeliveryModal Placeholder</div>
));
delete window.location
window.location = {reload: jest.fn()};
describe("OrderDelivery component", () => {
    afterEach(() => {
        jest.clearAllMocks();
        cleanup();
    })
    it('Order delivery is true', async () => {
        fetch.mockResolvedValueOnce({
            json: () => Promise.resolve({
                success: true,
                data: {post_name: "Mist", city_name: "Kiev", address_name: "Peremoga, 6"}
            })
        })

        render(<OrderDelivery/>);
        const post_name = await screen.findByText("Mist");
        expect(post_name).toBeInTheDocument();
        const city_name = await screen.findByText("Kiev");
        expect(city_name).toBeInTheDocument();
        const address_name = await screen.findByText("Peremoga, 6");
        expect(address_name).toBeInTheDocument();
    });
    it('Order delivery is false', async () => {
        fetch.mockResolvedValueOnce({
            json: () => Promise.resolve({
                success: false,
                data: {post_name: "Mist", city_name: "Kiev", address_name: "Peremoga, 6"}
            })
        })
        render(<OrderDelivery/>);
        expect(screen.getByText("Add delivery")).toBeInTheDocument();
        expect(screen.getByTestId("orderDeliveryModal_modal")).toBeInTheDocument();
    });
    it('Order delivery is delete', async () => {
        fetch
            .mockResolvedValueOnce({
            json: () => Promise.resolve({
                success: true,
                data: {post_name: "Mist", city_name: "Kiev", address_name: "Peremoga, 6"}
            })
        })
            .mockResolvedValueOnce({
                json: () => Promise.resolve({
                    success: true
                })
            })
        render(<OrderDelivery/>);
        const post_name = await screen.findByText("Mist");
        expect(post_name).toBeInTheDocument();
        const city_name = await screen.findByText("Kiev");
        expect(city_name).toBeInTheDocument();
        const address_name = await screen.findByText("Peremoga, 6");
        expect(address_name).toBeInTheDocument();
        const btn = screen.getByTestId("deleteDelivery");
        fireEvent.click(btn);
        await waitFor(() => {
            expect(window.location.reload).toHaveBeenCalled();
        })
    });
})