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

const LightChart = ({ data }) => {

  return (
    <div className="chart-container light-chart">

      <div className="chart-header">

        <h2>
          Luz
        </h2>

        <span>
          Monitoreo de iluminación ambiental
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
            domain={[0, 300]}
          />

          <Tooltip />

          {/* RANGO NORMAL */}

          <ReferenceLine
            y={100}
            stroke="orange"
            strokeDasharray="5 5"
          />

          {/* RANGO CRÍTICO */}

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
  );
};

export default LightChart;