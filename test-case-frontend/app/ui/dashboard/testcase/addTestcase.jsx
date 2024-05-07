"use client"

import React, { useState } from 'react';
import styles from "./addTestcase.module.css";

const AddTestcase = () => {
    const [questionId, setQuestionId] = useState('');
    const [testCaseValue, setTestCaseValue] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new URLSearchParams();
        formData.append('question_id', questionId);
        formData.append('testcase_value', testCaseValue);

        try {
            const response = await fetch('https://api.lamy.day/addtestcase', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                alert('Test case added successfully');
                // Optionally reset fields or handle state update
                setQuestionId('');
                setTestCaseValue('');
            } else {
                alert(`Failed to add test case: ${data.error}`);
            }
        } catch (error) {
            alert('Failed to send data to the server');
        }
    };

    return (
        <div className={styles.container}>
            <form className={styles.form} onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Question ID"
                    name="question_id"
                    required
                    value={questionId}
                    onChange={(e) => setQuestionId(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Test Case Value"
                    name="testcase_value"
                    required
                    value={testCaseValue}
                    onChange={(e) => setTestCaseValue(e.target.value)}
                />
                <div className={styles.buttonGroup}>
                    <button type="submit">Add</button>
                </div>
            </form>
        </div>
    );
};

export default AddTestcase;