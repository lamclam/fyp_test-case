"use client"
import React, { useState, useEffect } from 'react';
import styles from '@/app/ui/login/login.module.css';

const LoginPage = () => {
    const [userId, setUserId] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    // useEffect hook to clear localStorage when the component mounts
    useEffect(() => {
        localStorage.clear();
    }, []);

    const handleLogin = async (event) => {
        event.preventDefault();
        try {
            const response = await fetch('https://api.lamy.day/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    user_id: userId,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok) {
                console.log('Login Successful:', data);
                // Store each key-value pair in the local storage
                for (const key in data) {
                    localStorage.setItem(key, data[key]);
                }
                setErrorMessage('');
                window.location.href = '/dashboard'; // Redirect to dashboard
            } else if (data.Error) {
                console.error('Login Failed:', data.Error);
                setErrorMessage(data.Error);
            } else {
                console.error('Login Failed:', data);
                setErrorMessage('An unexpected error occurred.');
            }
        } catch (error) {
            console.error('Network error:', error);
            setErrorMessage('Failed to connect to the server.');
        }
    };

    return (
        <div className={styles.container}>
            <form className={styles.form} onSubmit={handleLogin}>
                <input
                    type="text"
                    placeholder="Student ID or teacher ID"
                    value={userId}
                    onChange={(e) => setUserId(e.target.value)}
                />
                <input
                    type='password'
                    placeholder='Password'
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Login</button>
                {errorMessage && <div className={styles.error}>{errorMessage}</div>}
            </form>
        </div>
    );
}

export default LoginPage;