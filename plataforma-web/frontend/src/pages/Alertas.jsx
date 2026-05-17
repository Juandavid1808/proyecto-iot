import { useEffect, useState } from "react";

import AlertCard from "../components/cards/AlertCard";

import { getAlertas } from "../services/alertasService";

import "./Alertas.css";

const Alertas = () => {

  const [alertas, setAlertas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlertas();
  }, []);

  const fetchAlertas = async () => {

    try {

      const response =
        await getAlertas();

      console.log(
        "RESPUESTA ALERTAS:",
        response
      );

      setAlertas(
        response.alertas || []
      );

    } catch (error) {

      console.error(
        "Error obteniendo alertas:",
        error
      );

    } finally {

      setLoading(false);

    }
  };

  return (
    <div className="alertas-page">

      <div className="page-header">

        <h1>
          Alertas Inteligentes
        </h1>

        <p>
          Monitoreo automático de
          condiciones ambientales.
        </p>

      </div>

      {loading ? (

        <p>Cargando alertas...</p>

      ) : (

        <div className="alerts-grid">

          {alertas.length > 0 ? (

            alertas.map((alerta) => (

              <AlertCard
                key={alerta.id}
                alerta={alerta}
              />

            ))

          ) : (

            <p>
              No hay alertas activas.
            </p>

          )}

        </div>

      )}

    </div>
  );
};

export default Alertas;