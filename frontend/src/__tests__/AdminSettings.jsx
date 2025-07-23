import React from "react";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import AdminSettings from "../components/admin/AdminSettings";

jest.mock("../helps/logs.mjs", () => jest.fn());
global.fetch = jest.fn();

jest.mock("../components/admin/AdminAddSettingModal", () => () => <div data-testid="modal-setting" />);

describe("AdminSettings component", () => {
  const mockSettings = [
    { id: 1, name: "SiteTitle", value: "MyShop" },
    { id: 2, name: "MaxOrders", value: "100" }
  ];

  beforeEach(() => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true, data: { settings: mockSettings } })
    });
    render(<AdminSettings />);
  });

  afterEach(() => {
    jest.clearAllMocks();
    cleanup();
  });

  it("renders settings from API", async () => {
    await waitFor(() => {
      expect(screen.getByDisplayValue("SiteTitle")).toBeInTheDocument();
      expect(screen.getByDisplayValue("MyShop")).toBeInTheDocument();
      expect(screen.getByDisplayValue("MaxOrders")).toBeInTheDocument();
      expect(screen.getByDisplayValue("100")).toBeInTheDocument();
    });
  });

  it("updates setting on button click", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    const nameInput = await screen.findByDisplayValue("SiteTitle");
    fireEvent.change(nameInput, { target: { value: "NewTitle" } });

    const updateButton = screen.getAllByTestId("item_update")[0];
    fireEvent.click(updateButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("/setting/update/1"),
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ name: "NewTitle", value: "MyShop" })
        })
      );
    });
  });

  it("deletes setting on button click", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    const deleteButton = await screen.findAllByTestId("item_delete");
    fireEvent.click(deleteButton[0]);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("/setting/delete/1"),
        expect.objectContaining({ method: "POST" })
      );
    });
  });

  it("renders modal component", () => {
    expect(screen.getByTestId("modal-setting")).toBeInTheDocument();
  });
});
