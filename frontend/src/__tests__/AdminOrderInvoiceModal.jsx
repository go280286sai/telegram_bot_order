import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import AdminOrderInvoiceModal from "../components/admin/AdminOrderInvoiceModal";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();
delete window.location;
window.location = {reload: jest.fn()};

describe("AdminOrderInvoiceModal", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("submits invoice to correct user and order", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    render(<AdminOrderInvoiceModal />);

    // Симулируем открытие модального окна c data-order-id и data-user-id
    const event = new CustomEvent("show.bs.modal", { bubbles: true });
    Object.defineProperty(event, "relatedTarget", {
      value: {
        getAttribute: (attr) => {
          return attr === "data-order-id" ? "99" : attr === "data-user-id" ? "42" : "";
        }
      }
    });

    const modal = document.getElementById("SendInvoice");
    modal.dispatchEvent(event);

    fireEvent.change(screen.getByLabelText("Invoice"), {
      target: { value: "Invoice for order #99" }
    });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "http://localhost:8000/order/send_invoice/42/99",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ body: "Invoice for order #99" })
        })
      );
      expect(window.location.reload).toHaveBeenCalled();
    });
  });

  it("logs error on failed invoice submission", async () => {
    const log = require("../helps/logs.mjs");
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: false })
    });

    render(<AdminOrderInvoiceModal />);

    const modal = document.getElementById("SendInvoice");
    const event = new CustomEvent("show.bs.modal");
    Object.defineProperty(event, "relatedTarget", {
      value: {
        getAttribute: (attr) => (attr === "data-order-id" ? "11" : "22")
      }
    });
    modal.dispatchEvent(event);

    fireEvent.change(screen.getByLabelText("Invoice"), {
      target: { value: "Problematic invoice" }
    });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(log).toHaveBeenCalledWith(
        "error",
        "send invoice user error",
        expect.any(Object)
      );
    });
  });
});
