"use client"

import React, { useState } from 'react';
import styles from '@/app/ui/dashboard/questions/addQuestion/addQuestion.module.css';
import Navbar from '@/app/ui/dashboard/navbar/navbar';

const AddUserPage = () => {
    const [userName, setUserName] = useState('');
    const [userId, setUserId] = useState('');
    const [password, setPassword] = useState('');
    const [isStudent, setIsStudent] = useState(false);

    const handleAccTypeChange = (event) => {
        setIsStudent(event.target.value === 'true');
    };

    const clearForm = () => {
        setUserName('');
        setUserId('');
        setPassword('');
        setIsStudent(false);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        const user_type = isStudent ? "student" : "teacher";
        const formData = {
            user_name: userName,
            user_id: userId,
            password: password,
            user_type: user_type
        };

        try {
            const response = await fetch('https://api.lamy.day/adduser', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();
            if (response.ok) {
                alert('User added successfully!');
                clearForm();
            } else {
                alert(`Error: ${result.error}`);
            }
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    };

    return (
        <>
            <Navbar title="Add User" />
            <div className={styles.container}>
                <form className={styles.form} onSubmit={handleSubmit}>
                    <input type="text" placeholder="User Name" name="user_name" required value={userName} onChange={e => setUserName(e.target.value)} />
                    <div className={styles.radioSelect}>
                        <p>Account Type</p>
                        <div className={styles.radioSelectChoice}>
                            <div className={styles.opt}>
                                <input
                                    type="radio"
                                    id="student"
                                    name="accountType"
                                    value="false"
                                    onChange={handleAccTypeChange}
                                    checked={!isStudent}
                                />
                                <label htmlFor="student">Student</label>
                            </div>
                            <div className={styles.opt}>
                                <input
                                    type="radio"
                                    id="teacher"
                                    name="accountType"
                                    value="true"
                                    onChange={handleAccTypeChange}
                                    checked={isStudent}
                                />
                                <label htmlFor="teacher">Teacher</label>
                            </div>
                        </div>
                    </div>
                    <input type="text" placeholder="User ID" name="user_id" required value={userId} onChange={e => setUserId(e.target.value)} />
                    <input type="password" placeholder="Password" name="password" required value={password} onChange={e => setPassword(e.target.value)} />
                    <div className={styles.buttonGroup}>
                        <button type="button" onClick={clearForm} className={styles.clrbtn}>Clear</button>
                        <button type="submit">Submit</button>
                    </div>
                </form>
            </div>
        </>
    );
}

export default AddUserPage;