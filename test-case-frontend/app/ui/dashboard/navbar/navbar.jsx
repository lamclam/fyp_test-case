"use client";
import { usePathname } from "next/navigation";
import styles from "./navbar.module.css";

const Navbar = ({ title }) => {
    const pathname = usePathname();
    if (!title || title == "") {
        title = pathname.split("/").pop()
    }

    return (
        <div className={styles.container}>
            <div className={styles.title}>{title}</div>
            <div className={styles.menu}>
                <div className={styles.icons}>
                </div>
            </div>
        </div>
    );
};

export default Navbar;