async function sendMessage() {
  const input = document.getElementById("user-input");
  const mode = document.getElementById("mode").value;
  const chatBox = document.getElementById("chat-box");

  const userMsg = input.value.trim();
  if (!userMsg) return;

  // Show user message
  chatBox.innerHTML += `<p><strong>You:</strong> ${userMsg}</p>`;

  try {
    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMsg, mode }),
    });

    const data = await response.json();
    const reply = data.response || "Oops, something went wrong!";

    // Show AI response
    chatBox.innerHTML += `<p><strong>GFAI143:</strong> ${reply}</p>`;

    // ✅ Play audio if present
    if (data.audio_url) {
      if (data.audio_url) {
        chatBox.innerHTML += `<p><em>🎶 Playing audio...</em></p>`;
        const audio = new Audio(`http://127.0.0.1:8000${data.audio_url}`);
        audio.play();
      }
    }
  } catch (error) {
    chatBox.innerHTML += `<p><strong>GFAI143:</strong> Error connecting to server.</p>`;
  }

  chatBox.scrollTop = chatBox.scrollHeight;
  input.value = "";
}
