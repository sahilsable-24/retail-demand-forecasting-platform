import { useState } from "react";
import { getPredictions } from "../api/client";

function ForecastForm({ selectedStore, onForecastResult }) {
  const [startDate, setStartDate] = useState("2015-07-01");
  const [horizonDays, setHorizonDays] = useState(7);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();

    if (!selectedStore) {
      setError("Please select a store first.");
      return;
    }

    setSubmitting(true);
    setError(null);

    const requestBody = {
      store_id: selectedStore,
      start_date: startDate,
      horizon_days: horizonDays,
      promo_schedule: Array(horizonDays).fill(0),
    };

    try {
      const result = await getPredictions(requestBody);
      onForecastResult(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label
            htmlFor="start-date"
            className="block text-sm font-medium text-slate-300 mb-1.5"
          >
            Start date
          </label>
          <input
            id="start-date"
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div>
          <label
            htmlFor="horizon"
            className="block text-sm font-medium text-slate-300 mb-1.5"
          >
            Forecast horizon (days)
          </label>
          <input
            id="horizon"
            type="number"
            min="1"
            max="30"
            value={horizonDays}
            onChange={(e) => setHorizonDays(Number(e.target.value))}
            className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={submitting}
        className="w-full sm:w-auto px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-700 disabled:cursor-not-allowed rounded-lg font-medium transition-colors"
      >
        {submitting ? "Forecasting..." : "Get Forecast"}
      </button>

      {error && <p className="text-red-400 text-sm">{error}</p>}
    </form>
  );
}

export default ForecastForm;