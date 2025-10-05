# Apify API Setup Guide
# Bali Restaurant Food Safety Checker

**Purpose:** Step-by-step instructions to set up Apify API for fetching Google Maps reviews

**Estimated Time:** 10-15 minutes

---

## What is Apify?

**Apify** is a web scraping and automation platform that provides ready-made "Actors" (pre-built scrapers) for various websites. We're using their **Google Maps Reviews Scraper** to fetch restaurant reviews.

**Why Apify?**
- ✅ Gets ALL reviews (not limited to 5 like Google's official API)
- ✅ Accepts full Google Maps URLs directly
- ✅ Supports filtering by date (last 6 months)
- ✅ Generous free tier: $5 in credits/month (~10,000 reviews)

---

## Step 1: Create Apify Account

### 1.1 Sign Up

1. Go to **https://apify.com/**
2. Click **"Sign Up"** or **"Get Started for Free"**
3. Choose sign-up method:
   - Email + Password
   - OR Google account
   - OR GitHub account

4. Verify your email (if using email signup)

### 1.2 Complete Registration

- You'll land in the Apify Console (dashboard)
- No credit card required for free tier
- You get **$5 in free credits** every month (renews monthly)

---

## Step 2: Get Your API Token

### 2.1 Navigate to Settings

1. In the Apify Console, click your profile icon (top right)
2. Select **"Settings"**
3. Click **"Integrations"** in the left sidebar

### 2.2 Copy Your API Token

1. You'll see a section called **"Personal API tokens"**
2. Your default token is already created
3. Click the **"Copy"** button next to the token

**Your API token looks like:** `apify_api_AbCdEfGh1234567890...`

**⚠️ Important:** Keep this token secret! Don't share it or commit it to git.

---

## Step 3: Add API Token to Your Project

### 3.1 Update .env File

1. Navigate to your project directory:
   ```bash
   cd /Users/alm/Documents/BaliRestaurants
   ```

2. Open `.env` file (or create it if it doesn't exist):
   ```bash
   # If file doesn't exist, create it:
   cp .env.example .env

   # Then open it in your editor:
   open .env
   # OR
   nano .env
   ```

3. Add your Apify API token:
   ```
   # Apify API Token
   APIFY_API_KEY=apify_api_YOUR_TOKEN_HERE
   ```

4. Save and close the file

### 3.2 Verify .env is in .gitignore

Make sure `.env` is listed in your `.gitignore` file so you don't accidentally commit your API key:

```bash
# Check if .env is in .gitignore:
grep ".env" .gitignore
```

You should see `.env` listed. If not, add it.

---

## Step 4: Install Apify Python Client

### 4.1 Activate Virtual Environment

```bash
cd /Users/alm/Documents/BaliRestaurants

# Activate virtual environment
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

### 4.2 Install Apify Client

```bash
pip install apify-client==1.6.0
```

**What this does:** Installs the official Apify Python library that makes it easy to interact with Apify API.

### 4.3 Verify Installation

```bash
pip list | grep apify
```

You should see:
```
apify-client    1.6.0
```

---

## Step 5: Test the Connection

### 5.1 Run Test Script

I've created a test script for you. Run it to verify everything works:

```bash
python test_apify.py
```

### 5.2 What to Expect

The script will:
1. Load your API key from `.env`
2. Connect to Apify
3. Fetch reviews from a test restaurant (Naughty Nuri's Warung in Bali)
4. Filter to last 6 months only
5. Limit to 1000 reviews max
6. Display sample results

**Successful output looks like:**
```
🔍 APIFY API TEST SCRIPT
========================

✓ API key loaded: apify_api_...
✓ Connected to Apify

Fetching reviews for test restaurant...
URL: https://www.google.com/maps/place/Naughty+Nuri's...

✓ Successfully fetched reviews
Restaurant: Naughty Nuri's Warung Seminyak
Rating: 4.7/5
Total Reviews: 12,599
Reviews Fetched: 847 (last 6 months)

Sample Review:
--------------
Author: John Doe
Rating: 5 stars
Date: 2 months ago
Text: Amazing ribs! Best in Bali...

✅ Test completed successfully!
```

### 5.3 Troubleshooting

**Error: "API token not found"**
- Make sure you added `APIFY_API_KEY` to your `.env` file
- Make sure you're running from the project directory
- Make sure you activated the virtual environment

**Error: "Authentication failed"**
- Double-check your API token is correct
- Make sure there are no extra spaces in the `.env` file

**Error: "ModuleNotFoundError: No module named 'apify_client'"**
- Make sure you activated the virtual environment (`source venv/bin/activate`)
- Run `pip install apify-client` again

---

## Step 6: Understanding the Costs

### Free Tier

**What you get:**
- **$5 in free credits per month** (renews monthly)
- **~10,000 reviews per month** at $0.35 per 1,000 reviews
- Perfect for testing and light usage

**With our 1000 review cap:**
- Can check **~10 restaurants per month** for free (at 1000 reviews each)
- OR **~50 restaurants per month** for free (at ~200 reviews average)

### Pricing After Free Tier

**Pay-as-you-go:**
- **$0.35 per 1,000 reviews**
- No monthly minimum
- Only pay for what you use

**Examples:**
- 50,000 reviews/month: ~$17.50
- 100,000 reviews/month: ~$35
- 200,000 reviews/month: ~$70

### Checking Your Usage

1. Go to **Apify Console** → **Billing**
2. View your credit balance
3. See detailed usage breakdown

---

## Step 7: Next Steps

Once the test passes, you're ready to:

✅ **Build the URL validator** - Simple check for Google Maps URLs
✅ **Create the detection engine** - Scan reviews for food poisoning keywords
✅ **Build the dashboard** - Display results in Streamlit

---

## Quick Reference

### Important Files

```
BaliRestaurants/
├── .env                    # YOUR API KEY HERE (not in git)
├── .env.example           # Template (in git)
├── test_apify.py          # Test script
├── requirements.txt       # Dependencies list
└── venv/                  # Virtual environment
```

### Key Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run test
python test_apify.py

# Deactivate virtual environment
deactivate
```

### Environment Variables

Your `.env` file should contain:
```
APIFY_API_KEY=apify_api_YOUR_ACTUAL_TOKEN_HERE
```

---

## Common Questions

### Q: How do I know how many credits I have left?

**A:** Check your Apify Console → Billing section. Free credits renew on the 1st of each month.

### Q: What happens if I exceed the free tier?

**A:** Apify will either:
- Ask you to add a payment method to continue
- OR stop your requests until next month (depending on your settings)

You can set spending limits in the Billing section.

### Q: Can I test without using credits?

**A:** The test script uses real API calls and will consume credits (~850 reviews = ~$0.30). But with $5/month free, you have plenty to test!

### Q: What if the test fails?

**A:** Common issues:
1. API key not in `.env` file
2. Virtual environment not activated
3. `apify-client` not installed
4. Typo in API key

Check the Troubleshooting section above.

---

## Security Best Practices

### ✅ DO:
- Keep your API token in `.env` file
- Add `.env` to `.gitignore`
- Use environment variables in code
- Rotate your token if compromised (Apify Console → Settings → Integrations)

### ❌ DON'T:
- Commit `.env` to git
- Share your API token publicly
- Hard-code the token in your code
- Post it in forums/Discord/Slack

---

## Getting Help

### Apify Resources:
- **Documentation:** https://docs.apify.com/
- **Support:** support@apify.com
- **Community:** https://discord.com/invite/jyEM2PRvMU

### Project Resources:
- **PRD:** `/specs/PRD_v1.md`
- **Technical Spec:** `/specs/technical_spec_v1.md`
- **Keywords:** `/specs/food_poisoning_keywords.md`

---

## Summary Checklist

Before proceeding to build the app, make sure:

- [ ] Apify account created
- [ ] API token copied from Settings → Integrations
- [ ] `.env` file created with `APIFY_API_KEY`
- [ ] Virtual environment activated
- [ ] `apify-client` installed
- [ ] Test script runs successfully
- [ ] Sample reviews displayed correctly

**Once all checked, you're ready to start building!** 🎉

---

**Document End**
