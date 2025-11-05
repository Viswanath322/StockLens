export default function ArticleList({ articles }) {
  const getSentimentColor = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive': return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'negative': return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'neutral': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const getSentimentIcon = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive': return '📈';
      case 'negative': return '📉';
      case 'neutral': return '➡️';
      default: return '📰';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center mb-6">
        <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center mr-4">
          <span className="text-2xl">📰</span>
        </div>
        <h2 className="text-2xl font-bold text-gradient">Related News Articles</h2>
      </div>

      <div className="space-y-4">
        {articles.map((article, index) => (
          <div 
            key={article.id} 
            className="bg-dark-800/50 rounded-xl p-6 border border-white/10 hover:border-purple-500/30 transition-all duration-300 hover:bg-dark-800/70"
          >
            <div className="flex items-start justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-100 leading-relaxed flex-1 pr-4">
                {article.headline}
              </h3>
              <div className={`px-3 py-1 rounded-full border text-sm font-medium whitespace-nowrap ${getSentimentColor(article.sentiment)}`}>
                {getSentimentIcon(article.sentiment)} {article.sentiment}
              </div>
            </div>
            
            <p className="text-gray-300 leading-relaxed mb-4">
              {article.summary}
            </p>
            
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center text-gray-400">
                <span className="mr-2">📊</span>
                Sentiment Score: <span className="font-semibold text-gray-200 ml-1">{article.score}</span>
              </div>
              <div className="text-gray-500">
                Article #{index + 1}
              </div>
            </div>
          </div>
        ))}
      </div>

      {articles.length === 0 && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4 opacity-50">📰</div>
          <p className="text-gray-400 text-lg">No articles found</p>
        </div>
      )}
    </div>
  );
}
