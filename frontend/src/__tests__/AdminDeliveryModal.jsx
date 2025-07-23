import React from "react";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import AdminDeliveryModal from "../components/admin/AdminDeliveryModal";

jest.mock("../helps/logs.mjs", () => jest.fn());
global.fetch = jest.fn();
delete window.location;
window.location = {reload: jest.fn()};

describe("AdminDeliveryModal", () => {
  const mockPosts = [{ id: 1, name: "Nova Poshta" }];
  const mockCities = [{ id: 2, name: "Kyiv" }];
  const mockAddresses = [{ id: 3, name: "Khreshchatyk 1" }];

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("loads select options and submits form successfully", async () => {
    fetch
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, data: { posts: mockPosts } })
      })
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, data: { cities: mockCities } })
      })
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, data: { addresses: mockAddresses } })
      })
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true })
      });

    render(<AdminDeliveryModal />);

    // wait for posts to load
    await waitFor(() => {
      expect(screen.getByText("Nova Poshta")).toBeInTheDocument();
    });

    fireEvent.change(screen.getByTestId("item_post"), { target: { value: "1", name: "post" } });

    await waitFor(() => {
      expect(screen.getByText("Kyiv")).toBeInTheDocument();
    });

    fireEvent.change(screen.getByTestId("item_city"), { target: { value: "2", name: "city" } });

    await waitFor(() => {
      expect(screen.getByText("Khreshchatyk 1")).toBeInTheDocument();
    });

    fireEvent.change(screen.getByTestId("item_address"), { target: { value: "3", name: "address" } });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "http://localhost:8000/delivery/create",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ post_id: "1", city_id: "2", address_id: "3" })
        })
      );
      expect(window.location.reload).toHaveBeenCalled();
    });
  });

  it("logs error on failed submission", async () => {
    const log = require("../helps/logs.mjs");
    fetch
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, data: { posts: mockPosts } })
      })
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, data: { cities: mockCities } })
      })
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, data: { addresses: mockAddresses } })
      })
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ success: false })
      });

    render(<AdminDeliveryModal />);

    await waitFor(() => {
      expect(screen.getByText("Nova Poshta")).toBeInTheDocument();
    });

    fireEvent.change(screen.getByTestId("item_post"), { target: { value: "1", name: "post" } });

    await waitFor(() => {
      expect(screen.getByText("Kyiv")).toBeInTheDocument();
    });

    fireEvent.change(screen.getByTestId("item_city"), { target: { value: "2", name: "city" } });

    await waitFor(() => {
      expect(screen.getByText("Khreshchatyk 1")).toBeInTheDocument();
    });

    fireEvent.change(screen.getByTestId("item_address"), { target: { value: "3", name: "address" } });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(log).toHaveBeenCalledWith("error", "add new item product error", expect.any(Object));
    });
  });
});
