function StoreSelector({ stores, selectedStore, onStoreChange }) {
  return (
    <div>
      <label
        htmlFor="store-select"
        className="block text-sm font-medium text-slate-300 mb-1.5"
      >
        Store
      </label>
      <select
        id="store-select"
        value={selectedStore || ""}
        onChange={(e) => onStoreChange(Number(e.target.value))}
        className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
      >
        <option value="">-- Choose a store --</option>
        {stores.map((store) => (
          <option key={store.Store} value={store.Store}>
            Store {store.Store} ({store.StoreType})
          </option>
        ))}
      </select>
    </div>
  );
}

export default StoreSelector;