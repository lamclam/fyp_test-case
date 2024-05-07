"use client"

import React, { useState, useEffect } from 'react';
import Link from "next/link"
import styles from "@/app/ui/dashboard/testcase/testcase.module.css";
import AddTestcase from "@/app/ui/dashboard/testcase/addTestcase";
import Navbar from "@/app/ui/dashboard/navbar/navbar";
import { fetchData } from '@/app/lib/data';

const TestCasePage = () => {
    const [testcaseData, setTestcaseData] = useState([]);

    useEffect(() => {
        fetchData('TestCases').then(data => {
            setTestcaseData(data);
        });
    }, []); // Empty dependency array means this effect runs only once after the initial render
    return (
        <>
            <Navbar title="" />
            <div className={styles.container}>
                <div className={styles.top}>
                    <AddTestcase />
                </div>
                <table className={styles.table}>
                    <thead>
                        <tr>
                            <td>Question ID</td>
                            <td>Test Case Value</td>
                            <td>Action</td>
                        </tr>
                    </thead>
                    <tbody>
                        {testcaseData.map((item) => (
                            <tr key={`${item.TestCasesID}`}>
                                <td>
                                    <div className={styles.question}>
                                        {item.QuestionID}
                                    </div>
                                </td>
                                <td>{item.TestCaseValue}</td>
                                <td>
                                    <div className={styles.buttons}>
                                        {/* <Link href={`/dashboard/testcase/${item.TestCaseID}`}>
                                            <button className={`${styles.button} ${styles.view}`}>
                                                View
                                            </button>
                                        </Link> */}
                                        <form action={`/delete/testcase/${item.TestCaseID}`} method="POST">
                                            <input type="hidden" name="id" value={item.TestCaseID} />
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

export default TestCasePage