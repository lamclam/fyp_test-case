import styles from './resultComp.module.css'

const ResultsComponentT = ({ data }) => {
    // Check if data is empty or missing essential properties
    if (!data || !data.results) {
        return (
            <div className={styles.helloText}>
                <p>Please enter your code in the text area on the left. Then click the &quot;Test&quot; button to test your code.</p>
                <p>When you are ready to submit, click &quot;Submit your code&quot; in the lower right corner</p>
            </div>
        );
    }

    const { results, suggestion } = data;

    // Calculate correct and incorrect counts
    const correctCount = results.filter(result => result.isCorrect).length;
    const incorrectCount = results.length - correctCount;
    const totalCount = results.length;

    return (
        <div className={styles.textArea}>
            <h1>Test Results</h1>
            <div className={styles.resultTextArea}>
                <p>Total test cases: <span className={styles.normalText}>{totalCount}</span></p>
                <p>Number of correct test cases: <span className={styles.greenText}>{correctCount}</span></p>
                <p>Number of incorrect test cases: <span className={styles.redText}>{incorrectCount}</span></p>
            </div>

            {/* Render all test cases */}
            <h2>All Test Cases</h2>
            <ul className={styles.allTestCases}>
                {results.map((test, index) => (
                    <li key={index} className={test.isCorrect ? styles.correctTestCase : styles.incorrectTestCase}>
                        Test Input: <strong>{test.stdin}</strong> - {test.isCorrect ? 'Correct' : 'Incorrect'}
                    </li>
                ))}
            </ul>

            {incorrectCount > 0 && (
                <>
                    <h2>Incorrect Test Cases</h2>
                    <ul className={styles.failedArea}>
                        {results.filter(result => !result.isCorrect).map((test, index) => (
                            <li key={index}>
                                Test Input: <strong>{test.stdin}</strong>
                            </li>
                        ))}
                    </ul>
                </>
            )}

            {suggestion && suggestion.length > 0 && (
                <>
                    <h2>Suggestions</h2>
                    <ul className={styles.suggestionArea}>
                        {suggestion.map((sugg, index) => (
                            <li key={index}>{sugg}</li>
                        ))}
                    </ul>
                </>
            )}
        </div>
    );
};

export default ResultsComponentT;