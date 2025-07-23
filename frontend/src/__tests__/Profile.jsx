import React from "react";
import {render, screen, fireEvent, waitFor, cleanup} from "@testing-library/react";
import Profile from "../components/Profile";

jest.mock("../helps/logs.mjs", () => jest.fn())
global.fetch = jest.fn();
const alertMock = jest.spyOn(window, "alert").mockImplementation(() => {
});
delete window.location;
window.location = {reload: jest.fn()};
describe("Profile component", () => {
    afterEach(() => {
        jest.clearAllMocks();
        cleanup();
    });

    it("Set first name is empty and set last name is empty", () => {
        render(<Profile user={{
            status: true,
            username: "user",
            first_name: "Admin",
            last_name: "Root",
            email: "admin@admin.com",
            phone: "+3800000000"
        }}/>)
        expect(screen.getByText("user")).toBeInTheDocument();
        expect(screen.getByText("Admin")).toBeInTheDocument();
        expect(screen.getByText("Root")).toBeInTheDocument();
        expect(screen.getByText("admin@admin.com")).toBeInTheDocument();
        expect(screen.getByText("+3800000000")).toBeInTheDocument();
        const btn = screen.getByTitle("first_last_name")
        fireEvent.click(btn)
        expect(alertMock).toHaveBeenCalledWith("First name or last name not is empty");
    })
    it("Set first name and set last name", async () => {
        render(<Profile user={{
            status: true,
            username: "user",
            first_name: "Admin",
            last_name: "Root",
            email: "admin@admin.com",
            phone: "+3800000000"
        }}/>)
        fetch.mockResolvedValue({
            json: () => Promise.resolve({
                data: {
                    success: true
                }
            })
        })
        const firstNameInput = screen.getByLabelText(/First name/i);
        const lastNameInput = screen.getByLabelText(/Last name/i);

        fireEvent.change(firstNameInput, {target: {value: "User1"}})
        fireEvent.change(lastNameInput, {target: {value: "Root1"}})

        const btn = screen.getByTitle("first_last_name")
        fireEvent.click(btn)

        await waitFor(() => {
            expect(alertMock).toHaveBeenCalledWith("Profile is update");
        })
        await waitFor(() => {
            expect(window.location.reload).toHaveBeenCalled();
        })
    })
    it("Save new password fail", async () => {
        render(<Profile user={{
            status: true,
            username: "user",
            first_name: "Admin",
            last_name: "Root",
            email: "admin@admin.com",
            phone: "+3800000000"
        }}/>)
        fetch.mockResolvedValue({
            json: () => Promise.resolve({
                data: {
                    success: false
                }
            })
        })
        const PasswordInput = screen.getByLabelText(/New password/i);
        const ConfirmPasswordInput = screen.getByLabelText(/Confirm Password/i);

        fireEvent.change(PasswordInput, {target: {value: "1234"}})
        fireEvent.change(ConfirmPasswordInput, {target: {value: "12345"}})

        const btn = screen.getByTitle("btn_password")
        fireEvent.click(btn)

        await waitFor(() => {
            expect(alertMock).toHaveBeenCalledWith("Passwords do not match.");
        })
    })
    it("Save new password fail 2", async () => {
        render(<Profile user={{
            status: true,
            username: "user",
            first_name: "Admin",
            last_name: "Root",
            email: "admin@admin.com",
            phone: "+3800000000"
        }}/>)
        fetch.mockResolvedValue({
            json: () => Promise.resolve({
                data: {
                    success: false
                }
            })
        })
        const PasswordInput = screen.getByLabelText(/New password/i);
        const ConfirmPasswordInput = screen.getByLabelText(/Confirm Password/i);

        fireEvent.change(PasswordInput, {target: {value: ""}})
        fireEvent.change(ConfirmPasswordInput, {target: {value: ""}})

        const btn = screen.getByTitle("btn_password")
        fireEvent.click(btn)

        await waitFor(() => {
            expect(alertMock).toHaveBeenCalledWith("Passwords not be empty");
        })
    })
    it("Save new password", async () => {
        render(<Profile user={{
            status: true,
            username: "user",
            first_name: "Admin",
            last_name: "Root",
            email: "admin@admin.com",
            phone: "+3800000000"
        }}/>)
        fetch.mockResolvedValue({
            json: () => Promise.resolve({
                data: {
                    success: true
                }
            })
        })
        const PasswordInput = screen.getByLabelText(/New password/i);
        const ConfirmPasswordInput = screen.getByLabelText(/Confirm Password/i);

        fireEvent.change(PasswordInput, {target: {value: "1234"}})
        fireEvent.change(ConfirmPasswordInput, {target: {value: "1234"}})

        const btn = screen.getByTitle("btn_password")
        fireEvent.click(btn)

        await waitFor(() => {
            expect(alertMock).toHaveBeenCalledWith("Password is update");
        })
        await waitFor(() => {
            expect(window.location.reload).toHaveBeenCalled()
        })
    })
    it("Save new password fail 3", async () => {
        render(<Profile user={{
            status: true,
            username: "user",
            first_name: "Admin",
            last_name: "Root",
            email: "admin@admin.com",
            phone: "+3800000000"
        }}/>)
        fetch.mockResolvedValue({
            json: () => Promise.resolve({
                data: {
                    success: false
                }
            })
        })
        const PasswordInput = screen.getByLabelText(/New password/i);
        const ConfirmPasswordInput = screen.getByLabelText(/Confirm Password/i);

        fireEvent.change(PasswordInput, {target: {value: "1234"}})
        fireEvent.change(ConfirmPasswordInput, {target: {value: "1234"}})

        const btn = screen.getByTitle("btn_password")
        fireEvent.click(btn)

        await waitFor(() => {
            expect(alertMock).toHaveBeenCalledWith("Error update password");
        })
    })
    it("Is lock account", async () => {
        render(<Profile user={{
            status: false,
            username: "user",
            first_name: "Admin",
            last_name: "Root",
            email: "admin@admin.com",
            phone: "+3800000000"
        }}/>)
        const body = await screen.findByText("Your account has been suspended. For more information, please contact support.")
        expect(body).toBeInTheDocument();
    })
    it("Run update", async () => {
        render(<Profile user={{
            status: true,
            username: "user",
            first_name: "Admin",
            last_name: "Root",
            email: "admin@admin.com",
            phone: "+3800000000"
        }}/>)
        fetch.mockResolvedValue({
            json: () => Promise.resolve({
                data: {
                    orders: [{
                        id: 1,
                        total: 1000,
                        status: 0,
                        created_at: "2025-02-02"
                    }]
                }
            })
        })
        const btn = screen.getByTitle("update");
        fireEvent.click(btn);
        const date = await screen.findByText("2025-02-02");
        expect(date).toBeInTheDocument();
        const id = await screen.findByText("1");
        expect(id).toBeInTheDocument();
        const status = await screen.findByText("Wait");
        expect(status).toBeInTheDocument();
        const total = await screen.findByText("1000");
        expect(total).toBeInTheDocument();

    })
})