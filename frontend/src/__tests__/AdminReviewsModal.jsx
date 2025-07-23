import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import AdminReviewsModal from "../components/admin/AdminReviewsModal";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();
delete window.location;
window.location = {reload: jest.fn()};

describe("AdminReviewsModal", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("submits review and reloads on success", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    render(<AdminReviewsModal />);

    fireEvent.change(screen.getByLabelText("Name"), { target: { value: "Alice" } });
    fireEvent.change(screen.getByLabelText("Text"), { target: { value: "Amazing service!" } });
    fireEvent.change(screen.getByLabelText("Gender"), { target: { value: "1" } });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "http://localhost:8000/review/create",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            name: "Alice",
            text: "Amazing service!",
            gender: "1"
          })
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

    render(<AdminReviewsModal />);

    fireEvent.change(screen.getByLabelText("Name"), { target: { value: "Bob" } });
    fireEvent.change(screen.getByLabelText("Text"), { target: { value: "Not great." } });
    fireEvent.change(screen.getByLabelText("Gender"), { target: { value: "0" } });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(log).toHaveBeenCalledWith(
        "error",
        "add new item review error",
        expect.any(Object)
      );
    });
  });
});
