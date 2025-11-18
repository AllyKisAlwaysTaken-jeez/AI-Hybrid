const form = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");

// Unique chat session for this user
let SESSION_ID = crypto.randomUUID();
let lastUserInput = null;

function addMessage(content, sender) {
  const div = document.createElement("div");
  div.classList.add("message", sender);
  div.innerHTML = content;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function addLoadingBubble() {
  const bubble = document.createElement("div");
  bubble.classList.add("message", "bot");
  bubble.id = "loading";
  bubble.innerText = "💭 Thinking...";
  chatBox.appendChild(bubble);
}

function removeLoadingBubble() {
  const bubble = document.getElementById("loading");
  if (bubble) bubble.remove();
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const industry = document.getElementById("industry").value.trim();
  const style = document.getElementById("style").value.trim();
  const goals = document.getElementById("goals").value.trim();
  const competitors = document
    .getElementById("competitors")
    .value.split(",")
    .map(c => c.trim())
    .filter(Boolean);

  addMessage(`Industry: <b>${industry}</b><br>Style: <b>${style}</b><br>Goals: <b>${goals}</b>`, "user");
  addLoadingBubble();

  lastUserInput = { industry, style, goals, competitors };

  const res = await fetch("/generate-portfolio-advice", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(lastUserInput),
  });

  const data = await res.json();
  removeLoadingBubble();

  addMessage(`
    <strong>📋 Copywriting:</strong><br>${data.copywriting.replace(/\n/g, "<br>")}<br><br>
    <strong>🔍 SEO Keywords:</strong> ${(data.seo_tips?.recommended_keywords || []).join(", ")}<br><br>
    <strong>🎨 Design Guidelines:</strong><br>${data.design_guidelines.map(g => "• " + g).join("<br>")}<br><br>
    <button id="generate-site-btn" class="generate-btn">🚀 Build My Portfolio Website</button>
  `, "bot");
});

chatBox.addEventListener("click", async (e) => {
  if (e.target.id === "generate-site-btn") {
    e.target.disabled = true;
    e.target.innerText = "🛠️ Building...";

    const res = await fetch("/generate-site", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(lastUserInput),
    });

    const data = await res.json();

    addMessage(
      `✅ Website generated!<br><a href="/preview" target="_blank">🔗 Click here to view your portfolio.</a>`,
      "bot"
    );
  }
});
