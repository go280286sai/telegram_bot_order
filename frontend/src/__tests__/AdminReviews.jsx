import React from "react";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import AdminReviews from "../components/admin/AdminReviews";

jest.mock("../helps/logs.mjs", () => jest.fn());
global.fetch = jest.fn();

jest.mock("../components/admin/AdminReviewsModal", () => () => <div data-testid="modal-reviews" />);

describe("AdminReviews component", () => {
  const mockReviews = [
    { id: 1, name: "Alice", text: "Great!", gender: 1 },
    { id: 2, name: "Bob", text: "Not bad", gender: 0 }
  ];

  beforeEach(() => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true, data: { reviews: mockReviews } })
    });
    render(<AdminReviews />);
  });

  afterEach(() => {
    jest.clearAllMocks();
    cleanup();
  });

  it("renders reviews from API", async () => {
    await waitFor(() => {
      expect(screen.getByDisplayValue("Alice")).toBeInTheDocument();
      expect(screen.getByDisplayValue("Great!")).toBeInTheDocument();
      expect(screen.getByDisplayValue("1")).toBeInTheDocument();
      expect(screen.getByDisplayValue("Bob")).toBeInTheDocument();
    });
  });

  it("updates input value and sends update", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    const nameInput = await screen.findByDisplayValue("Alice");
    fireEvent.change(nameInput, { target: { value: "Alicia" } });
    expect(nameInput.value).toBe("Alicia");

    const updateButtons = await screen.findAllByTestId("item_update");
    fireEvent.click(updateButtons[0]);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("/review/update/1"),
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            name: "Alicia",
            text: "Great!",
            gender: "1"
          })
        })
      );
    });
  });

  it("deletes review on button click", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    const deleteButtons = await screen.findAllByTestId("item_delete");
    fireEvent.click(deleteButtons[0]);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("/review/delete/1"),
        expect.objectContaining({ method: "POST" })
      );
    });
  });

  it("renders modal component", () => {
    expect(screen.getByTestId("modal-reviews")).toBeInTheDocument();
  });
});
