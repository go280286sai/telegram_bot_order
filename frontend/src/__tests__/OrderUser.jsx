import React from "react";
import {render, screen, fireEvent, waitFor, cleanup} from "@testing-library/react";
import OrderUser from "../components/order/OrderUser";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();
delete window.location;
window.location = {replace:jest.fn()}
const user_mock = {username: "AdminName", first_name:"Admin", last_name: "Root", email:"admin@admin.com", phone:"+38000000"}
describe("OrderUser component", ()=>{
    afterEach(()=>{
        jest.clearAllMocks();
        cleanup();
    })
    it('User form', () => {
        render(<OrderUser user={user_mock}/>)
        expect(screen.getByText(user_mock.username)).toBeInTheDocument();
        expect(screen.getByText(user_mock.first_name)).toBeInTheDocument();
        expect(screen.getByText(user_mock.last_name)).toBeInTheDocument();
        expect(screen.getByText(user_mock.email)).toBeInTheDocument();
        expect(screen.getByText(user_mock.phone)).toBeInTheDocument();
    });
})