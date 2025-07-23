import React from "react";
import { render, screen, waitFor, fireEvent, cleanup } from "@testing-library/react";
import AdminOrders from "../components/admin/AdminOrders";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();

// Замена модальных компонентов на заглушки
jest.mock("../components/admin/AdminProductsModal", () => () => <div data-testid="modal-products" />);
jest.mock("../components/admin/AdminOrderInvoiceModal", () => () => <div data-testid="modal-invoice" />);
jest.mock("../components/admin/AdminOrderCommentlModal", () => () => <div data-testid="modal-comment" />);
jest.mock("../components/admin/AdminOrderViewModal", () => () => <div data-testid="modal-view" />);

describe("AdminOrders component", () => {
  const mockOrders = [
    {
      id: 1,
      products: "Product A, Product B",
      user: "42",
      delivery: "Nova Poshta",
      total: "100",
      transaction_id: "tx123",
      status: false,
      created_at: "2025-07-20",
      invoice: "",
      comment: ""
    },
    {
      id: 2,
      products: "Product C",
      user: "99",
      delivery: "UkrPoshta",
      total: "200",
      transaction_id: "tx456",
      status: true,
      created_at: "2025-07-21",
      invoice: "paid",
      comment: "Delivered"
    }
  ];

  beforeEach(() => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({
        success: true,
        data: { orders: mockOrders }
      })
    });
    render(<AdminOrders />);
  });

  afterEach(() => {
    jest.clearAllMocks();
    cleanup();
  });

  it("renders orders from API", async () => {
    await waitFor(() => {
      expect(screen.getByText("Product A, Product B")).toBeInTheDocument();
      expect(screen.getByText("tx456")).toBeInTheDocument();
      expect(screen.getByText("Delivered")).toBeInTheDocument();
      expect(screen.getByText("Nova Poshta")).toBeInTheDocument();
    });
  });

  it("triggers delete when Delete button is clicked", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true, data: { orders: mockOrders } })
    });

    const deleteButtons = await screen.findAllByTestId("item_delete");
    fireEvent.click(deleteButtons[0]);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("/order/delete/1"),
        expect.objectContaining({ method: "POST" })
      );
    });
  });

  it("renders modal components", () => {
    expect(screen.getByTestId("modal-products")).toBeInTheDocument();
    expect(screen.getByTestId("modal-invoice")).toBeInTheDocument();
    expect(screen.getByTestId("modal-comment")).toBeInTheDocument();
    expect(screen.getByTestId("modal-view")).toBeInTheDocument();
  });
});
