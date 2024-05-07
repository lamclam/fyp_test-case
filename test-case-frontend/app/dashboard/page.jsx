"use client"

import { useEffect } from 'react';
import Card from "../ui/dashboard/card/card";
import styles from "../ui/dashboard/dashboard.module.css";
import Navbar from "../ui/dashboard/navbar/navbar";

const Dashboard = () => {
    const name = ""; // You can define or retrieve this value as needed

    useEffect(() => {
        const itemName = localStorage.getItem('userID'); // Replace 'itemName' with your specific key
        if (!itemName) {
            // If the item does not exist in localStorage, redirect
            window.location.href = '/login'; // Change '/login' to your specific URL
        }
    }, []); // Empty dependency array means this effect runs once after the initial render

    return (
        <>
            <Navbar title="Dashboard" />
            <div className={styles.wrapper}>
                <div className={styles.main}>
                    <Card item={name} />
                </div>
            </div>
        </>
    );
};

export default Dashboard;