import styles from "./card.module.css";

const Card = ({ item }) => {
    return (
        <div className={styles.container}>
            <div className={styles.texts}>
                <p>Welcome!</p>
            </div>
        </div>
    );
};

export default Card;