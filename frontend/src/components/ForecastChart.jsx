import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

function mergeForecastData(historical, predictions) {
  const historicalPoints = historical.map((point) => ({
    date: point.date,
    actual: point.sales,
    predicted: null,
  }));

  const predictedPoints = predictions.map((point) => ({
    date: point.date,
    actual: null,
    predicted: point.predicted_sales,
  }));

  return [...historicalPoints, ...predictedPoints];
}

function ForecastChart({ forecastResult }) {
  if (!forecastResult) return null;

  const chartData = mergeForecastData(
    forecastResult.historical,
    forecastResult.predictions
  );

  return (
    <div>
      <h2 className="text-lg font-semibold text-slate-100 mb-4">
        Demand Forecast — Store {forecastResult.store_id}
      </h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} />
          <YAxis stroke="#94a3b8" fontSize={12} />
          <Tooltip
            contentStyle={{
              backgroundColor: "#1e293b",
              border: "1px solid #334155",
              borderRadius: "8px",
            }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="actual"
            stroke="#818cf8"
            strokeWidth={2}
            name="Historical Sales"
            connectNulls={false}
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="predicted"
            stroke="#34d399"
            strokeWidth={2}
            name="Forecasted Sales"
            connectNulls={false}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ForecastChart;