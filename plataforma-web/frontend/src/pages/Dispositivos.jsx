import { useEffect, useState } from "react";

import DeviceCard from "../components/cards/DeviceCard";

import { getDevices } from "../services/deviceService";

import "./Dispositivos.css";

const Dispositivos = () => {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDevices();
  }, []);

  const fetchDevices = async () => {
    try {
      const response = await getDevices();

      console.log(
        "RESPUESTA API:",
        response
      );

      setDevices(
        response.dispositivos || []
      );
    } catch (error) {
      console.error(
        "Error obteniendo dispositivos:",
        error
      );

      setDevices([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="devices-page">
      <div className="page-header">
        <h1>Dispositivos IoT</h1>

        <p>
          Monitoreo y visualización de
          dispositivos conectados al sistema.
        </p>
      </div>

      {loading ? (
        <p>Cargando dispositivos...</p>
      ) : (
        <div className="devices-grid">
          {devices.length > 0 ? (
            devices.map((device) => (
              <DeviceCard
                key={device.id}
                nombre={device.nombre}
                activo={device.activo}
                sensores={device.sensores}
              />
            ))
          ) : (
            <p>
              No hay dispositivos
              registrados.
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default Dispositivos;