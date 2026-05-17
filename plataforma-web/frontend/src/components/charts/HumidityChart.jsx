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

const HumidityChart = ({ data }) => {

  return (
    <div className="chart-container humidity-chart">

      <div className="chart-header">

        <h2>
          Humedad
        </h2>

        <span>
          Monitoreo ambiental IoT
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
            domain={[0, 100]}
          />

          <Tooltip />

          {/* ZONA PREVENTIVA */}

          <ReferenceLine
            y={70}
            stroke="orange"
            strokeDasharray="5 5"
          />

          {/* ZONA CRÍTICA */}

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
  );
};

export default HumidityChart;