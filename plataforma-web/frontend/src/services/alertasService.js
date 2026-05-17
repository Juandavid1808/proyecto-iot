import api from "../api/axios";

export const getAlertas = async () => {
  try {

    const response =
      await api.get("/alertas/");

    return response.data;

  } catch (error) {

    console.error(
      "Error obteniendo alertas:",
      error
    );

    throw error;
  }
};