import React from "react";
import { render, screen } from "@testing-library/react";
import Social from "../components/Social";
import telegram from "../assets/img/telegram.png";
import viber from "../assets/img/viber.png";
import whatsapp from "../assets/img/whatsap.png";

const mockSettings = {
    telegram: "https://t.me/example",
    viber: "viber://chat?number=%2B1234567890",
    whatsapp: "https://wa.me/1234567890",
};

describe("Social component", () => {
    it("renders 3 social links with correct hrefs and images", () => {
        render(<Social settings={mockSettings} />);

        const links = screen.getAllByRole("link");
        expect(links).toHaveLength(3);

        expect(links[0]).toHaveAttribute("href", mockSettings.telegram);
        expect(links[1]).toHaveAttribute("href", mockSettings.viber);
        expect(links[2]).toHaveAttribute("href", mockSettings.whatsapp);

        expect(screen.getByAltText("Telegram")).toHaveAttribute("src", telegram);
        expect(screen.getByAltText("Viber")).toHaveAttribute("src", viber);
        expect(screen.getByAltText("WhatsApp")).toHaveAttribute("src", whatsapp);
    });
});
