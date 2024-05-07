"use client"

import React, { useState } from 'react';
import axios from 'axios'; // Import axios
import styles from '@/app/ui/dashboard/questions/addQuestion/addQuestion.module.css';
import Navbar from '@/app/ui/dashboard/navbar/navbar';

const AddQuestionPage = () => {
    const [questionName, setQuestionName] = useState('');
    const [questionId, setQuestionId] = useState('');
    const [correctArray, setCorrectArray] = useState('');
    const [fileName, setFileName] = useState('');
    const [driverName, setDriverName] = useState('');
    const [positiveKeywords, setPositiveKeywords] = useState('');
    const [negativeKeywords, setNegativeKeywords] = useState('');
    const [isDriverNeeded, setIsDriverNeeded] = useState(false);

    const handleDriverChange = (event) => {
        setIsDriverNeeded(event.target.value === 'true');
    };

    const handleFormSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('question_name', questionName);
        formData.append('question_id', questionId);
        formData.append('correct_array', correctArray);
        formData.append('driver_type', isDriverNeeded ? '1' : '0');
        formData.append('question_filename', fileName);
        formData.append('p_word', positiveKeywords);
        formData.append('n_word', negativeKeywords);

        if (isDriverNeeded) {
            formData.append('driver_name', driverName);
            const driverFile = document.querySelector('#driverFile').files[0];
            if (driverFile) {
                formData.append('file', driverFile);
            }
        }

        try {
            const response = await axios.post('https://api.lamy.day/addquestion', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            console.log(response.data);
            alert('Question added successfully!');
            clearForm();
        } catch (error) {
            console.error('Error submitting form:', error);
            alert('Failed to add question');
        }
    };

    const clearForm = () => {
        setQuestionName('');
        setQuestionId('');
        setCorrectArray('');
        setFileName('');
        setDriverName('');
        setPositiveKeywords('');
        setNegativeKeywords('');
        setIsDriverNeeded(false);
    };

    return (
        <>
            <Navbar title="Add New Question" />
            <div className={styles.container}>
                <form className={styles.form} onSubmit={handleFormSubmit}>
                    <input type="text" placeholder="Question Name" name="question_name" required value={questionName} onChange={e => setQuestionName(e.target.value)} />
                    <div className={styles.radioSelect}>
                        <p>Does this question need a driver program?</p>
                        <div className={styles.radioSelectChoice}>
                            <div className={styles.opt}>
                                <input
                                    type="radio"
                                    id="needDriver"
                                    name="needDriver"
                                    value={true}
                                    onChange={handleDriverChange}
                                    checked={isDriverNeeded}
                                />
                                <label htmlFor="needDriver">Yes</label>
                            </div>
                            <div className={styles.opt}>
                                <input
                                    type="radio"
                                    id="noNeedDriver"
                                    name="needDriver"
                                    value={false}
                                    onChange={handleDriverChange}
                                    checked={!isDriverNeeded}
                                />
                                <label htmlFor="noNeedDriver">No</label>
                            </div>
                        </div>
                    </div>
                    <input type="text" placeholder="Question ID" name="question_id" required value={questionId} onChange={e => setQuestionId(e.target.value)} />
                    <input type="text" placeholder="Correct Result Array" name="correct_array" required value={correctArray} onChange={e => setCorrectArray(e.target.value)} />
                    <input type="text" placeholder="File name" name="file_name" required value={fileName} onChange={e => setFileName(e.target.value)} />

                    {isDriverNeeded && (
                        <>
                            <input
                                type="text"
                                placeholder="Driver name"
                                name="driver_name"
                                value={driverName}
                                onChange={e => setDriverName(e.target.value)}
                            />
                            <div className={styles.fileInput}>
                                <label htmlFor="driverFile">Upload Driver File:</label>
                                <input type="file" id="driverFile" name="driver_file" />
                            </div>
                        </>
                    )}
                    <textarea
                        placeholder="Positive Keywords, separate by commas"
                        value={positiveKeywords}
                        onChange={e => setPositiveKeywords(e.target.value)}
                    ></textarea>
                    <textarea
                        placeholder="Negative Keywords, separate by commas"
                        value={negativeKeywords}
                        onChange={e => setNegativeKeywords(e.target.value)}
                    ></textarea>
                    <div className={
                        styles.buttonGroup}>
                        <button type="button" onClick={clearForm}>Clear</button>
                        <button type="submit">Submit</button>
                    </div>
                </form>
            </div>
        </>
    );
}

export default AddQuestionPage;