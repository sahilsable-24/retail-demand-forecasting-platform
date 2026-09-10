import { useEffect, useState } from "react";
import { getStores } from "./api/client";
import StoreSelector from "./components/StoreSelector";
import ForecastForm from "./components/ForecastForm";
import ForecastChart from "./components/ForecastChart";

function App() {
  const [selectedStore, setSelectedStore] = useState(null);
  const [stores, setStores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [forecastResult, setForecastResult] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getStores();
        setStores(data);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading)
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-400">
        Loading...
      </div>
    );
  if (error)
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-red-400">
        Error: {error.message}
      </div>
    );

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 px-6 py-10">
      <div className="max-w-5xl mx-auto space-y-8">
        <header>
          <h1 className="text-3xl font-semibold tracking-tight">
            Retail Demand Forecast
          </h1>
          <p className="text-slate-400 mt-1">
            Select a store and horizon to generate a sales forecast.
          </p>
        </header>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
          <StoreSelector
            stores={stores}
            selectedStore={selectedStore}
            onStoreChange={setSelectedStore}
          />
          <ForecastForm
            selectedStore={selectedStore}
            onForecastResult={setForecastResult}
          />
        </div>

        {forecastResult && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
            <ForecastChart forecastResult={forecastResult} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;