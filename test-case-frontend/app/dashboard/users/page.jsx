"use client"

import React, { useState, useEffect } from 'react';
import Link from "next/link"
import styles from "@/app/ui/dashboard/questions/questions.module.css";
import Navbar from "@/app/ui/dashboard/navbar/navbar";
import { fetchData } from '@/app/lib/data';

const UsersPage = () => {
    const [userData, setUserData] = useState([]);

    useEffect(() => {
        // Use Promise.all to handle both fetches simultaneously
        Promise.all([
            fetchData('Teachers'),
            fetchData('Students')
        ]).then(([teachersData, studentsData]) => {
            const transformedTeachers = teachersData.map(teacher => ({
                userID: teacher.TeacherID,
                name: teacher.Name,
                password: teacher.Password,
                type: "teacher"
            }));

            const transformedStudents = studentsData.map(student => ({
                userID: student.StudentID,
                name: student.Name,
                password: student.Password,
                type: "student"
            }));

            // Combine both arrays only after both have been fetched and transformed
            setUserData([...transformedStudents, ...transformedTeachers]);
        }).catch(error => {
            console.error("Failed to fetch data:", error);
            // Handle errors or set some error state to show in the UI
        });
    }, []);

    return (
        <>
            <Navbar title="" />
            <div className={styles.container}>
                <div className={styles.top}>
                    <Link href="/dashboard/users/add">
                        <button className={styles.addBtn}>Add New</button>
                    </Link>
                </div>
                <table className={styles.table}>
                    <thead>
                        <tr>
                            <td>User ID</td>
                            <td>User Name</td>
                            <td>Type</td>
                            <td>Action</td>
                        </tr>
                    </thead>
                    <tbody>
                        {userData.map((item) => (
                            <tr key={item.userID}>
                                <td>
                                    <div className={styles.question}>
                                        {item.userID}
                                    </div>
                                </td>
                                <td>{item.name}</td>
                                <td>{item.type}</td>
                                <td>
                                    <div className={styles.buttons}>
                                        {/* <Link href={`/dashboard/users/${item.userID}`}>
                                            <button className={`${styles.button} ${styles.view}`}>
                                                View
                                            </button>
                                        </Link> */}
                                        <form action={`/delete/users/${item.userID}`} method="POST">
                                            <input type="hidden" name="id" value={item.userID} />
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

export default UsersPage