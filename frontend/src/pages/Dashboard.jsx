import { useState } from "react";
import axios from "axios";
import SearchBar from "../components/SearchBar";
import ArticleList from "../components/ArticleList";
import SentimentSummary from "../components/SentimentSummary";
import AudioPlayer from "../components/AudioPlayer";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async (symbol) => {
    setLoading(true);
    setError("");
    setData(null);

    try {
      console.log("Calling API:", `${import.meta.env.VITE_API_URL}/api/sentiment?stock=${symbol}`);

      const res = await axios.get(
        `${import.meta.env.VITE_API_URL}/api/sentiment?stock=${symbol}`
      );

      setData(res.data);
    } catch (err) {
      console.error(err);
      setError("❌ Failed to fetch sentiment data. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen gradient-bg">
      {/* Header Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-purple-600/20 to-primary-600/20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <h1 className="text-5xl md:text-6xl font-bold text-gradient mb-4 animate-fade-in">
              📈 StockLens
            </h1>
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto animate-slide-up">
              AI-Powered Stock Sentiment Analysis & Market Intelligence
            </p>
            
            {/* Search Bar */}
            <div className="max-w-2xl mx-auto animate-slide-up">
              <SearchBar onSearch={handleSearch} />
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        {/* Loading State */}
        {loading && (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="relative">
              <div className="w-16 h-16 border-4 border-purple-200/20 border-t-purple-500 rounded-full animate-spin"></div>
              <div className="absolute inset-0 w-16 h-16 border-4 border-transparent border-t-primary-400 rounded-full animate-spin animate-pulse-slow"></div>
            </div>
            <p className="text-gray-300 mt-6 text-lg font-medium">Analyzing market sentiment...</p>
            <div className="flex space-x-1 mt-4">
              <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
              <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
            </div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="max-w-2xl mx-auto">
            <div className="glass-effect rounded-2xl p-8 text-center border border-red-500/20">
              <div className="text-red-400 text-6xl mb-4">⚠️</div>
              <p className="text-red-300 text-lg font-medium">{error}</p>
              <p className="text-gray-400 mt-2">Please check your connection and try again</p>
            </div>
          </div>
        )}

        {/* Data Display */}
        {data && (
          <div className="space-y-8 animate-fade-in">
            {/* Overall Sentiment Summary */}
            <div className="glass-effect rounded-2xl p-6 card-hover">
              <SentimentSummary data={data.overall_sentiment} />
            </div>

            {/* AI Summary Text */}
            {data.summary_text && (
              <div className="glass-effect rounded-2xl p-8 card-hover">
                <div className="flex items-center mb-6">
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-primary-500 rounded-xl flex items-center justify-center mr-4">
                    <span className="text-2xl">🧠</span>
                  </div>
                  <h3 className="text-2xl font-bold text-gradient">AI-Generated Summary</h3>
                </div>
                <div className="prose prose-invert max-w-none">
                  <p className="text-gray-200 leading-relaxed text-lg bg-dark-800/50 p-6 rounded-xl border border-white/10">
                    {data.summary_text}
                  </p>
                </div>
              </div>
            )}

            {/* Audio Player */}
            <div className="glass-effect rounded-2xl p-6 card-hover">
              <AudioPlayer audioUrl={data.audio_url} />
            </div>

            {/* Article List */}
            <div className="glass-effect rounded-2xl p-6 card-hover">
              <ArticleList articles={data.articles} />
            </div>
          </div>
        )}

        {/* Empty State */}
        {!data && !loading && !error && (
          <div className="text-center py-20">
            <div className="max-w-md mx-auto">
              <div className="text-8xl mb-6 opacity-50">📊</div>
              <h3 className="text-2xl font-bold text-gray-300 mb-4">Ready to Analyze</h3>
              <p className="text-gray-400 text-lg">
                Enter a stock symbol above to get started with AI-powered sentiment analysis
              </p>
              <div className="mt-8 flex flex-wrap justify-center gap-2">
                {['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN'].map((symbol) => (
                  <button
                    key={symbol}
                    onClick={() => handleSearch(symbol)}
                    className="px-4 py-2 bg-dark-800 hover:bg-dark-700 text-gray-300 hover:text-white rounded-lg transition-colors duration-200 border border-white/10 hover:border-purple-500/50"
                  >
                    {symbol}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
