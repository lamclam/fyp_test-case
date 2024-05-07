import axios from 'axios';

const url = 'https://api.lamy.day/getdata'

// Generalized function to fetch data based on table and optional where clause
export const fetchData = async (tableName, whereColumn = null, whereTarget = null) => {
    const params = { table_name: tableName };
    if (whereColumn && whereTarget) {
        params.where_column = whereColumn;
        params.where_target = whereTarget;
    }

    const options = {
        method: 'GET',
        url: url,
        params: params,
        timeout: 25000
    };

    try {
        const response = await axios.request(options);
        if (response.status !== 200) {
            console.error("Invalid response status", response);
            return null;
        }
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error(`Failed to fetch data from ${tableName}`);
    }
}

export const fetchFile = async (questionID, fileType, user_id) => {
    const params = {
        user_id: user_id,
        question_id: questionID,
        type: fileType
    };

    const options = {
        method: 'GET',
        url: url,
        params: params
    };

    try {
        const response = await axios.request(options);
        if (response.status !== 200) {
            console.error("Invalid response status", response);
            return;
        }
        console.log(response);
        return response;
    } catch (error) {
        console.error(error);
        throw new Error(`Failed to fetch file of ${fileType} in ${questionID} by ${user_id}`);
    }
}