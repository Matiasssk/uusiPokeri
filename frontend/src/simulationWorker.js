/*
// simulationWorker.js (create this file in src/)
import { rankCards } from "phe";

const ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"];
const suits = ["s", "h", "d", "c"];

// Luo ja sekoita pakka
function generateDeck() {
  return ranks.flatMap((r) => suits.map((s) => r + s));
}
function shuffle(array) {
  const a = array.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

self.onmessage = (e) => {
  const { card1, card2, players, simCount, batchSize = 500 } = e.data;
  let wins = 0,
    ties = 0;

  for (let start = 0; start < simCount; start += batchSize) {
    const end = Math.min(start + batchSize, simCount);
    for (let i = start; i < end; i++) {
      // Luo pakka ilman pelaajan kortteja
      let deck = generateDeck().filter((c) => c !== card1 && c !== card2);
      deck = shuffle(deck);
      let idx = 0;

      // Jaa vastustajille
      const opponentRanks = [];
      for (let p = 0; p < players - 1; p++) {
        const hand = [deck[idx], deck[idx + 1]];
        idx += 2;
        opponentRanks.push(
          rankCards([...hand, ...deck.slice(idx + 0, idx + 5)])
        );
      }
      // Jaa pöydälle
      const board = deck.slice(idx, idx + 5);
      const yourRank = rankCards([card1, card2, ...board]);

      const allRanks = [yourRank, ...opponentRanks];
      const best = Math.min(...allRanks);
      const winners = allRanks.filter((r) => r === best).length;
      if (yourRank === best) winners === 1 ? wins++ : ties++;
    }
    const progress = Math.floor(
      (Math.min(start + batchSize, simCount) / simCount) * 100
    );
    postMessage({ type: "progress", progress });
  }

  const losses = simCount - wins - ties;
  postMessage({
    type: "result",
    result: {
      win: (wins / simCount) * 100,
      tie: (ties / simCount) * 100,
      lose: (losses / simCount) * 100,
    },
  });
};
*/
// simulationWorker.js (create this file in src/)
import { rankCards } from "phe";

const ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"];
const suits = ["s", "h", "d", "c"];

// Luo ja sekoita pakka
function generateDeck() {
  return ranks.flatMap((r) => suits.map((s) => r + s));
}
function shuffle(array) {
  const a = array.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

self.onmessage = (e) => {
  const {
    card1,
    card2,
    players,
    simCount,
    batchSize = 500,
    board = [],
  } = e.data;
  let wins = 0,
    ties = 0;

  for (let start = 0; start < simCount; start += batchSize) {
    const end = Math.min(start + batchSize, simCount);
    for (let i = start; i < end; i++) {
      let deck = generateDeck().filter(
        (c) => ![card1, card2, ...board].includes(c)
      );
      deck = shuffle(deck);
      let idx = 0;

      const needed = 5 - board.length;
      const simulatedBoard = [...board, ...deck.slice(idx, idx + needed)];
      idx += needed;

      const yourRank = rankCards([card1, card2, ...simulatedBoard]);

      const opponentRanks = [];
      for (let p = 0; p < players - 1; p++) {
        const hand = [deck[idx], deck[idx + 1]];
        idx += 2;
        opponentRanks.push(rankCards([...hand, ...simulatedBoard]));
      }

      const allRanks = [yourRank, ...opponentRanks];
      const best = Math.min(...allRanks);
      const winners = allRanks.filter((r) => r === best).length;
      if (yourRank === best) winners === 1 ? wins++ : ties++;
    }
    const progress = Math.floor(
      (Math.min(start + batchSize, simCount) / simCount) * 100
    );
    postMessage({ type: "progress", progress });
  }

  const losses = simCount - wins - ties;
  postMessage({
    type: "result",
    result: {
      win: (wins / simCount) * 100,
      tie: (ties / simCount) * 100,
      lose: (losses / simCount) * 100,
    },
  });
};
