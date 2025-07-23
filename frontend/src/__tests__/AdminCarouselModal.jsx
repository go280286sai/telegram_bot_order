import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import AdminCarouselsModal from "../components/admin/AdminCarouselsModal";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();
delete window.location;
window.location = {reload: jest.fn()};

describe("AdminCarouselsModal", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("submits form and reloads page on success", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    render(<AdminCarouselsModal />);

    fireEvent.change(screen.getByLabelText(/Title/i), {
      target: { value: "Carousel Title" }
    });
    fireEvent.change(screen.getByLabelText(/Description/i), {
      target: { value: "Carousel Description" }
    });
    fireEvent.change(screen.getByLabelText(/Image/i), {
      target: { value: "carousel.jpg" }
    });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "http://localhost:8000/front/carousel/create",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            title: "Carousel Title",
            description: "Carousel Description",
            image: "carousel.jpg"
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

    render(<AdminCarouselsModal />);

    fireEvent.change(screen.getByLabelText(/Title/i), {
      target: { value: "Broken Title" }
    });
    fireEvent.change(screen.getByLabelText(/Description/i), {
      target: { value: "Broken Description" }
    });
    fireEvent.change(screen.getByLabelText(/Image/i), {
      target: { value: "error.png" }
    });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(log).toHaveBeenCalledWith(
        "error",
        "add new item carousel error",
        expect.any(Object)
      );
    });
  });
});
