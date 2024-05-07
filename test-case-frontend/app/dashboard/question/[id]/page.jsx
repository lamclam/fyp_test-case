"use client"

import React, { useState, useEffect } from 'react';
import { useParams } from 'next/navigation'
import styles from '@/app/ui/dashboard/question/question.module.css';
import ResultsComponent from '@/app/ui/dashboard/question/resultComp';
import ResultsComponentT from '@/app/ui/dashboard/question/resultCompTeacher';
import Navbar from '@/app/ui/dashboard/navbar/navbar';
import axios from 'axios';
import { fetchData } from '@/app/lib/data';

const QuestionPage = () => {
    const [formData, setFormData] = useState('');
    const [resultData, setResultData] = useState('');
    const [questionName, setQuestionName] = useState('');
    const [showTestcase, setShowTestcase] = useState(false);
    const [loading, setLoading] = useState(false);
    const [questionData, setQuestionData] = useState("");
    const [submissionMessage, setSubmissionMessage] = useState('');
    const [userID, setUserID] = useState('');

    const params = useParams()

    useEffect(() => {
        const user_type = localStorage.getItem("type");
        setUserID(localStorage.getItem("userID"));
        setShowTestcase(user_type !== "student");

        fetchData('Questions', 'QuestionID', params.id).then(data => {
            setQuestionName(data[0].QuestionName);
            setQuestionData(data[0]);
        }).catch(error => console.error("Error fetching question name: ", error));

    }, [params.id]);

    const clearForm = () => {
        setFormData('');
        setResultData('');
    };

    const fetchResult = async () => {
        setLoading(true);
        try {
            const options = {
                method: 'POST',
                url: 'https://api.lamy.day/test',
                params: { question_id: params.id, student_id: userID },
                headers: {
                    'content-type': 'text/plain',
                },
                data: formData
            };
            const response = await axios.request(options);
            if (response.status !== 200) {
                console.error("Invalid response status", response);
                return;
            }
            setResultData(response.data);
        } catch (error) {
            console.error("Error fetching data: ", error);
        } finally {
            setLoading(false);
        };
    }

    const submit = async () => {
        setLoading(true);
        console.log(resultData.result_array);
        console.log(JSON.parse(questionData.CorrectResult.toString()));
        let arrayArg = JSON.stringify(resultData.result_array) !== JSON.parse(questionData.CorrectResult) ? JSON.stringify(resultData.result_array) : "";
        console.log(arrayArg);
        if (formData == '') {
            console.error("Empty code");
            setLoading(false);
            return
        }
        try {
            const options = {
                method: 'POST',
                url: 'https://api.lamy.day/submit',
                params: { question_id: params.id, student_id: userID },
                headers: { 'content-type': 'text/plain' },
                data: arrayArg.toString(),
            };
            const response = await axios.request(options);
            if (response.status === 200) {
                alert("Submitted!")
            } else {
                setSubmissionMessage('Submission failed');
            }
        } catch (error) {
            console.error("Error during submission: ", error);
            setSubmissionMessage('Submission failed');
        } finally {
            setLoading(false);
        };
    }


    return (
        <>
            <Navbar title={`Question ${params.id}: ${questionName}`} />
            <div className={styles.mainArea}>
                {loading && <div className={styles.loader}></div>}
                {/* {submissionMessage && <div className={styles.message}>{submissionMessage}</div>} */}
                <div className={styles.container}>
                    <div className={styles.inputArea}>
                        <form className={styles.form}>
                            <textarea
                                name="test_code"
                                id="test_code"
                                placeholder="Code to test"
                                value={formData}
                                onChange={(e) => setFormData(e.target.value)}
                                required
                                rows="16"
                            ></textarea>
                            <div className={styles.buttonGroup}>
                                <button type="button" onClick={clearForm} className={styles.clrbtn}>Clear</button>
                                <button type="button" onClick={() => fetchResult()}>Test</button>
                            </div>
                        </form>
                    </div>
                </div>
                <div className={styles.resultArea}>
                    {showTestcase ? <div className={styles.container}>
                        <ResultsComponentT data={resultData} />
                    </div> : <div className={styles.container}>
                        <ResultsComponent data={resultData} />
                    </div>}
                    {!showTestcase && <div className={`${styles.container} ${styles.submitContainer}`} style={{ height: '10%' }}>
                        <button type="button" className={styles.submitBtn} onClick={submit}>Submit your code</button>
                    </div>}
                </div>
            </div >
        </>
    );
}

export default QuestionPage;