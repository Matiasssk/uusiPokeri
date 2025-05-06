import React, { useState, useRef } from "react";
import SimulationWorker from "./simulationWorker.js?worker";
import CardDetectionUploader from "./CardDetectionUploader"; // uusi komponentti

export default function PokerSimulator() {
  const [card1, setCard1] = useState("As");
  const [card2, setCard2] = useState("Kd");
  const [players, setPlayers] = useState(2);
  const [simCount, setSimCount] = useState(5000);
  const [result, setResult] = useState(null);
  const [progress, setProgress] = useState(0);
  const [running, setRunning] = useState(false);
  const [board, setBoard] = useState(["", "", "", "", ""]);
  const workerRef = useRef(null);

  const ranks = [
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "J",
    "Q",
    "K",
    "A",
  ];
  const suits = ["s", "h", "d", "c"];

  function generateDeck() {
    return ranks.flatMap((r) => suits.map((s) => r + s));
  }

  const allCards = generateDeck();

  const handleSimulate = () => {
    const deck = [...new Set(generateDeck())];
    const usedBoard = board.filter((c) => c.length === 2);
    if (!deck.includes(card1) || !deck.includes(card2) || card1 === card2) {
      alert("Syötä kaksi eri korttia muodossa 'As', 'Td' jne.");
      return;
    }
    if (new Set([card1, card2, ...usedBoard]).size !== 2 + usedBoard.length) {
      alert("Kortit eivät saa toistua.");
      return;
    }
    if (workerRef.current) workerRef.current.terminate();
    const worker = new SimulationWorker();
    workerRef.current = worker;
    worker.onmessage = (e) => {
      if (e.data.type === "progress") setProgress(e.data.progress);
      if (e.data.type === "result") {
        setResult(e.data.result);
        setRunning(false);
        worker.terminate();
      }
    };
    setRunning(true);
    setProgress(0);
    setResult(null);
    worker.postMessage({ card1, card2, players, simCount, board: usedBoard });
  };

  const cardOptions = allCards.map((card) => (
    <option key={card} value={card}>
      {card}
    </option>
  ));

  return (
    <div className="p-6 max-w-xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Preflop Poker Simulator</h1>

      <CardDetectionUploader
        onDetected={(cards) => {
          const uniqueCards = Array.from(new Set(cards));
          if (uniqueCards.length >= 2) {
            setCard1(uniqueCards[0]);
            setCard2(uniqueCards[1]);
          }
          const boardCards = uniqueCards.slice(2, 7);
          setBoard([...boardCards, ...Array(5 - boardCards.length).fill("")]);
        }}
      />

      <div className="grid grid-cols-2 gap-2">
        <select
          value={card1}
          onChange={(e) => setCard1(e.target.value)}
          className="border p-2 rounded"
        >
          {cardOptions}
        </select>
        <select
          value={card2}
          onChange={(e) => setCard2(e.target.value)}
          className="border p-2 rounded"
        >
          {cardOptions}
        </select>
      </div>

      <div className="grid grid-cols-5 gap-2 mt-2">
        {[...Array(5)].map((_, i) => (
          <select
            key={i}
            value={board[i] || ""}
            onChange={(e) => {
              const newBoard = [...board];
              newBoard[i] = e.target.value;
              setBoard(newBoard);
            }}
            className="border p-2 rounded w-20"
          >
            <option value="">
              {["Flop1", "Flop2", "Flop3", "Turn", "River"][i]}
            </option>
            {cardOptions}
          </select>
        ))}
      </div>

      <div className="mt-2 space-y-2">
        <div>
          <label>Players: </label>
          <select
            value={players}
            onChange={(e) => setPlayers(+e.target.value)}
            className="ml-2 border rounded p-1"
          >
            {[2, 3, 4, 5, 6].map((n) => (
              <option key={n} value={n}>
                {n}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Simulations: </label>
          <input
            type="number"
            min={100}
            step={100}
            value={simCount}
            onChange={(e) => setSimCount(+e.target.value)}
            className="ml-2 border rounded p-1 w-24"
          />
        </div>
      </div>

      <button
        disabled={running}
        onClick={handleSimulate}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        Simulate
      </button>

      {running && <p>Simulating... {progress}%</p>}

      {result && (
        <div
          style={{
            border: "1px solid #ccc",
            padding: "1rem",
            marginTop: "1rem",
          }}
        >
          <p>Win: {result.win.toFixed(2)} %</p>
          <p>Tie: {result.tie.toFixed(2)} %</p>
          <p>Lose: {result.lose.toFixed(2)} %</p>
        </div>
      )}
    </div>
  );
}
