# Scoring Rules

## Overview

The PGL Session Insights pipeline uses OpenAI GPT-3.5-Turbo to automatically score facilitator observations on two key dimensions: **Emotional Regulation** and **Social Integration**. Both use a 1–5 scale.

## Emotional Regulation Score (1–5)

Measures the child's ability to manage emotions, stay calm, and handle frustration.

| Score | Description | Example Indicators |
|-------|-------------|-------------------|
| 1 | **Very Poor** | Frequent outbursts, unable to calm down, gives up easily | Cries uncontrollably, yells at peers, leaves activity |
| 2 | **Poor** | Struggles to control emotions, needs significant adult support | Becomes frustrated quickly, needs reminding to breathe or pause |
| 3 | **Moderate** | Manages emotions with occasional support, recovers within reasonable time | Shows frustration but can refocus with encouragement |
| 4 | **Good** | Usually controls emotions, minor setbacks quickly resolved | Brief frustration after loss, but re-engages independently |
| 5 | **Excellent** | Consistently manages emotions, resilient to setbacks, models calmness | Smiles through challenges, helps others stay calm |

## Social Integration Score (1–5)

Measures the child's ability to interact with peers, share, cooperate, and communicate effectively.

| Score | Description | Example Indicators |
|-------|-------------|-------------------|
| 1 | **Very Poor** | Isolates from group, refuses to cooperate, conflicts with peers | Sits alone, doesn't respond to peers, argues frequently |
| 2 | **Poor** | Minimal interaction, needs adult facilitation to join group | Reluctant to participate, prefers one-on-one interaction |
| 3 | **Moderate** | Participates with prompting, sometimes leads, sometimes withdrawn | Joins group with encouragement, plays well sometimes |
| 4 | **Good** | Actively engages with peers, occasional friction, generally cooperative | Initiates play, shares resources, minor disagreements |
| 5 | **Excellent** | Natural leader, highly cooperative, helps others, resolves conflicts independently | Organizes group activities, supports struggling peers, includes others |

## Resilience Notes Summary

A short (1–2 sentence) descriptive field capturing:
- Observable coping strategies (e.g., "takes breaks when frustrated")
- Resilience indicators (e.g., "bounces back quickly after setbacks")
- Adaptability (e.g., "adjusts behavior when reminded")
- Social strengths (e.g., "helps teammates despite personal frustration")

## How the LLM Interprets Notes

The GPT-3.5-Turbo prompt analyzes facilitator observations by:

1. **Identifying emotional cues** – Language like "frustrated," "smiled," "quiet," "yelled"
2. **Recognizing social behaviors** – "helped peers," "refused to cooperate," "initiated play"
3. **Assessing coping responses** – "rejoined after 5 minutes," "needed reminding," "independent recovery"
4. **Mapping to scale** – Assigning the most appropriate 1–5 score based on behavioral indicators

## Example Interpretations

### Example 1: Social Helper
**Raw Note:** "Child spoke up confidently for the first time in 3 sessions. Helped peers during activity and offered support when another child became frustrated."

**Scoring:**
- Emotional Regulation: **4** (manages others' emotions, stable presence)
- Social Integration: **5** (confident speaking, proactively helps, includes others)
- Resilience Notes: "Breakthrough in confidence and peer support. Demonstrates empathy and emerging leadership."

### Example 2: Frustrated But Resilient
**Raw Note:** "Child got frustrated after losing the game but rejoined after 5 minutes. Apologized to peer."

**Scoring:**
- Emotional Regulation: **3** (shows frustration but recovers independently)
- Social Integration: **3** (re-engages, repairs social connection)
- Resilience Notes: "Self-regulated after setback and demonstrated conflict resolution skills."

### Example 3: Quiet Observer
**Raw Note:** "Child was quiet during group work but smiled when helping peers. Preferred one-on-one interaction."

**Scoring:**
- Emotional Regulation: **3** (calm, stable, no distress)
- Social Integration: **3** (participates selectively, engaged in supportive roles)
- Resilience Notes: "Introverted but engaged; comfortable helping in smaller settings."

## Validation & Fallback

If the LLM cannot parse a note or returns invalid JSON:
- Default score: **3** (Moderate)
- Default summary: "Unable to analyze - returned default values"

Scores are automatically constrained to 1–5 range (no values below 1 or above 5).

## Notes on Reliability

- **Facilitator note quality** significantly impacts scoring accuracy. Clear, specific observations (e.g., "child yelled and threw blocks") yield more precise scores than vague notes (e.g., "seemed upset").
- **Temperature setting** (0.3) ensures consistent scoring for similar observations.
- **Weekly reviews** of sampled scored notes are recommended to validate LLM interpretation against facilitator intent.
