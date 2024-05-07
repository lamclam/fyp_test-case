"use client"

import React, { useState, useEffect } from 'react';
import Link from "next/link"
import styles from "@/app/ui/dashboard/questions/questions.module.css";
import Navbar from "@/app/ui/dashboard/navbar/navbar";
import { fetchData } from '@/app/lib/data';

const ClustersPage = () => {
    const [questionId, setQuestionId] = useState('');
    const [threshold, setThreshold] = useState(2);
    const [clusters, setClusters] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Function to fetch data
        async function fetchData() {
            if (!questionId) return; // Don't fetch if questionId is not set

            setIsLoading(true);
            setError(null);

            try {
                const res = await fetch(`https://api.lamy.day/cluster?question_id=${questionId}&threshold=${threshold}`);
                if (!res.ok) throw new Error('Failed to fetch data from the server');

                const data = await res.json();
                setClusters(data);
            } catch (err) {
                setError(err.message);
                setClusters([]);
            } finally {
                setIsLoading(false);
            }
        }

        fetchData();
    }, [questionId, threshold]); // Only re-run the effect if these values change

    return (
        <>
            <Navbar title="" />
            <div className={styles.container}>
                <div>
                    <h1>Student Clusters</h1>
                    <div className={styles.form}>
                        <label>Question ID:
                            <input
                                type="text"
                                value={questionId}
                                onChange={(e) => setQuestionId(e.target.value)}
                            />
                        </label>
                        <label>Threshold:
                            <input
                                type="number"
                                value={threshold}
                                onChange={(e) => setThreshold(parseInt(e.target.value, 10) || 0)}
                            />
                        </label>
                    </div>
                    {isLoading ? (
                        <p>Loading...</p>
                    ) : error ? (
                        <p>Error: {error}</p>
                    ) : (
                        clusters.map((cluster, index) => (
                            <div key={index}>
                                <h2>Cluster {index + 1}</h2>
                                <ul>
                                    {cluster.map((student) => (
                                        <li key={student.StudentID}>
                                            {student.StudentID} - Mark: {student.Mark}
                                            <br />
                                            TestCase Results: {student.TestCaseResult}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </>
    )
}

export default ClustersPage