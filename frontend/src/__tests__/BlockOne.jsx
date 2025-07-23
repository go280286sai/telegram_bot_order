import React from "react";
import {render, screen, cleanup} from "@testing-library/react";
import BlockOne from "../components/BlockOne";



jest.mock("../helps/logs.mjs", () => jest.fn());
global.fetch = jest.fn();
jest.mock('../components/Social', () => () => <div data-testid="social-mock">Social Placeholder</div>);
jest.mock("../components/Register", () => () => <div data-testid={"register-mock"}>Register Placeholder</div>)
jest.mock("../components/Login", () => () => <div data-testid={"login-mock"}>Login Placeholder</div>)
jest.mock("../components/Profile", () => () => <div data-testid={"profile-mock"}>Profile Placeholder</div>)

describe("Block One component", () => {
    afterEach(() => {
        jest.clearAllMocks();
        cleanup();
    });
    it("Is auth", async () => {
        render(<BlockOne settings={{"title": "Title", "description": "Description"}}/>)
        const title = await screen.findByText("Title");
        expect(title).toBeInTheDocument();
        const description = await screen.findByText("Description");
        expect(description).toBeInTheDocument();
        const login = screen.getByTitle("login_modal")
        expect(login).toBeInTheDocument();
        const login_modal = screen.getByTestId("login-mock");
        expect(login_modal).toBeInTheDocument();
        const register_modal = screen.getByTestId("register-mock");
        expect(register_modal).toBeInTheDocument();
        const social_modal = screen.getByTestId("social-mock");
        expect(social_modal).toBeInTheDocument();
        const profile_modal = screen.getByTestId("profile-mock");
        expect(profile_modal).toBeInTheDocument();
    });
    test('shows Profile/Logout when user is authenticated', async () => {
        fetch.mockResolvedValueOnce({
            json: async () => ({
                success: true,
                data: {
                    user: {username: 'Alex', email: 'test@test.com', phone: '0000', status: true},
                },
            }),
        });

        render(<BlockOne settings={{"title": "Title", "description": "Description"}}/>);

        const profile_title_mock = await screen.findByTestId("profile_title_mock");
        expect(profile_title_mock).toBeInTheDocument();
        expect(screen.queryByTestId("login_title_mock")).toBeNull();
        expect(screen.queryByTestId("register_title_mock")).toBeNull();
        const logout_title_mock = await screen.findByTestId("logout_title_mock");
        expect(logout_title_mock).toBeInTheDocument();
    });
    test('shows Login/Register when user is not authenticated', async () => {
        fetch.mockResolvedValueOnce({
            json: async () => ({
                success: true,
                data: {
                    user: {username: 'Alex', email: 'test@test.com', phone: '0000', status: false},
                },
            }),
        });

        render(<BlockOne settings={{"title": "Title", "description": "Description"}}/>);

        expect(screen.queryByTestId("profile_title_mock")).toBeNull();
        expect(screen.getByTestId("login_title_mock")).toBeInTheDocument();
        expect(screen.getByTestId("register_title_mock")).toBeInTheDocument();
        expect(screen.queryByTestId("logout_title_mock")).toBeNull();
    });

})