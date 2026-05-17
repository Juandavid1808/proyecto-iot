import axios from "axios"

const API_URL =
  "http://127.0.0.1:8000/api/historial/"

export const getHistorial = async () => {

  try {

    const response = await axios.get(API_URL)

    return response.data

  } catch (error) {

    console.error(
      "Error obteniendo historial:",
      error
    )

    throw error
  }
}