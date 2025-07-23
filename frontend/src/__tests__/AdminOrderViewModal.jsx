import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import AdminOrderViewModal from "../components/admin/AdminOrderViewModal";

jest.mock("../helps/logs.mjs", () => jest.fn());
global.fetch = jest.fn();

describe("AdminOrderViewModal", () => {
  const mockOrder = {
    id: 123,
    created: "2025-07-24",
    total: 300,
    invoice: "INV-2025",
    products: [
      { name: "Product A", amount: 2, price: 50 },
      { name: "Service B", amount: 1, price: 200 }
    ],
    user: { first_name: "Alex", last_name: "Developer" },
    delivery: { post_name: "Nova Poshta", city_name: "Kyiv", address_name: "Khreshchatyk 1" }
  };

  beforeEach(() => {
    jest.clearAllMocks();
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true, data: mockOrder })
    });
  });

  it("renders modal and fetches order details", async () => {
    render(<AdminOrderViewModal />);

    // simulate modal open with relatedTarget
    const event = new CustomEvent("show.bs.modal", { bubbles: true });
    Object.defineProperty(event, "relatedTarget", {
      value: { getAttribute: () => "123" }
    });

    const modal = document.getElementById("AdminViewOrder");
    modal.dispatchEvent(event);

    await waitFor(() => {
      expect(screen.getByText(/Purchase invoice/i)).toBeInTheDocument();
      expect(screen.getByText("Order Id:")).toBeInTheDocument();
      expect(screen.getByText(/Product A/)).toBeInTheDocument();
      expect(screen.getByText(/Alex Developer/)).toBeInTheDocument();
      expect(screen.getByText(/Nova Poshta/)).toBeInTheDocument();
      expect(screen.getByText(/Khreshchatyk 1/)).toBeInTheDocument();
    });
  });
});
