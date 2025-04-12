const quizBox = document.getElementById("quiz-box");
const nextBtn = document.getElementById("next-btn");

const questions = [
  {
    question: "Your perfect date night?",
    options: [
      "🌃 Candlelight dinner",
      "🎬 Movie cuddle",
      "🌌 Stargazing under sky",
    ],
  },
  {
    question: "What's your ideal girlfriend vibe?",
    options: ["💋 Flirty & bold", "🎀 Cute & caring", "🧠 Deep & poetic"],
  },
  {
    question: "How do you express love?",
    options: ["📝 Love letters", "👐 Tight hugs", "🎁 Little surprises"],
  },
  {
    question: "What's your love language?",
    options: [
      "💞 Words of affirmation",
      "💌 Quality time",
      "🔥 Physical touch",
    ],
  },
  {
    question: "How fast do you fall in love?",
    options: [
      "💓 Slowly & deeply",
      "🌪️ Head over heels",
      "👀 Love at first sight",
    ],
  },
];

let currentQuestion = 0;
let score = 0;

function renderQuestion(index) {
  const q = questions[index];
  quizBox.innerHTML = `<h2>${q.question}</h2>`;
  q.options.forEach((option, i) => {
    quizBox.innerHTML += `
      <div>
        <input type="radio" name="option" value="${i}" id="opt${i}">
        <label for="opt${i}">${option}</label>
      </div>
    `;
  });
}

function nextQuestion() {
  const selected = document.querySelector('input[name="option"]:checked');
  if (!selected) return alert("Pick one, darling 💖");

  score += parseInt(selected.value); // use value to mix scores
  currentQuestion++;

  if (currentQuestion < questions.length) {
    renderQuestion(currentQuestion);
  } else {
    showResult();
  }
}

function showResult() {
  nextBtn.style.display = "none";
  let compatibility = "";
  let flirtyLine = "";

  if (score <= 4) {
    compatibility = "70% 💞 We're a sweet match!";
    flirtyLine =
      "You're the soft type. I'd love to hold your hand under the stars 😘";
  } else if (score <= 8) {
    compatibility = "85% 🔥 We're spicy and romantic!";
    flirtyLine = "You like love that excites the heart... so do I 😘";
  } else {
    compatibility = "100% 💘 Perfect soulmates!";
    flirtyLine = "You’re exactly my type, baby. Let's write our love story 💋";
  }

  quizBox.innerHTML = `
    <h2>Result: ${compatibility}</h2>
    <p>${flirtyLine}</p>
    <p>Wanna try again? Refresh me 😉</p>
  `;
}

window.onload = () => renderQuestion(currentQuestion);
