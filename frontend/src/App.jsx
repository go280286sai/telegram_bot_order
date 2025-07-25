import './App.css';
import BlockOne from "./components/BlockOne";
import BlockTwo from "./components/BlockTwo";
import Separation from "./components/Separation";
import Carousel from "./components/Carousel";
import Footer from "./components/Footer";
import {useState, useEffect} from "react";
import log from "./helps/logs.mjs";
import AboutUs from "./components/AboutUs";

<script src="https://kit.fontawesome.com/cf24694bb0.js" crossOrigin="anonymous"></script>

function App() {
    const [settings, setSettings] = useState({});

    useEffect(() => {
        const fetchSettings = async () => {
            try {
                const response = await fetch("http://localhost:8000/setting/gets", {
                    method: "GET",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json"
                    }
                });

                const data = await response.json();

                if (data?.data?.settings) {
                    const parsedSettings = Object.fromEntries(
                        data.data.settings.map(item => [item.name, item.value])
                    );
                    setSettings(parsedSettings);
                }

            } catch (error) {
                await log("error", "fetch_settings", error);
            }
        };

        fetchSettings();
    }, []);

    return (
        <>
            <BlockOne settings={settings}/>
            <Separation/>
            <Carousel/>
            <Separation/>
            <BlockTwo/>
            <Separation/>
            <AboutUs/>
            <Separation/>
            <Footer settings={settings}/>
        </>
    );
}

export default App;
