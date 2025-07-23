import React from "react";
import { render, screen, waitFor, fireEvent, cleanup } from "@testing-library/react";
import AdminProducts from "../components/admin/AdminProducts";

jest.mock("../helps/logs.mjs", () => jest.fn());
global.fetch = jest.fn();

jest.mock("../components/admin/AdminProductsModal", () => () => <div data-testid="modal-products" />);

describe("AdminProducts component", () => {
  const mockProducts = [
    {
      id: 1,
      name: "Product A",
      description: "Desc A",
      amount: 10,
      service: 1,
      price: 100
    },
    {
      id: 2,
      name: "Product B",
      description: "Desc B",
      amount: 5,
      service: 0,
      price: 50
    }
  ];

  beforeEach(() => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({
        success: true,
        data: { products: mockProducts }
      })
    });

    render(<AdminProducts />);
  });

  afterEach(() => {
    jest.clearAllMocks();
    cleanup();
  });

  it("renders product fields after fetch", async () => {
    await waitFor(() => {
      expect(screen.getByDisplayValue("Product A")).toBeInTheDocument();
      expect(screen.getByDisplayValue("Desc B")).toBeInTheDocument();
      expect(screen.getByDisplayValue("10")).toBeInTheDocument();
      expect(screen.getByDisplayValue("0")).toBeInTheDocument();
      expect(screen.getByDisplayValue("50")).toBeInTheDocument();
    });
  });

  it("calls fetchUpdate when clicking Update", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    const updateButtons = await screen.findAllByTestId("item_update");
    fireEvent.click(updateButtons[0]);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("/product/update/1"),
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            name: "Product A",
            description: "Desc A",
            amount: 10,
            service: "1",
            price: 100
          })
        })
      );
    });
  });

  it("calls fetchDelete when clicking Delete", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    const deleteButtons = await screen.findAllByTestId("item_delete");
    fireEvent.click(deleteButtons[1]);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("/product/delete/2"),
        expect.objectContaining({
          method: "POST"
        })
      );
    });
  });

  it("updates input value on change", async () => {
    const input = await screen.findByDisplayValue("Product B");
    fireEvent.change(input, { target: { value: "Product B Updated" } });
    expect(input.value).toBe("Product B Updated");
  });
});
