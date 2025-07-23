import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import AdminCityModal from "../components/admin/AdminCityModal";

jest.mock("../helps/logs.mjs", () => jest.fn());

global.fetch = jest.fn();
delete window.location;
window.location = {reload: jest.fn()};

describe("AdminCityModal", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("submits form and reloads page on success", async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ success: true })
    });

    render(<AdminCityModal />);

    fireEvent.change(screen.getByTestId("item_name"), {
      target: { value: "Dnipro" }
    });
    fireEvent.change(screen.getByTestId("item_post_id"), {
      target: { value: "45" }
    });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "http://localhost:8000/city/create",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            name: "Dnipro",
            post_id: "45"
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

    render(<AdminCityModal />);

    fireEvent.change(screen.getByTestId("item_name"), {
      target: { value: "Kharkiv" }
    });
    fireEvent.change(screen.getByTestId("item_post_id"), {
      target: { value: "99" }
    });

    fireEvent.click(screen.getByText("Send"));

    await waitFor(() => {
      expect(log).toHaveBeenCalledWith(
        "error",
        "add new item city error",
        expect.any(Object)
      );
    });
  });
});
