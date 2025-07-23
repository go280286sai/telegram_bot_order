import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import AdminPredict from "../components/admin/AdminPredict";

jest.mock("../helps/logs.mjs", () => jest.fn());
global.fetch = jest.fn();

describe("AdminPredict", () => {
  const mockData = {
    success: true,
    data: {
      predict: [
        {
          id: 1,
          ds: "2025-07-24",
          yhat: 150,
          yhat_lower: 120,
          yhat_upper: 180
        },
        {
          id: 2,
          ds: "2025-07-25",
          yhat: 160,
          yhat_lower: 130,
          yhat_upper: 190
        }
      ]
    }
  };

  beforeEach(() => {
    jest.clearAllMocks();
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve(mockData)
    });
  });

  it("submits form and displays predictions", async () => {
    render(<AdminPredict />);

    fireEvent.change(screen.getByLabelText(/Term/i), {
      target: { value: "123" }
    });

    fireEvent.click(screen.getByText("Ok"));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "http://localhost:8000/order/get_predict/123",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ id: "123" })
        })
      );

      expect(screen.getByText("2025-07-24")).toBeInTheDocument();
      expect(screen.getByText("150")).toBeInTheDocument();
      expect(screen.getByText("120")).toBeInTheDocument();
      expect(screen.getByText("180")).toBeInTheDocument();
    });
  });

  it("logs error if request fails", async () => {
    fetch.mockRejectedValueOnce(new Error("Network error"));

    render(<AdminPredict />);
    fireEvent.change(screen.getByLabelText(/Term/i), {
      target: { value: "456" }
    });

    fireEvent.click(screen.getByText("Ok"));

  });
});
