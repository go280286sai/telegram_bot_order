import './App.css';
import BlockOne from "./components/BlockOne";
import BlockTwo from "./components/BlockTwo";
import Separation from "./components/Separation";
import Carousel from "./components/Carousel";
import Footer from "./components/Footer";


function App() {
    return (
        <>
            <BlockOne/>
            <Separation/>
            <Carousel/>
            <Separation/>
            <BlockTwo/>
            <Separation/>
            <Footer/>
        </>

    )
}

export default App;
