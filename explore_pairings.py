
import pandas as pd

# Load the current 2026-27 NHL season
url = "lines_2026_27.csv"

# Read the CSV into Python
data = pd.read_csv(url)

# Check how many rows and columns are in the dataset
print("Dataset dimensions:")
print(data.shape)

# Examine the available columns
print("First 15 column names:")
print(data.columns[:15].tolist())


# Filter the dataset to Pittsburgh Penguins defensive pairings
penguins = data[
    (data["team"] == "PIT") &
    (data["position"] == "pairing") &
    (data["situation"] == "5on5")
].copy()

# Convert ice time from seconds to minutes
penguins["TOI_minutes"] = penguins["icetime"] / 60

# Sort pairings by total ice time together
penguins = penguins.sort_values(
    by="TOI_minutes",
    ascending=False
)

# Display the number of Pittsburgh defensive pairings
print("\nTotal Penguins defensive pairings:")
print(len(penguins))

# Display the ten most-used defensive pairings
print("\nTop 10 Penguins defensive pairings:")
print(penguins[["name", "games_played", "TOI_minutes"]].head(10).to_string(index=False))

# Calculate expected goals per 60 minutes for Penguins defensive pairings

# Remove any pairings with zero ice time
penguins = penguins[penguins["icetime"] > 0].copy()

# Calculate expected goals for per 60 minutes
penguins["xGF60"] = (
    penguins["xGoalsFor"] / penguins["icetime"]
) * 3600

# Calculate expected goals against per 60 minutes
penguins["xGA60"] = (
    penguins["xGoalsAgainst"] / penguins["icetime"]
) * 3600

# Calculate expected goal differential per 60 minutes
penguins["xGD60"] = penguins["xGF60"] - penguins["xGA60"]

# Display the 10 most-used Penguins defensive pairings
print("\nPenguins Defensive Pairing Performance:")

print(
    penguins[
        ["name", "TOI_minutes", "xGF60", "xGA60", "xGD60"]
    ].head(10).round(2).to_string(index=False)
)

# STEP 6: Adjust defensive pairing performance for sample size

# Use 10 games at 12 minutes of shared ice time per game
prior_minutes = 120

# Calculate the reliability weight for each defensive pairing
penguins["reliability_weight"] = (
    penguins["TOI_minutes"] /
    (penguins["TOI_minutes"] + prior_minutes)
)

# Adjust xGD/60 toward a neutral baseline of 0.00
penguins["adjusted_xGD60"] = (
    penguins["xGD60"] * penguins["reliability_weight"]
)

# Rank defensive pairings by their adjusted xGD/60
adjusted_rankings = penguins.sort_values(
    by="adjusted_xGD60",
    ascending=False
)

# Display the sample-adjusted defensive pairing rankings
print("\nPenguins Sample-Adjusted Defensive Pairing Rankings:")

print(
    adjusted_rankings[
        ["name", "TOI_minutes", "xGD60", "reliability_weight", "adjusted_xGD60"]
    ].round(2).to_string(index=False)
)

# STEP 7: Compare raw and adjusted defensive pairing rankings

# Rank pairings based on their original xGD/60
penguins["raw_rank"] = penguins["xGD60"].rank(
    ascending=False,
    method="min"
).astype(int)

# Rank pairings based on their adjusted xGD/60
penguins["adjusted_rank"] = penguins["adjusted_xGD60"].rank(
    ascending=False,
    method="min"
).astype(int)

# Calculate how many ranking positions each pairing gained or lost
penguins["rank_change"] = (
    penguins["raw_rank"] - penguins["adjusted_rank"]
)

# Create our final comparison table
results = penguins[
    [
        "name",
        "TOI_minutes",
        "xGD60",
        "adjusted_xGD60",
        "raw_rank",
        "adjusted_rank",
        "rank_change"
    ]
].sort_values(by="adjusted_rank")

# Display the results
print("\nPenguins Defensive Pairing Ranking Comparison:")
print(results.round(2).to_string(index=False))

# Save the rankings to a new CSV file
results.to_csv(
    "penguins_pairing_rankings_2026_27.csv",
    index=False
)

print("\nRanking comparison saved successfully!")


# STEP 8: Evaluate offensive and defensive performance separately

# Rank offensive performance (higher xGF/60 is better)
penguins["offensive_rank"] = penguins["xGF60"].rank(
    ascending=False,
    method="min"
).astype(int)

# Rank defensive performance (lower xGA/60 is better)
penguins["defensive_rank"] = penguins["xGA60"].rank(
    ascending=True,
    method="min"
).astype(int)

# Create a table comparing offensive and defensive performance
performance = penguins[
    [
        "name",
        "TOI_minutes",
        "xGF60",
        "xGA60",
        "offensive_rank",
        "defensive_rank",
        "adjusted_rank"
    ]
].sort_values(by="adjusted_rank")

# Display the results
print("\nPenguins Offensive and Defensive Pairing Rankings:")
print(performance.round(2).to_string(index=False))


# STEP 9: Import historical NHL defensive pairing data

# Load the 2025-26 MoneyPuck dataset
# Skip the first row because our original CSV contains an extra "lines" header
historical = pd.read_csv("lines.csv", skiprows=1)

# Select NHL defensive pairings at 5-on-5
historical_pairings = historical[
    (historical["position"] == "pairing") &
    (historical["situation"] == "5on5")
].copy()

# Display historical dataset information
print("\n2025-26 Historical Defensive Pairing Dataset:")

print("Seasons:", historical_pairings["season"].unique())

print("Total NHL defensive pairings:", len(historical_pairings))

# Identify Pittsburgh pairings from the historical season
historical_penguins = historical_pairings[
    historical_pairings["team"] == "PIT"
]

print("Pittsburgh defensive pairings:", len(historical_penguins))

# STEP 10: Analyze historical NHL defensive pairing performance

# Remove pairings with zero ice time
historical_pairings = historical_pairings[
    historical_pairings["icetime"] > 0
].copy()

# Convert ice time from seconds into minutes
historical_pairings["TOI_minutes"] = (
    historical_pairings["icetime"] / 60
)

# Calculate expected goals for per 60 minutes
historical_pairings["xGF60"] = (
    historical_pairings["xGoalsFor"] /
    historical_pairings["icetime"]
) * 3600

# Calculate expected goals against per 60 minutes
historical_pairings["xGA60"] = (
    historical_pairings["xGoalsAgainst"] /
    historical_pairings["icetime"]
) * 3600

# Calculate expected goal differential per 60 minutes
historical_pairings["xGD60"] = (
    historical_pairings["xGF60"] -
    historical_pairings["xGA60"]
)

# Identify the 10 most-used NHL defensive pairings
top_historical = historical_pairings.sort_values(
    by="TOI_minutes",
    ascending=False
).head(10)

# Display historical pairing performance
print("\nTop 10 Most-Used NHL Defensive Pairings (2025-26):")

print(
    top_historical[
        ["name", "team", "TOI_minutes", "xGF60", "xGA60", "xGD60"]
    ].round(2).to_string(index=False)
)

import pandas as pd

# STEP 12: Prepare historical game-by-game NHL data

# Load 2025-26 MoneyPuck game data
games = pd.read_csv("2025_Game_Data.csv")

# Keep only defensive pairings at 5-on-5
pairing_games = games[
    (games["position"] == "pairing") &
    (games["situation"] == "5on5")
].copy()

# Convert game dates into Python date format
pairing_games["gameDate"] = pd.to_datetime(
    pairing_games["gameDate"].astype(str),
    format="%Y%m%d"
)

# Sort each pairing's games chronologically
pairing_games = pairing_games.sort_values(
    by=["lineId", "gameDate", "gameId"]
)

# Display dataset information
print("\nHistorical Game-by-Game Dataset:")
print("Total observations:", len(pairing_games))
print("NHL teams:", pairing_games["playerTeam"].nunique())

# Isolate Pittsburgh's defensive pairings
pit_games = pairing_games[
    pairing_games["playerTeam"] == "PIT"
].copy()

print("Penguins pairing-game observations:", len(pit_games))

# Preview the data
print("\nFirst 5 Penguins pairing-game records:")

print(
    pit_games[
        ["name", "gameDate", "icetime", "xGoalsFor", "xGoalsAgainst"]
    ].head(5).to_string(index=False)
)

# STEP 13: Create training and testing datasets

# Keep games with at least 3 minutes of shared 5v5 ice time
qualified_games = pairing_games[
    pairing_games["icetime"] >= 180
].copy()

# Sort games chronologically for each defensive pairing
qualified_games = qualified_games.sort_values(
    by=["playerTeam", "lineId", "gameDate", "gameId"]
)

# Number each pairing's qualifying games chronologically
qualified_games["game_number"] = (
    qualified_games.groupby(["playerTeam", "lineId"]).cumcount() + 1
)

# Count total qualifying games for each pairing
qualified_games["total_games"] = (
    qualified_games.groupby(["playerTeam", "lineId"])["gameId"]
    .transform("size")
)

# Keep pairings with at least 20 qualifying games
eligible_games = qualified_games[
    qualified_games["total_games"] >= 20
].copy()

# First 10 games: training data
training_games = eligible_games[
    eligible_games["game_number"] <= 10
].copy()

# Next 10 games: testing data
testing_games = eligible_games[
    eligible_games["game_number"].between(11, 20)
].copy()

# Display our results
print("\nHistorical Training and Testing Datasets:")

print(
    "Eligible NHL pairings:",
    training_games.groupby(["playerTeam", "lineId"]).ngroups
)

print("Training observations:", len(training_games))
print("Testing observations:", len(testing_games))

# Show eligible Pittsburgh defensive pairings
print("\nEligible Penguins defensive pairings:")

pit_training = training_games[
    training_games["playerTeam"] == "PIT"
]

print(
    (pit_training.groupby("name")["icetime"].sum() / 60)
    .round(2)
    .to_string()
)

# STEP 14: Build and evaluate our first predictive model

# Group the first 10 games for each defensive pairing
train_summary = training_games.groupby(
    ["playerTeam", "lineId"]
).agg(
    name=("name", "first"),
    train_TOI=("icetime", "sum"),
    train_xGF=("xGoalsFor", "sum"),
    train_xGA=("xGoalsAgainst", "sum")
).reset_index()

# Group the next 10 games for each defensive pairing
test_summary = testing_games.groupby(
    ["playerTeam", "lineId"]
).agg(
    test_TOI=("icetime", "sum"),
    test_xGF=("xGoalsFor", "sum"),
    test_xGA=("xGoalsAgainst", "sum")
).reset_index()

# Combine training and testing results
predictions = train_summary.merge(
    test_summary,
    on=["playerTeam", "lineId"],
    validate="one_to_one"
)

# Calculate xGD/60 from the first 10 games
predictions["raw_prediction"] = (
    (predictions["train_xGF"] - predictions["train_xGA"])
    / predictions["train_TOI"] * 3600
)

# Calculate actual xGD/60 from games 11-20
predictions["actual_xGD60"] = (
    (predictions["test_xGF"] - predictions["test_xGA"])
    / predictions["test_TOI"] * 3600
)

# Apply our 120-minute reliability adjustment
prior_minutes = 120

predictions["reliability_weight"] = (
    (predictions["train_TOI"] / 60) /
    ((predictions["train_TOI"] / 60) + prior_minutes)
)

predictions["adjusted_prediction"] = (
    predictions["raw_prediction"] *
    predictions["reliability_weight"]
)

# Measure the absolute prediction errors
predictions["raw_error"] = (
    predictions["raw_prediction"] -
    predictions["actual_xGD60"]
).abs()

predictions["adjusted_error"] = (
    predictions["adjusted_prediction"] -
    predictions["actual_xGD60"]
).abs()

# Calculate Mean Absolute Error (MAE)
raw_MAE = predictions["raw_error"].mean()
adjusted_MAE = predictions["adjusted_error"].mean()
baseline_MAE = predictions["actual_xGD60"].abs().mean()

# Display the results
print("\nSTEP 14: Predictive Model Evaluation")
print("Pairings evaluated:", len(predictions))
print(f"Raw prediction MAE: {raw_MAE:.3f}")
print(f"Adjusted prediction MAE: {adjusted_MAE:.3f}")
print(f"Neutral baseline MAE: {baseline_MAE:.3f}")

# Display predictions for historical Penguins pairings
print("\nPenguins Historical Predictions:")

print(
    predictions[predictions["playerTeam"] == "PIT"][
        ["name", "raw_prediction", "adjusted_prediction",
         "actual_xGD60"]
    ].round(2).to_string(index=False)
)

# STEP 15: Evaluate how consistently our model improves predictions

# Calculate the neutral baseline prediction error for each pairing
predictions["neutral_error"] = (
    predictions["actual_xGD60"].abs()
)

# Check whether adjusted predictions outperform raw predictions
predictions["beats_raw"] = (
    predictions["adjusted_error"] < predictions["raw_error"]
)

# Check whether adjusted predictions outperform the neutral baseline
predictions["beats_neutral"] = (
    predictions["adjusted_error"] < predictions["neutral_error"]
)

# Count the number of pairings where adjusted predictions perform better
better_than_raw = predictions["beats_raw"].sum()
better_than_neutral = predictions["beats_neutral"].sum()

# Calculate the percentage of pairings where our model performs better
total_pairings = len(predictions)

print("\nSTEP 15: Model Performance Analysis")

print("Total pairings:", total_pairings)

print(
    "Adjusted model beats raw:",
    better_than_raw,
    f"({better_than_raw / total_pairings * 100:.1f}%)"
)

print(
    "Adjusted model beats neutral:",
    better_than_neutral,
    f"({better_than_neutral / total_pairings * 100:.1f}%)"
)

# STEP 16: Evaluate prediction accuracy based on shared ice time

# Convert training ice time from seconds into minutes
predictions["train_TOI_minutes"] = (
    predictions["train_TOI"] / 60
)

# Divide defensive pairings into three ice-time categories
predictions["TOI_group"] = pd.cut(
    predictions["train_TOI_minutes"],
    bins=[0, 60, 120, float("inf")],
    labels=["0-60 min", "60-120 min", "Over 120 min"],
    include_lowest=True
)

# Compare prediction accuracy for each category
toi_analysis = predictions.groupby(
    "TOI_group",
    observed=True
).agg(
    pairings=("name", "count"),
    raw_MAE=("raw_error", "mean"),
    adjusted_MAE=("adjusted_error", "mean"),
    neutral_MAE=("neutral_error", "mean"),
    adjusted_win_rate=("beats_neutral", "mean")
)

# Convert the win rate into a percentage
toi_analysis["adjusted_win_rate"] *= 100

# Display the results
print("\nSTEP 16: Prediction Accuracy by Ice Time")

print(toi_analysis.round(2).to_string())

# STEP 17: Test the relationship between past and future performance

# Calculate correlation between the first 10 and next 10 games
overall_correlation = predictions["raw_prediction"].corr(
    predictions["actual_xGD60"]
)

print("\nSTEP 17: Historical Performance Correlation")

print(f"Overall NHL correlation: {overall_correlation:.3f}")

# Calculate correlation for each shared ice-time category
print("\nCorrelation by Shared Ice Time:")

for group_name, group_data in predictions.groupby(
    "TOI_group",
    observed=True
):

    correlation = group_data["raw_prediction"].corr(
        group_data["actual_xGD60"]
    )

    print(f"{group_name}: {correlation:.3f}")


# STEP 18: Export historical prediction results

# Select the statistics we want to save
model_results = predictions[
    [
        "playerTeam",
        "name",
        "train_TOI_minutes",
        "raw_prediction",
        "adjusted_prediction",
        "actual_xGD60",
        "raw_error",
        "adjusted_error",
        "neutral_error",
        "TOI_group"
    ]
].copy()

# Save the historical results to a CSV file
model_results.to_csv(
    "historical_pairing_predictions_2025_26.csv",
    index=False
)

print("\nSTEP 18: Historical Predictions Exported Successfully!")
print("Total pairings saved:", len(model_results))

# Visualizations Color Pallet

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# STEP 19: Pittsburgh Penguins Defensive Pairing Visualizations

# Pittsburgh Penguins color palette
PENS_GOLD = "#FFB81C"
PENS_BLACK = "#101820"
PENS_CREAM = "#DDCBA4"
PENS08_BLUE = "#69B3E7"
PENS11_NAVY = "#041E42"

# Create a folder to store our visualizations
output_folder = Path("visualizations")
output_folder.mkdir(exist_ok=True)

# Load our current-season and historical model results
penguins = pd.read_csv(
    "penguins_pairing_rankings_2026_27.csv"
)

historical = pd.read_csv(
    "historical_pairing_predictions_2025_26.csv"
)

# Use consistent formatting across all three graphs
plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 15,
    "axes.titleweight": "bold",
    "axes.labelcolor": PENS_BLACK,
    "text.color": PENS_BLACK,
    "xtick.color": PENS_BLACK,
    "ytick.color": PENS_BLACK,
    "figure.facecolor": "white",
    "axes.facecolor": "white"
})


# GRAPH 1: Penguins Sample-Adjusted Defensive Pairing Rankings

# Select the 10 pairings with the most shared ice time
top_pairings = penguins.nlargest(
    10, "TOI_minutes"
).copy()

# Sort the selected pairings by adjusted xGD/60
top_pairings = top_pairings.sort_values(
    "adjusted_xGD60"
)

fig, ax = plt.subplots(figsize=(12, 7))

# Gold indicates positive performance; navy indicates negative
colors = [
    PENS_GOLD if value >= 0 else PENS11_NAVY
    for value in top_pairings["adjusted_xGD60"]
]

bars = ax.barh(
    top_pairings["name"],
    top_pairings["adjusted_xGD60"],
    color=colors
)

# Add a reference line at zero
ax.axvline(
    0,
    color=PENS_BLACK,
    linewidth=1
)

# Add numerical values beside each bar
for bar, value in zip(
    bars, top_pairings["adjusted_xGD60"]
):
    ax.annotate(
        f"{value:+.2f}",
        xy=(value, bar.get_y() + bar.get_height() / 2),
        xytext=(6 if value >= 0 else -6, 0),
        textcoords="offset points",
        ha="left" if value >= 0 else "right",
        va="center",
        fontsize=10,
        color=PENS_BLACK
    )

# Leave room for the value labels
values = top_pairings["adjusted_xGD60"]
padding = max(values.abs().max() * 0.30, 0.15)

ax.set_xlim(
    min(0, values.min()) - padding,
    max(0, values.max()) + padding
)

ax.set_title(
    "Pittsburgh Penguins Defensive Pairing Rankings | 2026-27",
    pad=18
)

ax.set_xlabel("Sample-Adjusted xGD/60")
ax.set_ylabel("Defensive Pairing")

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.20
)

ax.set_axisbelow(True)

fig.tight_layout()

fig.savefig(
    output_folder / "penguins_adjusted_rankings.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# GRAPH 2: Raw vs. Sample-Adjusted Performance

fig, ax = plt.subplots(figsize=(9, 7))

# Use Penguins 2008 Winter Classic baby blue
ax.scatter(
    penguins["xGD60"],
    penguins["adjusted_xGD60"],
    s=85,
    color=PENS08_BLUE,
    edgecolors=PENS11_NAVY,
    linewidths=1,
    alpha=0.90
)

# Add reference lines at zero
ax.axhline(
    0,
    color=PENS11_NAVY,
    linestyle="--",
    linewidth=1,
    alpha=0.6
)

ax.axvline(
    0,
    color=PENS11_NAVY,
    linestyle="--",
    linewidth=1,
    alpha=0.6
)

# Add a diagonal reference showing where raw = adjusted
low = min(
    penguins["xGD60"].min(),
    penguins["adjusted_xGD60"].min()
)

high = max(
    penguins["xGD60"].max(),
    penguins["adjusted_xGD60"].max()
)

ax.plot(
    [low, high],
    [low, high],
    linestyle=":",
    color=PENS_CREAM,
    linewidth=2,
    label="Raw = Adjusted"
)

ax.set_title(
    "Raw vs. Adjusted Defensive Pairing Performance",
    pad=18
)

ax.set_xlabel("Raw xGD/60")
ax.set_ylabel("Sample-Adjusted xGD/60")

ax.legend(frameon=False)

ax.grid(
    linestyle="--",
    alpha=0.15
)

fig.tight_layout()

fig.savefig(
    output_folder / "raw_vs_adjusted.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# GRAPH 3: Historical Predictive Model Accuracy

# Calculate the Mean Absolute Error for all three methods
raw_mae = historical["raw_error"].mean()
adjusted_mae = historical["adjusted_error"].mean()
neutral_mae = historical["neutral_error"].mean()

models = [
    "Raw Performance",
    "120-Min Adjusted",
    "Neutral Baseline"
]

mae_values = [
    raw_mae,
    adjusted_mae,
    neutral_mae
]

fig, ax = plt.subplots(figsize=(10, 7))

# Use cream, gold, and navy for model comparisons
bars = ax.bar(
    models,
    mae_values,
    color=[
        PENS_CREAM,
        PENS_GOLD,
        PENS11_NAVY
    ],
    edgecolor=PENS_BLACK,
    linewidth=0.8,
    width=0.60
)

# Display MAE above each bar
for bar, value in zip(bars, mae_values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.02,
        f"{value:.3f}",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
        color=PENS_BLACK
    )

ax.set_title(
    "Historical Predictive Accuracy | 2025-26 NHL",
    pad=18
)

ax.set_ylabel("Mean Absolute Error (Lower Is Better)")

ax.set_ylim(
    0,
    max(mae_values) * 1.25
)

ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.20
)

ax.set_axisbelow(True)

fig.tight_layout()

fig.savefig(
    output_folder / "historical_model_accuracy.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# FINAL: Confirm that our graphs were successfully created

print("\nSTEP 19: Visualizations Created Successfully!")

print("1. Penguins adjusted rankings chart saved")
print("2. Raw vs. adjusted performance chart saved")
print("3. Historical predictive accuracy chart saved")

print("\nHistorical Model Performance:")
print(f"Raw MAE: {raw_mae:.3f}")
print(f"Adjusted MAE: {adjusted_mae:.3f}")
print(f"Neutral Baseline MAE: {neutral_mae:.3f}")

print("\nAll three graphs are saved in the visualizations folder.")

