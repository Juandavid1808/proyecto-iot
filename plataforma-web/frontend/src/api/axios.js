import axios from 'axios'

const api = axios.create({
    baseURL: 'https://proyecto-iot-d7gb.onrender.com/api/',

    headers: {
        'Content-Type': 'application/json',
    },
})

export default api
