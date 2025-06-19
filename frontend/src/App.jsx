import './App.css';
import BlockOne from "./components/BlockOne";
import BlockTwo from "./components/BlockTwo";
import Separation from "./components/Separation";
import Reklama from "./components/Reklama";
import Footer from "./components/Footer";
import Trash from "./components/Trash";

function App() {
    return (
        <div className="container App">
            <BlockOne/>
            <Separation/>
            <Reklama/>
            <Separation/>
            <BlockTwo/>
            <Separation/>
            <Footer/>
        </div>
    );
}

export default App;
