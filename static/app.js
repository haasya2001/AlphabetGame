const socket = io();

const currentLetter = document.getElementById("current-letter");
const wordList = document.getElementById("word-list");
const wordInput = document.getElementById("word-input");
const errorMessage = document.getElementById("error-message");

document.getElementById("generate-letter").addEventListener("click", () => {
  socket.emit("generate_letter");
});

document.getElementById("submit-word").addEventListener("click", () => {
  const word = wordInput.value.trim();
  if (word) {
    socket.emit("submit_word", { word });
    wordInput.value = "";
    errorMessage.textContent = "";
  }
});

socket.on("new_letter", (data) => {
  currentLetter.textContent = data.letter;
  wordList.innerHTML = "";
});

socket.on("update_game", (data) => {
  currentLetter.textContent = data.letter;
  wordList.innerHTML = "";
  data.history.forEach((word) => {
    const li = document.createElement("li");
    li.textContent = word;
    wordList.appendChild(li);
  });
});

socket.on("invalid_word", (data) => {
  errorMessage.textContent = data.message;
});
