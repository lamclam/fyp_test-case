import SideBar from "../ui/dashboard/sidebar/sidebar"
import styles from "../ui/dashboard/dashboard.module.css"

const Layout = ({ children }) => {
    return (
        <div className={styles.container}>
            <div className={styles.menu}>
                <SideBar />
            </div>
            <div className={styles.content}>
                {children}
            </div>
        </div>
    )
}

export default Layout