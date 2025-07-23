import React from "react";
import { render, screen, waitFor, cleanup } from "@testing-library/react";
import AdminDelivery from "../components/admin/AdminDelivery";

jest.mock("../helps/logs.mjs", () => jest.fn());

// Заглушки вложенных компонентов
jest.mock("../components/admin/AdminPost", () => () => <div data-testid="admin-post" />);
jest.mock("../components/admin/AdminCity", () => () => <div data-testid="admin-city" />);
jest.mock("../components/admin/AdminAddress", () => () => <div data-testid="admin-address" />);

global.fetch = jest.fn();

describe("AdminDelivery component", () => {
  const mockDeliveries = [
    { post_name: "Nova Poshta", city_name: "Kyiv", address_name: "Khreshchatyk 1" },
    { post_name: "UkrPoshta", city_name: "Lviv", address_name: "Shevchenka 5" }
  ];

  beforeEach(() => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({
        success: true,
        data: { deliveries: mockDeliveries }
      })
    });
    render(<AdminDelivery />);
  });

  afterEach(() => {
    jest.clearAllMocks();
    cleanup();
  });

  it("fetches delivery data and displays it", async () => {
    await waitFor(() => {
      expect(screen.getByText("Nova Poshta")).toBeInTheDocument();
      expect(screen.getByText("Kyiv")).toBeInTheDocument();
      expect(screen.getByText("Khreshchatyk 1")).toBeInTheDocument();

      expect(screen.getByText("UkrPoshta")).toBeInTheDocument();
      expect(screen.getByText("Lviv")).toBeInTheDocument();
      expect(screen.getByText("Shevchenka 5")).toBeInTheDocument();
    });
  });

  it("renders nested components", () => {
    expect(screen.getByTestId("admin-post")).toBeInTheDocument();
    expect(screen.getByTestId("admin-city")).toBeInTheDocument();
    expect(screen.getByTestId("admin-address")).toBeInTheDocument();
  });
});
