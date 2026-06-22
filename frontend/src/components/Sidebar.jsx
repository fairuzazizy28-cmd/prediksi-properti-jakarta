import React from 'react';

function Sidebar({ currentView, setCurrentView }) {
  const menuItems = [
    { id: 'home', label: 'Home', icon: HomeIcon },
    { id: 'prediction', label: 'Price Prediction', icon: ChartIcon },
    { id: 'insight', label: 'Analytical Insight', icon: InsightIcon },
  ];

  return (
    <div className="w-64 h-screen fixed left-0 top-0 bg-[#0A0F24] border-r border-white/5 flex flex-col pt-8 pb-6 shadow-2xl z-50">
      {/* Logo */}
      <div className="px-8 mb-10">
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Hargain</h1>
        <p className="text-[10px] text-slate-400 font-bold tracking-[0.2em] mt-1 uppercase">Premium Property AI</p>
      </div>

      {/* Navigation */}
      <nav className="flex-grow">
        <ul className="space-y-2 px-4">
          {menuItems.map((item) => {
            const isActive = currentView === item.id;
            return (
              <li key={item.id}>
                <button
                  onClick={() => setCurrentView(item.id)}
                  className={`w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all duration-300 relative group ${
                    isActive ? 'bg-[#1E2538] text-white font-semibold' : 'text-slate-400 hover:text-white hover:bg-white/5'
                  }`}
                >
                  {isActive && <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-primary rounded-r-full" />}
                  <item.icon className={`w-5 h-5 ${isActive ? 'text-primary' : 'text-slate-500 group-hover:text-slate-300'}`} />
                  <span className="text-sm">{item.label}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Bottom Section */}
      <div className="px-6 space-y-4">
        <button 
          onClick={() => setCurrentView('prediction')}
          className="w-full flex items-center justify-center gap-2 py-3 rounded-xl border border-white/10 text-sm font-semibold text-white hover:bg-white/5 transition-colors"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
          New Prediction
        </button>
        
        <div className="pt-4 border-t border-white/5 flex flex-col gap-2">
          <button className="flex items-center gap-3 px-4 py-2 text-sm text-slate-400 hover:text-white transition-colors">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
            Settings
          </button>
          <button className="flex items-center gap-3 px-4 py-2 text-sm text-slate-400 hover:text-white transition-colors">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            Support
          </button>
        </div>
      </div>
    </div>
  );
}

// Icons
const HomeIcon = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
);

const ChartIcon = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
);

const InsightIcon = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" /></svg>
);

export default Sidebar;
