import { useEffect, useState } from "react";

import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

import { getHistorial } from "../services/historialService";

import "./Historial.css";

const Historial = () => {
  const [historial, setHistorial] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistorial();
  }, []);

  const fetchHistorial = async () => {
    try {
      const response = await getHistorial();

      console.log(
        "RESPUESTA HISTORIAL:",
        response
      );

      setHistorial(
        response.historial || []
      );

      setStats(
        response.estadisticas || {}
      );

    } catch (error) {
      console.error(
        "Error obteniendo historial:",
        error
      );
    } finally {
      setLoading(false);
    }
  };

  // FILTROS POR SENSOR

  const temperaturaData =
    historial.filter(
      (item) =>
        item.sensor === "temperatura"
    );

  const humedadData =
    historial.filter(
      (item) =>
        item.sensor === "humedad"
    );

  const ruidoData =
    historial.filter(
      (item) =>
        item.sensor === "sonido"
    );

  const luzData =
    historial.filter(
      (item) =>
        item.sensor === "luz"
    );

  return (
    <div className="historial-page">

      <div className="page-header">
        <h1>Historial Ambiental</h1>

        <p>
          Monitoreo histórico y análisis
          estadístico de sensores IoT.
        </p>
      </div>

      {/* KPIs */}

      <div className="stats-grid">

        <div className="stat-card">
          <h3>Temperatura Promedio</h3>

          <p>
            {
              stats.promedios
                ?.temperatura || "--"
            } °C
          </p>
        </div>

        <div className="stat-card">
          <h3>Humedad Promedio</h3>

          <p>
            {
              stats.promedios
                ?.humedad || "--"
            } %
          </p>
        </div>

        <div className="stat-card">
          <h3>Ruido Promedio</h3>

          <p>
            {
              stats.promedios
                ?.sonido || "--"
            } dB
          </p>
        </div>

        <div className="stat-card">
          <h3>Luz Promedio</h3>

          <p>
            {
              stats.promedios
                ?.luz || "--"
            } lx
          </p>
        </div>

      </div>

      {/* TABLA */}

      {!loading && (

        <div className="table-container">

          <table className="historial-table">

            <thead>
              <tr>
                <th>Sensor</th>
                <th>Valor</th>
                <th>Unidad</th>
                <th>Fecha</th>
              </tr>
            </thead>

            <tbody>

              {historial.map((item) => (

                <tr key={item.id}>

                  <td>
                    {item.sensor}
                  </td>

                  <td>
                    {item.valor}
                  </td>

                  <td>
                    {item.unidad}
                  </td>

                  <td>
                    {item.fecha}
                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      )}

      {/* GRÁFICAS */}

      <div className="charts-grid">

        {/* TEMPERATURA */}

        <div className="chart-container">

          <h2>Temperatura</h2>

          <ResponsiveContainer
            width="100%"
            height={250}
          >

            <LineChart
              data={temperaturaData}
            >

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="fecha" />

              <YAxis
                domain={[-10, 50]}
              />

              <Tooltip />

              <ReferenceLine
                y={35}
                stroke="orange"
                strokeDasharray="5 5"
              />

              <ReferenceLine
                y={45}
                stroke="red"
                strokeDasharray="5 5"
              />

              <Line
                type="monotone"
                dataKey="valor"
                stroke="#ef4444"
                strokeWidth={3}
                dot={{ r: 6 }}
                activeDot={{ r: 8 }}
                connectNulls
              />

            </LineChart>

          </ResponsiveContainer>

        </div>

        {/* HUMEDAD */}

        <div className="chart-container">

          <h2>Humedad</h2>

          <ResponsiveContainer
            width="100%"
            height={250}
          >

            <LineChart
              data={humedadData}
            >

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="fecha" />

              <YAxis
                domain={[0, 100]}
              />

              <Tooltip />

              <ReferenceLine
                y={70}
                stroke="orange"
                strokeDasharray="5 5"
              />

              <ReferenceLine
                y={85}
                stroke="red"
                strokeDasharray="5 5"
              />

              <Line
                type="monotone"
                dataKey="valor"
                stroke="#3b82f6"
                strokeWidth={3}
                dot={{ r: 6 }}
                activeDot={{ r: 8 }}
                connectNulls
              />

            </LineChart>

          </ResponsiveContainer>

        </div>

        {/* SONIDO */}

        <div className="chart-container">

          <h2>Ruido</h2>

          <ResponsiveContainer
            width="100%"
            height={250}
          >

            <LineChart
              data={ruidoData}
            >

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="fecha" />

              <YAxis
                domain={[0, 130]}
              />

              <Tooltip />

              <ReferenceLine
                y={70}
                stroke="orange"
                strokeDasharray="5 5"
              />

              <ReferenceLine
                y={100}
                stroke="red"
                strokeDasharray="5 5"
              />

              <Line
                type="monotone"
                dataKey="valor"
                stroke="#22c55e"
                strokeWidth={3}
                dot={{ r: 6 }}
                activeDot={{ r: 8 }}
                connectNulls
              />

            </LineChart>

          </ResponsiveContainer>

        </div>

        {/* LUZ */}

        <div className="chart-container">

          <h2>Luz</h2>

          <ResponsiveContainer
            width="100%"
            height={250}
          >

            <LineChart
              data={luzData}
            >

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="fecha" />

              <YAxis
                domain={[0, 300]}
              />

              <Tooltip />

              <ReferenceLine
                y={100}
                stroke="orange"
                strokeDasharray="5 5"
              />

              <ReferenceLine
                y={250}
                stroke="red"
                strokeDasharray="5 5"
              />

              <Line
                type="monotone"
                dataKey="valor"
                stroke="#eab308"
                strokeWidth={3}
                dot={{ r: 6 }}
                activeDot={{ r: 8 }}
                connectNulls
              />

            </LineChart>

          </ResponsiveContainer>

        </div>

      </div>

    </div>
  );
};

export default Historial;