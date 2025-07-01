import React from 'react';
import ReactDOM from 'react-dom/client';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';

import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import AdminMain from "./components/admin/AdminMain";
import BlockOne from "./components/BlockOne";
import Footer from "./components/Footer";
import Order from "./components/order/Order";
import Separation from "./components/Separation";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <BrowserRouter>
        <React.StrictMode>
            <Routes>
                <Route path="/" element={<App/>}/>
                <Route path={"/order"} element={
                    <>
                        <BlockOne/>
                        <Separation/>
                        <Order/>
                        <Separation/>
                        <Footer/>
                    </>
                }/>
                <Route path={"/admin"} element={<AdminMain/>}/>
            </Routes>
        </React.StrictMode>
    </BrowserRouter>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
