import axios from 'axios';

const apiUrl = import.meta.env.VITE_API_URL;

export const executeBatch = (code) => {
    return axios.post(`${apiUrl}/hongik/api/execute/batch/`, {code});
};
