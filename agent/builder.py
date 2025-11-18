import os

def build_portfolio_website(industry, style, goals, project_info="", output_dir="/tmp"):
    html = f"""
    <html>
    <head>
        <title>{industry} Portfolio</title>
        <style>
            body {{
                font-family: Arial;
                margin: 40px;
            }}
        </style>
    </head>
    <body>
        <h1>{industry} Portfolio</h1>
        <p><strong>Style:</strong> {style}</p>
        <p><strong>Goals:</strong> {goals}</p>
        <p><strong>Competitor Insights:</strong> {project_info}</p>
    </body>
    </html>
    """

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "index.html")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    return path
