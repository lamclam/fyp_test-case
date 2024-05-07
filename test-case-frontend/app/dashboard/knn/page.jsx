"use client"

import React, { useState, useEffect } from 'react';
import Link from "next/link"
import styles from "@/app/ui/dashboard/knn/knn.module.css";
import Navbar from "@/app/ui/dashboard/navbar/navbar";
import { fetchData } from '@/app/lib/data';

const KNNPage = () => {
    const [knnData, setKnnData] = useState([]);

    useEffect(() => {
        fetchData('KNNClasses').then(data => {
            setKnnData(data);
        });
    }, []); // Empty dependency array means this effect runs only once after the initial render

    return (
        <>
            <Navbar title="KNN Classification" />
            <div className={styles.container}>
                <div className={styles.top}>
                    <Link href="/dashboard/knn/add">
                        <button className={styles.addBtn}>Add New</button>
                    </Link>
                </div>
                <table className={styles.table}>
                    <thead>
                        <tr>
                            <td>Question ID</td>
                            <td>KNN Class</td>
                            <td>Class Array</td>
                            <td>Suggestion</td>
                            <td>Action</td>
                        </tr>
                    </thead>
                    <tbody>
                        {knnData.map((item) => (
                            <tr key={`${item.QuestionID}${item.KNNClass}`}>
                                <td>
                                    <div className={styles.question}>
                                        {item.QuestionID}
                                    </div>
                                </td>
                                <td>{item.KNNClass}</td>
                                <td>{item.KNNClassData}</td>
                                <td>{item.KNNClassSuggestion}</td>
                                <td>
                                    <div className={styles.buttons}>
                                        {/* <Link href={`/dashboard/knn/${item.QuestionID}${item.KNNClass}`}>
                                            <button className={`${styles.button} ${styles.view}`}>
                                                View
                                            </button>
                                        </Link> */}
                                        <form action={`/delete/knn/${item.QuestionID}${item.KNNClass}`} method="POST">
                                            <input type="hidden" name="id" value={item.QuestionID} />
                                            <button type="submit" className={`${styles.button} ${styles.delete}`}>
                                                Delete
                                            </button>
                                        </form>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </>
    )
}

export default KNNPage