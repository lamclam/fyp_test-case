import styles from './resultComp.module.css'

const ResultsComponent = ({ data }) => {
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

            {suggestion && suggestion.length > 0 && (
                <>
                    <h2>Possible reason:</h2>
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

export default ResultsComponent;