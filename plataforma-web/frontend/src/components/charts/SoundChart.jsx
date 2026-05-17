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

const SoundChart = ({ data }) => {

  return (
    <div className="chart-container sound-chart">

      <div className="chart-header">

        <h2>
          Ruido
        </h2>

        <span>
          Monitoreo acústico ambiental
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
            domain={[0, 130]}
          />

          <Tooltip />

          {/* NIVEL CONVERSACIONAL */}

          <ReferenceLine
            y={70}
            stroke="orange"
            strokeDasharray="5 5"
          />

          {/* NIVEL CRÍTICO */}

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
  );
};

export default SoundChart;