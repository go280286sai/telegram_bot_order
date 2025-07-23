import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import AdminSendEmailModal from "../components/admin/AdminSendEmailModal";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();
global.alert = jest.fn();

describe("AdminSendEmailModal", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("submits email and alerts on success", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    render(<AdminSendEmailModal />);

    // simulate modal open with relatedTarget
    const event = new CustomEvent("show.bs.modal", { bubbles: true });
    Object.defineProperty(event, "relatedTarget", {
      value: {
        getAttribute: (attr) => (attr === "data-user-id" ? "42" : "user@example.com")
      }
    });

    const modal = document.getElementById("SendEmail");
    modal.dispatchEvent(event);

    fireEvent.change(screen.getByLabelText("Header"), { target: { value: "Welcome" } });
    fireEvent.change(screen.getByLabelText("Title"), { target: { value: "Account activated" } });
    fireEvent.change(screen.getByLabelText("Body"), { target: { value: "Enjoy our platform!" } });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "http://localhost:8000/user/send_email/42/user@example.com",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            header: "Welcome",
            title: "Account activated",
            body: "Enjoy our platform!"
          })
        })
      );
      expect(global.alert).toHaveBeenCalledWith("Done");
    });
  });

  it("logs error on failed submission", async () => {
    const log = require("../helps/logs.mjs");

    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: false })
    });

    render(<AdminSendEmailModal />);

    const modal = document.getElementById("SendEmail");
    const event = new CustomEvent("show.bs.modal");
    Object.defineProperty(event, "relatedTarget", {
      value: {
        getAttribute: (attr) => (attr === "data-user-id" ? "55" : "fail@mail.com")
      }
    });
    modal.dispatchEvent(event);

    fireEvent.change(screen.getByLabelText("Header"), { target: { value: "Oops" } });
    fireEvent.change(screen.getByLabelText("Title"), { target: { value: "Something wrong" } });
    fireEvent.change(screen.getByLabelText("Body"), { target: { value: "Please try again" } });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(log).toHaveBeenCalledWith("error", "send email user error", expect.any(Object));
    });
  });
});
