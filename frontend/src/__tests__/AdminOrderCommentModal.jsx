import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import AdminOrderCommentModal from "../components/admin/AdminOrderCommentlModal";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();
delete window.location;
window.location = {reload: jest.fn()};

describe("AdminOrderCommentModal", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("submits comment for given order ID and reloads on success", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    render(<AdminOrderCommentModal />);

    // Симулируем открытие модального окна с data-orders-id="42"
    const event = new CustomEvent("show.bs.modal", {
      detail: {},
      bubbles: true,
    });
    Object.defineProperty(event, "relatedTarget", {
      value: { getAttribute: () => "42" }
    });

    const modal = document.getElementById("AddOrderComment");
    modal.dispatchEvent(event);

    fireEvent.change(screen.getByLabelText("Body"), {
      target: { value: "Processing started" }
    });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "http://localhost:8000/order/add_comment/42",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ body: "Processing started" })
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

    render(<AdminOrderCommentModal />);

    const modal = document.getElementById("AddOrderComment");
    const event = new CustomEvent("show.bs.modal");
    Object.defineProperty(event, "relatedTarget", {
      value: { getAttribute: () => "99" }
    });
    modal.dispatchEvent(event);

    fireEvent.change(screen.getByLabelText("Body"), {
      target: { value: "This is a comment" }
    });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(log).toHaveBeenCalledWith(
        "error",
        "add comment error",
        expect.any(Object)
      );
    });
  });
});
