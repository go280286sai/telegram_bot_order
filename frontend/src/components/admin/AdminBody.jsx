import React, {useState, useEffect} from "react";
import {LineChart, Line, CartesianGrid, XAxis, YAxis, Legend, Tooltip} from 'recharts';
import {fetchAuth} from "./fetchAuth";
import log from "../../helps/logs.mjs";

export default function AdminBody() {
    const [contentUsers, setContentUsers] = useState([]);
    const [chartData, setChartData] = useState([]);
    const [contentOrders, setContentOrders] = useState([]);
    const [chartDataOrder, setChartDataOrder] = useState([]);
    const fetchUsers = async () => {
        try {
            await fetchAuth();
            const response = await fetch("http://localhost:8000/user/gets", {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            if (data.success) {
                setContentUsers(data.data.users);
                console.log(data.data.users)
            }
        } catch (error) {
            await log("error", "users", error);
        }
    };
    const fetchOrders = async () => {
        try {
            await fetchAuth();
            const response = await fetch("http://localhost:8000/order/gets", {
                method: "POST",
                credentials: "include",
                headers: {"Content-Type": "application/json"}
            });
            const data = await response.json();
            if (data.success) {
                setContentOrders(data.data.orders);
            }
        } catch (error) {
            await log("error", "users", error);
        }
    };
    useEffect(() => {
        fetchUsers();
        fetchOrders();
    }, []);

    useEffect(() => {
        const dateCounts = {};
        contentUsers.forEach(user => {
            const date = new Date(user.created_at).toISOString().split("T")[0]; // "YYYY-MM-DD"
            dateCounts[date] = (dateCounts[date] || 0) + 1;
        });
        const formattedData = Object.entries(dateCounts).map(([date, count]) => ({
            date,
            count
        }));
        formattedData.sort((a, b) => new Date(a.date) - new Date(b.date));
        setChartData(formattedData);
    }, [contentUsers]);
    useEffect(() => {
        const dateCounts = {};
        contentOrders.forEach(order => {
            const date = new Date(order.created_at).toISOString().split("T")[0];
            dateCounts[date] = (dateCounts[date] || 0) + 1;
        });
        const formattedData = Object.entries(dateCounts).map(([date, count]) => ({
            date,
            count
        }));
        formattedData.sort((a, b) => new Date(a.date) - new Date(b.date));
        setChartDataOrder(formattedData);
    }, [contentOrders]);
    return (
        <div className={"row block_1"}>
            <LineChart width={800} height={400} data={chartData}>
                <CartesianGrid stroke="#ccc"/>
                <XAxis dataKey="date"/>
                <YAxis allowDecimals={false}/>
                <Tooltip/>
                <Legend/>
                <Line type="monotone" dataKey="count" stroke="#8884d8" name="Users Registered"/>
            </LineChart>
            <h4>Total users: {contentUsers.length}</h4>
            <LineChart width={800} height={400} data={chartDataOrder}>
                <CartesianGrid stroke="#ccc"/>
                <XAxis dataKey="date"/>
                <YAxis allowDecimals={false}/>
                <Tooltip/>
                <Legend/>
                <Line type="monotone" dataKey="count" stroke="#8884d8" name="Orders operation"/>
            </LineChart>
            <h4>Total orders: {contentOrders.length}</h4>
        </div>
    )
}