"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;

/** Start */

async function start() {
  const response = await fetch(`/api/new-game`, {
    method: "POST",
  });
  const gameData = await response.json();

  gameId = gameData.gameId;
  let board = gameData.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();
  // loop over board and create the DOM tr/td structure
  const $tableBody = $('<tbody>');

  for (let row of board) {
    const $rowToFill = $('<tr>');
    for (let elem of row) {
      $rowToFill.append($(`<td>${elem}</td>`));
    }
    $tableBody.append($rowToFill);
  }
  $table.append($tableBody);
}

async function makeRequest(word) {
  console.log("HERE");
  const response = await fetch('/api/score-word',
    {
      method: "POST",
      body: JSON.stringify({ word, gameId }),
      headers: {
        "Content-Type": "application/json"
      }
    }
  );
  console.log("MAYBE");
  const response_data = await response.json();
  console.log(response_data);
  return response_data.result;
}

function updateUiOnFormSubmit(word, result) {
  $message.empty();

  if (result === "ok") {
    $playedWords.append($(`<li>${word}</li>`));
  }

  if (result === "not-word") {
    $message.append($("<p>Not a word</p>"));
  }

  if (result === "not-on-board") {
    $message.append($("<p>Not on board</p>"));
  }

}

async function handleFormSubmit() {
  console.log("HUHHHHHH");
  const word = $wordInput.val();
  const result = await makeRequest(word);
  updateUiOnFormSubmit(word, result);
}

$form.on('submit', handleFormSubmit);

start();