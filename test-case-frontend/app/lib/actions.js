import axios from 'axios';
import { revalidatePath } from 'next/cache';

const addUrl = 'https://api.lamy.day/addRecord';
const updateUrl = 'https://api.lamy.day/updateRecord';

// Usage:
// const formDataStudent = new Map([['Name', 'John'], ['Password', 'abc123'], ['StudentID', 's123456']]);
// addItem(formDataStudent, 'student');
export const addItem = async (formData, type) => {
    // Define table names and columns based on the type
    const config = {
        student: {
            tableName: 'Students',
            columns: ['Name', 'Password', 'StudentID'],
            revalidatePath: 'dashbeard/users'
        },
        teacher: {
            tableName: 'Teachers',
            columns: ['Name', 'Password', 'TeacherID'],
            revalidatePath: 'dashbeard/users'
        },
        question: {
            tableName: 'Questions',
            columns: ['QuestionID', 'QuestionName', 'CorrectResult', 'TeacherID', 'DriverType', 'QuestionFileName', 'QuestionDriverName'],
            revalidatePath: 'dashbeard/questions'
        },
        keyword: {
            tableName: 'QuestionsKeyWords',
            columns: ['QuestionID', 'QuestionsKeyWord', 'WordType'],
            revalidatePath: 'dashbeard/questions'
        },
        testCase: {
            tableName: 'TestCases',
            columns: ['QuestionID', 'TestCaseValue'],
            revalidatePath: 'dashbeard/questions'
        },
        testCaseResult: {
            tableName: 'TestCaseResults',
            columns: ['StudentID', 'QuestionID', 'TestCaseResult', 'Mark'],
            revalidatePath: 'dashbeard/questions'
        }
    };

    if (!config[type]) {
        throw new Error(`Unsupported type: ${type}`);
    }

    const { tableName, columns, revalidatePath: path } = config[type];
    const values = columns.map(column => formData.get(column));

    const options = {
        method: 'POST',
        url: addUrl,
        headers: { 'content-type': 'application/json' },
        data: {
            table_name: tableName,
            columns: columns,
            values: values
        }
    };

    try {
        const { data } = await axios.request(options);
        console.log(data);
        revalidatePath(path);

        return data;
    } catch (error) {
        console.error(error);
        throw new Error(`Failed to create ${type}`);
    }
}


// Usage:
// const formDataStudent = new Map([['Name', 'John'], ['Password', 'newpass123'], ['StudentID', 's123456']]);
// const whereClause = { StudentID: 's123456' };
// updateItem(formDataStudent, 'student', whereClause);
export const updateItem = async (formData, type, whereClause) => {
    // Define table names and columns based on the type
    const config = {
        student: {
            tableName: 'Students',
            columns: ['Name', 'Password', 'StudentID'],
            revalidatePath: 'dashbeard/users'
        },
        teacher: {
            tableName: 'Teachers',
            columns: ['Name', 'Password', 'TeacherID'],
            revalidatePath: 'dashbeard/users'
        },
        question: {
            tableName: 'Questions',
            columns: ['QuestionID', 'QuestionName', 'CorrectResult', 'TeacherID', 'DriverType', 'QuestionFileName', 'QuestionDriverName'],
            revalidatePath: 'dashbeard/questions'
        },
        keyword: {
            tableName: 'QuestionsKeyWords',
            columns: ['QuestionID', 'QuestionsKeyWord', 'WordType'],
            revalidatePath: 'dashbeard/questions'
        },
        testCase: {
            tableName: 'TestCases',
            columns: ['QuestionID', 'TestCaseValue'],
            revalidatePath: 'dashbeard/questions'
        },
    };

    if (!config[type]) {
        throw new Error(`Unsupported type: ${type}`);
    }

    const { tableName, columns, revalidatePath: path } = config[type];
    const values = columns.map(column => formData.get(column));

    const options = {
        method: 'PATCH',
        url: updateUrl,
        headers: { 'content-type': 'application/json' },
        data: {
            table_name: tableName,
            columns: columns,
            values: values,
            where_clause: whereClause
        }
    };

    try {
        const { data } = await axios.request(options);
        console.log(data);
        revalidatePath(path);

        return data;
    } catch (error) {
        console.error(error);
        throw new Error(`Failed to update ${type}`);
    }
}

export const deleteRecord = async(userID, type)