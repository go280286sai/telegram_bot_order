import React from "react";
import {render, screen, fireEvent, waitFor, cleanup} from "@testing-library/react";
import OrderPay from "../components/order/OrderPay";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();
delete window.location;
window.location = {replace:jest.fn()}

describe("OrderPay component", ()=>{
    afterEach(()=>{
        jest.clearAllMocks();
        cleanup();
    })
    it('Send pay', async () => {
        fetch
            .mockResolvedValueOnce({
                json: ()=>Promise.resolve({
                    success: true,
                    data:{transaction_id:"123456789"}
                })
            })
            .mockResolvedValueOnce({
                json: ()=>Promise.resolve({
                    success: true
                })
            })
        render(<OrderPay/>);
        const cart_number = screen.getByLabelText(/Card Number/i);
        fireEvent.change(cart_number, {target:{value: 1234567897894561}});

        const cart_year = screen.getByLabelText(/Expiry Year/i);
        fireEvent.change(cart_year, {target:{value: 26}});

        const cart_month = screen.getByLabelText(/Expiry Month/i);
        fireEvent.change(cart_month, {target:{value: 2}});

        const cart_secret = screen.getByLabelText(/Card cvv/i);
        fireEvent.change(cart_secret, {target:{value: 123}});
        const btn = screen.getByTestId("pay_btn");
        fireEvent.click(btn);
        await waitFor(()=>{
            expect(window.location.replace).toHaveBeenCalledWith("/");
        })
    });
    it('Send pay card error', async () => {
        fetch
            .mockResolvedValueOnce({
                json: ()=>Promise.resolve({
                    success: true,
                    data:{transaction_id:"123456789"}
                })
            })
            .mockResolvedValueOnce({
                json: ()=>Promise.resolve({
                    success: true
                })
            })
        render(<OrderPay/>);
        const cart_number = screen.getByLabelText(/Card Number/i);
        fireEvent.change(cart_number, {target:{value: 123456789789451}});

        const cart_year = screen.getByLabelText(/Expiry Year/i);
        fireEvent.change(cart_year, {target:{value: 26}});

        const cart_month = screen.getByLabelText(/Expiry Month/i);
        fireEvent.change(cart_month, {target:{value: 2}});

        const cart_secret = screen.getByLabelText(/Card cvv/i);
        fireEvent.change(cart_secret, {target:{value: 123}});
        const btn = screen.getByTestId("pay_btn");
        fireEvent.click(btn);
        const err = await screen.findByText("Number card error");
        expect(err).toBeInTheDocument();
    });
})