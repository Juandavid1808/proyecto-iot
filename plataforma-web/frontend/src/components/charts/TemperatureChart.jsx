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

import "./Chart.css";

const TemperatureChart = ({ data }) => {

  return (
    <div className="chart-container">

      <div className="chart-header">

        <h2>
          Temperatura
        </h2>

        <span>
          Sensor ambiental IoT
        </span>

      </div>

      <ResponsiveContainer
        width="100%"
        height={260}
      >

        <LineChart data={data}>

          <CartesianGrid
            strokeDasharray="3 3"
          />

          <XAxis dataKey="fecha" />

          <YAxis
            domain={[-10, 50]}
          />

          <Tooltip />

          {/* RANGO PREVENTIVO */}

          <ReferenceLine
            y={35}
            stroke="orange"
            strokeDasharray="5 5"
          />

          {/* RANGO CRÍTICO */}

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
  );
};

export default TemperatureChart;