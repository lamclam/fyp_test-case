"use client"

import React, { useState, useEffect } from 'react';
import Link from "next/link"
import styles from "@/app/ui/dashboard/questions/questions.module.css";
import Navbar from "@/app/ui/dashboard/navbar/navbar";
import { fetchData } from '@/app/lib/data';

const QuestionsPage = () => {
    const [questionData, setQuestionData] = useState([]);

    useEffect(() => {
        fetchData('Questions').then(data => {
            setQuestionData(data);
        });
    }, []); // Empty dependency array means this effect runs only once after the initial render

    return (
        <>
            <Navbar title="" />
            <div className={styles.container}>
                <div className={styles.top}>
                    <Link href="/dashboard/questions/add">
                        <button className={styles.addBtn}>Add New</button>
                    </Link>
                </div>
                <table className={styles.table}>
                    <thead>
                        <tr>
                            <td>Question ID</td>
                            <td>Question Name</td>
                            <td>Teacher ID</td>
                            <td>Action</td>
                        </tr>
                    </thead>
                    <tbody>
                        {questionData.map((item) => (
                            <tr key={item.QuestionID}>
                                <td>
                                    <div className={styles.question}>
                                        {item.QuestionID}
                                    </div>
                                </td>
                                <td>{item.QuestionName}</td>
                                <td>{item.TeacherID}</td>
                                <td>
                                    <div className={styles.buttons}>
                                        {/* <Link href={`/dashboard/questions/${item.QuestionID}`}>
                                            <button className={`${styles.button} ${styles.view}`}>
                                                View
                                            </button>
                                        </Link> */}
                                        <form action={`/delete/questions/${item.QuestionID}`} method="POST">
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

export default QuestionsPage