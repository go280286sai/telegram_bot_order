import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import AdminMailModal from "../components/admin/AdminMailModal";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();
delete window.location;
window.location = {reload: jest.fn()};

describe("AdminMailModal", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("submits form and reloads on success", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    render(<AdminMailModal />);

    fireEvent.change(screen.getByLabelText("Header"), {
      target: { value: "Promo" }
    });
    fireEvent.change(screen.getByLabelText("Title"), {
      target: { value: "Summer Sale" }
    });
    fireEvent.change(screen.getByLabelText("Body"), {
      target: { value: "Up to 50% off!" }
    });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "http://localhost:8000/template/create",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            header: "Promo",
            title: "Summer Sale",
            body: "Up to 50% off!"
          })
        })
      );
      expect(window.location.reload).toHaveBeenCalled();
    });
  });

  it("logs error on failed submission", async () => {
    const log = require("../helps/logs.mjs");
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: false })
    });

    render(<AdminMailModal />);

    fireEvent.change(screen.getByLabelText("Header"), {
      target: { value: "ErrorHeader" }
    });
    fireEvent.change(screen.getByLabelText("Title"), {
      target: { value: "ErrorTitle" }
    });
    fireEvent.change(screen.getByLabelText("Body"), {
      target: { value: "ErrorBody" }
    });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(log).toHaveBeenCalledWith(
        "error",
        "add new item template error",
        expect.any(Object)
      );
    });
  });
});
