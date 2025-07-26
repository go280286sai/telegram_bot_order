import React from "react";
import {render, screen, fireEvent, waitFor, cleanup} from "@testing-library/react";
import BlockTwo from "../components/BlockTwo";

global.fetch = jest.fn();
jest.mock("../assets/img/trash.png", () => "trash")
jest.mock("../helps/logs.mjs", () => jest.fn())

describe("BlockTwo component", () => {
    afterEach(() => {
        jest.clearAllMocks();
        cleanup();
    })
    it('Get products', async () => {
        fetch
            .mockResolvedValueOnce({
                json: () => Promise.resolve({
                    data: {
                        products: [
                            {"id": 1, "name": "Name1", "description": "Description1", "price": 20.00},
                            {"id": 2, "name": "Name2", "description": "Description2", "price": 40.00},
                            {"id": 3, "name": "Name3", "description": "Description3", "price": 60.00}
                        ]
                    }
                })
            })
            .mockResolvedValueOnce({
                json: () => Promise.resolve({
                    data: {
                        cart: []
                    }
                })
            });

        render(<BlockTwo/>);
        const id = await screen.findByText("Name1");
        expect(id).toBeInTheDocument();
        const product = await screen.findByText("1");
        expect(product).toBeInTheDocument();
        const description = await screen.findByText("Description1");
        expect(description).toBeInTheDocument();
        const price = await screen.findByText("$20");
        expect(price).toBeInTheDocument();
        fetch
            .mockResolvedValueOnce({})
            .mockResolvedValueOnce({
                json: () => Promise.resolve({
                    data: {
                        cart: [
                            {"id": 1, "name": "Name1", "amount": 1, "amounts": 5, "price": 20.00},
                        ]
                    }
                })
            });

        const btn = screen.getAllByTestId("add_to_cart");
        expect(btn.length).toEqual(3);
        fireEvent.click(btn[0]);
        const modal_name = await screen.findByTestId("modal_name");
        expect(modal_name.textContent).toEqual("Name1");
        const calculateTotal = await screen.findByTestId("calculateTotal")
        expect(calculateTotal.textContent).toEqual("20 $")
    });
})