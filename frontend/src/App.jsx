import './App.css';
import BlockOne from "./components/BlockOne";
import BlockTwo from "./components/BlockTwo";
import Separation from "./components/Separation";
import Carousel from "./components/Carousel";
import Footer from "./components/Footer";
import {useState, useEffect} from "react";
import log from "./helps/logs.mjs";

function App() {
    const [settings, setSettings] = useState({})
    let title = "";
    let description = "";
    let telegram = "";
    let viber = "";
    let whatsapp = "";
    useEffect(() => {
        const fetchUser = async () => {
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
                    }
                }
                setSettings({
                    "title": title,
                    "description": description,
                    "telegram": telegram,
                    "viber": viber,
                    "whatsapp": whatsapp
                })
            } catch (error) {
                await log("error", "is_auth", error);
            }
        };
        fetchUser();
    }, []);
    return (
        <>
            <BlockOne settings={settings}/>
            <Separation/>
            <Carousel/>
            <Separation/>
            <BlockTwo/>
            <Separation/>
            <Footer settings={settings}/>
        </>

    )
}

export default App;
