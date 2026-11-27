from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

# 1. LOAD DATA in my local environment
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_excel(BASE_DIR / "NFL Stats 2022 Update.xlsx", header=1)
df.columns = df.columns.str.strip()
df = df.dropna(axis=1, how="all")
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
# 2. DEFINE INDICATORS => This part matters the most in the assessment since it shows my analytical understanding based on the scenario's requirenments.
seconds = [
    "40 yard dash (seconds)",
    "20 Yard Shuttle (seconds)",
    "60 Yard Shuttle (seconds)",
    "3 Cone Drill (seconds)"
]

power = [
    "Vertical Jump (inches)",
    "Broad Jump (inches)"
]

strength = ["Bench Press (102 kg) (no. of reps)"]

receiving = [
    "No. of Receives in Prev. Season",
    "Avg. Catch %",
    "Total Receiving Yards*",
    "Receiving Touchdowns**",
    "Yards after Catch p/receive",
    "Expected YAC p/receive"
]

physical = ["Age", "Height (cm)", "Mass (kg)"]
#Make a list based on the groupings above so that I can easily convert the columns to numeric and handle missing values.
all_columns = seconds + power + strength + receiving + physical + ["Player"]

for col in all_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")
#Drop rows with no player information
df = df.dropna(subset=["Player"])
#Choose my player of interest whom I'll have to justify why I've chosen him/her .
player = df[df["Player"] == 18].iloc[0]

# 3. SUMMARY TABLES
def summary_table(columns):
    return (
        df[columns]
        .agg(["mean", "std", "min", "max"])
        .T.round(2)
        .reset_index()
        .rename(columns={"index": "Indicator"})
        .to_html(index=False, classes="data-table", border=0)
    )

# 4. PLAYER VS GROUP AVERAGE
def comparison_chart(columns, title, lower_is_better=False):

    averages = df[columns].mean()
    values = player[columns]

    difference = (
        (averages - values) / averages * 100
        if lower_is_better
        else (values - averages) / averages * 100
    )

    fig = go.Figure(go.Bar(
        x=difference.values,
        y=columns,
        orientation="h",
        marker_color=[
            "#D62828" if v >= 0 else "#8293A5"
            for v in difference.values
        ],
        text=[f"{v:+.1f}%" for v in difference.values],
        textposition="outside"
    ))

    fig.add_vline(x=0, line_color="#172B4D")

    fig.update_layout(
        title=title,
        xaxis_title="% difference compared with group average",
        template="plotly_white",
        height=350,
        margin=dict(l=20, r=60, t=60, b=40)
    )

    return fig.to_html(full_html=False, include_plotlyjs="cdn")

# 5. CORRELATIONS
correlations = (
    df.corr(numeric_only=True)["Total Receiving Yards*"]
    .drop("Total Receiving Yards*", errors="ignore")
    .sort_values(ascending=False)
)

corr_table = correlations.round(3).reset_index()
corr_table.columns = ["Indicator", "Correlation with receiving yards"]
corr_html = corr_table.to_html(index=False, classes="data-table", border=0)

# 6. GENERATE HTML
html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Wide Receiver Scouting Report</title>

<style>
body {{
    font-family: Arial, sans-serif;
    background: #F2F4F7;
    color: #263445;
    margin: 0;
}}
.container {{
    max-width: 1100px;
    margin: auto;
    padding: 25px;
}}
header {{
    background: #172B4D;
    color: white;
    padding: 25px;
    border-radius: 10px;
}}
section {{
    background: white;
    padding: 22px;
    margin-top: 20px;
    border-radius: 10px;
}}
h2 {{ color: #172B4D; }}
h3 {{ color: #D62828; }}
.profile {{
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    background: #EDF2F7;
    padding: 15px;
    border-radius: 8px;
}}
.profile div {{ text-align: center; padding: 10px; }}
.profile strong {{ display: block; font-size: 22px; }}
.data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
}}
.data-table th, .data-table td {{
    padding: 11px;
    border-bottom: 1px solid #ddd;
    text-align: left;
}}
.data-table th {{ background: #EDF2F7; }}
.note {{ color: #65758B; font-size: 13px; }}
</style>
</head>

<body>
<div class="container">
<header>
    <h1>Wide Receiver Scouting Report</h1>
    <p>NFL Combine and Receiving Performance | 2022</p>
</header>
<section>
    <h2>Player Profile</h2>
    <div class="profile">
        <div><strong>18</strong>Player Number</div>
        <div><strong>{player["Age"]}</strong>Age (years)</div>
        <div><strong>{player["Height (cm)"]}</strong>Height (cm)</div>
        <div><strong>{player["Mass (kg)"]}</strong>Mass (kg)</div>
        <div><strong>WR</strong>Position</div>
    </div>
    <p class="note">Club, market value and player image are not available in the dataset.</p>
</section>

<section>
    <h2>1. Speed and Agility</h2>
    <p>Lower completion times indicate better performance.</p>
    {comparison_chart(seconds, "Speed and Agility vs Group Average", True)}
    {summary_table(seconds)}
</section>

<section>
    <h2>2. Explosive Power</h2>
    <p>Jumping performance indicates lower-body explosive ability.</p>
    {comparison_chart(power, "Explosive Power vs Group Average")}
    {summary_table(power)}
</section>

<section>
    <h2>3. Strength</h2>
    {comparison_chart(strength, "Bench Press vs Group Average")}
    {summary_table(strength)}
</section>

<section>
    <h2>4. Receiving Performance</h2>
    <p>On-field indicators of receiving ability and effectiveness.</p>
    {comparison_chart(receiving, "Receiving Performance vs Group Average")}
    {summary_table(receiving)}
</section>

<section>
    <h2>5. Correlation Analysis</h2>
    <p>Relationship between player characteristics and total receiving yards.</p>
    {corr_html}
    <p class="note">
    Correlation indicates association, not causation.
    </p>
</section>

<footer class="note">
    <p>Analysis based on {len(df)} player records. Player 18 is compared
    with the dataset average.</p>
</footer>

</div>
</body>
</html>
"""
# 7. SAVE REPORT
output = BASE_DIR / "match_report.html"
output.write_text(html, encoding="utf-8")

print("Report generated:", output)
