import React from "react";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import AdminPost from "../components/admin/AdminPost";

jest.mock("../helps/logs.mjs", () => jest.fn());
global.fetch = jest.fn();

describe("AdminPost component", () => {
  const mockPosts = [
    { id: 1, name: "Nova Poshta" },
    { id: 2, name: "UkrPoshta" }
  ];

  beforeEach(() => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({
        success: true,
        data: { posts: mockPosts }
      })
    });

    render(<AdminPost />);
  });

  afterEach(() => {
    jest.clearAllMocks();
    cleanup();
  });

  it("renders posts after fetch", async () => {
    await waitFor(() => {
      expect(screen.getByDisplayValue("Nova Poshta")).toBeInTheDocument();
      expect(screen.getByDisplayValue("UkrPoshta")).toBeInTheDocument();
    });
  });

  it("calls fetchUpdate when clicking Update button", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    const updateButtons = await screen.findAllByTestId("item_update");
    fireEvent.click(updateButtons[0]);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("/post/update/1"),
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ name: "Nova Poshta" })
        })
      );
    });
  });

  it("calls fetchDelete when clicking Delete button", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    const deleteButtons = await screen.findAllByTestId("item_delete");
    fireEvent.click(deleteButtons[1]);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("/post/delete/2"),
        expect.objectContaining({
          method: "POST"
        })
      );
    });
  });

  it("updates input value", async () => {
    const input = await screen.findByDisplayValue("Nova Poshta");
    fireEvent.change(input, { target: { value: "Новая Почта" } });
    expect(input.value).toBe("Новая Почта");
  });
});
