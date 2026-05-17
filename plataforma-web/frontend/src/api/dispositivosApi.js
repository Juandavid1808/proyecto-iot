import api from './axios'

export const obtenerDispositivos = async () => {

    const response = await api.get('dispositivos/')

    return response.data
}