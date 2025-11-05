import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

export default function SentimentSummary({ data }) {
  const pieData = [
    { name: "Positive", value: data.positive_articles, color: "#10b981" },
    { name: "Negative", value: data.negative_articles, color: "#ef4444" },
    { name: "Neutral", value: data.neutral_articles, color: "#f59e0b" },
  ];

  const COLORS = ["#10b981", "#ef4444", "#f59e0b"];

  const getSentimentColor = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive': return 'text-green-400';
      case 'negative': return 'text-red-400';
      case 'neutral': return 'text-yellow-400';
      default: return 'text-gray-400';
    }
  };

  const getSentimentIcon = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive': return '📈';
      case 'negative': return '📉';
      case 'neutral': return '➡️';
      default: return '📊';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center mb-6">
        <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl flex items-center justify-center mr-4">
          <span className="text-2xl">📊</span>
        </div>
        <h2 className="text-2xl font-bold text-gradient">Sentiment Analysis</h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Chart */}
        <div className="flex flex-col items-center">
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                dataKey="value"
                cx="50%"
                cy="50%"
                outerRadius={100}
                innerRadius={40}
                paddingAngle={5}
                stroke="none"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{
                  backgroundColor: '#1e293b',
                  border: '1px solid #334155',
                  borderRadius: '12px',
                  color: '#f1f5f9'
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Stats */}
        <div className="space-y-4">
          <div className="text-center mb-6">
            <div className="text-4xl font-bold text-gradient mb-2">
              {getSentimentIcon(data.overall)} {data.overall}
            </div>
            <p className="text-gray-400">Overall Market Sentiment</p>
          </div>

          <div className="space-y-3">
            {pieData.map((item, index) => (
              <div key={item.name} className="flex items-center justify-between p-4 bg-dark-800/50 rounded-xl border border-white/10">
                <div className="flex items-center">
                  <div 
                    className="w-4 h-4 rounded-full mr-3" 
                    style={{ backgroundColor: COLORS[index] }}
                  ></div>
                  <span className="text-gray-200 font-medium">{item.name}</span>
                </div>
                <div className="text-right">
                  <div className="text-xl font-bold text-gray-100">{item.value}</div>
                  <div className="text-sm text-gray-400">articles</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
