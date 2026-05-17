import api from './axios'

export const obtenerAlertas = async () => {

    const response = await api.get('alertas/')

    return response.data
}