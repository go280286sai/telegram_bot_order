import React from "react";
import {render, screen, waitFor, cleanup} from "@testing-library/react";
import Order from "../components/order/Order";

global.fetch = jest.fn();
delete window.location;
window.location = { replace: jest.fn() };
jest.mock("../helps/logs.mjs", () => jest.fn());
const alertMock = jest.spyOn(window, "alert").mockImplementation(() => {});

jest.mock("../components/Register", () => () => <div data-testid="register_mock">Register Placeholder</div>);
jest.mock("../components/Login", () => () => <div data-testid="login_mock">Login Placeholder</div>);
jest.mock("../components/order/OrderCart", () => () => <div data-testid="orderCart_mock">OrderCart Placeholder</div>);
jest.mock("../components/order/OrderUser", () => () => <div data-testid="orderUser_mock">OrderUser Placeholder</div>);

describe("Order component", () => {
    afterEach(() => {
        jest.clearAllMocks();
        cleanup();
    });

    it("Is not register (shows alert and redirects)", async () => {
        fetch.mockResolvedValueOnce({
            json: () => Promise.resolve({
                success: true,
                data: {
                    status: false,
                    username: "user",
                    first_name: null,
                    last_name: null,
                    email: "admin@admin.com",
                    phone: "+3800000000",
                    is_admin: 0
                }
            })
        });

        render(<Order />);

        // Wait for alert and redirect
        await waitFor(() => {
            expect(alertMock).toHaveBeenCalledWith("The name or surname cannot be empty. Edit profile");
            // eslint-disable-next-line testing-library/no-wait-for-multiple-assertions
            expect(window.location.replace).toHaveBeenCalledWith("/");
        });

        expect(screen.getByTestId("register_mock")).toBeInTheDocument();
        expect(screen.getByTestId("login_mock")).toBeInTheDocument();
        expect(screen.queryByTestId("orderUser_mock")).toBeNull();
        expect(screen.queryByTestId("orderCart_mock")).toBeNull();
    });

    it("Is registered (shows order blocks)", async () => {
        fetch.mockResolvedValueOnce({
            json: () => Promise.resolve({
                success: true,
                data: {
                    status: true,
                    username: "user",
                    first_name: "Admin",
                    last_name: "Root",
                    email: "admin@admin.com",
                    phone: "+3800000000",
                    is_admin: 0
                }
            })
        });

        render(<Order />);

        await waitFor(() => {
            expect(screen.getByTestId("orderUser_mock")).toBeInTheDocument();
            // eslint-disable-next-line testing-library/no-wait-for-multiple-assertions
            expect(screen.getByTestId("orderCart_mock")).toBeInTheDocument();
        });

        expect(screen.queryByTestId("register_mock")).toBeNull();
        expect(screen.queryByTestId("login_mock")).toBeNull();
    });
});
