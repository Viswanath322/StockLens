export default function AudioPlayer({ audioUrl }) {
  if (!audioUrl) return null;
  
  return (
    <div className="space-y-4">
      <div className="flex items-center mb-4">
        <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mr-4">
          <span className="text-2xl">🎧</span>
        </div>
        <h3 className="text-2xl font-bold text-gradient">AI-Generated Audio Summary</h3>
      </div>
      
      <div className="bg-dark-800/50 rounded-xl p-6 border border-white/10">
        <div className="flex items-center justify-center">
          <audio 
            controls 
            src={`${import.meta.env.VITE_API_URL}${audioUrl}`} 
            className="w-full max-w-md bg-dark-700 rounded-lg"
            style={{
              filter: 'invert(1) hue-rotate(180deg)',
            }}
          />
        </div>
        <p className="text-gray-400 text-sm mt-3 text-center">
          Listen to the AI-generated summary of market sentiment
        </p>
      </div>
    </div>
  );
}
