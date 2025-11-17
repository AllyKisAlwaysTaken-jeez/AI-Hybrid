const form = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");

function addMessage(content, sender) {
  const message = document.createElement("div");
  message.classList.add("message", sender);
  message.innerHTML = content;
  chatBox.appendChild(message);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function addLoadingBubble() {
  const loading = document.createElement("div");
  loading.classList.add("message", "bot");
  loading.id = "loading";
  loading.innerHTML = "💭 Thinking...";
  chatBox.appendChild(loading);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeLoadingBubble() {
  const loading = document.getElementById("loading");
  if (loading) loading.remove();
}

// Store user data to reuse for generating website
let lastUserInput = null;

form.addEventListener("submit", async (e) => {
  e.preventDefault(); // stop refresh

  const safe = (val) => (val || "").toString().trim();

  const industry = safe(document.getElementById("industry")?.value);
  const style = safe(document.getElementById("style")?.value);
  const goals = safe(document.getElementById("goals")?.value);

  const competitorsRaw = document.getElementById("competitors")?.value || "";
  const competitors = competitorsRaw
    .split(",")
    .map((c) => c.trim())
    .filter((c) => c);

  const userMessage = `
    Industry: <strong>${industry}</strong><br>
    Style: <strong>${style}</strong><br>
    Goals: <strong>${goals}</strong>
  `;

  addMessage(userMessage, "user");
  form.reset();

  addLoadingBubble();

  try {
    const res = await fetch("/generate-portfolio-advice", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ industry, style, goals, competitors }),
    });

    const data = await res.json();
    removeLoadingBubble();

    const botMessage = `
      <strong>📋 Copywriting Advice:</strong><br>${data.copywriting.replace(/\n/g, "<br>")}<br><br>
      <strong>🔍 SEO Tips:</strong> ${data.seo_tips.recommended_keywords.join(", ")}<br>
      <strong>🎨 Design Guidelines:</strong><br>
      ${data.design_guidelines.map((g) => `• ${g}`).join("<br>")}<br><br>
      <button id="generate-site-btn" class="generate-btn">🚀 Build My Portfolio Website</button>
    `;

    addMessage(botMessage, "bot");
    lastUserInput = { industry, style, goals, competitors };

  } catch (err) {
    removeLoadingBubble();
    addMessage(`❌ Error: ${err.message}`, "bot");
  }
});

// Handle "Generate Website" button click
chatBox.addEventListener("click", async (e) => {
  if (e.target && e.target.id === "generate-site-btn") {
    if (!lastUserInput) return;
    e.target.disabled = true;
    e.target.innerText = "🛠️ Building website...";

    try {
      const res = await fetch("/generate-site", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(lastUserInput),
      });

      const data = await res.json();

      if (data.path) {
        const sitePath = encodeURIComponent(data.path);
        const previewLink = `/preview-site?path=${sitePath}`;

        addMessage(
          `✅ Your portfolio website has been generated!<br><a href="${previewLink}" target="_blank">🔗 Click here to preview it.</a>`,
          "bot"
        );
      } else {
        addMessage("⚠️ Something went wrong while building your website.", "bot");
      }
    } catch (err) {
      addMessage(`❌ Error: ${err.message}`, "bot");
    }
  }
});
