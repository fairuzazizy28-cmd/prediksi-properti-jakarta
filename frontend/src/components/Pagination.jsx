import React from 'react';

const Pagination = ({ currentPage, totalPages, onPageChange }) => {
  if (totalPages <= 1) return null;

  const pages = [];
  // Calculate which page numbers to show
  let startPage = Math.max(1, currentPage - 2);
  let endPage = Math.min(totalPages, currentPage + 2);
  
  if (currentPage <= 2) endPage = Math.min(totalPages, 5);
  if (currentPage >= totalPages - 1) startPage = Math.max(1, totalPages - 4);

  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }

  return (
    <div className="flex items-center justify-center gap-2 mt-8 mb-4">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className={`px-4 py-2 rounded-xl text-sm font-bold transition-all flex items-center gap-2 ${
          currentPage === 1 
            ? 'bg-white/5 text-slate-500 cursor-not-allowed border border-white/5' 
            : 'bg-[#1A1F36] text-white hover:bg-primary hover:text-white border border-white/10 hover:border-primary shadow-lg hover:shadow-[0_0_15px_rgba(45,104,255,0.4)]'
        }`}
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7" /></svg>
        Prev
      </button>

      <div className="flex items-center gap-1">
        {startPage > 1 && (
          <>
            <button onClick={() => onPageChange(1)} className="w-10 h-10 rounded-xl text-sm font-bold text-slate-400 hover:text-white hover:bg-white/10 transition-all border border-transparent">1</button>
            {startPage > 2 && <span className="text-slate-500">...</span>}
          </>
        )}

        {pages.map(page => (
          <button
            key={page}
            onClick={() => onPageChange(page)}
            className={`w-10 h-10 rounded-xl text-sm font-bold transition-all ${
              currentPage === page 
                ? 'bg-primary text-white border border-primary shadow-[0_0_15px_rgba(45,104,255,0.4)]' 
                : 'text-slate-400 hover:text-white hover:bg-white/10 border border-transparent'
            }`}
          >
            {page}
          </button>
        ))}

        {endPage < totalPages && (
          <>
            {endPage < totalPages - 1 && <span className="text-slate-500">...</span>}
            <button onClick={() => onPageChange(totalPages)} className="w-10 h-10 rounded-xl text-sm font-bold text-slate-400 hover:text-white hover:bg-white/10 transition-all border border-transparent">{totalPages}</button>
          </>
        )}
      </div>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className={`px-4 py-2 rounded-xl text-sm font-bold transition-all flex items-center gap-2 ${
          currentPage === totalPages 
            ? 'bg-white/5 text-slate-500 cursor-not-allowed border border-white/5' 
            : 'bg-[#1A1F36] text-white hover:bg-primary hover:text-white border border-white/10 hover:border-primary shadow-lg hover:shadow-[0_0_15px_rgba(45,104,255,0.4)]'
        }`}
      >
        Next
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" /></svg>
      </button>
    </div>
  );
};

export default Pagination;
