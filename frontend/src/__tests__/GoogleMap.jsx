import React from "react";
import { render, screen } from "@testing-library/react";
import GoogleMaps from "../components/GoogleMaps";

const mockSettings = {
    map: "https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d18786.52658104362!2d14.429132556912391!3d50.052595026866626!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f1"
}

describe("GoogleMap component",  () => {
    it('Get map', () => {
        render(<GoogleMaps settings={mockSettings}/>)
        const iframe = screen.getByTitle("google-maps")
        expect(iframe).toHaveAttribute("src", mockSettings.map);
    });
});
