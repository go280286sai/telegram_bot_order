import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import AdminProductsModal from "../components/admin/AdminProductsModal";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();
delete window.location;
window.location = {reload: jest.fn()};

describe("AdminProductsModal", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("submits product and reloads on success", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    render(<AdminProductsModal />);

    fireEvent.change(screen.getByLabelText("Name"), { target: { value: "Test Product" } });
    fireEvent.change(screen.getByLabelText("Description"), { target: { value: "Product Description" } });
    fireEvent.change(screen.getByLabelText("Amount"), { target: { value: "10" } });
    fireEvent.change(screen.getByLabelText("Price"), { target: { value: "200" } });
    fireEvent.change(screen.getByLabelText("Service"), { target: { value: "1" } });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "http://localhost:8000/product/create",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            name: "Test Product",
            description: "Product Description",
            amount: "10",
            price: "200",
            service: "1"
          })
        })
      );
      expect(window.location.reload).toHaveBeenCalled();
    });
  });

  it("logs error when submission fails", async () => {
    const log = require("../helps/logs.mjs");

    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: false })
    });

    render(<AdminProductsModal />);

    fireEvent.change(screen.getByLabelText("Name"), { target: { value: "Fail Product" } });
    fireEvent.change(screen.getByLabelText("Description"), { target: { value: "Fail Description" } });
    fireEvent.change(screen.getByLabelText("Amount"), { target: { value: "5" } });
    fireEvent.change(screen.getByLabelText("Price"), { target: { value: "99" } });
    fireEvent.change(screen.getByLabelText("Service"), { target: { value: "0" } });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(log).toHaveBeenCalledWith("error", "add new item product error", expect.any(Object));
    });
  });
});
