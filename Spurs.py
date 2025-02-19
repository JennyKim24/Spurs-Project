#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 08:47:19 2024

@author: jennykim
"""


import sqlite3
import pandas as pd
import random

# Connect to the SQLite database (replace 'nba.db' with your database file path)
conn = sqlite3.connect('nba.db')
cursor = conn.cursor()

# Question 1: SQL Query to Retrieve Player Statistics
try:
    query = """
    SELECT 
        p.PlayerId,
        p.FirstName || ' ' || p.LastName AS FullName,
        COUNT(s.ShotId) AS TotalShotsTaken,
        SUM(CASE WHEN s.Footwork IS NOT NULL THEN 1 ELSE 0 END) AS ShotsWithFootwork,
        SUM(CASE WHEN s.Footwork = 'Pivot' THEN 1 ELSE 0 END) AS PivotFootworkShots,
        SUM(CASE WHEN s.Footwork = 'Hop' THEN 1 ELSE 0 END) AS HopFootworkShots,
        SUM(CASE WHEN s.Footwork = 'Hop' THEN 1 ELSE 0 END) AS WalkInShots,
        ROUND(100.0 * SUM(CASE WHEN s.Footwork IS NOT NULL THEN 1 ELSE 0 END) / COUNT(s.ShotId), 2) AS PercentShotsWithFootwork,
        ROUND(100.0 * SUM(CASE WHEN s.Footwork = 'Pivot' THEN 1 ELSE 0 END) / COUNT(s.ShotId), 2) AS PercentPivotFootworkShots,
        ROUND(100.0 * SUM(CASE WHEN s.Footwork = 'Hop' THEN 1 ELSE 0 END) / COUNT(s.ShotId), 2) AS PercentHopFootworkShots
    FROM 
        nba_Players p
    LEFT JOIN 
        nba_Shot s
    ON 
        p.PlayerId = s.ShooterId
    WHERE 
        s.Season = 2025 -- Replace with the relevant season
    GROUP BY 
        p.PlayerId
    """
    # Execute the query
    player_stats_df = pd.read_sql_query(query, conn)

    # Display the results
    print("Player Statistics:")
    print(player_stats_df)

    # Save the results to a CSV
    player_stats_df.to_csv('player_shot_stats.csv', index=False)
except Exception as e:
    print(f"Error in Question 1: {e}")

# Question 2: NBA Lottery Simulation
def nba_lottery_simulation():
    # Teams participating in the lottery
    teams = {
        "Team1": 140, "Team2": 140, "Team3": 140, "Team4": 125, "Team5": 105,
        "Team6": 90, "Team7": 75, "Team8": 60, "Team9": 45, "Team10": 30,
        "Team11": 20, "Team12": 15, "Team13": 10, "Team14": 5
    }

    # Generate lottery combinations
    lottery_pool = [team for team, combinations in teams.items() for _ in range(combinations)]
    random.shuffle(lottery_pool)

    # Draw the first 4 picks
    winners = []
    while len(winners) < 4:
        pick = random.choice(lottery_pool)
        if pick not in winners:
            winners.append(pick)

    # Assign the remaining teams based on record
    remaining_teams = [team for team in teams.keys() if team not in winners]
    winners.extend(remaining_teams)

    return winners

# Simulate the lottery
lottery_results = nba_lottery_simulation()
print("\nNBA Lottery Results:")
for pick, team in enumerate(lottery_results, start=1):
    print(f"Pick {pick}: {team}")

# Question 3
def gm_plan_for_spurs():
    plan = """
    General Manager Plan for the San Antonio Spurs:

    1. **Strengths**:
        - Victor Wembanyama's generational talent as a versatile big man who can dominate offensively and defensively.
        - A young core with high potential, including Devin Vassell, Keldon Johnson, Jeremy Sochan, Julian Champagne.
        - Strong coaching staff led by Gregg Popovich, with a history of player development and success.

    2. **Weaknesses**:
        - Lack of veteran leadership to guide the rookies during critical moments.
        - Inconsistent three-point shooting and perimeter defense.
        

    3. **Plan for the 24-25 Season**:
        - **Trade or Free Agency**:
            - Pursue a veteran point guard (e.g., Derrick White, Giannis Antetokounmpo, Anthony Edwards-type player) to provide elite floor spacing and improve shot creation.
            - Sign a consistent three-point shooter to space the floor for Wembanyama and others.
            - Stephan Castle has a lot of potential, develop him as a point guard. 
            - Need good rotational players
        
        - **Draft Strategy**:
            - Focus on acquiring a dynamic wing player who can defend multiple positions and contribute offensively.
        
        - **Player Development**:
            - Develop Jeremy Sochan as a secondary playmaker to complement Wembanyama.
            - Work on improving Wembanyama's physicality to handle NBA-level centers.
        
        - **Rotation Optimization**:
            - Build lineups that maximize Wembanyama’s versatility, pairing him with stretch forwards and defensive wings.
            - Utilize analytics to manage player minutes and reduce the risk of injuries.

        - **Long-Term Goals**:
            - Develop the young core into a playoff-contending team over the next two years.
            - Leverage cap flexibility to sign another star player to pair with Wembanyama during his prime.
    """
    return plan

# Print the Spurs GM plan
print("\nGM Plan for the San Antonio Spurs:")
print(gm_plan_for_spurs())


# Close the database connection
conn.close()

