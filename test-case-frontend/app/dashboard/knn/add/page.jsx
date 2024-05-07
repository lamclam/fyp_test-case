"use client"

import React, { useState } from 'react';
import axios from 'axios';
import styles from '@/app/ui/dashboard/questions/addQuestion/addQuestion.module.css';
import Navbar from '@/app/ui/dashboard/navbar/navbar';

const ROOT = 'https://api.lamy.day';

const AddKNNPage = () => {
    const [questionId, setQuestionId] = useState('');
    const [knnClass, setKnnClass] = useState('');
    const [suggestion, setSuggestion] = useState('');
    const [knnArray, setKnnArray] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post(`${ROOT}/addknn`, {
                question_id: questionId,
                knn_class: knnClass,
                suggestion: suggestion,
                knn_array: knnArray,
            });
            console.log(response.data);
            alert('KNN data added successfully');
        } catch (error) {
            console.error('Failed to add KNN data:', error);
            alert('Failed to add KNN data');
        }
    };

    const clearForm = () => {
        setQuestionId('');
        setKnnClass('');
        setSuggestion('');
        setKnnArray('');
    };

    return (
        <>
            <Navbar title="Add New KNN Class" />
            <div className={styles.container}>
                <form className={styles.form} onSubmit={handleSubmit}>
                    <input type="text" placeholder="Question ID" name="question_id" required value={questionId} onChange={e => setQuestionId(e.target.value)} />
                    <input type="text" placeholder="KNN Class" name="knn_class" required value={knnClass} onChange={e => setKnnClass(e.target.value)} />
                    <input type="text" placeholder="KNN Array" name="knn_array" required value={knnArray} onChange={e => setKnnArray(e.target.value)} style={{ width: '100%' }} />
                    <textarea
                        name="suggestion"
                        id="suggestion"
                        placeholder="Suggestion"
                        value={suggestion}
                        onChange={e => setSuggestion(e.target.value)}
                        required
                        rows="16"
                    ></textarea>
                    <div className={styles.buttonGroup}>
                        <button type="button" onClick={clearForm}>Clear</button>
                        <button type="submit">Submit</button>
                    </div>
                </form>
            </div>
        </>
    );
}

export default AddKNNPage;