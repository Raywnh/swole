export default function Home() {
  return (
    <main className="flex-col justify-center items-center h-screen bg-slate-900 text-center font-mono">
      <h1 className="text-yellow-300 text-7xl mb-2">gyattifier</h1>
      <h2 className="text-slate-400 text-lg mb-5">this app does plastic surgery on a body part and makes it bigger lol</h2>
      <div className="mx-20 flex-row justify-center items-center bg-slate-200 p-6 rounded-lg shadow-lg">
        <div className="flew-col justify-center items-center mb-5">
          <input type="file" id="file-upload"></input>
        </div>
        <div className="mx-15 flex-row justify-center items-center bg-slate-300 p-6 rounded-lg shadow-md mb-5"></div>
        <button className="rounded-lg bg-yellow-300 p-3 text-zinc-800 shadow-md hover:bg-yellow-400">make ass bigger</button>
      </div>
    </main>
  );
} 
