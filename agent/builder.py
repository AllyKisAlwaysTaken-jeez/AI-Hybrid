import os
from datetime import datetime
from typing import Optional

# Use your OpenAI-based helper instead of local HF models
from ai_generator import generate_response

def safe_generate_with_openai(prompt: str) -> str:
    """Use ai_generator.generate_response (OpenAI) as the text generation backend.
       Falls back to a short placeholder if something goes wrong.
    """
    try:
        resp = generate_response(prompt, style="auto", goals="auto")
        # ai_generator returns a string — use it directly. If it returns an error string, keep it.
        if resp and isinstance(resp, str):
            return resp.strip()
    except Exception as e:
        return f"(AI generation failed: {e}) Placeholder text."

    return "Lorem ipsum — AI couldn't generate content for this section."

def build_portfolio_website(industry: str, style: str, goals: str, project_info: Optional[str]=None, output_dir="generated_sites"):
    """
    Generate a multi-page portfolio website (Home, About, Projects, Contact).
    Returns absolute path to index.html of generated site.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    site_dir = os.path.join(output_dir, f"site_{timestamp}")
    os.makedirs(site_dir, exist_ok=True)
    assets_dir = os.path.join(site_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    # Compose prompts
    home_prompt = (
        f"Create 2 short, engaging paragraphs for the HOME page of a personal portfolio website.\n"
        f"Industry: {industry}. Style: {style}. Goals: {goals}.\n"
        "Include 3 short bullet highlights of skills or services."
    )
    about_prompt = (
        f"Write an ABOUT page copy (2-3 paragraphs) for a portfolio. Include background, experience highlights, and a short mission statement. Industry: {industry}. Style: {style}."
    )
    projects_prompt = (
        f"Write a PROJECTS page introduction listing 3 example project summaries each 1-2 sentences, relevant to Industry: {industry}. If project details are provided, incorporate them: {project_info}."
    )
    contact_prompt = (
        f"Write a short CONTACT page paragraph inviting clients to reach out. Provide an example contact form intro and a short polite closing."
    )

    # Generate content using OpenAI helper
    home_text = safe_generate_with_openai(home_prompt)
    about_text = safe_generate_with_openai(about_prompt)
    projects_text = safe_generate_with_openai(projects_prompt)
    contact_text = safe_generate_with_openai(contact_prompt)

    def to_html_paragraphs(text):
        parts = [p.strip() for p in text.split("\n\n") if p.strip()]
        return "\n".join(f"<p>{p}</p>" for p in parts)

    home_html = to_html_paragraphs(home_text)
    about_html = to_html_paragraphs(about_text)
    projects_html = to_html_paragraphs(projects_text)
    contact_html = to_html_paragraphs(contact_text)

    # Create basic pages (same HTML as before)
    index_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{industry.title()} Portfolio — Home</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<nav class="nav">
  <div class="nav-inner">
    <a class="brand" href="index.html">{industry.title()} Portfolio</a>
    <div class="links">
      <a href="index.html">Home</a>
      <a href="about.html">About</a>
      <a href="projects.html">Projects</a>
      <a href="contact.html">Contact</a>
    </div>
  </div>
</nav>

<header class="hero">
  <div class="container">
    <h1>Build a modern, {style} portfolio for {industry.title()}</h1>
    {home_html}
    <div class="cta">
      <a class="btn" href="projects.html">See Projects</a>
      <a class="btn ghost" href="contact.html">Contact Me</a>
    </div>
  </div>
</header>

<section class="features container">
  <div class="card">
    <h3>What I do</h3>
    <ul>
      <li>Customized portfolio design</li>
      <li>Case studies & copywriting</li>
      <li>SEO & performance optimisation</li>
    </ul>
  </div>
  <div class="card">
    <h3>Goal</h3>
    <p>{goals}</p>
  </div>
  <div class="card">
    <h3>Industry</h3>
    <p>{industry.title()}</p>
  </div>
</section>

<footer class="site-footer">
  <div class="container">
    <p>&copy; {datetime.now().year} — Generated Portfolio</p>
  </div>
</footer>
</body>
</html>
"""

    # (create other page strings as in your original code)
    about_page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>About — {industry.title()} Portfolio</title><link rel="stylesheet" href="style.css"></head>
<body>
<nav class="nav"><div class="nav-inner"><a class="brand" href="index.html">{industry.title()} Portfolio</a><div class="links"><a href="index.html">Home</a><a href="about.html">About</a><a href="projects.html">Projects</a><a href="contact.html">Contact</a></div></div></nav>
<main class="container"><h1>About Me</h1>{about_html}</main>
<footer class="site-footer"><div class="container"><p>&copy; {datetime.now().year} — Generated Portfolio</p></div></footer>
</body></html>"""

    projects_page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Projects — {industry.title()} Portfolio</title><link rel="stylesheet" href="style.css"></head>
<body>
<nav class="nav"><div class="nav-inner"><a class="brand" href="index.html">{industry.title()} Portfolio</a><div class="links"><a href="index.html">Home</a><a href="about.html">About</a><a href="projects.html">Projects</a><a href="contact.html">Contact</a></div></div></nav>
<main class="container"><h1>Selected Projects</h1>{projects_html}<p>For full demos or code links, replace these summaries with real project pages.</p></main>
<footer class="site-footer"><div class="container"><p>&copy; {datetime.now().year} — Generated Portfolio</p></div></footer>
</body></html>"""

    contact_page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Contact — {industry.title()} Portfolio</title><link rel="stylesheet" href="style.css"></head>
<body>
<nav class="nav"><div class="nav-inner"><a class="brand" href="index.html">{industry.title()} Portfolio</a><div class="links"><a href="index.html">Home</a><a href="about.html">About</a><a href="projects.html">Projects</a><a href="contact.html">Contact</a></div></div></nav>
<main class="container"><h1>Contact Me</h1>{contact_html}
<form class="contact-form" onsubmit="alert('This is a demo. Replace with real backend/email service.') ; return false;">
<label>Name</label><input type="text" placeholder="Your name" required>
<label>Email</label><input type="email" placeholder="you@example.com" required>
<label>Message</label><textarea placeholder="Tell me about your project..." required></textarea>
<button class="btn" type="submit">Send Message</button>
</form></main>
<footer class="site-footer"><div class="container"><p>&copy; {datetime.now().year} — Generated Portfolio</p></div></footer>
</body></html>"""

    css_text = """/* minimal CSS (same idea as your original) */
body { font-family: Inter, system-ui, Arial; margin:0; padding:0; background:#f7fafc; color:#111827;}
.container{max-width:1100px;margin:0 auto;padding:20px;}
a{color:#2563eb;}
"""
    # write files
    with open(os.path.join(site_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    with open(os.path.join(site_dir, "about.html"), "w", encoding="utf-8") as f:
        f.write(about_page)
    with open(os.path.join(site_dir, "projects.html"), "w", encoding="utf-8") as f:
        f.write(projects_page)
    with open(os.path.join(site_dir, "contact.html"), "w", encoding="utf-8") as f:
        f.write(contact_page)
    with open(os.path.join(site_dir, "style.css"), "w", encoding="utf-8") as f:
        f.write(css_text)

    return os.path.abspath(os.path.join(site_dir, "index.html"))
