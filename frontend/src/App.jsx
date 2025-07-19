import './App.css';
import BlockOne from "./components/BlockOne";
import BlockTwo from "./components/BlockTwo";
import Separation from "./components/Separation";
import Carousel from "./components/Carousel";
import Footer from "./components/Footer";
import {useState, useEffect} from "react";
import log from "./helps/logs.mjs";
import AboutUs from "./components/AboutUs";

function App() {
    const [settings, setSettings] = useState({})
    let title = "";
    let description = "";
    let telegram = "";
    let viber = "";
    let whatsapp = "";
    let phone = "";
    let email = "";
    let address = "";
    let map = "";
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
                if (data.data) {
                    for (let item of data.data.settings) {
                        if (item.name === "title") {
                            title = item.value;
                        }
                        if (item.name === "description") {
                            description = item.value;
                        }
                        if (item.name === "telegram") {
                            telegram = item.value;
                        }
                        if (item.name === "viber") {
                            viber = item.value;
                        }
                        if (item.name === "whatsapp") {
                            whatsapp = item.value;
                        }
                        if (item.name === "phone") {
                            phone = item.value;
                        }
                        if (item.name === "email") {
                            email = item.value;
                        }
                        if (item.name === "address") {
                            address = item.value;
                        }
                        if (item.name === "map") {
                            map = item.value;
                        }
                    }
                }
                setSettings({
                    "title": title,
                    "description": description,
                    "telegram": telegram,
                    "viber": viber,
                    "whatsapp": whatsapp,
                    "phone": phone,
                    "email": email,
                    "address": address,
                    "map": map
                })
            } catch (error) {
                await log("error", "is_auth", error);
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

    )
}

export default App;
