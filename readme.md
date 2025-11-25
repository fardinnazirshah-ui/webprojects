# JEE College Predictor

A web-based tool to estimate your engineering college admission chances by the JEE(Joint Entrance Examination)
---

## Table of Contents
- [Overview](# Overview)
- [Why I Built It](#Why-I-built-it)
- [Design & Vibe](#design-and-vibe)
- [How It Works](#how-it-works)
  - [Database & Schema](#database-schema)
  - [Cutoff Generation](#cutoff-generation)
  - [Prediction Logic](#prediction-logic)
- [Frontend & Experience](#frontend-experience)
- [Future Ideas](#future-ideas)

---

## Overview
The **JEE College Predictor** is a web app that helps you figure out your chances of getting into engineering colleges based on your JEE rank, exam type and reservation category.
I built it using Flask and SQLite, implementing html and css, using llm and ai based data synthesis and predictions and using python for the main logic.
This became sort of a culmination of my two favorite problem sets in cs50: Fiftyville and Finance as well as hints of David's Froshims code.
Being stuck on Finance problem for more than two weeks taught quite a lot which then helped me extrapolate the same concepts and use them for this project. Initially I tried to create a similar app using real data from josaa which was of no avail as I was unable to scrape the historical data and use the logic in a js script(I am not very uncomfortable with java).

---

## Why I Built It
I’ve been in the shoes of a JEE aspirant: making spreadsheets, combing forums, guessing cutoffs, stressing. I realised a lot of students go through the same worry-cycle. During the CS50 course from Harvard I learned how to build tools that matter. So this project is me combining the student stress I knew with the knowledge I gained.


---

## Design & Vibe
Intentionally simple, functional, and easy on the eyes. Reminds me of the 2010s webpage era.
Although I think that it can be better designed using bootstrap and templates, I love the antique vibe of the design(also I am just not that interested in design and aesthetics as I naturally suck at them)

---

## How It Works

### Database & Schema
- `institutes` table: colleges (IITs, NITs,IIITs, GFTIs) with metadata.
- `branches` table: academic streams (CSE, ECE, ME, etc.) each with a competitiveness multiplier.
- `categories` table: Reservation categories (OPEN, EWS, OBC-NCL, SC, ST) and how they affect rank multipliers.
- `cutoffs` table: The core data linking institute, branch, category, and year to opening & closing ranks.
– Foreign keys and indexes keep everything neat and performant.

### Cutoff Generation(AI-BASED SOLUTION)
Rather than manually scraping and updating every year, the tool uses realistic heuristics to generate synthetic data that *mimics* real cutoff behaviour:
- Each branch gets a competitiveness multiplier (e.g., CSE ~1.0, Mechanical ~2.3)
- Reservation category multipliers simulate quota effects (e.g., ST might be ~4.67× base)
- Year-trends applied (2022 = 1.08, 2023 = 1.04, 2024 = 1.00)
- Institute-tier adjustments (top IITs stricter; GFTIs more relaxed)
- Small stochastic noise (±2–3%) to add realism

This gives the database flexibility and scalability without relying on external APIs or manual updates.

### Prediction Logic
The algorithm is quite straightforward and measures deviation from closing ranks.
The core algorithm works like this:
- If your **rank ≤ opening rank** → 100% probability of admit
- If your rank is **between opening and closing** → probability interpolates linearly (but never less than 50%)
- If your rank is **worse than the closing rank** → probability drops off based on distance from closing

Then, results are shown grouped by (institute, branch) across years, giving you:
- Best-case, average, worst closing rank

---

## Frontend & Experience
- Simple form: input your rank (1–30,000)
 -choose exam type and reservation category
- Tables that display cutoff data clearly
- Error checking and user-friendly messages

---

## Getting Started

### Prerequisites
- Python
- Flask
- SQLite

