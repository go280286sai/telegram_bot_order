import React from 'react';
import ReactDOM from 'react-dom/client';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';

import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import AdminBody from "./components/admin/AdminBody";
import Order from "./components/order/Order";
import Separation from "./components/Separation";
import AdminSettings from "./components/admin/AdminSettings";
import AdminHeader from "./components/admin/AdminHeader";
import AdminCarousels from "./components/admin/AdminCarousels";
import AdminReviews from "./components/admin/AdminReviews";
import AdminProducts from "./components/admin/AdminProducts";
import AdminDelivery from "./components/admin/AdminDelivery";
import AdminUsers from "./components/admin/AdminUsers";
import AdminOrders from "./components/admin/AdminOrders";
import AdminMail from "./components/admin/AdminMail";
import AdminPredict from "./components/admin/AdminPredict";

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
    <BrowserRouter>
        <React.StrictMode>
            <Routes>
                <Route path="/" element={<App/>}/>
                <Route path={"/order"} element={
                    <>
                        <Order/>
                        <Separation/>
                    </>
                }/>
                <Route path={"/admin"} element={
                    <>
                        <AdminHeader/>
                        <Separation/>
                        <AdminBody/>
                    </>
                }/>
                <Route path={"/admin/settings"} element={
                    <>
                        <AdminHeader/>
                        <Separation/>
                        <AdminSettings/>
                    </>
                }/>
                <Route path={"/admin/carousels"} element={
                    <>
                        <AdminHeader/>
                        <Separation/>
                        <AdminCarousels/>
                    </>
                }/>
                <Route path={"/admin/reviews"} element={
                    <>
                        <AdminHeader/>
                        <Separation/>
                        <AdminReviews/>
                    </>
                }/>
                <Route path={"/admin/products"} element={
                    <>
                        <AdminHeader/>
                        <Separation/>
                        <AdminProducts/>
                    </>
                }/>
                <Route path={"/admin/delivery"} element={
                    <>
                        <AdminHeader/>
                        <Separation/>
                        <AdminDelivery/>
                    </>
                }/>
                <Route path={"/admin/users"} element={
                    <>
                        <AdminHeader/>
                        <Separation/>
                        <AdminUsers/>
                    </>
                }/>
                <Route path={"/admin/orders"} element={
                    <>
                        <AdminHeader/>
                        <Separation/>
                        <AdminOrders/>
                    </>
                }/>
                <Route path={"/admin/mailing"} element={
                    <>
                        <AdminHeader/>
                        <Separation/>
                        <AdminMail/>
                    </>
                }/>
                <Route path={"/admin/predict"} element={
                    <>
                        <AdminHeader/>
                        <Separation/>
                        <AdminPredict/>
                    </>
                }/>
            </Routes>
        </React.StrictMode>
    </BrowserRouter>
);


reportWebVitals();
