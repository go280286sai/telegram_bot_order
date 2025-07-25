import React from "react";
import {render, screen, fireEvent, waitFor, cleanup} from "@testing-library/react";
import Login from "../components/Login";


jest.mock("../helps/logs.mjs", () => jest.fn());
delete window.location;
window.location = {reload: jest.fn()};
const alertMock = jest.spyOn(window, "alert").mockImplementation(() => {
});
global.fetch = jest.fn();

describe("Login component", () => {
    afterEach(() => {
        jest.clearAllMocks();
        cleanup();
    })

    it("Send login and password fail 1", async () => {
        render(<Login/>);
        const Username = screen.getByLabelText(/Username/i);
        const Password = screen.getByLabelText(/Password/i);

        fireEvent.change(Username, {target: {value: "   "}});
        fireEvent.change(Password, {target: {value: "   "}});

        const btn = screen.getByTestId("login_send");
        fireEvent.click(btn);
        await waitFor(() => {
            expect(alertMock).toHaveBeenCalledWith("Login or password error");
        })
    })
    it("Send login and password fail 2", async () => {
        render(<Login/>);
        fetch.mockResolvedValue({
            json: () => Promise.resolve({
                    success: false
            })
        })
        const Username = screen.getByLabelText(/Username/i);
        const Password = screen.getByLabelText(/Password/i);

        fireEvent.change(Username, {target: {value: "User"}});
        fireEvent.change(Password, {target: {value: "1234"}});

        const btn = screen.getByTestId("login_send");
        fireEvent.click(btn);
        const res = await screen.findByText("Incorrect username or password");
        expect(res).toBeInTheDocument();
    })
    it("Send login and password", async () => {
        render(<Login/>);
        fetch.mockResolvedValue({
            json: () => Promise.resolve({
                    success: true
            })
        })
        const Username = screen.getByLabelText(/Username/i);
        const Password = screen.getByLabelText(/Password/i);

        fireEvent.change(Username, {target: {value: "User"}});
        fireEvent.change(Password, {target: {value: "1234"}});

        const btn = screen.getByTestId("login_send");
        fireEvent.click(btn);
        await waitFor(() => {
            expect(window.location.reload).toHaveBeenCalled()
        })

    })
    it('Recover password', async () => {
        render(<Login/>);
        fetch.mockResolvedValue({
            json: () => Promise.resolve({
                    success: true
            })
        })
        const btn = screen.getByTestId("recovery_link");
        fireEvent.click(btn);
        const title = await screen.findByText("Recover password");
        expect(title).toBeInTheDocument();
        const username = screen.getByLabelText(/Input you username/i);
        const email = screen.getByLabelText(/Input you Email/i);

        fireEvent.change(username, {target: {value: "User"}});
        fireEvent.change(email, {target: {value: "admin@admin.com"}});

        const btn_rec = screen.getByTestId("recovery_password");
        fireEvent.click(btn_rec);
        const login = await screen.findByText("Username")
        expect(login).toBeInTheDocument();
    });
    it('Recover password fail', async () => {
        render(<Login/>);
        fetch.mockResolvedValue({
            json: () => Promise.resolve({
                    success: false
            })
        })
        const btn_recover = screen.getByTestId("recovery_link")
        console.log(btn_recover)
        fireEvent.click(btn_recover);
        const title = await screen.findByText("Recover password");
        expect(title).toBeInTheDocument();
        const username = screen.getByLabelText(/Input you username/i);
        const email = screen.getByLabelText(/Input you Email/i);

        fireEvent.change(username, {target: {value: "User"}});
        fireEvent.change(email, {target: {value: "admin@admin.com"}});

        const btn_rec = screen.getByTestId("recovery_password");
        fireEvent.click(btn_rec);
        await waitFor(()=>{
            expect(window.location.reload).toHaveBeenCalled();
        })
    });
})