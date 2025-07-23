import React from "react";
import {render, screen} from "@testing-library/react";
import Carousel from "../components/Carousel";

jest.mock("../helps/logs.mjs", () => ({
    default: jest.fn()
}));
jest.mock("../assets/img/carusel/1.webp", () => "one");
jest.mock("../assets/img/carusel/2.webp", () => "two");
jest.mock("../assets/img/carusel/3.webp", () => "three");
jest.mock("../assets/img/carusel/4.webp", () => "four");
jest.mock("../assets/img/carusel/5.webp", () => "five");
jest.mock("../assets/img/carusel/1.webp", () => "six");
jest.mock("../assets/img/carusel/2.webp", () => "seven");
jest.mock("../assets/img/carusel/3.webp", () => "eight");
jest.mock("../assets/img/carusel/4.webp", () => "nine");
jest.mock("../assets/img/carusel/5.webp", () => "ten");
global.fetch = jest.fn();
const mockCarousels = [
    {title: "Title1", description: "Description1", image: "Image1"},
    {title: "Title2", description: "Description2", image: "Image2"},
    {title: "Title3", description: "Description3", image: "Image3"},
    {title: "Title4", description: "Description4", image: "Image4"},
    {title: "Title5", description: "Description5", image: "Image5"},
    {title: "Title6", description: "Description6", image: "Image6"},
    {title: "Title7", description: "Description7", image: "Image7"},
    {title: "Title8", description: "Description8", image: "Image8"},
    {title: "Title9", description: "Description9", image: "Image9"},
    {title: "Title10", description: "Description10", image: "Image10"}
];

describe("Carousel component", () => {
    beforeEach(() => {
        fetch.mockResolvedValue({
            json: () => Promise.resolve({
                data: {
                    carousels: mockCarousels
                }
            })
        })
    });
    afterEach(() => {
            jest.clearAllMocks();
        });
    it("Fetch carousel", async () => {
        render(<Carousel/>)
        const images = await screen.findAllByRole("img");
        expect(images.length).toEqual(10);
        for (const data of mockCarousels) {
            let title = await screen.findByText(data.title);
        expect(title).toBeInTheDocument();
        let description = await screen.findByText(data.description);
        expect(description).toBeInTheDocument();
        let alt = await screen.findByAltText(`slide-${data.image}`);
        expect(alt).toBeInTheDocument();
        }

    })
});
