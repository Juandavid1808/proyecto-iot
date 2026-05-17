import api from "../api/axios";

export const getDevices = async () => {
  try {
    const response = await api.get("/dispositivos/");

    return response.data;
  } catch (error) {
    console.error(
      "Error obteniendo dispositivos:",
      error
    );

    throw error;
  }
};