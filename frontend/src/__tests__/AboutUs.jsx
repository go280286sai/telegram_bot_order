import React from "react";
import {render, screen, waitFor} from "@testing-library/react";
import AboutUs from "../components/AboutUs";

// Мокаем изображения
jest.mock("../assets/img/women.webp", () => "woman.webp");
jest.mock("../assets/img/man.webp", () => "man.webp");
// Мокаем логер
jest.mock("../helps/logs.mjs", () => ({
    default: jest.fn()
}));
// Мокаем fetch
global.fetch = jest.fn();
const mockReviews = [
    {gender: 0, name: "Alice", text: "Отличный сервис!"},
    {gender: 1, name: "Bob", text: "Все понравилось!"},
];

describe("Social component", () => {
    beforeEach(() => {
        fetch.mockResolvedValue({
                json: () => Promise.resolve({
                    data: {reviews: mockReviews}
                })
            }
        )
    })
    afterEach(() => {
        jest.clearAllMocks();
    });
    it("render for about us component", async () => {
        render(<AboutUs/>);
        let name = await screen.findByText("Alice")
        expect(name).toBeInTheDocument();
        let description = await screen.findByText("Отличный сервис!");
        expect(description).toBeInTheDocument();
        let alt = await screen.findByAltText("Alice's avatar")
        expect(alt).toHaveAttribute("src", "woman.webp");

        name = await screen.findByText("Bob");
        expect(name).toBeInTheDocument();
        description = await screen.findByText("Все понравилось!");
        expect(description).toBeInTheDocument();
        alt = await screen.findByAltText("Bob's avatar")
        expect(alt).toHaveAttribute("src", "man.webp");
    });
    it("renders fallback message when no reviews", async () => {
        fetch.mockResolvedValue({
            json: () => Promise.resolve({ data: { reviews: [] } }),
        });

        render(<AboutUs />);
        await waitFor(() => {
            expect(screen.getByText("There are no reviews yet")).toBeInTheDocument();
        });
    });
});
