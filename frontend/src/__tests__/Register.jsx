import React from "react";
import {render, screen, fireEvent, waitFor, cleanup} from "@testing-library/react";
import Register from "../components/Register";


jest.mock("../helps/logs.mjs", () => jest.fn());
const alertMock = jest.spyOn(window, "alert").mockImplementation(() => {
});
delete window.location;
window.location = {reload: jest.fn()};
global.fetch = jest.fn();

describe("Register component", () => {
    afterEach(() => {
        jest.clearAllMocks();
        cleanup();
    })
    it('Register', async () => {
        render(<Register/>);
        fetch.mockResolvedValue({
            json: ()=>Promise.resolve({
                success: true
            })
        })
        const username = screen.getByLabelText(/Username/i);
        const email = screen.getByLabelText(/Email address/i);
        const phone = screen.getByLabelText(/Phone number/i);
        const password = screen.getByLabelText("Password");
        const confirmPassword = screen.getByLabelText(/Confirm Password/i);

        fireEvent.change(username, {target:{value: "User"}});
        fireEvent.change(email, {target:{value: "User@user.com"}});
        fireEvent.change(phone, {target:{value: "+380000000"}});
        fireEvent.change(password, {target:{value: "1234"}});
        fireEvent.change(confirmPassword, {target:{value: "1234"}});

        const btn = screen.getByTitle("register");
        fireEvent.click(btn);
        await waitFor(()=>{
            expect(window.location.reload).toHaveBeenCalled();
        })
    });
    it('Wrong password', async () => {
        render(<Register/>);
        fetch.mockResolvedValue({
            json: ()=>Promise.resolve({
                success: true
            })
        })
        const username = screen.getByLabelText(/Username/i);
        const email = screen.getByLabelText(/Email address/i);
        const phone = screen.getByLabelText(/Phone number/i);
        const password = screen.getByLabelText("Password");
        const confirmPassword = screen.getByLabelText(/Confirm Password/i);

        fireEvent.change(username, {target:{value: "User"}});
        fireEvent.change(email, {target:{value: "User@user.com"}});
        fireEvent.change(phone, {target:{value: "+380000000"}});
        fireEvent.change(password, {target:{value: "1234"}});
        fireEvent.change(confirmPassword, {target:{value: "123"}});

        const btn = screen.getByTitle("register");
        fireEvent.click(btn);
        await waitFor(()=>{
            expect(alertMock).toHaveBeenCalledWith("Passwords do not match.");
        })
    });
    it('Wrong register', async () => {
        render(<Register/>);
        fetch.mockResolvedValue({
            json: ()=>Promise.resolve({
                success: false
            })
        })
        const username = screen.getByLabelText(/Username/i);
        const email = screen.getByLabelText(/Email address/i);
        const phone = screen.getByLabelText(/Phone number/i);
        const password = screen.getByLabelText("Password");
        const confirmPassword = screen.getByLabelText(/Confirm Password/i);

        fireEvent.change(username, {target:{value: "User"}});
        fireEvent.change(email, {target:{value: "User@user.com"}});
        fireEvent.change(phone, {target:{value: "+380000000"}});
        fireEvent.change(password, {target:{value: "1234"}});
        fireEvent.change(confirmPassword, {target:{value: "1234"}});

        const btn = screen.getByTitle("register");
        fireEvent.click(btn);
        await waitFor(()=>{
            expect(alertMock).toHaveBeenCalledWith("Register is error");
        })
    });
})