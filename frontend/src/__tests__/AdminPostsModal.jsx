import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import AdminPostsModal from "../components/admin/AdminPostsModal";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();
delete window.location;
window.location = {reload: jest.fn()};

describe("AdminPostsModal", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("submits form and reloads on success", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    render(<AdminPostsModal />);

    fireEvent.change(screen.getByLabelText("Name"), {
      target: { value: "Nova Poshta" }
    });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "http://localhost:8000/post/create",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ name: "Nova Poshta" })
        })
      );
      expect(window.location.reload).toHaveBeenCalled();
    });
  });

  it("logs error on failed submission", async () => {
    const log = require("../helps/logs.mjs");
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: false })
    });

    render(<AdminPostsModal />);

    fireEvent.change(screen.getByLabelText("Name"), {
      target: { value: "UkrPoshta" }
    });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(log).toHaveBeenCalledWith(
        "error",
        "add new item post error",
        expect.any(Object)
      );
    });
  });
});
