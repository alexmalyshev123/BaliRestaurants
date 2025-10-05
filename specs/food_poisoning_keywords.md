# Food Poisoning Detection Keywords & Patterns
# Version 1.0

**Purpose:** Define the keywords and regex patterns used to detect food poisoning mentions in restaurant reviews.

**Last Updated:** October 5, 2025

---

## Table of Contents
1. [Overview](#overview)
2. [Direct Mentions](#direct-mentions)
3. [Illness Symptoms](#illness-symptoms)
4. [Safety & Hygiene Concerns](#safety--hygiene-concerns)
5. [Regex Patterns](#regex-patterns)
6. [Implementation](#implementation)
7. [Testing Examples](#testing-examples)
8. [Edge Cases](#edge-cases)
9. [False Positives](#false-positives)

---

## Overview

### Detection Strategy
- **Case-insensitive** matching (matches "Food Poisoning", "food poisoning", "FOOD POISONING")
- **Word boundary** detection to avoid false matches (e.g., don't match "miss" when looking for "sick")
- **Multiple variations** of the same concept

### Confidence Levels

**High Confidence (Explicit Mentions):**
- "food poisoning"
- "food borne illness"
- "got sick from the food"

**Medium Confidence (Strong Symptoms):**
- "vomiting"
- "diarrhea"
- "severe stomach pain"

**Lower Confidence (Mild Symptoms):**
- "upset stomach"
- "didn't feel well"
- "stomach felt off"

For V1, we'll flag **all confidence levels** and let users judge severity from context.

---

## Direct Mentions

### Primary Keywords

These are explicit mentions of food poisoning:

```
food poisoning
food poison
got food poisoned
food poisoned
foodborne illness
food borne illness
food-borne illness
food safety issue
food safety concern
food contamination
contaminated food
```

### Regex Pattern (Direct Mentions)
```regex
\b(food\s*(poison(ing|ed)?|borne|safety|contamination))\b
\bcontaminated\s*food\b
```

---

## Illness Symptoms

### Category 1: Getting Sick

Reviews mentioning becoming ill after eating:

```
got sick
became sick
got ill
became ill
gotten sick
gotten ill
made me sick
made us sick
made me ill
made us ill
feeling sick
felt sick
felt ill
feeling unwell
felt unwell
```

### Regex Pattern (Getting Sick)
```regex
\b(got|became|gotten|made\s+(me|us)|feeling|felt)\s+(sick|ill|unwell)\b
```

---

### Category 2: Gastrointestinal Symptoms

Common symptoms of food poisoning:

**Stomach Issues:**
```
stomach ache
stomach pain
stomach cramps
stomach issue
stomach problems
upset stomach
bad stomach
severe stomach pain
terrible stomach pain
```

**Nausea:**
```
nausea
nauseous
nauseated
feeling nauseous
felt nauseous
feel nauseous
```

**Vomiting:**
```
vomit
vomiting
vomited
threw up
throw up
throwing up
puking
puked
```

**Diarrhea:**
```
diarrhea
diarrhoea
diarrhœa
had diarrhea
got diarrhea
terrible diarrhea
severe diarrhea
```

### Regex Patterns (Gastrointestinal)

**Stomach:**
```regex
\bstomach\s*(ache|pain|cramps?|issue|problems?)\b
\b(upset|bad|terrible|severe)\s*stomach\b
```

**Nausea:**
```regex
\bnause(a|ous|ated)\b
\b(feeling|felt|feel)\s*nauseous\b
```

**Vomiting:**
```regex
\b(vomit(ing|ed)?|threw\s*up|throw(ing)?\s*up|puk(e|ed|ing))\b
```

**Diarrhea:**
```regex
\b(diarrh[oeœ]a)\b
\b(had|got|terrible|severe)\s*diarrh[oeœ]a\b
```

---

### Category 3: Duration & Severity

Phrases indicating serious illness:

```
sick for days
sick for a week
sick all night
up all night
couldn't sleep
bedridden
hospital
emergency room
ER visit
doctor
medical attention
antibiotics
```

### Regex Pattern (Duration/Severity)
```regex
\bsick\s*for\s*(days|hours|a\s*week)\b
\b(hospital|emergency|doctor|medical\s*attention)\b
\bbedridden\b
```

---

## Safety & Hygiene Concerns

### Food Hygiene Issues

Mentions that suggest food safety problems:

```
food safety
food hygiene
hygiene issue
hygiene problem
dirty kitchen
unclean
unsanitary
not fresh
spoiled food
rotten food
undercooked
raw chicken
raw meat
smelled bad
smelled off
tasted bad
tasted off
tasted weird
```

### Regex Pattern (Hygiene)
```regex
\b(food\s*(safety|hygiene)|hygiene\s*(issue|problem))\b
\b(dirty|unclean|unsanitary)\b
\b(spoiled|rotten)\s*food\b
\b(undercooked|raw)\s*(chicken|meat|seafood|fish)\b
\b(smelled|tasted)\s*(bad|off|weird|funny)\b
```

---

## Regex Patterns

### Complete Pattern List for Implementation

```python
FOOD_POISONING_KEYWORDS = [
    # Direct mentions
    r'\bfood\s*poison(ing|ed)?\b',
    r'\bfood\s*borne\s*(illness|disease)\b',
    r'\bcontaminated\s*food\b',
    r'\bfood\s*safety\s*(issue|concern|problem)\b',

    # Getting sick
    r'\b(got|became|gotten)\s+(sick|ill)\b',
    r'\bmade\s+(me|us|them)\s+(sick|ill)\b',
    r'\b(feeling|felt|feel)\s+(sick|ill|unwell)\b',

    # Stomach issues
    r'\bstomach\s*(ache|pain|cramps?|issue|problems?)\b',
    r'\b(upset|bad|terrible|severe)\s*stomach\b',

    # Nausea
    r'\bnause(a|ous|ated)\b',
    r'\b(feeling|felt|feel)\s*nauseous\b',

    # Vomiting
    r'\b(vomit(ing|ed)?|threw\s*up|throw(ing)?\s*up|puk(e|ed|ing))\b',

    # Diarrhea (multiple spellings)
    r'\bdiarrh[oeœ]a\b',

    # Duration/Severity
    r'\bsick\s*for\s*(days|hours|a\s*week)\b',
    r'\b(hospital|emergency\s*room|ER|doctor)\b',
    r'\bmedical\s*attention\b',

    # Hygiene concerns
    r'\b(dirty|unclean|unsanitary)\s*(kitchen|restaurant|food)?\b',
    r'\b(spoiled|rotten|bad)\s*food\b',
    r'\b(undercooked|raw)\s*(chicken|meat|seafood|fish|egg)\b',
    r'\b(smelled|tasted)\s*(bad|off|weird|funny|strange)\b',
]
```

### Pattern Options

**Strict Mode** (fewer false positives):
- Only match explicit phrases
- Require word boundaries
- More specific patterns

**Lenient Mode** (catch more cases):
- Allow partial matches
- Broader patterns
- May have more false positives

**Recommendation for V1:** Start with strict mode, adjust based on testing.

---

## Implementation

### Python Implementation

```python
import re

# Keyword patterns (from above)
FOOD_POISONING_KEYWORDS = [
    r'\bfood\s*poison(ing|ed)?\b',
    r'\bfood\s*borne\s*(illness|disease)\b',
    # ... (full list from above)
]

def detect_food_poisoning(review_text: str) -> tuple:
    """
    Detect food poisoning mentions in review text

    Args:
        review_text: The review text to analyze

    Returns:
        tuple: (is_flagged: bool, matched_keywords: list)
    """
    matched_keywords = []

    # Check each pattern
    for pattern in FOOD_POISONING_KEYWORDS:
        # Compile with case-insensitive flag
        regex = re.compile(pattern, re.IGNORECASE)

        # Search for matches
        match = regex.search(review_text)

        if match:
            # Store the actual matched text (not the pattern)
            matched_keywords.append(match.group(0))

    # Flag if any matches found
    is_flagged = len(matched_keywords) > 0

    return is_flagged, matched_keywords

# Example usage:
review = "We got terrible food poisoning after eating here. Had stomach aches for days."
is_flagged, keywords = detect_food_poisoning(review)

print(f"Flagged: {is_flagged}")  # True
print(f"Matched: {keywords}")    # ['food poisoning', 'stomach aches']
```

---

## Testing Examples

### Should Flag (True Positives)

**Example 1: Direct Mention**
```
Review: "We got food poisoning after eating here."
Expected: ✅ Flagged
Keywords: ["food poisoning"]
```

**Example 2: Multiple Symptoms**
```
Review: "Had terrible stomach pain and vomiting all night."
Expected: ✅ Flagged
Keywords: ["stomach pain", "vomiting"]
```

**Example 3: Getting Sick**
```
Review: "Made me sick. Never going back."
Expected: ✅ Flagged
Keywords: ["made me sick"]
```

**Example 4: Hygiene Issue**
```
Review: "The chicken was undercooked and tasted off."
Expected: ✅ Flagged
Keywords: ["undercooked chicken", "tasted off"]
```

**Example 5: Duration Mentioned**
```
Review: "Got ill and was sick for days after eating here."
Expected: ✅ Flagged
Keywords: ["got ill", "sick for days"]
```

---

### Should NOT Flag (True Negatives)

**Example 1: Positive Review**
```
Review: "Amazing food! Best restaurant in Bali."
Expected: ❌ Not Flagged
Keywords: []
```

**Example 2: Service Complaint (No Health Issue)**
```
Review: "Service was slow and staff were rude."
Expected: ❌ Not Flagged
Keywords: []
```

**Example 3: Price Complaint**
```
Review: "Too expensive for what you get."
Expected: ❌ Not Flagged
Keywords: []
```

**Example 4: Ambiance Issue**
```
Review: "Restaurant was too loud and crowded."
Expected: ❌ Not Flagged
Keywords: []
```

---

## Edge Cases

### Borderline Cases to Consider

**Case 1: "Sick" in Different Context**
```
Review: "I'm sick of paying these prices!"
Current Behavior: May flag "sick"
Recommendation: Keep simple for V1, accept some false positives
```

**Case 2: Past Issues Resolved**
```
Review: "Had food poisoning here 5 years ago, but returned recently and it was great!"
Current Behavior: Will flag
Recommendation: Flag it - user can read full context
```

**Case 3: Second-Hand Information**
```
Review: "My friend got sick here last year, but I was fine."
Current Behavior: Will flag
Recommendation: Flag it - still valuable information
```

**Case 4: Hypothetical**
```
Review: "Could cause food poisoning if not careful."
Current Behavior: Will flag
Recommendation: Flag it - indicates concern
```

**Case 5: Negative of a Negative**
```
Review: "No food poisoning concerns, everything was fresh!"
Current Behavior: Will flag "food poisoning"
Recommendation: Accept for V1, improve in V2 with sentiment analysis
```

---

## False Positives

### Known False Positive Scenarios

**1. Idiomatic Expressions**
```
"Sick of waiting" → May flag "sick"
"Killing it with these flavors" → Won't flag (no keywords)
"To die for!" → Won't flag
```

**2. Compliments with Keywords**
```
"So good it made me sick (in a good way)!" → May flag "made me sick"
```

**3. Context is Positive**
```
"No food safety issues at all" → May flag "food safety"
```

**Mitigation Strategy for V1:**
- Accept some false positives
- Users will read full reviews and judge context
- Future versions can add sentiment analysis

### Acceptable False Positive Rate

**Target:** < 20% false positive rate

**Definition:** Less than 20% of flagged reviews are actually positive/neutral when read in context.

---

## Customization & Tuning

### Adding New Keywords

To add new keywords based on testing:

```python
# Add to the list:
FOOD_POISONING_KEYWORDS.append(r'\bnew_keyword_pattern\b')
```

### Removing Too Broad Keywords

If a pattern causes too many false positives:

```python
# Remove or comment out:
# r'\bproblematic_pattern\b',  # Too many false positives
```

### Regional Variations

Consider local terms used in Bali/Indonesia:

```
"Bali belly"        # Common term for traveler's diarrhea in Bali
"traveler's diarrhea"
"Montezuma's revenge"
```

Add these:
```python
r'\b(bali\s*belly|travelers?\s*diarrh[oeœ]a)\b',
```

---

## Keyword Categories Summary

### Final Keyword Count

**Category Breakdown:**
- Direct mentions: ~10 patterns
- Getting sick: ~8 patterns
- Gastrointestinal: ~15 patterns
- Duration/Severity: ~5 patterns
- Hygiene concerns: ~10 patterns

**Total:** ~48 regex patterns

---

## Future Enhancements

### V2 Improvements

**1. Sentiment Analysis**
- Determine if mention is positive or negative
- Filter out "No food poisoning" mentions

**2. Context Understanding**
- Use NLP to understand surrounding context
- Differentiate between "got sick" (illness) vs "sick of waiting" (idiom)

**3. Severity Scoring**
- Assign confidence scores to matches
- Prioritize high-confidence matches

**4. Machine Learning**
- Train model on labeled data
- Automatically detect new patterns

**5. Multi-language Support**
- Translate reviews to English
- Support Indonesian keywords

---

## Testing Checklist

Before deploying detection engine:

- [ ] Test all patterns individually
- [ ] Test on real restaurant reviews
- [ ] Verify case-insensitivity works
- [ ] Check word boundary matching
- [ ] Test with known positive cases
- [ ] Test with known negative cases
- [ ] Measure false positive rate
- [ ] Review borderline cases
- [ ] Test all spelling variations
- [ ] Validate regex syntax

---

## Usage Example

### Complete Detection Flow

```python
# 1. Load keywords
from keywords import FOOD_POISONING_KEYWORDS

# 2. Fetch reviews
reviews = [
    {"author": "John", "text": "Got food poisoning here!"},
    {"author": "Jane", "text": "Amazing food, loved it!"},
    {"author": "Bob", "text": "Made me sick, terrible stomach ache"},
]

# 3. Detect in each review
flagged_reviews = []

for review in reviews:
    is_flagged, matched = detect_food_poisoning(review['text'])

    if is_flagged:
        review['matched_keywords'] = matched
        flagged_reviews.append(review)

# 4. Results
print(f"Found {len(flagged_reviews)} flagged reviews:")
for review in flagged_reviews:
    print(f"- {review['author']}: {review['matched_keywords']}")

# Output:
# Found 2 flagged reviews:
# - John: ['food poisoning']
# - Bob: ['made me sick', 'stomach ache']
```

---

## References

### Medical Terms
- Food-borne illness symptoms (CDC)
- Common food poisoning symptoms
- Gastrointestinal distress indicators

### Review Analysis
- Common phrases in negative restaurant reviews
- Hospitality industry complaint patterns

---

**Document End**

**Note:** This keyword list should be treated as a living document. Update based on:
- Real-world testing results
- User feedback
- New patterns discovered
- False positive/negative analysis
