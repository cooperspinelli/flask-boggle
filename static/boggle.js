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

async function handleFormSubmit() {
  const word = $wordInput.val();
  const response = await fetch('api/score-word',
    {
      method: POST,
      body: { word, gameId }
    }
  );
  const response_data = await response.json()
  result = response_data.result
}

$form.on('submit', tobedetermined);

start();