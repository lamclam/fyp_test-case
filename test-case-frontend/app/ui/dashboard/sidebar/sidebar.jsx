"use client"

import Image from "next/image";
import MenuLink from "./menuLink/menuLink";
import styles from "./sidebar.module.css";
import {
    MdDashboard,
    MdQuestionAnswer,
    MdOutlineSettings,
    MdLogout,
} from "react-icons/md";

const menuItemsTeacher = [
    {
        title: "",
        list: [
            {
                title: "Dashboard",
                path: "/dashboard",
                icon: <MdDashboard />,
            },
        ],
    },
    {
        title: "Questions",
        list: [
            {
                title: "Question 1",
                path: "/dashboard/question/1",
                icon: <MdQuestionAnswer />,
            },
            {
                title: "Question 2",
                path: "/dashboard/question/2",
                icon: <MdQuestionAnswer />,
            },
        ],
    },
    {
        title: "User",
        list: [
            {
                title: "All Users",
                path: "/dashboard/users",
                icon: <MdOutlineSettings />,
            },
            {
                title: "All Questions",
                path: "/dashboard/questions",
                icon: <MdOutlineSettings />,
            },
            {
                title: "All KNN Classes",
                path: "/dashboard/knn",
                icon: <MdOutlineSettings />,
            },
            {
                title: "All Test Cases",
                path: "/dashboard/testcase",
                icon: <MdOutlineSettings />,
            },
            {
                title: "Cluster",
                path: "/dashboard/cluster",
                icon: <MdOutlineSettings />,
            },
        ],
    },
    {
        title: "Logout",
        list: [
            {
                title: "Logout",
                path: "/login",
                icon: <MdLogout />,
                action: "logout",
            }
        ],
    },
];

const menuItemsStudent = [
    {
        title: "",
        list: [
            {
                title: "Dashboard",
                path: "/dashboard",
                icon: <MdDashboard />,
            },
        ],
    },
    {
        title: "Questions",
        list: [
            {
                title: "Question 1",
                path: "/dashboard/question/1",
                icon: <MdQuestionAnswer />,
            },
            {
                title: "Question 2",
                path: "/dashboard/question/2",
                icon: <MdQuestionAnswer />,
            },
        ],
    },
    {
        title: "Logout",
        list: [
            {
                title: "Logout",
                path: "/login",
                icon: <MdLogout />,
                action: "logout",
            }
        ],
    },
];

const SideBar = () => {
    const username = localStorage.getItem("userName");
    const userType = localStorage.getItem("type");
    let menuItems
    if (userType == "student")
        menuItems = menuItemsStudent;
    else
        menuItems = menuItemsTeacher;
    return (
        <div className={styles.container}>
            <div className={styles.user}>
                <div className={styles.userDetail}>
                    <span className={styles.username}>{username}</span>
                    <span className={styles.userTitle}>{userType}</span>
                </div>
            </div>
            <ul className={styles.list}>
                {menuItems.map(cat => (
                    <li key={cat.title}>
                        <span className={styles.cat}>{cat.title}</span>
                        {cat.list.map((item) => (
                            item.action === "logout" ?
                                <a key={item.title} className={`${styles.logoutLink} ${styles.logoutLink}`} href={item.path}>
                                    <span>{item.icon}</span>{item.title}
                                </a> :
                                <MenuLink item={item} key={item.title} />
                        ))}
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default SideBar;