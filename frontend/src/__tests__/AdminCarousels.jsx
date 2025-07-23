import React from "react";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import AdminCarousels from "../components/admin/AdminCarousels";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();

describe("AdminCarousels component", () => {
  const mockCarousels = [
    {
      id: 1,
      title: "Spring Sale",
      description: "Get up to 50% off!",
      image: "spring.png"
    },
    {
      id: 2,
      title: "New Collection",
      description: "Autumn 2025 styles",
      image: "autumn.png"
    }
  ];

  beforeEach(() => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true, data: { carousels: mockCarousels } })
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
    cleanup();
  });

  it("renders carousel items after fetch", async () => {
          render(<AdminCarousels />);
    await waitFor(() => {
      expect(screen.getByDisplayValue("Spring Sale")).toBeInTheDocument();
      expect(screen.getByDisplayValue("Get up to 50% off!")).toBeInTheDocument();
      expect(screen.getByDisplayValue("spring.png")).toBeInTheDocument();
    });

    expect(screen.getByDisplayValue("New Collection")).toBeInTheDocument();
    expect(screen.getByDisplayValue("Autumn 2025 styles")).toBeInTheDocument();
    expect(screen.getByDisplayValue("autumn.png")).toBeInTheDocument();
  });

  it("updates carousel item when Update is clicked", async () => {
    fetch
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, data: { carousels: mockCarousels } })
      }) // initial fetchCarousels
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true })
      }) // fetchUpdate
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, data: { carousels: mockCarousels } })
      }); // refetch after update
    render(<AdminCarousels />);

    const item_updates = await screen.findAllByTestId("item_update");
    await waitFor(() => {
      expect(item_updates[0]).toBeInTheDocument();
    });

    fireEvent.click(item_updates[0]);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("/carousel/update/1"),
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            title: "Spring Sale",
            description: "Get up to 50% off!",
            image: "spring.png"
          })
        })
      );
    });
  });

  it("deletes carousel item when Delete is clicked", async () => {
    fetch
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, data: { carousels: mockCarousels } })
      }) // initial fetchCarousels
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true })
      }) // fetchDelete
      .mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, data: { carousels: mockCarousels } })
      }); // refetch after delete
    render(<AdminCarousels />);
        const item_delete = await screen.findAllByTestId("item_delete");
    await waitFor(() => {
      expect(item_delete[0]).toBeInTheDocument();
    });

    fireEvent.click(item_delete[0]);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("/carousel/delete/1"),
        expect.objectContaining({ method: "POST" })
      );
    });
  });
});
