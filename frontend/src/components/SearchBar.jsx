import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [symbol, setSymbol] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (symbol.trim()) onSearch(symbol.trim().toUpperCase());
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="relative group">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <span className="text-gray-400 text-xl">🔍</span>
        </div>
        <input
          type="text"
          placeholder="Enter Stock Symbol (e.g. AAPL, GOOGL, MSFT)"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          className="w-full pl-12 pr-32 py-4 bg-dark-800/50 border border-white/10 rounded-2xl text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all duration-300 backdrop-blur-sm"
        />
        <button 
          type="submit" 
          className="absolute right-2 top-2 bottom-2 px-6 bg-gradient-to-r from-purple-600 to-primary-600 hover:from-purple-500 hover:to-primary-500 text-white font-semibold rounded-xl transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-purple-500/50 shadow-lg hover:shadow-purple-500/25"
        >
          Analyze
        </button>
      </div>
      <p className="text-gray-400 text-sm mt-3 text-center">
        Get instant AI-powered sentiment analysis for any stock
      </p>
    </form>
  );
}
