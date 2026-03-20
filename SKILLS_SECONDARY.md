# Replit AI Agent — Secondary Skill Documents (Internal Instructions)

**Date:** March 20, 2026
**Purpose:** Secondary skills for specialized domains. Note skills for high-risk domains: stock-analyzer, insurance-optimizer, tax-reviewer, legal-contract, real-estate-analyzer, invoice-generator.

---

## Secondary Skill: ad-creative

**Path:** `.local/secondary_skills/ad-creative/SKILL.md`

```markdown
---
name: ad-creative
description: Design static ad creatives for social media and display advertising campaigns.
---

# Ad Creative Maker

Design static ad creatives for social media ads, display banners, and digital advertising campaigns. Build production-ready ads via the design subagent and present them as iframes on the canvas.

## When to Use

- User needs ad creatives for Facebook, Instagram, LinkedIn, Google Display, or TikTok
- User wants banner ads or display advertising assets
- User needs multiple ad variants for A/B testing
- User wants ad copy and visual design together
- User wants to iterate on ad creative based on performance data

## When NOT to Use

- Organic social media content (use content-machine skill)
- Video ads or animated content (use storyboard skill for planning)
- Full landing pages (use the `artifacts` skill)

## Methodology

### Step 1: Creative Brief

Gather these inputs:

- **Platform & Format**: Which platform? (Google Ads, Meta, LinkedIn, TikTok, X/Twitter) Which format? (Search RSAs, feed, stories, display)
- **Objective**: Awareness, consideration, or conversion?
- **Target audience**: Who will see this ad? What stage of awareness? (Problem-aware, solution-aware, product-aware)
- **Key message**: Single most important thing to communicate
- **CTA**: What action should the viewer take?
- **Brand assets**: Logo, colors, fonts, product images
- **Performance data** (if iterating): Which headlines/descriptions are performing best/worst? What angles have been tested?

### Step 2: Platform Specifications (2025-2026)

**Enforce these programmatically.** Count characters in code, don't eyeball.

#### Meta (Facebook/Instagram) — Visual

| Placement | Dimensions | Safe zone (keep critical elements inside) |
|---|---|---|
| Feed (square) | 1080×1080 | ~100px margin all edges |
| Feed (portrait) — **preferred** | 1080×1350 (4:5) | 4:5 outperforms 1:1 on CTR; mobile-first |
| Stories | 1080×1920 | Top 14% (270px) + bottom 20% (380px) = dead zones |
| Reels | 1080×1920 | Top 14% + **bottom 35% (670px)** — like/comment/share UI is taller |
| **Universal safe core** | **1010×1280 centered** | Design inside this box → works everywhere |

Upload at 2x pixel density (2160×2160 for a 1080 slot) for Retina sharpness. JPG/PNG, 30MB max.

**20% text rule: officially removed** — Meta no longer rejects text-heavy images, but the delivery algorithm still quietly throttles them. Keep text minimal; move details to primary text.

#### Meta — Text

| Element | Limit | Notes |
|---|---|---|
| Primary text | 125 chars visible feed / **~72 chars visible in Reels** | Write for 72 |
| Headline | 40 chars rec | Below image |
| Description | 30 chars rec | Often hidden on mobile |

#### Google Ads

**Responsive Search Ads (RSA):**

| Element | Limit | Qty | Rule |
|---|---|---|---|
| Headlines | 30 chars | up to 15, min 3 | Each must work standalone — Google combines randomly |
| Descriptions | 90 chars | up to 4, min 2 | Complement, don't repeat headlines |
| Display path | 15 chars × 2 | — | |

Pin sparingly — pinning drops Ad Strength and limits ML optimization. Supply ≥5 headlines + ≥5 descriptions for ~10% more conversions at same CPA.

**Responsive Display Ads (RDA) — default Display format:**

| Asset | Spec | Qty |
|---|---|---|
| Landscape image | 1200×628 (1.91:1) | up to 15 total |
| Square image | 1200×1200 (1:1) | required |
| Portrait image | 1200×1500 (4:5) | optional, expands inventory |
| Logo square | 1200×1200 (128 min) | up to 5 |
| Logo wide | 1200×300 (4:1) | optional |
| Short headline | 30 chars | up to 5 |
| Long headline | 90 chars | 1 |
| Description | 90 chars | up to 5 |

All images ≤5MB, JPG/PNG only (no GIF in RDA). Keep file size <150KB for fast load.

**Highest-inventory static sizes** (if uploading fixed banners): 300×250 (medium rectangle — most served, works desktop+mobile), 728×90 (leaderboard), 320×50 (mobile banner), 300×600 (half-page — premium CPM, high CTR), 336×280.

**Performance Max:** same asset pool serves across Search/Display/YouTube/Gmail/Maps/Discover. Upload all 3 image ratios + a YouTube video (≤30s) or Google auto-generates one — don't let it.

#### LinkedIn Ads

| Element | Limit |
|---|---|
| Intro text | 150 chars rec (600 max) |
| Headline | 70 chars rec (200 max) |
| Image | 1200×627 (1.91:1) or 1200×1200 |

#### TikTok Ads

1080×1920, 9:16. Ad text: 100 char max (~80 visible). For Spark Ads (boosting organic creator posts), get the authorization code from the creator — Spark Ads outperform In-Feed Ads on engagement because they retain organic engagement metrics.

### Step 3: Define Angles

Before writing individual copy, establish 3-5 distinct angles — different reasons someone would click:

| Category | Example |
|----------|---------|
| Pain point | "Stop wasting time on X" |
| Outcome | "Achieve Y in Z days" |
| Social proof | "Join 10,000+ teams who..." |
| Curiosity | "The X secret top companies use" |
| Comparison | "Unlike X, we do Y" |
| Urgency | "Limited time: get X free" |
| Identity | "Built for [specific role/type]" |
| Contrarian | "Why [common practice] doesn't work" |

### Step 4: Design Principles

**Visual hierarchy (read order):** 1) Hero element → 2) Benefit/offer → 3) CTA → 4) Logo (corner, small).

**Rules:**

- <20 words total on the image — move everything else to primary text
- One focal point. If the eye doesn't know where to land in 0.5s, it's too busy.
- High contrast text/background — verify WCAG 4.5:1 minimum (use `chroma.contrast()` if building programmatically)
- CTA button: contrasting color, rounded corners, verb-first ("Get the guide" not "Learn more")
- Faces looking *toward* the CTA increase click-through (gaze cueing)
- Keep file <150KB for display; Meta accepts up to 30MB but slow loads hurt auction performance

### Step 5: Generate Variations

For each angle, generate multiple variations. Vary:

- **Word choice** — synonyms, active vs. passive
- **Specificity** — numbers vs. general claims ("Cut reporting time 75%" beats "Save time")
- **Tone** — direct vs. question vs. command
- **Structure** — short punch vs. full benefit statement

**Strong headlines:** Specific over vague. Benefits over features. Active voice. Include numbers when possible ("3x faster," "in 5 minutes").

**Strong descriptions:** Complement headlines, don't repeat them. Add proof points, handle objections ("No credit card required"), reinforce CTAs.

### Step 6: Validate and Deliver

Before presenting, check every piece against character limits. Flag anything over and provide a trimmed alternative. Include character counts.

```text

## Angle: [Pain Point — Manual Reporting]

### Headlines (30 char max)

1. "Stop Building Reports by Hand" (29)
2. "Automate Your Weekly Reports" (28)
3. "Reports in 5 Min, Not 5 Hrs" (27)

### Descriptions (90 char max)

1. "Marketing teams save 10+ hours/week with automated reporting. Start free." (73)
2. "Connect your data sources once. Get automated reports forever. No code required." (80)

```

### Step 7: Build Ad Creatives — Design Subagents + Canvas

**Launch a separate design subagent for each variation in parallel** using `startAsyncSubagent`. Each subagent builds one ad variation as a standalone HTML page. This is much faster than building them sequentially.

#### Canvas Layout

**Default to square iframes (1080x1080) for ad creatives** so they fully fit on the canvas without clipping. The HTML inside uses `100vw`/`100vh` to fill the iframe regardless of size. Group by angle in rows, with a landing page iframe alongside:

```text
x=0,    y=0:    [Label: "Angle 1: [Pain Point] — Ad"]
x=0,    y=40:   [Iframe: angle1-ad]              (1080x1080)

x=1200, y=0:    [Label: "Angle 1: [Pain Point] — Landing Page"]
x=1200, y=40:   [Iframe: angle1-landing]         (1280x720)

x=0,    y=1220: [Label: "Angle 2: [Social Proof] — Ad"]
x=0,    y=1260: [Iframe: angle2-ad]              (1080x1080)

x=1200, y=1220: [Label: "Angle 2: [Social Proof] — Landing Page"]
x=1200, y=1260: [Iframe: angle2-landing]         (1280x720)

x=0,    y=2440: [Label: "Angle 3: [Outcome] — Ad"]
x=0,    y=2480: [Iframe: angle3-ad]              (1080x1080)

x=1200, y=2440: [Label: "Angle 3: [Outcome] — Landing Page"]
x=1200, y=2480: [Iframe: angle3-landing]         (1280x720)
```

#### Parallel design subagent delegation

**Launch all variations simultaneously.** Each subagent gets one ad + its landing page. Use `startAsyncSubagent` for each, then `waitForBackgroundTasks` to collect results.

```javascript
// Launch all 3 angles in parallel — each subagent builds one angle's assets
await startAsyncSubagent({
    task: `Create a production-ready ad creative and matching landing page for the following angle.

Brand: [name]
Colors: Primary [hex], Secondary [hex], Accent [hex]
Fonts: [display font], [body font] (load from Google Fonts)
Logo: [path or description]
User's stated style preferences: [include any specific preferences the user mentioned]

**Angle: [Pain Point]**
- Headline: "[headline text]"
- CTA: "[cta text]"

Build these files:

1. **angle1-ad.html** (square, 1:1) — the actual ad creative
2. **angle1-landing.html** (desktop, 1280px wide) — a mock marketing landing page this ad would link to. Include hero section, value props, social proof, and CTA. This should look like a real product page, not a wireframe.

**CRITICAL — viewport-relative sizing for iframes:**
The ad HTML will be embedded in an iframe on a canvas. The content MUST fill the iframe exactly — no overflow, no scrollbars, no clipping. Use this CSS pattern:

\`\`\`css
html, body {
  margin: 0;
  padding: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}
.ad-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  /* use vw/vh for all internal sizing too */
}
/* Use vw for font sizes so they scale: e.g., font-size: 5vw; */
/* Use vw/vh for padding/margins: e.g., padding: 3vw; */
\`\`\`

This ensures the ad looks correct at any iframe size — 1080x1080 on canvas, or any other size. **Never use fixed pixel dimensions** (e.g., width: 1080px) for the ad container.

Design rules:
- Each ad must look like a real ad you'd see in your feed — polished, professional, production-ready
- **No gradients** — use flat colors, solid backgrounds, clean color blocking
- Styling must match the brand concept and any specific preferences the user stated (e.g., if they said "minimal" don't make it busy, if they said "bold" don't make it subtle)
- <20 words on the ad image. Visual hierarchy: hero element → benefit → CTA → logo (corner, small)
- High contrast text/background (WCAG 4.5:1 minimum)
- CTA button: contrasting color, rounded corners, verb-first
- Use image generation for hero imagery if no product photo is provided
- Use the brand's actual colors and fonts throughout — the landing page should feel like a continuation of the ad`,
    specialization: "DESIGN",
    relevantFiles: []
});

// Repeat for Angle 2 and Angle 3 in the same message — all 3 launch simultaneously
await startAsyncSubagent({
    task: `... Angle 2: [Social Proof] ...`,
    specialization: "DESIGN",
    relevantFiles: []
});

await startAsyncSubagent({
    task: `... Angle 3: [Outcome] ...`,
    specialization: "DESIGN",
    relevantFiles: []
});

// Wait for all 3 to complete
await waitForBackgroundTasks();
```

After all subagents finish, embed each page as an iframe on the canvas using `apply_canvas_actions`. Tell the user what was created and offer to focus the viewport.

#### Styling rules — no exceptions

- **Viewport-relative sizing.** All ad HTML must use `100vw`/`100vh` for the container and `vw`-based font sizes/padding. Never fixed pixel dimensions for the ad container. The ad must fill whatever iframe it's placed in without clipping or scrollbars.
- **No gradients.** Use flat, solid colors. Color blocking with the brand palette is fine; linear-gradient/radial-gradient is not.
- **Match the concept.** If the user said "minimalist," don't add decorative elements. If they said "bold and energetic," don't make it muted. Re-read the user's stated preferences before delegating.
- **Consistency across angles.** All 3 angles should feel like they're from the same brand — same fonts, same color usage patterns, same visual language. The angles differ in message, not in design system.
- **Landing page = real page.** The mock landing page should look like where the ad actually leads — hero section echoing the ad's message, value props, testimonials/social proof section, and a CTA. Not a wireframe, not a placeholder.

#### Export

The user can screenshot each iframe directly, or open the HTML files in a browser at the desired export size. Since the ads use `vw`/`vh` sizing, they'll adapt to any viewport. For batch export at specific dimensions: `npx playwright screenshot angle1-ad.html --viewport-size=1080,1080`.

## Iterating from Performance Data

When the user provides performance data:

1. **Analyze winners**: Identify winning themes, structures, word patterns, and character utilization in top performers (by CTR, conversion rate, or ROAS)
2. **Analyze losers**: Identify themes that fall flat and common patterns in underperformers
3. **Generate new variations**: Double down on winning themes, extend winning angles, test 1-2 new unexplored angles, avoid patterns from underperformers
4. **Document the iteration**: Track what was learned, what's being tested, and what angles were retired

## Research Before Writing

Use `webSearch` to find examples of top-performing ads in the user's vertical. Search for ad breakdowns, swipe files, and case studies — e.g. `webSearch("[industry] top performing Facebook ads 2026")` or `webSearch("[industry] TikTok ad examples")`. The TikTok Creative Center and Meta Ad Library are useful reference sites but require direct browser interaction to filter; web search can surface articles and analyses that reference their data. Reverse-engineer: what hook, what angle, what visual pattern. Don't guess what works — look it up.

## Common Mistakes

- Writing RSA headlines that only work in sequence (Google combines them randomly — each must stand alone)
- Ignoring the Reels 72-char visible limit (writing for the 125-char feed limit → truncated on Reels)
- All variations = same angle reworded (vary the *psychology*, not the synonyms)
- Placing text in the bottom 35% of a 9:16 ad (covered by UI on every platform)
- Retiring creative before 1,000+ impressions per variant
- Letting Performance Max auto-generate video — always supply your own

## Limitations

- Cannot run or measure ad campaigns
- Cannot access ad platform analytics
- Cannot create animated or video ads
- Image generation requires the media-generation skill

```

---

## Secondary Skill: ai-recruiter

**Path:** `.local/secondary_skills/ai-recruiter/SKILL.md`

```markdown
---
name: ai-recruiter
description: Source and evaluate candidates with job analysis, search strategies, specific candidate profiles, and outreach templates.
---

# AI Recruiter

Help source and evaluate candidates for open roles. Analyze job descriptions, build search strategies, find specific candidate profiles, and draft outreach messages.

## When to Use

- User needs to hire for a role and wants sourcing strategy
- User wants to improve a job description
- User needs interview questions for a specific role
- User wants candidate evaluation criteria
- User wants to find specific candidate profiles for a role

## When NOT to Use

- Sales prospecting (use find-customers skill)
- General market research (use deep-research skill)
- Writing job-related content (use content-machine skill)

## Workflow — Follow This Order

### Step 0: Research First, Then Ask Questions

Before producing any output, always do two things in this order:

**0a. Search for the role and company.**
If the user names a company or role, use `webSearch` to find:

- The actual job posting (check Ashby, Lever, Greenhouse, the company careers page)
- Latest company details: funding, valuation, headcount, ARR, recent news
- Competitor landscape for the role

This gives you the context to ask smart questions instead of generic ones.

**0b. Ask the user clarifying questions.**
Do not assume details. Ask about:

- Which specific role (if the company has multiple open positions, list them as choices)
- Seniority level
- Location / remote policy
- What candidate background matters most (domain-specific vs. open to adjacent backgrounds)
- Whether competitors are fair game for sourcing
- Any specific gaps on the team they're trying to fill (e.g., growth, technical, enterprise, design)
- Any other preferences (e.g., founder background, specific skills)

Only proceed to output after you have answers.

### Step 1: Calibrate the Role

Split requirements into three buckets — be ruthless, most JDs list nice-to-haves as must-haves and shrink the pool 80%:

- **Must-have** (3-4 max): Deal-breakers. Can't do the job without these on day one.
- **Learnable in 90 days**: Most "required" skills belong here.
- **Pedigree signals**: School, FAANG experience, etc. — these filter for bias, not ability. Drop them unless there's a specific reason.

**Comp research:** `webSearch: "levels.fyi [role] [company tier]"` or `"[role] salary [city] site:glassdoor.com"`. For startups, `webSearch: "Pave [role] equity benchmarks"`. Keep comp in the internal strategy doc for reference but do NOT include it in outreach templates by default.

### Step 2: Build Boolean Search Strings

Boolean-savvy recruiters fill roles ~23% faster (LinkedIn 2023 data). LinkedIn Recruiter caps each field at ~300 chars — split across Title and Keywords rather than cramming one field.

**Core pattern — put role in Title, skills in Keywords:**

```text
Title: ("staff engineer" OR "senior engineer" OR "tech lead" OR "principal")
Keywords: (Rust OR Go OR "distributed systems") AND (Kubernetes OR k8s) NOT (manager OR director OR intern)
```

**Synonym rings — the #1 missed tactic.** Titles fragment massively across companies:

```text
("product manager" OR "product owner" OR "PM" OR "program manager" OR "product lead")
("data scientist" OR "ML engineer" OR "machine learning engineer" OR "applied scientist" OR "research scientist")
("SRE" OR "site reliability" OR "devops engineer" OR "platform engineer" OR "infrastructure engineer")
```

**Impact-verb trick** — surface doers, not title-holders:

```text
("built" OR "shipped" OR "launched" OR "scaled" OR "led migration" OR "0 to 1")
```

**X-ray search (Google, bypasses LinkedIn limits):**

```text
site:linkedin.com/in ("staff engineer" OR "principal engineer") "rust" "san francisco" -recruiter -hiring
```

### Step 3: Provide Direct LinkedIn Search Links

Always generate at least 5 clickable LinkedIn search URLs that the user can open directly in their browser. These should be pre-built with URL-encoded keywords, location filters, and relevant company/skill terms.

**URL format:**

```text
https://www.linkedin.com/search/results/people/?keywords=URL_ENCODED_KEYWORDS&geoUrn=%5B%22GEO_ID%22%5D&origin=FACETED_SEARCH
```

**Common geo IDs:**

- SF Bay Area: `102095887`
- New York: `103644278`
- US: `103644278`
- London: `90009496`

Create separate links for different search angles:

1. Candidates at direct competitors
2. Candidates with the specific skill/background the user prioritized
3. Candidates at adjacent companies in the space
4. Candidates at tier 2/3 companies (bigger pool)
5. Broader keyword search for passive candidates

### Step 4: Find Specific Candidate Profiles

Always use `webSearch` with `site:linkedin.com/in` queries to find specific named candidates. Search multiple angles:

- PMs/engineers at competitor companies
- People with the specific background the user asked for (e.g., founder experience, UI expertise)
- People at adjacent companies in the same space

Present candidates in a table with:

- Name
- Current role
- Why they fit (1 sentence)
- Hyperlinked LinkedIn profile URL

Aim for 10-15 specific profiles, organized into tiers (e.g., direct competitors, adjacent companies, broader pool).

### Step 5: Source Beyond LinkedIn

LinkedIn InMail response rates have dropped from 30%+ to 10-13% over 5 years as the platform saturated. Diversify:

| Channel | Best for | Tactic |
|---------|----------|--------|
| **GitHub** | Engineers | `webFetch` their profile — check contribution graph (consistent > spiky), pinned repos, languages bar, PR review quality on public projects. |
| **GitHub Search** | Niche skills | `site:github.com "location: [city]" language:Rust` or search commits/issues in relevant OSS projects |
| **Stack Overflow** | Deep specialists | Top answerers on niche tags — check profile for contact info |
| **Conference talks** | Senior/staff+ | `webSearch: "[conference name] speakers 2025"` — speakers are pre-vetted for communication skills |
| **Papers/Google Scholar** | ML/research | Co-authors on relevant papers, often with .edu emails |
| **HN "Who wants to be hired"** | Startup-minded | Monthly thread, candidates self-describe, `site:news.ycombinator.com "who wants to be hired"` |
| **Product Hunt** | Builder-types | Makers of top products in the relevant category |
| **Twitter/X** | Thought leaders | Search for people posting about the relevant domain |
| **YC Alumni** | Founder-PMs | Founders whose startups ended and moved into PM/leadership roles |
| **Paid aggregators** | Volume | SeekOut, HireEZ (45+ platforms), Gem, Juicebox/PeopleGPT |

### Step 6: Outreach That Gets Replies

**2025 benchmarks:** Cold InMail averages 10-13% response. Personalized outreach with a specific hook hits 20%+. 86% of candidates ignore generic messages entirely (TalentBoard 2024).

**Structure — 4 sentences max:**

1. **Hook** (why *them*, specifically): "Saw your PR on the Tokio scheduler — the approach to work-stealing was clean."
2. **Why this role matters** (to them, not to you): "We're 12 engineers, pre-Series-B, and the entire storage layer is unowned."
3. **One concrete detail**: Remote policy, a tech problem they'd find interesting, team size, or growth metrics. Avoid listing comp — save that for when they respond.
4. **Low-friction CTA**: "Worth 15 min to hear more?" — not "Let me know if you're open to opportunities."

**Do NOT include compensation in outreach templates.** Comp details belong in the internal strategy section. If a candidate responds, share comp on the first call. Leading with comp in cold outreach can anchor low or signal desperation.

**Subject lines:** Use their project name or the specific tech, not "Opportunity at [Company]." Lowercase, short, looks like a peer wrote it.

**Follow-up:** One bump at day 5 with a *new* piece of info (funding news, a blog post, the hiring manager's name). Never "just following up."

**Generate 3 outreach templates** tailored to different candidate segments (e.g., competitors, adjacent companies, career-changers). Customize the angle for each.

### Step 7: Suggested Interview Questions

Include a short section of suggested interview questions at the bottom of the output. Use behavioral questions (STAR format) over hypothetical ones. Organize by the key criteria identified in Step 1.

Keep it lightweight — 2 questions per criterion, 3-4 criteria max. No scoring rubrics or evaluation matrices unless the user specifically asks for one.

## Hiring Benchmarks

- **Time-to-fill**: 44 days US average (SHRM 2025); tech roles run longer
- **Cost-per-hire**: $6-7k standard tech roles; $12k+ for ML/security/staff+ (Deloitte 2024)
- **Funnel**: Tech roles see ~110 applicants/opening, ~5% get interviews
- **Speed matters**: Top candidates are off-market in 10 days. The interview-to-offer stage is where most teams lose — compressing it cuts time-to-hire by ~26%.
- **LinkedIn Recruiter cost**: $1.6k/yr (Lite) to $10.8k+/yr (Corporate, 150+ InMails/mo)

## Bias Reduction

- Strip unnecessary degree requirements — they filter for socioeconomic background, not skill
- Run JD through `webSearch: "gender decoder job description"` tools — "rockstar," "ninja," "aggressive" skew male applicant pools
- Same questions, same order for every candidate
- Score immediately after each interview, before discussing with other interviewers (anchoring bias)
- Source from non-traditional channels (HN, PH, YC alumni, blogs) to avoid LinkedIn-only pool bias

## Output Structure

The final deliverable should follow this order:

1. **Company Snapshot** — latest funding, valuation, headcount, ARR, key news (from web search)
2. **Role Details** — title, posting link, focus area, seniority, location, key needs (from user answers)
3. **Estimated Comp Range** — internal reference only, not for outreach
4. **Requirements** — must-haves / learnable / pedigree signals to drop
5. **Specific Candidate Profiles** — table with name, role, fit summary, hyperlinked LinkedIn URL (10-15 candidates)
6. **LinkedIn Search Links** — at least 5 clickable URLs the user can open directly
7. **Boolean Search Strings** — for LinkedIn Recruiter and Google X-ray
8. **Sourcing Channels** — beyond LinkedIn (table format)
9. **Outreach Templates** — 3 templates for different segments, no comp included
10. **Sourcing Action Plan** — 2-week day-by-day plan with target funnel
11. **Bias Reduction Checklist**
12. **Suggested Interview Questions** — lightweight, behavioral, organized by key criteria

## Limitations

- Cannot log into LinkedIn Recruiter, SeekOut, Gem, or HireEZ — builds search strings the user pastes in
- Cannot send InMails or emails
- Cannot verify employment history or run background checks
- GitHub analysis via `webFetch` only works for public profiles/repos
- LinkedIn search URLs use public search — results may vary based on the user's LinkedIn account tier

```

---

## Secondary Skill: ai-secretary

**Path:** `.local/secondary_skills/ai-secretary/SKILL.md`

```markdown
---
name: ai-secretary
description: Draft emails, manage calendar scheduling, prepare meeting agendas, and organize productivity
---

# AI Secretary

Help manage email, calendar scheduling, and daily productivity workflows. Draft emails, organize schedules, prepare meeting agendas, and summarize communications.

## Communication Style

Talk to the user like a helpful human assistant, not a developer tool. Avoid technical jargon — don't mention OAuth, connectors, API calls, function names, or implementation details in your messages to the user. Just do the work and communicate in plain language.

- **Say**: "I'll need to connect to your Google Calendar — you'll get a quick sign-in prompt"
- **Don't say**: "I'll use `searchIntegrations('google calendar')` to find the connector and then call `proposeIntegration` to initiate the OAuth flow"
- **Say**: "Here's what your week looks like" then show the schedule
- **Don't say**: "I executed a calendar API query and retrieved the following event objects"

## Calendar Safety — Read Only Until Confirmed

**NEVER create, modify, or delete a calendar event without explicit user confirmation.** Calendar access is read-first:

1. Read the user's calendar freely — show them their schedule, flag conflicts, suggest open slots
2. When you want to create or change an event, **describe what you plan to do** and ask the user to confirm before writing anything
3. Only after the user says yes (e.g., "yes, schedule it", "go ahead", "looks good") should you create or modify the event

This applies to every write operation — new events, rescheduling, cancellations, invite changes. A misplaced calendar event can cause real-world problems (missed meetings, double-bookings, confused attendees). Always confirm first.

## When to Use

- User wants help drafting or organizing emails
- User needs to plan their calendar or schedule meetings
- User wants meeting agendas or follow-up summaries
- User asks about productivity workflows or time management
- User wants to organize their day, week, or priorities

## When NOT to Use

- Cold outreach emails (use cold-email-writer skill)
- Marketing email sequences (use content-machine skill)
- Project management / PRDs (use product-manager skill)

## Methodology

### Email Drafting — BLUF Pattern

Use **BLUF (Bottom Line Up Front)** — the US military writing standard. State the ask or conclusion in the first line, *then* provide context. Readers should know what you need without scrolling.

**Subject line = action keyword + topic.** Military convention uses bracketed prefixes:

- `[ACTION]` — recipient must do something
- `[DECISION]` — recipient must choose
- `[SIGN]` — signature/approval needed
- `[INFO]` / `[FYI]` — no action, read when convenient
- `[REQUEST]` — asking a favor

**Structure:**

```text
Subject: [ACTION] Approve Q2 budget by Fri 5pm

BOTTOM LINE: Need your sign-off on the attached Q2 budget ($142K) by Friday 5pm ET so finance can close the month.

BACKGROUND:

- $12K over Q1 due to the added contractor (approved in Feb)
- Line 14 is the only new item — everything else is run-rate
- If no response by Friday, I'll assume approved and submit

[attachment]

```

**The 5-sentence rule:** If an email needs more than 5 sentences, it probably needs to be a document, a meeting, or a phone call. Default to shorter.

**Batch triage when user dumps an inbox:**

1. Tag each: `REPLY-NOW` (blocking someone) / `REPLY-TODAY` / `FYI` (archive) / `DECISION` (needs user input — don't draft, just summarize the choice)
2. Draft `REPLY-NOW` and `REPLY-TODAY` in the user's voice
3. For `DECISION` items, give a 1-line summary + the options, not a draft

### Calendar & Scheduling

**Meeting scheduling:**

- Identify time zones for all participants
- Suggest 2-3 time slots based on stated preferences
- Draft calendar invite with: title, agenda, location/link, duration
- Include pre-meeting prep notes if relevant

**Weekly planning:**

- Review upcoming commitments
- Identify conflicts or over-scheduled days
- Suggest time blocks for deep work, meetings, and breaks
- Flag preparation needed for upcoming meetings

**Time-blocking strategy:**

- Morning: Deep work / high-priority tasks (protect this time)
- Mid-day: Meetings and collaborative work
- Afternoon: Email, admin, lower-priority tasks
- Build in 15-minute buffers between meetings
- Block "no meeting" days if possible (at least half-days)

### Meeting Agendas — Pick a Model

**Amazon 6-pager (silent reading):** For high-stakes decisions. Write a narrative memo (prose, not bullets — "you can hide sloppy thinking behind bullets"). Meeting opens with 10–30 min of silent reading, then discussion. Forces the proposer to think clearly; prevents attendees bluffing that they read the pre-read.

**GitLab live-doc (async-first):** A shared doc that IS the meeting. Agenda items added by anyone beforehand, newest at top. Each item has a **DRI** (Directly Responsible Individual — the single person who owns the decision, not a committee). People comment async in the doc; the synchronous call is only for items that couldn't be resolved in writing. Attendance is optional — the doc is the source of truth.

**Default agenda template:**

```text

# [Meeting Title] — [Date] — [Duration]
DRI: [single name — who owns the outcome]

## Decision needed
[One sentence. If you can't write this, cancel the meeting.]

## Pre-read (read BEFORE, not during — unless doing Amazon silent-read)

- [link]

## Agenda
| Time | Topic | Owner | Outcome wanted |
|------|-------|-------|----------------|
| 5m   | ...   | ...   | Decide / Inform / Discuss |

## Decisions made  [fill in live]

## Action items    [fill in live — owner + date, always]

```

**Post-meeting output (send within 2 hours):**

- Decisions: what was decided, by whom
- Actions: `@owner — task — due date` (every action has all three or it's not real)
- Parking lot: what was raised but deferred

### Scheduling Etiquette

- Offer 3 specific slots, not "what works for you?" — decision fatigue is real
- Always state timezone explicitly: `Tue 3pm ET / 12pm PT / 8pm GMT`
- Default to 25 or 50 minutes, not 30/60 — builds in transition buffer
- For external meetings: send a calendar hold immediately, finalize details later
- If >5 people: make attendance optional for anyone not presenting or deciding

## Output Format

For email drafts:

```text
Subject: [subject line]

Hi [Name],

[body]

Best,
[User's name]

```

For schedules, use clear time-blocked format:

```text

## Monday, [Date]

9:00-10:30  Deep work: [project]
10:30-10:45 Break
10:45-11:30 Meeting: [title] w/ [people]
...

```

## Best Practices

1. **Respect the user's voice** — match their writing style, not generic corporate speak
2. **Be specific with times** — "EOD Friday" beats "soon"
3. **Default to shorter** — most emails should be under 150 words
4. **Protect deep work time** — don't let meetings fill every hour
5. **Follow up proactively** — suggest reminders for unanswered emails

## Connecting to Real Email & Calendar via Replit Connectors

You can go beyond drafting and actually access the user's email and calendar using **Replit connectors**. Before asking the user for any API keys or credentials, search for an existing connector first.

### How to connect

1. Search for the relevant connector using `searchIntegrations("google calendar")`, `searchIntegrations("gmail")`, or `searchIntegrations("outlook")`
2. If a connector exists, use `proposeIntegration` to prompt the user to sign in — this gives you real access to their calendar and email
3. Once connected, you can read calendar events, create new events (with confirmation), read emails, and send emails on the user's behalf

**Important:** When talking to the user about this, just say something like "I can connect to your Google Calendar so I can see your real schedule — you'll get a quick sign-in prompt." Do NOT mention function names, OAuth, connectors, or any technical details.

### What connectors unlock

- **Google Calendar / Outlook Calendar** — Read upcoming events, check for conflicts, create calendar invites, suggest open time slots based on actual availability
- **Gmail / Outlook Mail** — Read inbox messages, draft and send replies, triage emails with real data instead of copy-pasted content

### When to suggest connecting

- User asks to "check my calendar" or "what do I have this week" — suggest the calendar connector
- User asks to "go through my emails" or "help me with my inbox" — suggest the email connector
- User wants to schedule a meeting and check real availability — suggest the calendar connector
- Any time the workflow would be dramatically better with real data vs. copy-paste

### If no connector is available

Fall back to the manual workflow: the user copy-pastes email content or tells you their schedule, and you draft responses and suggest time blocks based on what they share. This still works — it's just slower.

## Limitations

- Cannot join or record meetings
- Real email/calendar access requires the user to authorize a Replit connector (Google or Outlook) — without it, the user must copy/paste content manually

```

---

## Secondary Skill: apartment-finder

**Path:** `.local/secondary_skills/apartment-finder/SKILL.md`

```markdown
---
name: apartment-finder
description: Find apartments for rent, evaluate listings, detect scams, analyze neighborhoods, and compare rental options. Use when the user asks to find, evaluate, or compare apartments or rental housing.
---

# Apartment Finder

Find real listings, evaluate them, detect scams, vet neighborhoods, and flag lease traps.

## When to Use

- Finding apartments in a specific city/area matching user criteria
- Evaluating a specific listing (especially Craigslist/FB Marketplace)
- Comparing units on true cost, not sticker rent
- Lease review before signing

## When NOT to Use

- Home buying; active lease disputes (use legal-contract)

## Search Methodology

When a user asks to find apartments, run a multi-site search and return specific units with addresses, prices, and direct links. Users do not want generic search page links — they want listings they can act on.

### Search Process

1. Determine criteria from the user: city/neighborhood, bedrooms, max budget, preferences (waterfront, views, parking, pets, etc.)
2. Search all major sites in parallel using `webSearch`:
   - **Zillow** (`zillow.com [city] [beds] bedroom [type] for rent [neighborhood] [preferences]`)
   - **Apartments.com** (`apartments.com [city] [beds] bedroom [neighborhood] rent`)
   - **Redfin** (`redfin.com [city] [beds] bedroom [type] for rent [neighborhood]`)
   - **Craigslist** (`craigslist [city] [beds] bedroom [type] [neighborhood] rent`)
3. Fetch actual listing pages using `webFetch` on the most relevant result URLs to extract specific unit data (addresses, prices, sqft, features)
4. Present individual units — each listing needs: address, unit number, price, beds/baths, sqft, key features, and a direct link

### Listing Type Preferences

Prefer individual units over managed-building "starting at" prices. Large apartment complexes advertise teaser "starting at" rates that are often for unavailable or least-desirable units. When possible:

- Search for condos for rent, townhouses for rent, and "by owner" listings
- Filter by property type = condo/townhouse on Redfin and Zillow
- On Craigslist, use the "housing by owner" filter
- On Apartments.com, look for "for rent by owner" listings
- Present the actual asking price for the specific unit, not "starting at" ranges
- When large buildings are included, note that the listed price is a floor and the user should expect higher for desirable units/floors.

### Price Verification — Unit vs. Building

Listing sites often show a building's lowest "starting at" price that may be for a different unit type, floor plan, or even bedroom count than what the user asked for. Before presenting any listing:

1. **Confirm the price is for the right bedroom count.** A building page might say "$3,450+" but that's for a 1BR — the 2BR starts at $5,200. Always drill into the specific floor plan.
2. **Confirm the unit actually exists at that price.** "Starting at" prices on Apartments.com, Zillow building pages, and RentCafe are often for a single unit or a unit that's already leased. If you can see individual unit prices on the page, quote those instead.
3. **Quote specific unit prices when available.** If a building has Unit 4B at $5,250 and Unit 7A at $5,800, present those individually — don't say "$5,250+". The user can evaluate each one.
4. **Flag uncertainty.** If you can only find a building-wide range and not a specific unit price, say so explicitly: "Building lists 2BRs from $X,XXX but specific unit pricing requires contacting leasing office."
5. **Watch for furnished vs. unfurnished.** Some sites (Blueground, Zeus, corporate housing) list furnished units at 30-50% premiums. Always note if a price includes furnishing.

### Output Format

Present listings in tiers based on value relative to the user's budget:

```text
**[Address, Unit #]** — **$X,XXX/mo** | Xbd/Xba | X,XXX sq ft
- [Key feature 1], [key feature 2], [key feature 3]
- [Why this is good value / what stands out]
- [Direct link to listing](URL)
```

Group into:

- **Best Value** — significantly under budget, punches above its price
- **Strong Mid-Range** — solid quality at a fair price within budget
- **Top of Budget** — premium units near the ceiling that justify the spend

After the listings, include:

- A "Top Picks" summary (2-3 sentences on the best overall deals and why)
- Filtered search links for each site so the user can monitor new listings
- True cost notes (parking, utilities, fees) relevant to the market

### Scam Warnings on Presented Listings

When presenting any listing, actively scan for red flags and warn the user inline. Do not present a suspicious listing without a warning attached.

Auto-flag if any of these are true:

- Price is 30%+ below neighborhood average for its size/type — add: "Price is well below market. Verify this is real before sending any money."
- Listing source is Craigslist or FB Marketplace with no verifiable landlord identity — add: "Listed on [platform] with no identity verification. Confirm ownership via county assessor before touring."
- Photos look professional but listing is "by owner" at a suspiciously low price — add: "Reverse-image-search the photos to confirm they aren't stolen from another listing."
- Listing says "no background check" or "no credit check" — add: "Legitimate landlords almost always run background/credit checks. Proceed with caution."
- Any mention of mailing keys, wiring money, or inability to show the unit in person — add: "DO NOT send money. This matches a known scam pattern."

For every Craigslist/FB listing presented, append this standard note:

> Craigslist/FB listings have no identity verification. Before sending any deposit: tour the unit in person, verify the owner via county property records, and pay only by check to a verified business entity. Never pay via Zelle/Venmo/CashApp/wire/gift card.

For individual condo/owner listings from any site, note:

> Private owner listing — verify ownership at [county] county assessor's website before signing anything or sending money.

### Search Queries That Work

Tailor queries to each site's strengths:

| Site | Best query pattern | What it finds well |
|------|-------------------|-------------------|
| Zillow | `[city] [neighborhood] [beds] bedroom condo for rent` | Individual owner-listed condos, specific addresses |
| Redfin | `[city] [neighborhood] [beds] bedroom [condo/apartment] for rent` | Condos for rent with MLS-quality data, specific units |
| Apartments.com | `[city] [neighborhood] [beds] bedrooms` | Both complexes and individual units, good amenity filters |
| Craigslist | `[city metro] [beds]br [neighborhood] [preferences]` | Private owner deals, below-market gems, fast turnover |
| Homes.com | `[city] [neighborhood] condos for rent [beds] bedrooms` | Individual condo units with detailed pricing |

Run at least 2 rounds of searches: a broad initial sweep, then targeted follow-ups on the most promising neighborhoods/buildings using `webFetch` on specific listing pages.

### Identifying "Underpriced" Listings

When the user wants deals or value:

- Search for average rent in the target neighborhood using `webSearch`
- Flag any listing priced 15%+ below neighborhood average for its size
- Look for: older buildings with recent renovations, move-in concessions (1 month free, weeks free), private owners pricing to fill quickly (vacant 30+ days), winter/off-season listings
- Check for concession-adjusted effective rent (e.g., 1 month free on 12-month lease = ~8% discount)

## Scam Detection — Named Patterns

Craigslist and FB Marketplace have no identity verification — scammers exploit this. FB is worse now because aged accounts with fake friends buy false trust.

**The "overseas landlord" script** (most common): Owner is abroad for work/military/missionary trip → can't show unit but will "mail keys" after deposit → below-market rent → no background check needed → pushes Zelle/Venmo/CashApp → disappears. If any two of these appear together, stop.

**The hijacked listing:** Scammer copies photos/description from a real Zillow/Realtor.com listing, reposts at ~50% of real rent. **Verification:** reverse-image-search the photos (images.google.com); webSearch the address on Zillow — if it's listed for sale or at a much higher rent, the cheap listing is fake.

**The "Zelle stopped working" escalation:** After partial Zelle payment, claims a technical issue and pivots to gift cards. Gift cards = 100% scam, zero exceptions.

| Hard rule | Why |
|-----------|-----|
| Never pay via Zelle/Venmo/CashApp/wire/crypto/gift card for deposit | Irreversible. Legitimate landlords accept checks to a business entity |
| Never pay before in-person tour of the actual unit | "Video tour" is not sufficient |
| Ask a question only someone who's been inside can answer | "What brand is the stove?" "Which wall has the thermostat?" Scammers can't answer |
| Verify owner via county assessor website | webSearch `"[county name] property records"` — public and free. Name should match |
| Reverse-search the "landlord's" profile photo | Stolen photos are standard |

**FB profile tells:** <50 friends OR hundreds of friends all from one foreign country; account created recently; no posts before the last few months.

## Neighborhood Research (webSearch/webFetch)

| Data | Source |
|------|--------|
| Crime by block | `crimemapping.com`, `spotcrime.com`, or `[city] police department crime map` |
| Walk/Transit/Bike scores | `walkscore.com/[address]` |
| Noise (flight paths, highways, rail) | `howloud.com` |
| School ratings | `greatschools.org` (only include if the user asks about schools) |
| Flood risk | `floodfactor.com` (FEMA maps underestimate) |
| Cell coverage | `coveragemap.com` — dead zones are real |
| Sex offender registry | `nsopw.gov` |
| Street-level vibe | Google Street View — check image date, walk the block virtually |

**IRL check:** Visit at 10pm on a Friday and 7am on a weekday. Noise, parking, and neighbor quality only show up in person.

## Lease Red Flags

| Clause | What it actually means | Response |
|--------|------------------------|----------|
| "Joint and several liability" | Roommate skips → you owe 100% of rent, not your share. Landlord can evict all of you for one person's non-payment | Unavoidable in most shared leases — choose roommates like you'd choose a business partner. Get a side agreement in writing |
| Automatic renewal with 60+ day notice | Miss the window → locked into another full year | Calendar the notice deadline the day you sign |
| "As-is" / waives repair duty | Landlord disclaims habitability | Illegal in most states — habitability can't be waived. Cross out |
| Landlord entry without notice | Violates quiet enjoyment | 24-48hr written notice is standard in most states |
| Tenant pays all legal fees regardless of outcome | You lose even if you win | Negotiate to "prevailing party" |
| Non-refundable "deposit" | Deposits are refundable by definition in most states | Fees can be non-refundable; deposits cannot. Get it renamed |

## True Cost Comparison

Rent is 60-80% of actual cost. Build the full picture:

| Line | Notes |
|------|-------|
| Base rent | |
| Utilities not included | Ask for last tenant's avg bills. Electric heat in cold climate can add $200+/mo |
| Parking | Can be $100-400/mo in cities |
| Pet rent + pet deposit | Often $25-75/mo + $200-500 upfront |
| Renters insurance | ~$15-25/mo, often required |
| Laundry | In-unit vs coin-op = ~$40/mo difference |
| Commute delta | 20 extra min each way × gas/transit × 22 days |
| **Move-in:** first + last + security (often 1 mo) + app fee ($25-100) + broker fee (0-15% annual rent in NYC/Boston) | |

Always present true monthly cost alongside base rent when comparing listings.

## Rent Negotiation

Works best in soft markets or with private landlords (corporate property managers have less flexibility).

- **Leverage:** longer lease term (18-24 mo), move-in during winter (Nov-Feb = lowest demand), proof of income >3× rent, 750+ credit, offer to start lease immediately on a vacant unit
- **Ask for:** $50-100/mo off, one month free (amortize it), waived app/admin fee, free parking spot, waived pet deposit
- **Data:** pull 3 comps from Zillow/Apartments.com at lower rent, bring printouts

## Before Move-In

- Video walkthrough with timestamps — every wall, inside every cabinet, run every faucet. Email it to yourself AND the landlord same-day
- Test: all outlets, water pressure hot+cold, all appliances, HVAC in both modes, every window lock, smoke detectors

## Interactive Map — Web App Visualization

After gathering listings, **build a web app** that displays all found apartments on an interactive map so the user can visually compare locations.

### Requirements

- **Color-coded markers** by tier: green = Best Value, blue = Strong Mid-Range, orange = Top of Budget, red = flagged/suspicious
- **Popup on each marker** showing: address, price, beds/baths, sqft, key features, and a link to the listing
- **Sidebar or panel** with the full listing list — clicking a listing pans/zooms to its marker

### Geocoding Addresses

Use the free Nominatim API (OpenStreetMap) to convert addresses to lat/lng — no API key required:

```text
https://nominatim.openstreetmap.org/search?q={url_encoded_address}&format=json&limit=1
```

Rate limit: max 1 request/second. Batch geocode all listings before building the map, and hardcode the coordinates into the app.

Always generate the map alongside the text-based listing output — the map is a visual complement, not a replacement for the detailed listings.

## Limitations

- Cannot access live MLS/listing feeds directly — use `webSearch` and `webFetch` to pull from public listing sites
- Listing data changes daily — always note the search date and tell users to verify availability
- Ownership verification requires user to check county records
- Lease law varies by state — flag issues, recommend local tenant-rights org for specifics

```

---

## Secondary Skill: branding-generator

**Path:** `.local/secondary_skills/branding-generator/SKILL.md`

```markdown
---
name: branding-generator
description: Create brand identity kits with color palettes, typography, logo concepts, and brand guidelines.
---

# Branding Generator

Create brand identity kits. Interview the user, research the space, then deliver 3 distinct brand directions with visual assets.

## When to Use

- "I need branding / a brand identity / brand kit"
- Color palettes, typography, visual identity from scratch
- Rebranding or brand refresh

## When NOT to Use

- Full UI design (use design skill) · Slide decks (use slides skill)

## Step 1: Brand Interview

Conduct this like a real branding agency discovery session. Ask these questions **conversationally, not as a wall of text** — adapt based on answers, ask follow-ups, go deeper where it matters. Group into 2-3 messages max.

### Round 1 — The Business

- What does your company/product do, in one sentence?
- Who is your target audience? (Be specific — age, role, lifestyle, not just "everyone")
- What problem do you solve that nobody else does?
- What's your pricing position? (Budget / mid-market / premium / luxury)

### Round 2 — The Feeling

- Name 3 brands you admire (any industry) and what you admire about them
- If your brand were a person, how would they dress? How would they speak?
- What emotions should someone feel when they see your brand for the first time?
- What's the one word you'd want people to associate with you?
- Any colors, styles, or aesthetics you absolutely hate?

### Round 3 — Practical Constraints

- Do you have any existing brand assets (logo, colors, fonts) you want to keep?
- Where will this brand primarily live? (Web app, mobile app, physical product, social media, print)
- Any industry conventions you need to follow — or deliberately break?
- Competitor URLs or screenshots? (If provided, extract their palettes with colorthief for contrast analysis)

**Do not proceed until you have solid answers.** Push back if answers are vague — "everyone" is not a target audience, "clean and modern" is not a personality.

## Step 2: Research

After the interview, do targeted research before generating directions:

- **Competitor analysis** — If the user named competitors or you can infer them, search for their visual identities. Extract color palettes from screenshots using colorthief. Note what's common in the space so you can differentiate.
- **Mood/reference gathering** — Search for visual references matching the interview answers (e.g., "minimalist premium SaaS branding", "bold playful fintech design").
- **Industry conventions** — What do users in this space expect? Where is there room to stand out?

## Step 3: Generate 3 Brand Directions

**Always present exactly 3 distinct directions.** Each should feel like a different creative team's pitch — not slight variations.

For each direction, provide:

1. **Concept name & 1-2 sentence narrative** — the strategic thinking behind this direction
2. **Color palette** — primary, secondary, accent with hex + OKLCH values. Include neutral scale (50-900) tinted toward the primary hue. Verify WCAG AA contrast for all text/background pairs.
3. **Typography** — display + body font pairing from Google Fonts with rationale
4. **Voice** — 3-5 adjectives defining how the brand speaks, plus an example headline
5. **Visual mood** — overall aesthetic description (photography style, illustration approach, texture usage). Reference 2-3 real-world brands that share elements.

## Step 4: User Picks a Direction

Present all 3 and ask the user to pick one or mix elements. Don't proceed to assets until they approve.

## Step 5: Deliver the Brand Kit

Once a direction is approved, **delegate to the design subagent** (`subagent` with `specialization="DESIGN"`) to build polished visual boards. Embed them as iframes on the canvas.

### Deliverables

**Board 1 — Color & Typography:** Color swatches with hex + OKLCH values, shade ramps (50-900), typography specimen at heading/body/caption sizes with Google Fonts loaded, contrast audit table, dark mode variant.

**Board 2 — Logo Concepts:** 3-4 logo variations (wordmark, icon+text, icon-only) built as **inline SVG**. Show on light and dark backgrounds at multiple sizes. Include SVG source for export.

**Board 3 — Brand in Action:** A realistic mock landing page using the brand's colors, fonts, and voice. Should look like a real product page, not a wireframe.

**Board 4 — Brand Guidelines:** Color usage rules, typography hierarchy, voice & tone guidelines, 1-2 sample applications (business card, social post).

### Exportable Tokens

Also provide in chat:

- **CSS custom properties** — `--primary: #2563eb; --primary: oklch(60% 0.18 250);`
- **Tailwind config** — `colors: { primary: { 50: '...', ..., 900: '...' } }`

## Color Science

- Work in OKLCH color space (perceptually uniform — same L = same perceived lightness across hues)
- Use color harmony from OKLCH hue space: complementary (H+180°), analogous (H±30°), triadic (H±120°), split-comp (H+150°/H+210°)
- Generate shade ramps by stepping L linearly in OKLCH — avoids the muddy-middle problem of RGB interpolation
- WCAG 2.2 AA: 4.5:1 contrast for normal text, 3:1 for large text and UI components
- Use chroma-js or apcach for programmatic contrast verification
- Dark mode: backgrounds at `oklch(15-20% 0.01 H)` not pure black. Desaturate brand colors slightly (reduce C by ~0.02).

## Limitations

- Logo concepts are starting points — final production logos should be refined with a dedicated designer
- Fonts limited to Google Fonts / open-source unless user provides custom fonts

```

---

## Secondary Skill: competitive-analysis

**Path:** `.local/secondary_skills/competitive-analysis/SKILL.md`

```markdown
---
name: competitive-analysis
description: Perform competitive market analysis with feature comparisons, positioning, and strategic recommendations.
---

# Competitive Analysis

Identify competitors, analyze positioning, and deliver actionable recommendations. Skip textbook frameworks (Porter's, PESTLE) unless specifically requested — they're MBA artifacts, not operator tools.

## When to Use

- "Who are my competitors?" / "How do we compare to X?"
- Feature comparison matrix or positioning map needed
- Fundraising deck competition slide
- Finding market gaps

## When NOT to Use

- General market sizing (use deep-research)
- SEO-specific competitor keyword analysis (use seo-auditor)

## What Practitioners Actually Use

Skip Porter's Five Forces. Operators use these four:

**1. April Dunford's Positioning (from "Obviously Awesome")** — the most-used positioning method in B2B SaaS. Five inputs in strict order:

   1. Competitive alternatives (what customers would do if you didn't exist — including "spreadsheets" and "nothing")
   2. Unique attributes you have that alternatives lack
   3. Value those attributes deliver (with proof)
   4. Best-fit customer characteristics
   5. Market category you win in
   Key insight: positioning starts from *alternatives*, not features. Your "competitor" might be Excel.

**2. Wardley Mapping** (Simon Wardley, free book at medium.com/wardleymaps) — plot components on two axes: visibility-to-user (y) vs evolution Genesis → Custom → Product → Commodity (x). Reveals: where competitors overinvest in commoditizing components, where to build vs buy, what's about to become table stakes. Tool: onlinewardleymaps.com (free). Best for platform/infra competition.

**3. Feature comparison matrix** — the unglamorous workhorse. Rows = capabilities, columns = competitors, cells = ✓/✗/partial. Battlecards for sales teams are this + "trap-setting questions." Key: weight features by how often they appear in lost-deal notes, not by what engineering thinks matters.

**4. Kano mapping applied to competitors** — categorize each competitor feature as Basic (expected, table stakes), Performance (more = better), or Delighter (unexpected). Kano's insight: today's delighters become tomorrow's basics. Competitors' delighters tell you where the bar is moving.

## Research Toolchain

| Need | Tool | How to use |
|---|---|---|
| Find competitors | `webSearch("[product] alternatives site:g2.com")` | G2's "alternatives" pages are crowdsourced competitor lists |
| Verified user complaints | `webSearch("[competitor] site:g2.com")`, Capterra, TrustRadius | Filter reviews to 1-3 stars. Look for repeated phrases — those are exploitable weaknesses |
| Enterprise IT buyers | PeerSpot (formerly IT Central Station) | More technical, less marketing-gamed than G2 |
| Pricing (often hidden) | `webFetch` competitor /pricing page, Wayback Machine for historical, `webSearch("[competitor] pricing reddit")` for leaked enterprise quotes | |
| Tech stack | `webFetch("https://builtwith.com/[domain]")` — 673M+ sites, 85k+ technologies. Wappalyzer similar. | Reveals: are they on legacy stack? What vendors? Switching cost signals |
| Traffic/channel mix | SimilarWeb (reliable for large sites, unreliable <50k visits/mo) | See which channels drive competitor traffic |
| Funding/team size | Crunchbase free tier, `webSearch("[competitor] raises TechCrunch")` | |
| Strategic direction | `webSearch("[competitor] site:linkedin.com/jobs")` — hiring = roadmap. 5 ML engineers = AI features in 6mo. | |
| Historical messaging | `webFetch("https://web.archive.org/web/2024*/[competitor].com")` | Shows positioning pivots — what they tried and abandoned |
| SEO/content strategy | Ahrefs (paid, $129+/mo) or `webSearch("site:[competitor].com")` to map content | |

## Methodology

**Step 1: Frame** — Get from user: their product, target customer, and who THEY think competes. Their list is always incomplete.

**Step 2: Expand the competitor set** — Run `webSearch("[known competitor] alternatives")` and `webSearch("[category] vs")`. Check G2 category pages. Add indirect competitors (different product, same job) and the "do nothing" option.

**Step 3: Per-competitor dossier** — For each (limit to 5-7 for depth):

- Positioning one-liner (their homepage H1)
- Pricing model + tiers (webFetch pricing page; screenshot if complex)
- Top 3 strengths (from 5-star G2 reviews)
- Top 3 weaknesses (from 1-2 star G2 reviews — use exact customer language)
- Funding stage + headcount (Crunchbase/LinkedIn)
- Recent product launches (changelog, blog, Product Hunt)

**Step 4: Synthesize** — Build the feature matrix. Plot on a 2×2 (pick the two axes the *buyer* cares about, not the ones that make user look good). Identify white space.

**Step 5: Recommend** — Not "monitor the threat." Specific: "Competitor X's reviews mention slow support 23 times — lead with your SLA in sales calls."

## Output — Ask the User First

Before building any deliverable, **ask the user how they want the analysis presented** using the query tool:

> "How would you like your competitive analysis presented — as a **slide deck** or a **written report**?"

Then follow the appropriate path below. Do not default to one format without asking.

---

### Option A: Slide Deck

**Load the `slides` skill** and build a Replit slide deck. Follow the slides skill's conventions for manifest, components, and design. Structure the deck as:

1. **Title slide** — Product name, category, date
2. **Executive summary** — Positioning statement (Dunford format) + top 3 recommendations
3. **Competitive landscape** — Table: Company, Stage, Pricing, Strength, Weakness
4. **Feature matrix** — Rows = capabilities, columns = competitors, cells = checkmark/x/partial, color-coded
5. **Positioning map** — 2×2 chart (matplotlib/plotly image)
6. **White space & opportunities** — Gaps + Kano analysis
7. **Action plan** — Top 3 specific actions + battlecard trap-setting questions
8. **Sources** — Numbered URLs for every claim

---

### Option B: Written Report (PDF + Web Preview)

**Do not output a markdown summary.** Build a polished competitive analysis report as a professional PDF using **jsPDF**, with a React web preview that visually matches page-by-page. The report should look like a strategy consulting deliverable.

**Build order:** Generate the PDF first and present it to the user. Then build the web preview. The PDF is the primary deliverable — the web app is a visual complement.

#### Report Structure

1. **Page 1 — Executive Summary:** Product name, category, date. Positioning statement (Dunford format): For [target customer] who [need], [product] is a [category] that [key benefit]. Unlike [primary alternative], we [key differentiator]. Top 3 strategic recommendations (the "so what").
2. **Page 2 — Competitive Landscape:** Table with Company, Stage, Pricing, Strength (from reviews), Weakness (from reviews). Funding/headcount context for each competitor.
3. **Page 3 — Feature Matrix:** Rows = capabilities, columns = competitors, cells = checkmark/x/partial. Weight column (1-5) based on buyer conversation frequency. Color-code: green where the user's product wins, red where it loses.
4. **Page 4 — Positioning Map:** 2x2 chart with axes based on buyer decision criteria (not vanity metrics). Each competitor plotted with logo or labeled dot. Generated via matplotlib or plotly, embedded as image.
5. **Page 5 — White Space & Opportunities:** Gaps no one serves well, with evidence from reviews and market data. Kano analysis: which competitor features are Basics vs Performance vs Delighters.
6. **Page 6 — Action Plan:** Top 3 specific actions with source citations. Battlecard-style "trap-setting questions" for sales calls.
7. **Final Page — Sources:** Numbered URLs for every claim.

#### PDF Generation (jsPDF)

Use **jsPDF** to generate the PDF with explicit point-based layout:

- `new jsPDF({ unit: "pt", format: "letter" })` — US Letter: 612×792pt
- Use 36pt margins (0.5in). Content area: 540w × 720h points.
- **Track Y position** as you render each element. When the next element would exceed `PAGE_H - MARGIN`, call `doc.addPage()` and reset Y to the top margin. Never let content silently overflow — always check before rendering.
- Embed charts as images via `doc.addImage()` — scale to fit content width while respecting remaining page height.
- Add a **header** and **footer** on each page. **Footer must save/restore Y position** — do not let footer drawing move the content cursor, or subsequent content will force blank pages.
- Before any manual page break, check whether a fresh page was already added (track an `isNewPage` flag). Only add a page if you're not already on a fresh one.
- **Required before presenting:** After generating the PDF, verify there are no blank pages. If any page is blank, fix the page-break logic and regenerate.

#### Web Preview

The React web artifact renders the same report data as an HTML version that **visually mirrors the PDF page-by-page**. Each "page" should be a fixed-size container (816×1056px — US Letter at 96dpi) with the same margins, typography, and chart placement as the PDF.

## Honesty Rules

- If the user's product loses on most dimensions, say so — then find the niche where they win
- "No competitors" is never true. The competitor is always at least "build it yourself" or "do nothing"
- Flag when data is thin (e.g., "SimilarWeb shows <50k visits — estimate is low-confidence")
- Cite every claim to a URL the user can verify

## Limitations

- G2/Capterra reviews skew toward mid-market SaaS; thin for enterprise and consumer
- SimilarWeb is inaccurate for sites under ~50k monthly visits
- Cannot access paid CI tools (Klue, Crayon, Kompyte) or PitchBook
- Pricing pages lie — enterprise pricing is almost never public

```

---

## Secondary Skill: content-machine

**Path:** `.local/secondary_skills/content-machine/SKILL.md`

```markdown
---
name: content-machine
description: Create social media posts, newsletters, and marketing content calibrated to your voice and platform.
---

# Content Machine

Create social posts, newsletters, and marketing copy that respects platform mechanics — truncation points, algorithm signals, and hook physics — not just "good writing."

## When to Use

- Social posts (X/Twitter, LinkedIn, Instagram, TikTok captions, Threads)
- Newsletters, blog posts, content calendars, cross-platform repurposing

## When NOT to Use

- Cold outreach (cold-email-writer) · Paid ad copy (ad-creative) · Research reports (deep-research) · SEO audits (seo-auditor)

## Step 1: Voice Analysis

Ask for 3-5 existing posts. Extract: avg sentence length, contraction usage, emoji density, POV (I/we/you), signature phrases. If none exist, ask for 2 creators they want to sound like and use `webFetch` to pull recent posts as voice reference.

## Step 2: Platform Mechanics (2025-2026 Specs)

### LinkedIn — 3,000 char max, but truncation is what matters

- **"...see more" cutoff: ~140 chars desktop, ~110 chars mobile.** 57%+ of LinkedIn traffic is mobile — write the hook for 110 chars.
- **Algorithm weights:** comments count ~2x likes; dwell time is a primary signal; first 60-120 min engagement velocity determines reach ceiling.
- **Optimal length:** 800-1,000 chars (not 3,000). Short paragraphs (1-2 lines) + white space increase dwell time.
- **Structure:** Hook (110 chars, no throat-clearing like "I wanted to share...") → story/insight → single question CTA. Reply to every comment in the first hour to extend the test window.
- **Hashtags:** 3-5 max, at the very end. LinkedIn deprioritized hashtag discovery.

### X/Twitter — 280 chars (free), 25,000 chars (Premium)

- Long posts on Premium truncate at ~280 chars in the feed — the hook rule still applies.
- **Thread structure:** Tweet 1 = the full promise ("How I went from X to Y in Z — thread 🧵"). Each tweet must stand alone for retweets. Last tweet = CTA + loop back to tweet 1.
- Line breaks double engagement vs. wall-of-text.

### Instagram — 2,200 char caption, ~125 chars visible before "...more"

- **Hashtags: 3-5, not 30.** Instagram's @creators account officially reversed the old advice; 20+ hashtags now reads as spam and can suppress reach. Put them inline or at the end, not in a comment.
- First line = hook. Emoji as bullet points scan faster than dashes on mobile.

### TikTok captions — 4,000 chars (up from 2,200)

- TikTok is now a search engine — ~40% of Gen Z searches here before Google. Front-load keywords in the caption for TikTok SEO. The caption is indexed; use it for terms your video doesn't say out loud.

### Newsletters — Optimize for clicks, not opens

- **Apple Mail Privacy Protection (MPP) inflates open rates by ~18 percentage points.** Apple Mail is ~46% market share and pre-fetches tracking pixels. A "42% open rate" in 2025 ≈ a 24% open rate in 2020. **Track click rate (benchmark: ~2%) and CTOR (10-20%) instead.**
- **Subject line:** 30-50 chars. Avoid "Free," ALL CAPS, multiple "!!!" — spam filter triggers. B2B: longer, specific subject lines outperform short clever ones.
- **Preview/preheader text:** adds ~6pp to open rate when used — but Gmail's Gemini now auto-generates previews, so don't rely on controlling it. Write the first sentence of the body as a second hook.
- One primary CTA. Every additional CTA cuts click rate.

## Step 3: Hook Formulas (Named Patterns)

Don't say "write a hook" — pick a pattern:

| Pattern | Template | Why it works |
|---|---|---|
| **Contrarian** | "Everyone says X. Here's why that's wrong." | Cognitive dissonance forces resolution |
| **Curiosity gap** | "I tried X for 30 days. Day 17 broke me." | Open loop — brain needs closure |
| **Specificity signal** | "$47,212 in 90 days. Here's the exact stack." | Odd numbers read as true, round numbers read as marketing |
| **Negative hook** | "3 mistakes that cost me [outcome]" | Loss aversion > gain seeking |
| **Callout** | "If you're a [role] still doing X, read this." | Self-selection = higher-intent readers |
| **Slippery slope** | "It started with one Slack message." | Narrative momentum |
| **Permission** | "Unpopular opinion: [take]" | Pre-frames disagreement as expected |

**Banned openers:** "I'm excited to share," "Hey everyone," "As a [title]," "In today's fast-paced world."

## Step 4: Repurposing Waterfall

One long-form piece → 6+ assets:

1. **Blog post** (1,500 words) →
2. **X thread** (extract each H2 as a tweet, intro = hook) →
3. **LinkedIn post** (pick the single most contrarian point, 800 chars) →
4. **LinkedIn carousel** (each H2 = 1 slide; carousels get highest dwell time) →
5. **Newsletter section** (add personal context + behind-the-scenes) →
6. **Instagram carousel** (same slides, 1080×1350, 4:5) →
7. **TikTok/Reel script** (the hook + the #1 takeaway in 30 sec)

Build repurposing scripts in Python when batch-processing: parse markdown H2s → split into platform templates → enforce char limits programmatically.

## Content Frameworks

- **PAS** (Problem → Agitate → Solve) — best for conversion-focused posts
- **BAB** (Before → After → Bridge) — best for transformation stories
- **AIDA** (Attention → Interest → Desire → Action) — best for launches
- **SLAP** (Stop → Look → Act → Purchase) — best for short-form (Reels/TikTok captions)

## Validation

Before delivering, verify: char counts against platform limits (count programmatically, don't eyeball), hook fits in the truncation window, no banned openers, one CTA per piece.

## Limitations

- Cannot post to platforms or access analytics
- Cannot generate images/video (use media-generation skill)
- Voice matching quality scales with example count

```

---

## Secondary Skill: deep-research

**Path:** `.local/secondary_skills/deep-research/SKILL.md`

```markdown
---
name: deep-research
description: Conduct thorough, multi-source research on complex topics with structured findings and citations.
---

# Deep Research

Conduct comprehensive, multi-source research on complex topics. Systematically gather, evaluate, and synthesize information into structured reports with proper citations.

## When to Use

- User needs thorough research on a complex topic
- User asks "research this," "find out about," or "do a deep dive on"
- User needs a literature review, market analysis, or technology evaluation
- User wants to understand a topic from multiple angles with cited sources
- User needs to verify claims or compare conflicting information

## When NOT to Use

- Simple factual lookups (just use web-search directly)
- Searching within the user's own codebase (use grep/glob)
- Looking up Replit-specific features (use replit-docs skill)
- Product recommendations without research depth (use a more specific skill)

## Research Architecture

This skill follows a tree-like exploration pattern inspired by leading open-source research tools:

- **GPT Researcher** (github.com/assafelovic/gpt-researcher, ~17k stars) -- uses "plan and execute" with parallel sub-question research
- **STORM** (github.com/stanford-oval/storm, ~18k stars) -- Stanford's perspective-guided research that simulates multiple expert viewpoints
- **open_deep_research** (github.com/langchain-ai/open_deep_research) -- LangChain's iterative search-and-synthesize approach

The core pattern: decompose the question -> search broadly -> read deeply -> identify gaps -> refine queries -> synthesize with citations.

## Methodology

### Phase 1: Scope Definition

Before starting research, clearly define:

- **Research question**: What specific question(s) are you answering?
- **Scope boundaries**: What is in/out of scope?
- **Depth level**: Overview, moderate analysis, or exhaustive deep-dive?
- **Output expectations**: Report format, length, audience

### Phase 2: Parallel Source Discovery via Subagents

Decompose the topic into **5 distinct focus areas**, then launch **5 research subagents in parallel** using `startAsyncSubagent`. Each subagent gets a specific focus area and set of search terms, searches independently, and returns its findings with citations.

**How to decompose:** After the broad landscape search in Phase 1, identify 5 non-overlapping angles. For example, researching "state of electric vehicles 2026" might decompose into:

1. **Market & Competition** — market share, sales figures, manufacturer rankings
2. **Technology** — battery chemistry, charging standards, range improvements
3. **Policy & Regulation** — government incentives, emissions mandates, trade tariffs
4. **Infrastructure** — charging network growth, grid capacity, urban vs rural
5. **Consumer & Economics** — total cost of ownership, resale value, adoption demographics

**Launch all 5 in parallel:**

```javascript
// Launch 5 research subagents simultaneously
await startAsyncSubagent({
    task: `Research FOCUS AREA 1: [Market & Competition]

Topic context: [brief description of the overall research question]

Your job: Search for information specifically about [focus area]. Run at least 3-4 webSearch queries with different angles:
- [specific search term 1]
- [specific search term 2]
- [specific search term 3]
- [specific search term 4]

For the most promising results, use webFetch to read the full article.

Return your findings as a structured summary with:
- Key facts and data points (with source URLs)
- Notable claims that need cross-referencing
- Gaps or unanswered questions
- At least 5 distinct sources with URLs`
});

// Repeat for focus areas 2-5 with their own tailored search terms
await startAsyncSubagent({ task: `Research FOCUS AREA 2: [Technology] ...` });
await startAsyncSubagent({ task: `Research FOCUS AREA 3: [Policy & Regulation] ...` });
await startAsyncSubagent({ task: `Research FOCUS AREA 4: [Infrastructure] ...` });
await startAsyncSubagent({ task: `Research FOCUS AREA 5: [Consumer & Economics] ...` });

// Wait for all subagents to complete
const results = await waitForBackgroundTasks();
```

Each subagent should:

- Run 3-4 `webSearch` queries with different phrasings and angles
- Use `webFetch` on the 2-3 most relevant results to extract detailed data
- Return structured findings with source URLs
- Flag any claims that conflict with other results

This approach gathers **25+ distinct sources** across 5 focus areas simultaneously, producing far more comprehensive coverage than sequential searching.

After collecting all subagent results, proceed to Phase 3 to evaluate and cross-reference.

### Phase 3: Source Evaluation

Assess each source for credibility:

- **Authority**: Who published it? What are their credentials?
- **Currency**: When was it published? Is the information still current?
- **Objectivity**: Is there obvious bias? Is it sponsored content?
- **Accuracy**: Can claims be cross-referenced with other sources?
- **Coverage**: Does it cover the topic in sufficient depth?

Use webFetch to read full articles from the most promising search results.

### Phase 4: Information Synthesis

Organize findings thematically (what separates deep research from simple search):

- Group related findings across sources
- Identify areas of consensus and disagreement
- Note gaps in available information -- conduct follow-up searches to fill them
- Cross-reference critical claims across at least 2-3 independent sources
- Build a narrative that answers the research question
- Distinguish between established facts, expert opinions, and speculation
- Draw connections between sources that reveal patterns not visible in any single source

### Phase 5: Report Writing

Structure the final report clearly:

- Lead with the most important findings
- Support claims with specific sources
- Acknowledge limitations and uncertainties
- Provide actionable recommendations where appropriate

## Output Format

### Research Report Structure

```text

# [Research Topic]

## Executive Summary
[2-3 paragraph overview of key findings and conclusions]

## Background
[Context needed to understand the topic]

## Key Findings

### Finding 1: [Theme]
[Detailed analysis with source citations]

### Finding 2: [Theme]
[Detailed analysis with source citations]

### Finding 3: [Theme]
[Detailed analysis with source citations]

## Analysis
[Cross-cutting analysis, patterns, implications]

## Limitations
[What couldn't be determined, data gaps, caveats]

## Recommendations
[Actionable next steps based on findings]

## Sources
[Numbered list of all sources with URLs]

```

## Best Practices

1. **Cast a wide net first, then narrow** -- start with broad searches before diving into specifics
2. **Cross-reference critical claims** -- never rely on a single source for important facts
3. **Cite everything** -- every factual claim should trace back to a source
4. **Note disagreements** -- when sources conflict, present both sides and analyze why
5. **Timestamp your research** -- note when the research was conducted, as information changes
6. **Separate facts from analysis** -- clearly distinguish between what sources say and your interpretation

## Example Workflow

```javascript
// Phase 1: Broad landscape search to identify focus areas
const overview = await webSearch({ query: "state of electric vehicle market 2026" });

// Phase 2: Launch 5 parallel research subagents
await startAsyncSubagent({
    task: `Research EV Market & Competition: search for "EV market share by manufacturer 2025 2026",
    "electric vehicle sales global rankings", "Tesla BYD market share comparison".
    Use webFetch on best results. Return findings with source URLs.`
});
await startAsyncSubagent({
    task: `Research EV Battery Technology: search for "solid state battery progress 2026",
    "EV battery cost per kwh trend", "lithium iron phosphate vs NMC comparison".
    Use webFetch on best results. Return findings with source URLs.`
});
await startAsyncSubagent({
    task: `Research EV Policy & Regulation: search for "EV tax credit policy 2026",
    "emissions regulations electric vehicles", "EV tariffs trade policy".
    Use webFetch on best results. Return findings with source URLs.`
});
await startAsyncSubagent({
    task: `Research EV Charging Infrastructure: search for "EV charging network growth statistics",
    "NACS vs CCS charging standard adoption", "fast charging stations by country".
    Use webFetch on best results. Return findings with source URLs.`
});
await startAsyncSubagent({
    task: `Research EV Consumer Economics: search for "EV total cost of ownership vs gas 2026",
    "electric vehicle resale value trends", "EV adoption demographics income".
    Use webFetch on best results. Return findings with source URLs.`
});

// Collect all results
const results = await waitForBackgroundTasks();

// Phase 3-5: Evaluate sources, cross-reference claims, synthesize into structured report
// Write comprehensive report with all findings and citations from all 5 subagents

```

## Limitations

- Cannot access paywalled academic journals or subscription databases
- Cannot access social media content (LinkedIn, Twitter, Reddit)
- Web sources may have varying levels of reliability
- Research is a snapshot in time -- findings may change
- Cannot conduct primary research (surveys, interviews, experiments)

```

---

## Secondary Skill: design-thinker

**Path:** `.local/secondary_skills/design-thinker/SKILL.md`

```markdown
---
name: design-thinker
description: Apply IDEO-style design thinking methodology to solve complex problems creatively, then present the analysis on canvas and/or as a web artifact.
---

# Design Thinking

Apply human-centered problem solving. Three frameworks dominate industry practice — pick based on what the user actually needs, don't default to IDEO's 5 phases.

## When to Use

- Ambiguous problem space, no obvious solution
- "Why aren't users adopting X?" / "What should we build next?"
- Stuck and needs structured divergence

## When NOT to Use

- Known problem, known solution, just needs execution (skip straight to PRD)
- Visual/UI implementation (use design skill)
- Technical debugging

## Three Frameworks — Choose Wisely

### 1. Double Diamond (UK Design Council, 2004) — for ambiguous problems

Two diamonds = two diverge-then-converge cycles. **Discover** (go wide on problem research) → **Define** (narrow to problem statement) → **Develop** (go wide on solutions) → **Deliver** (narrow to one, ship it).

Critical insight: most teams skip the first diamond and jump straight to solution brainstorming. The first diamond exists to prevent solving the wrong problem beautifully.

**Use when**: problem isn't yet defined, timeline is weeks not days.

### 2. GV Design Sprint (Jake Knapp, Google Ventures, 2010) — for validation speed

5 days, 5 phases, hard time-box. Map (Mon) → Sketch (Tue) → Decide (Wed) → Prototype (Thu) → Test with 5 real users (Fri). Full method free at `gv.com/sprint` and `designsprintkit.withgoogle.com`.

**Known weakness**: users appear on Day 5, not Day 1. The sprint relies on team intuition to frame the problem — you can spend 5 days sprinting toward the wrong target. Fix: run JTBD interviews *before* the sprint to pick the problem.

**Use when**: problem is defined, team can commit 5 uninterrupted days, you need a go/no-go decision fast.

**"5 users" is not arbitrary**: Nielsen Norman Group research shows 5 users find ~85% of usability problems. Diminishing returns after that.

### 3. JTBD Switch Interview (Bob Moesta / Re-Wired Group) — for understanding why people buy

Not a workshop — a forensic interview technique. Interview people who *recently switched* (bought your product, or churned to a competitor). 45-60 minutes. Reconstruct their timeline, don't ask about features.

**The Timeline** (walk backward through their actual purchase):

1. **First thought** — when did it first occur to you this was a problem?
2. **Passive looking** — noticing solutions but not acting
3. **Event one** — something happens that makes it urgent
4. **Active looking** — comparing options, raised hand
5. **Deciding** — what tipped it?
6. **Buying** — the actual moment

**The Four Forces** (what made the switch happen):

| Force | Direction | Probe |
|---|---|---|
| Push of the situation | Toward switch | "What was happening that made the old way stop working?" |
| Pull of the new solution | Toward switch | "When you imagined having this, what got you excited?" |
| Anxiety of the new | Against switch | "What worried you about switching?" |
| Habit of the present | Against switch | "What was good enough about what you had?" |

Switch only happens when Push + Pull > Anxiety + Habit. If someone didn't buy, one of the blocking forces won.

**Key technique**: ask about the *situation*, never the feature. Not "do you like the dashboard?" but "walk me through the last time you opened it — what were you in the middle of?" Reference: the "Mattress Interview" at `jobstobedone.org` — Moesta interviews a guy about buying a mattress for 45 min and uncovers it was actually about his marriage.

**Use when**: you have customers but don't understand why they chose you, or you're losing deals and don't know why.

## Core Tools (Framework-Agnostic)

**How Might We (HMW)** — reframe problem as opportunity. Scope test: too narrow bakes in the solution ("HMW add a share button"), too broad is unactionable ("HMW make users happy"). Right: "HMW help busy parents find 20-minute recipes without meal-planning guilt?"

**Crazy 8s** (from GV Sprint) — fold paper into 8 panels, sketch 8 distinct ideas in 8 minutes. Forces past the obvious first 3 ideas. Works solo or in groups.

**Assumption Mapping** — plot assumptions on Importance × Evidence 2×2. High-importance + low-evidence = test first. This picks your prototype target.

**Empathy Map** (Dave Gray, XPLANE) — Say / Think / Do / Feel quadrants around a user. "Think" and "Feel" are where insight lives — they're the gap between what users say and what they do.

**5-Act Interview** (GV test-day script): Friendly welcome → context questions → intro the prototype → tasks (watch, don't help) → debrief. One person interviews, team watches on video in another room and takes notes.

## Output Format

```markdown

# [Challenge]

## Framework Used
[Double Diamond / GV Sprint / JTBD — and why this one]

## Problem Definition

### HMW Statement

### Key Insights (with evidence — quote or observation, not assumption)

## [If JTBD] Forces Diagram
| Push | Pull | Anxiety | Habit |
|---|---|---|---|

## Solution Concepts
| Concept | Desirable? | Feasible? | Viable? | Riskiest assumption |
|---|---|---|---|---|

## Prototype Plan

- What to build (lowest fidelity that tests the assumption)
- Who to test with (5 users, recruited how)
- What "success" looks like

## Next Steps

```

## Canvas Presentation

When presenting design thinking analysis on the canvas, follow these rules for a clear, skimmable board.

### Shape Types & When to Use Each

| Shape | Use For | Why |
|---|---|---|
| `note` (sticky note) | Section headers, sidebar annotations, key stats | Fixed 200px width. Auto-sizes font based on text length — fewer words = bigger text. Perfect for bold single-word headers. |
| `geo` (rectangle) | Content cards, full-width banners, problem statements | Respects `w` and `h` — use for wide content (500px+ cards, 1600px+ banners). Set `fill: "solid"` and pick a color. |
| `geo` (arrow-down / arrow-right) | Flow indicators between sections | Shows the progression through the framework. Use `fill: "solid"`. |
| `text` | Small inline labels like "vs" between forces | Auto-sizes, minimal visual weight. |

### Layout Rules

1. **Headers as sticky notes with minimal text** — Use 1-2 words max (e.g., "DISCOVER", "DEFINE", "FORCES"). The note shape auto-scales font size inversely to text length, so short text = large, skimmable headers.

2. **Content cards as geo rectangles** — 500px wide for 3-column layouts, 780px for 2-column layouts, 1600px+ for full-width banners. Always set `fill: "solid"` and a color.

3. **Left-column header notes, right-side content** — Place header sticky notes at x=1400, content cards starting at x=1670 (leaving a 70px gap after the 200px-wide header note).

4. **Vertical spacing** — 80-100px between rows within a section, 120-150px between sections. This keeps the board breathable and skimmable.

5. **Arrow shapes between sections** — Place `geo` shapes with `arrow-down` geo centered horizontally between sections to show flow. Use the section's color.

6. **Annotation stickies as sidebar** — Place `note` shapes at x=3350 (far right) aligned vertically with their related section. Use for market stats, key quotes, risk callouts — short punchy content that adds context without cluttering the main flow.

7. **Color coding by section** — Be consistent:
   - Violet: title, concepts
   - Blue: discover
   - Green: define
   - Orange: develop / forces
   - Red: deliver
   - Yellow: key callouts (problem statement, switch rule, recommendation)
   - Light-* variants for content cards within each section

8. **JTBD Forces layout** — Use 2x2 grid: Push (top-left, light-red) vs Pull (top-right, light-green), Anxiety (bottom-left, orange) vs Habit (bottom-right, grey). Place arrow-right shapes and "vs" text labels between the pairs.

### Canvas Gotchas

- **Sticky notes (`note` type) are always 200px wide** — the `w` parameter is ignored. Plan layouts around this constraint.
- **`labelColor: "white"` can cause rendering errors** — avoid it. Use lighter fill colors where default black text is readable.
- **`color: "black"` on geo shapes with `fill: "solid"` causes errors** — use `grey` or a dark supported color instead.
- **Always call `get_canvas_state` before placing shapes** — check for existing content and find empty space.
- **Delete before recreate** — when updating shapes, delete first then create fresh. Updates to notes can behave unexpectedly.

### Example: Placing a Section

```text
1. Header note (big text):
   { type: "note", x: 1400, y: Y, w: 200, h: 200, color: "blue", text: "DISCOVER" }

2. Content cards (3-column):
   { type: "geo", geo: "rectangle", x: 1670, y: Y, w: 500, h: 260, color: "light-blue", fill: "solid", text: "..." }
   { type: "geo", geo: "rectangle", x: 2220, y: Y, w: 500, h: 260, color: "light-violet", fill: "solid", text: "..." }
   { type: "geo", geo: "rectangle", x: 2770, y: Y, w: 500, h: 260, color: "light-green", fill: "solid", text: "..." }

3. Flow arrow to next section:
   { type: "geo", geo: "arrow-down", x: 2300, y: Y+300, w: 80, h: 60, color: "blue", fill: "solid" }

4. Sidebar annotation:
   { type: "note", x: 3350, y: Y, w: 200, h: 200, color: "yellow", text: "$45.5B\nmarket by 2028" }
```

## Research

- `webSearch("[user's problem domain] user research")` for prior art
- `webFetch("https://www.gv.com/sprint/")` for full sprint method
- `webSearch("[product category] reviews site:reddit.com")` — unfiltered user language for push/anxiety forces
- IDEO Design Kit free methods: `designkit.org/methods`

## Hard Truths

- Agent cannot run real interviews — can write the discussion guide, analyze transcripts the user pastes in, and build the synthesis
- Personas without research are fiction. Push user for real data (support tickets, reviews, churn interviews) before building empathy maps
- Most "design thinking" fails because teams do ideation theater and skip the uncomfortable research. Bias toward the first diamond

```

---

## Secondary Skill: excel-generator

**Path:** `.local/secondary_skills/excel-generator/SKILL.md`

```markdown
---
name: excel-generator
description: Create professional Excel spreadsheets with formatting, formulas, charts, and data validation
---

# Excel & Spreadsheet Generator

Create .xlsx files with formulas, formatting, charts, and data validation.

## Library Selection

| Need | Use | Install |
|---|---|---|
| Create new .xlsx from scratch, fast, large files | **xlsxwriter** | `pip install xlsxwriter` |
| Read/modify existing .xlsx, or round-trip edits | **openpyxl** | `pip install openpyxl` |
| Read legacy .xls (Excel 97-2003) | **xlrd** | `pip install xlrd` |
| Dump a DataFrame quickly | `df.to_excel()` | uses openpyxl/xlsxwriter as engine |

**Key gotchas:**

- Neither openpyxl nor xlsxwriter can read `.xls` — only `.xlsx`. Use `xlrd` for `.xls`.
- xlsxwriter is **write-only** — it cannot open an existing file. Use openpyxl to edit.
- openpyxl uses ~50x the file size in RAM. For 100K+ rows, use xlsxwriter or `openpyxl.Workbook(write_only=True)`.
- Formulas are **stored as strings** — Python does not evaluate them. Excel computes on open. `openpyxl` reading a formula cell gives you `=SUM(A1:A10)`, not the result (unless you use `data_only=True`, which reads the last cached value).

## Core Recipe — openpyxl

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.formatting.rule import ColorScaleRule, DataBarRule
from openpyxl.worksheet.datavalidation import DataValidation

wb = Workbook()
ws = wb.active
ws.title = "Sales"

# --- Write data ---
headers = ["Product", "Units", "Price", "Revenue"]
ws.append(headers)
rows = [("Widget", 120, 9.99), ("Gadget", 80, 14.50), ("Gizmo", 200, 4.25)]
for r in rows:
    ws.append(r)

# --- Formulas (Excel computes these on open) ---
for row in range(2, len(rows) + 2):
    ws[f"D{row}"] = f"=B{row}*C{row}"
ws[f"D{len(rows)+2}"] = f"=SUM(D2:D{len(rows)+1})"

# --- Header styling ---
header_fill = PatternFill(start_color="2F5496", fill_type="solid")
thin = Side(border_style="thin", color="CCCCCC")
for cell in ws[1]:
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal="center")
    cell.border = Border(bottom=Side(border_style="medium"))

# --- Number formats ---
for row in ws.iter_rows(min_row=2, min_col=3, max_col=4):
    for cell in row:
        cell.number_format = '"$"#,##0.00'

# --- Column widths (auto-fit approximation) ---
for col in ws.columns:
    max_len = max(len(str(c.value or "")) for c in col)
    ws.column_dimensions[get_column_letter(col[0].column)].width = max_len + 3

# --- Freeze header row ---
ws.freeze_panes = "A2"

# --- Excel Table (enables filtering, structured refs, banded rows) ---
tab = Table(displayName="SalesTable", ref=f"A1:D{len(rows)+1}")
tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True)
ws.add_table(tab)

# --- Conditional formatting: data bars on Revenue ---
ws.conditional_formatting.add(f"D2:D{len(rows)+1}",
    DataBarRule(start_type="min", end_type="max", color="638EC6"))

# --- Dropdown validation ---
dv = DataValidation(type="list", formula1='"Active,Paused,Archived"', allow_blank=True)
ws.add_data_validation(dv)
dv.add("E2:E100")

wb.save("output.xlsx")

```

## Charts (openpyxl)

```python
from openpyxl.chart import BarChart, LineChart, PieChart, Reference

chart = BarChart()
chart.title = "Revenue by Product"
chart.y_axis.title = "Revenue ($)"
data = Reference(ws, min_col=4, min_row=1, max_row=4)  # includes header for series name
cats = Reference(ws, min_col=1, min_row=2, max_row=4)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
ws.add_chart(chart, "F2")  # anchor cell

```

**Chart gotchas:**

- `Reference` uses 1-indexed rows/cols (not 0-indexed).
- `titles_from_data=True` consumes the first row of the data range as the series label — include the header row in `data` but NOT in `cats`.
- Supported: `BarChart`, `LineChart`, `PieChart`, `ScatterChart`, `AreaChart`, `DoughnutChart`, `RadarChart`. 3D variants exist but render inconsistently.
- Charts reference cells — if you later insert rows above, the chart range does NOT auto-adjust.

## xlsxwriter (faster, write-only, richer formatting)

```python
import xlsxwriter

wb = xlsxwriter.Workbook("report.xlsx")
ws = wb.add_worksheet("Data")

header_fmt = wb.add_format({"bold": True, "bg_color": "#2F5496", "font_color": "white", "border": 1})
money_fmt  = wb.add_format({"num_format": "$#,##0.00"})

ws.write_row(0, 0, ["Product", "Units", "Price", "Revenue"], header_fmt)
data = [("Widget", 120, 9.99), ("Gadget", 80, 14.50)]
for i, (p, u, pr) in enumerate(data, start=1):
    ws.write(i, 0, p)
    ws.write(i, 1, u)
    ws.write(i, 2, pr, money_fmt)
    ws.write_formula(i, 3, f"=B{i+1}*C{i+1}", money_fmt)

ws.autofit()         # xlsxwriter has true autofit; openpyxl does not
ws.freeze_panes(1, 0)
wb.close()           # MUST call close() or file is corrupt

```

## pandas Shortcut (multi-sheet with formatting)

```python
import pandas as pd

with pd.ExcelWriter("out.xlsx", engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Data", index=False)
    summary.to_excel(writer, sheet_name="Summary", index=False)

    # Access underlying workbook for formatting
    wb, ws = writer.book, writer.sheets["Data"]
    ws.set_column("A:A", 20)
    ws.autofilter(0, 0, len(df), len(df.columns) - 1)

```

## Common Formula Patterns

| Need | Formula |
|---|---|
| Running total | `=SUM($B$2:B2)` (drag down) |
| Lookup (modern) | `=XLOOKUP(A2, Data!A:A, Data!C:C, "Not found")` |
| Lookup (compat) | `=VLOOKUP(A2, Data!A:C, 3, FALSE)` |
| Conditional sum | `=SUMIFS(C:C, A:A, "Widget", B:B, ">100")` |
| Count matching | `=COUNTIFS(A:A, "Active")` |
| Percent of total | `=B2/SUM($B$2:$B$100)` |
| Safe division | `=IFERROR(A2/B2, 0)` |

**Gotcha:** When writing formulas from Python, use US-English function names and comma separators regardless of the user's locale. Excel translates on open.

## Number Format Codes

| Format | Code |
|---|---|
| Currency | `"$"#,##0.00` |
| Thousands | `#,##0` |
| Percent | `0.0%` |
| Date | `yyyy-mm-dd` |
| Negative in red | `#,##0;[Red]-#,##0` |

## Data Gathering — Use Web Search When Relevant

Before building the spreadsheet, determine whether the data requires external research. If the user asks for a report, analysis, or dataset about a **public company, industry, market, or any publicly available information**, use `webSearch` and `webFetch` to gather real data first.

Examples that require web search:

- "Build me a financial model for Tesla" → search for Tesla's latest 10-K/10-Q, revenue, margins, guidance
- "Create a comp table for SaaS companies" → search for revenue, ARR, multiples, headcount
- "Make a spreadsheet comparing EV manufacturers" → search for production numbers, market cap, deliveries
- "Summarize Apple's last 5 quarters" → search for quarterly earnings data

Do **not** fabricate numbers. If you cannot find a specific data point, leave the cell blank or mark it as "N/A — not found" rather than guessing. Always cite the source (e.g., "Source: Tesla 10-K FY2025") in a notes row or sheet.

## Output

Always present key findings and recommendations as a plaintext summary in chat, even when also generating files. The user should be able to understand the results without opening any files.

## Limitations

- Cannot write VBA macros (`.xlsm` requires `keep_vba=True` in openpyxl to *preserve* existing macros, not create them)
- Formulas are not computed by Python — open in Excel/LibreOffice to see results
- openpyxl auto-width is an approximation (no font metrics); xlsxwriter's `autofit()` is better
- Google Sheets import may drop some conditional formatting and chart styles

```

---

## Secondary Skill: file-converter

**Path:** `.local/secondary_skills/file-converter/SKILL.md`

```markdown
---
name: file-converter
description: Convert files between formats including CSV, JSON, YAML, XML, Markdown, and image formats.
---

# File Converter

Convert between data, document, and image formats. One-liners for each conversion pair.

## Tool Map

| Domain | Tool | Install |
|---|---|---|
| CSV/JSON/Excel/Parquet | `pandas` | `pip install pandas openpyxl pyarrow` |
| YAML | `pyyaml` | `pip install pyyaml` |
| XML ↔ dict | `xmltodict` | `pip install xmltodict` |
| Any doc format ↔ any | **pandoc** (CLI) | `apt install pandoc` or `pip install pypandoc_binary` |
| Markdown → HTML | `markdown` | `pip install markdown` |
| HTML → Markdown | `markdownify` | `pip install markdownify` |
| .docx read/write | `python-docx` | `pip install python-docx` |
| PDF → text/tables | `pdfplumber` | `pip install pdfplumber` |
| PDF → images | `pdf2image` | `pip install pdf2image` + `apt install poppler-utils` |
| PDF manipulation | `pypdf` | `pip install pypdf` |
| Images | `Pillow` | `pip install Pillow` |
| SVG → PNG | `cairosvg` | `pip install cairosvg` |
| HEIC → JPG | `pillow-heif` | `pip install pillow-heif` |

## Data Formats

```python
import pandas as pd, json, yaml, xmltodict

# --- CSV ↔ JSON ---
pd.read_csv("in.csv").to_json("out.json", orient="records", indent=2)
pd.read_json("in.json").to_csv("out.csv", index=False)

# --- CSV → Excel / Excel → CSV ---
pd.read_csv("in.csv").to_excel("out.xlsx", index=False, engine="openpyxl")
pd.read_excel("in.xlsx", sheet_name="Sheet1").to_csv("out.csv", index=False)

# All sheets: pd.read_excel("in.xlsx", sheet_name=None) → dict of DataFrames

# --- CSV → Parquet (columnar, compressed) ---
pd.read_csv("in.csv").to_parquet("out.parquet", engine="pyarrow", compression="snappy")

# --- YAML ↔ JSON ---
data = yaml.safe_load(open("in.yaml"))          # ALWAYS safe_load, never load()
json.dump(data, open("out.json", "w"), indent=2)
yaml.safe_dump(json.load(open("in.json")), open("out.yaml", "w"), sort_keys=False)

# --- XML ↔ JSON ---
data = xmltodict.parse(open("in.xml").read())
json.dump(data, open("out.json", "w"), indent=2)
open("out.xml", "w").write(xmltodict.unparse(data, pretty=True))

# --- JSONL (one JSON object per line) ---
pd.read_json("in.jsonl", lines=True).to_csv("out.csv", index=False)

```

**Encoding gotchas:**

- `pd.read_csv("f.csv", encoding="utf-8-sig")` strips the BOM that Excel inserts
- Auto-detect: `import chardet; enc = chardet.detect(open("f.csv","rb").read())["encoding"]`
- CSV delimiter sniffing: `pd.read_csv("f.csv", sep=None, engine="python")`

**Nested JSON → flat CSV:**

```python
pd.json_normalize(data, sep=".").to_csv("out.csv", index=False)  # {"a":{"b":1}} → column "a.b"

```

## Document Formats — pandoc is the Swiss Army knife

```bash

# Markdown → PDF (requires LaTeX: apt install texlive-xetex)
pandoc input.md -o output.pdf --pdf-engine=xelatex

# Markdown → DOCX
pandoc input.md -o output.docx

# DOCX → Markdown (extracts images to ./media/)
pandoc input.docx -o output.md --extract-media=.

# HTML → Markdown
pandoc input.html -o output.md -t gfm

# Any → Any (pandoc supports ~40 formats)
pandoc -f docx -t rst input.docx -o output.rst

```

```python

# From Python
import pypandoc
pypandoc.convert_file("in.md", "docx", outputfile="out.docx")

```

**Without pandoc (pure Python):**

```python

# Markdown → HTML
import markdown
html = markdown.markdown(open("in.md").read(), extensions=["tables", "fenced_code", "toc"])

# HTML → Markdown
from markdownify import markdownify
md = markdownify(html, heading_style="ATX")  # ATX = # headers, not underlines

```

## PDF Operations

```python

# --- Extract text + tables ---
import pdfplumber
with pdfplumber.open("in.pdf") as pdf:
    text = "\n".join(p.extract_text() or "" for p in pdf.pages)
    tables = pdf.pages[0].extract_tables()  # list of list-of-rows

# --- PDF → images (one PNG per page) ---
from pdf2image import convert_from_path
for i, img in enumerate(convert_from_path("in.pdf", dpi=200)):
    img.save(f"page_{i+1}.png")

# --- Merge / split / rotate ---
from pypdf import PdfReader, PdfWriter
writer = PdfWriter()
for path in ["a.pdf", "b.pdf"]:
    for page in PdfReader(path).pages:
        writer.add_page(page)
writer.write("merged.pdf")

# Extract pages 2–5
reader = PdfReader("in.pdf")
writer = PdfWriter()
for p in reader.pages[1:5]:
    writer.add_page(p)
writer.write("pages_2-5.pdf")

```

**PDF gotchas:**

- `pdf2image` needs `poppler-utils` installed system-wide (not a pip package)
- Scanned PDFs have no text layer — pdfplumber returns `None`. Use `pytesseract` OCR on pdf2image output.
- `PyPDF2` is deprecated → use `pypdf` (same API, maintained fork)

## Image Formats

```python
from PIL import Image

# --- Basic conversion ---
Image.open("in.png").convert("RGB").save("out.jpg", quality=90)

# convert("RGB") is REQUIRED: JPEG can't store alpha channel, will raise OSError

# --- WebP (best web format) ---
Image.open("in.jpg").save("out.webp", quality=85, method=6)  # method 0-6, 6=best compression

# --- AVIF (smallest, Pillow 11+) ---
Image.open("in.jpg").save("out.avif", quality=75)

# --- HEIC (iPhone photos) → JPG ---
from pillow_heif import register_heif_opener
register_heif_opener()
Image.open("in.heic").convert("RGB").save("out.jpg", quality=90)

# --- SVG → PNG ---
import cairosvg
cairosvg.svg2png(url="in.svg", write_to="out.png", output_width=1024)

# --- Batch convert directory ---
from pathlib import Path
for p in Path("imgs").glob("*.png"):
    Image.open(p).convert("RGB").save(p.with_suffix(".jpg"), quality=85)

```

**Image gotchas:**

- PNG → JPG: **must** `convert("RGB")` first or transparency crashes the save
- `quality` for PNG is meaningless (lossless) — use `optimize=True, compress_level=9`
- Pillow can't open `.svg` natively — use `cairosvg` or `svglib`
- GIF → MP4 is a video operation: `ffmpeg -i in.gif -pix_fmt yuv420p out.mp4`

## Validation

Always verify output:

```python

# Row count parity
assert len(pd.read_csv("out.csv")) == len(pd.read_json("in.json"))

# JSON well-formed
json.load(open("out.json"))

# Image opens
Image.open("out.jpg").verify()

```

```

---

## Secondary Skill: find-customers

**Path:** `.local/secondary_skills/find-customers/SKILL.md`

```markdown
---
name: find-customers
description: Find relevant companies and leads for B2B sales with ICP definition and qualification frameworks.
---

# Find Customers

Find relevant companies and leads for B2B sales. Define ideal customer profiles, identify target accounts, qualify prospects, and organize research for outreach.

## When to Use

- User wants to find companies that match their ICP
- User needs to build a prospect list for sales outreach
- User wants to research target accounts
- User needs lead qualification analysis

## When NOT to Use

- Writing outreach sequences (use sdr-outreach or cold-email-writer skills)
- Recruiting candidates (use ai-recruiter skill)
- General market research (use deep-research skill)

## Methodology

### Step 0: Interview the User About Their Business

**Before doing any research, interview the user.** Most users won't give you enough context unprompted — they'll say "find me customers" without explaining what they sell or who buys it. Use multi-option quizzes to make this fast and low-friction. Ask one question at a time.

**Question flow:**

1. **What do you sell?**
   - A) Software / SaaS
   - B) Physical product
   - C) Professional services / consulting
   - D) Marketplace / platform
   - E) Something else (describe)

2. **Who buys it?**
   - A) Other businesses (B2B)
   - B) Consumers (B2C / DTC)
   - C) Both

3. **(If B2B) What size companies?**
   - A) Startups / small teams (1-50 people)
   - B) Mid-market (50-500)
   - C) Enterprise (500+)
   - D) Not sure yet

4. **What's your price point?**
   - A) Under $100/mo
   - B) $100-$1,000/mo
   - C) $1,000-$10,000/mo
   - D) $10,000+/mo or custom pricing
   - E) One-time purchase

5. **Who inside the company makes the buying decision?**
   - A) Engineering / technical (CTO, VP Eng, developers)
   - B) Marketing (CMO, growth, content)
   - C) Sales / revenue (CRO, VP Sales, RevOps)
   - D) Operations / finance (COO, CFO)
   - E) Founder / CEO directly
   - F) Not sure

6. **Do you have existing customers?**
   - A) Yes, paying customers — I can describe who they are
   - B) A few early users / pilots
   - C) No customers yet

7. **(If they have customers) What do your best customers have in common?** (free text — this is the most valuable answer)

8. **Any industries or verticals you're focused on?** (free text or skip)

**If the user provides a detailed prompt upfront**, skip the questions they already answered. Don't re-ask what's obvious. But if key info is missing (who buys, what size, what price), ask before proceeding — the ICP will be wrong without it.

### Step 1: Define ICP (Ideal Customer Profile)

An ICP describes accounts where three things are true: they **can buy** (budget/size fit), they **will buy** (pain exists now), and they **will stay** (retention profile). Pick 6-10 attributes — more than 10 and nothing qualifies.

| Attribute | How to define it | Example |
|-----------|------------------|---------|
| Headcount | Hard range, not "SMB" | 50-500 employees |
| Revenue | Estimate from headcount if private | $10M-$100M ARR |
| Industry | NAICS/SIC codes or named verticals | SaaS, fintech, digital health |
| Geography | Where you can legally sell + support | US, UK, Canada |
| Tech stack | Tools that signal fit (technographics) | Uses Salesforce + Segment + AWS |
| Funding stage | Proxy for budget + growth pressure | Series A-C, raised in last 18mo |
| Hiring signals | Job posts reveal priorities | Hiring "RevOps" or "Head of Data" |
| Negative signals | Disqualifiers — the sharpest filter | <20 employees, agency model, on-prem only |

**ICP vs Buyer Persona:** ICP = which company. Persona = which human inside it. A Series B fintech (ICP) has a VP Eng who cares about velocity and a CFO who cares about cloud spend (two personas, different messaging).

### Step 2: Source Accounts

**Free sources (use `webSearch` + `webFetch`):**

- **Crunchbase** — `site:crunchbase.com "series a" fintech 2025` for funding events
- **LinkedIn** — `site:linkedin.com/company [industry] "11-50 employees"` (headcount filter leaks into page text)
- **BuiltWith / Wappalyzer lookups** — `webFetch` a prospect's homepage, then scan source for tech signatures (Segment snippet, Intercom widget, Shopify checkout)
- **Job boards** — `site:linkedin.com/jobs "[target company]" "data engineer"` reveals what they're building; `site:greenhouse.io` and `site:lever.co` for startup hiring
- **G2 / Capterra category pages** — companies reviewing competitors are in-market
- **GitHub orgs** — public repos reveal tech stack and eng team size for dev-tool ICPs
- **SEC EDGAR** (public cos) — 10-K "Risk Factors" sections list the exact problems they're worried about

**Paid sources the user likely has (shape output for these):**

- **Apollo** (~210M contacts, $49+/mo) — best value for SMB/mid-market, filters on headcount growth + job postings + intent
- **LinkedIn Sales Navigator** (~1B profiles) — most accurate job-change data, but no email export
- **ZoomInfo** — strongest US enterprise coverage + intent data (tracks content consumption across the web)
- **Clay** ($134+/mo) — waterfall enrichment: chains Apollo → Hunter → Cognism to maximize match rate. Best for teams with RevOps capacity.
- **Cognism** — best EU/UK data + phone-verified mobiles (GDPR-compliant)

### Step 3: Buying Signals (Trigger Events)

Prospects with an active trigger convert 3-5x higher. Rank by signal strength:

| Signal | Why it matters | How to find it |
|--------|----------------|----------------|
| New exec in target persona | New VPs buy tools in first 90 days | `site:linkedin.com "[company]" "I'm excited to join"` or Sales Nav job-change alerts |
| Funding round | Budget just unlocked | Crunchbase, `webSearch: "[company] raises"` |
| Hiring spike in relevant role | Building the team that needs you | LinkedIn Jobs count, `site:greenhouse.io/[company]` |
| Tech stack change | Migration = pain = budget | BuiltWith historical, job posts mentioning "migrating from X" |
| Competitor displacement | Negative G2 review of competitor | `site:g2.com "[competitor]" 1-star OR 2-star` |
| M&A / new product launch | Org chaos creates tool gaps | Press releases, TechCrunch |
| Earnings call mentions | Public co priority signals | `webFetch` SeekingAlpha transcripts, Ctrl-F for your problem space |

### Step 4: Qualify & Tier

**Fast disqualification (do this first):** Before researching, kill accounts that fail any hard constraint — wrong geo, below headcount floor, competitor customer under contract, recent layoffs (no budget).

**Qualification frameworks:**

- **BANT** (Budget / Authority / Need / Timeline) — fine for transactional/SMB
- **MEDDPICC** (Metrics / Economic buyer / Decision criteria / Decision process / Paper process / Identify pain / Champion / Competition) — use for enterprise deals >$50k. The extra P's (paper process, competition) matter because enterprise deals die in legal/procurement, not in the pitch.

**Tiering:**

- **Tier 1** — ICP match + active trigger in last 30 days → full personalization, multi-channel, SDR owns it
- **Tier 2** — ICP match, no trigger → lighter-touch automated sequence, monitor for triggers
- **Tier 3** — Partial fit → newsletter/nurture, revisit quarterly

### Step 5: Scale with Parallel Agents

**Target minimum 40 prospects.** A single sequential search won't get there fast enough. Use `startAsyncSubagent` to run **5 parallel research agents**, each focused on a different search angle:

1. **Industry/vertical search** — companies in the target vertical via Crunchbase, G2 category pages
2. **Funding/growth search** — recently funded companies matching the ICP
3. **Hiring signal search** — companies hiring for roles that indicate they need the user's product
4. **Competitor customer search** — companies using competitors or reviewing them on G2/Capterra
5. **Lookalike search** — competitors and alternatives to any strong-fit companies already found

Each agent should return 10-15 prospects with all columns filled in. Deduplicate after all agents return via `waitForBackgroundTasks`, then merge into the final spreadsheet.

### Step 6: Output as a Spreadsheet

**Build a real spreadsheet** using the excel-generator skill or write a CSV file — not a markdown table. The output should be something the user can import directly into a CRM, Clay, or Apollo.

**Columns:**

| Company | Domain | Headcount | Fit Score (1-5) | Trigger | Trigger Date | Target Contact Name | Target Title | LinkedIn URL | Email (if found) | Why Now (1 sentence) |

- **LinkedIn URL** — search for the target persona at the company: `site:linkedin.com/in "[company]" "[title]"`. Include direct profile links.
- **Email** — look for email patterns via `webSearch("[company] email format" OR "[name] [company] email")`. Common patterns: `first@company.com`, `first.last@company.com`. If not found, leave blank and note the likely format.
- **Why Now** — the most valuable column. It's the first line of the cold email.

The spreadsheet should be downloadable and ready to import — not just displayed as text.

### Deep Research for Complex ICPs

For industries or markets you don't know well, pull in the **deep-research** skill to build context before prospecting. This is especially useful when:

- The user sells into a niche vertical you don't have strong priors on (e.g., "construction tech", "veterinary SaaS")
- You need to understand market landscape, key players, and buyer behavior before defining the ICP
- The user wants competitor analysis as part of the prospecting process

Use deep-research to gather industry context, then return here to build the prospect list with that knowledge.

## Agent Tactics

**Tech stack detection:**
Use `webSearch("[company] tech stack" OR "[company] built with")` to find BuiltWith/Wappalyzer/StackShare profiles. Common signatures to look for in search results:

- Segment, Intercom, Stripe, Shopify, Google Analytics
- Job postings often reveal stack: `webSearch("[company] careers engineering")`

Note: `webFetch` returns markdown content, not raw HTML — script tags and asset URLs are stripped. Use search-based detection rather than HTML source scanning.

**Waterfall search pattern:** If one query returns nothing, don't stop — try synonym variants. "VP Engineering" OR "Head of Engineering" OR "Engineering Lead" OR "CTO" all map to the same persona at different company sizes.

**Lookalike expansion:** Once you find 5 good-fit accounts, search for their direct competitors — `webSearch: "[good-fit company] vs"` or `"[good-fit company] alternatives"` surfaces the category.

## Best Practices

1. **50 researched > 500 sprayed** — reply rates on researched lists run 3-5x higher
2. **Disqualify before you qualify** — negative filters are cheaper to check
3. **Trigger freshness decays fast** — a funding round is a 60-day window, a job change is a 90-day window
4. **Enrich once, cache the result** — don't re-research the same account every sequence
5. **B2B data decays ~30%/year** — any list older than 6 months needs re-verification

## Limitations

- Cannot log into LinkedIn Sales Navigator, Apollo, ZoomInfo, or Clay — builds search strategies the user executes
- Cannot verify email deliverability (user should run through NeverBounce/ZeroBounce before sending)
- Cannot detect intent data (Bombora/6sense-style content consumption signals require paid platforms)
- Company headcount/revenue estimates from public web are approximate — private company data is inherently fuzzy

```

---

## Secondary Skill: flashcard-generator

**Path:** `.local/secondary_skills/flashcard-generator/SKILL.md`

```markdown
---
name: flashcard-generator
description: Generate flashcards, quizzes, and study materials from notes or topics using spaced repetition principles.
---

# Flashcard & Quiz Generator

Generate study materials grounded in memory science. Follow Wozniak's formulation rules, schedule with SM-2, export to Anki via `genanki`.

## When to Use

- User pastes notes/textbook content to convert to cards, needs exam prep, or wants an Anki deck

## When NOT to Use

- In-depth research (deep-research), data analysis (data-analysis)

## Why Spaced Repetition Works

Ebbinghaus (1885) showed memory decays as `R = e^(-t/S)` where `S` is memory stability — without review, ~50-70% of new information is gone within 24 hours. The curve was replicated in 2015 (Murre & Dros, PLOS ONE). Each successful recall increases `S`, flattening the curve. **The core insight: reviewing just before you'd forget is the most efficient moment to review.** Active recall (retrieving the answer) builds stability far more than passive re-reading — this is why cards beat highlighting.

## Card Formulation: Wozniak's 20 Rules

Piotr Wozniak (SuperMemo creator; Anki forked his SM-2 algorithm) published the canonical rules in 1999 at supermemo.com. The ones that matter most for card generation:

**Rule 1-2: Understand before you memorize.** Don't make cards for material the user hasn't grasped yet. Cards reinforce; they don't teach.

**Rule 4: Minimum Information Principle — the single most important rule.** One atomic fact per card. Complex cards get forgotten as a unit — if any part fails, the whole card resets. Split aggressively.

- Bad: `Q: What are the three branches of US government and what does each do?` (6 facts, fails together)
- Good: Six cards. `Q: Which branch of US government writes laws? A: Legislative` × each branch × each function.

**Rule 5: Cloze deletion is the fastest path from prose to cards.** Take a sentence, blank one term. Beginners who struggle with minimum-information should default to cloze.

- Source: `TCP guarantees ordered delivery; UDP does not.`
- Cards: `{{c1::TCP}} guarantees ordered delivery; {{c2::UDP}} does not.` → 2 cards from one sentence

**Rule 9-10: Avoid sets and enumerations.** "List all 7 OSI layers" is a nightmare card — high failure rate, painful reviews. Instead, use **overlapping cloze**: one sentence with the full list, generate N cards each blanking one item. The redundancy is intentional — it's extra *cards*, not extra info per card.

**Rule 11: Combat interference.** Similar cards confuse each other (`affect` vs `effect`, port 80 vs 443). Add disambiguating context: `Q: [web, unencrypted] Default HTTP port? A: 80`.

**Rule 14: Personalize.** `Q: What's O(n log n)? A: Merge sort — like the algorithm you botched in the Stripe interview` sticks better than the abstract definition.

**The diagnostic:** If a card's ease factor drops below 1.3 in review, the card is malformed, not hard. Rewrite it, don't grind it.

## Card Types

| Type | Use for | Example |
|---|---|---|
| **Basic Q→A** | Single facts | `Q: Capital of Mongolia? A: Ulaanbaatar` |
| **Cloze** | Converting prose fast; lists | `The {{c1::mitochondria}} produces {{c2::ATP}} via {{c3::oxidative phosphorylation}}` → 3 cards |
| **Reversed** | Bidirectional recall (vocab) | Generates both `fr→en` and `en→fr` |
| **Application** | Understanding, not recall | `Q: Revenue +20%, profit −5%. Why? A: Costs grew faster than revenue` |
| **Image occlusion** | Anatomy, diagrams, maps | Blank one label on a diagram per card (Wozniak rule 8) |

Mix Bloom's levels: ~40% remember (basic/cloze), ~30% understand, ~30% apply/analyze. Pure recall decks feel productive but fail on exams that test transfer.

## SM-2 Scheduling (What Anki Runs)

Wozniak's 1987 algorithm. Each card tracks three values: repetition count `n`, ease factor `EF` (starts at 2.5), interval `I` in days. After each review, grade 0-5:

```text
if grade >= 3:               # correct
    if n == 0: I = 1
    elif n == 1: I = 6
    else: I = round(I * EF)   # exponential growth
    n += 1
else:                         # forgot
    n = 0; I = 1              # reset interval, keep EF

EF += 0.1 - (5-grade) * (0.08 + (5-grade)*0.02)
EF = max(EF, 1.3)             # floor — below this, card is malformed

```

Grade 5 → EF +0.10. Grade 4 → no change. Grade 3 → EF −0.14. A card you always rate "good" (4) with EF 2.5 goes: 1 → 6 → 15 → 38 → 94 days. **FSRS** (Anki 23.10+) is the ML successor — fits a personal forgetting curve, ~20-30% fewer reviews for same retention. Mention it; default to SM-2 for simplicity.

## Export to Anki: `genanki`

`pip install genanki` (github.com/kerrickstaley/genanki). Generates `.apkg` files that import directly via File → Import.

```python
import genanki, random

# Generate these ONCE, then hardcode — stable IDs let users re-import updates
MODEL_ID = random.randrange(1 << 30, 1 << 31)  # e.g. 1607392319
DECK_ID  = random.randrange(1 << 30, 1 << 31)

basic = genanki.Model(MODEL_ID, 'Basic',
    fields=[{'name': 'Q'}, {'name': 'A'}],
    templates=[{'name': 'Card 1', 'qfmt': '{{Q}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{A}}'}],
    css='.card { font-family: Arial; font-size: 20px; text-align: center; }')

deck = genanki.Deck(DECK_ID, 'Biology :: Cell Structure')
deck.add_note(genanki.Note(model=basic,
    fields=['What organelle produces ATP?', 'Mitochondria']))

# Cloze uses built-in model — second field required (can be empty) since 0.13.0
deck.add_note(genanki.Note(model=genanki.builtin_models.CLOZE_MODEL,
    fields=['The {{c1::mitochondria}} produces {{c2::ATP}}', '']))

genanki.Package(deck).write_to_file('cells.apkg')

```

**Gotchas:** Fields are HTML — `html.escape()` any user content with `<`, `>`, `&`. For images/audio, set `package.media_files = ['diagram.png']` and reference by **basename only** in the field: `<img src="diagram.png">` (paths break). Stable GUIDs let re-imports update cards in place — subclass `Note` and override `guid` to hash only the question field.

**Quizlet/CSV fallback:** Tab-separated, one card per line: `question\tanswer\n`. Quizlet imports directly. Also works for Anki's File → Import → Text.

## Output: Always Build a Web App

**Every flashcard generation MUST produce an interactive web app as the primary output.** Do not output cards as plain text or markdown — always build a React + Vite single-page app with **two modes** the user can switch between:

### Mode 1: Flashcard Review

1. **Card display** — show front of card, flip to back on click or spacebar
2. **SM-2 grading** — four buttons: Again (1), Hard (3), Good (4), Easy (5), wired to the SM-2 algorithm above
3. **Spaced repetition queue** — `localStorage` persistence for `{cardId: {n, EF, I, due}}`. Sort queue by `due` date. Cards due today appear first.
4. **Session stats** — cards reviewed, accuracy %, cards due tomorrow, total remaining
5. **Card type support** — render Basic Q→A, Cloze (hide blanked terms), and Reversed cards correctly
6. **Flip animation** — CSS 3D transform, keyboard shortcuts (Space to flip, 1/2/3/4 for grading)

### Mode 2: AI Quiz

An AI-powered quiz mode that generates and grades questions:

1. **Quiz setup** — user picks a topic (or all topics) and number of questions (5, 10, 20, custom)
2. **Question generation** — use AI integrations to generate N questions from the card material. Mix question types: multiple choice, short answer, and true/false. Questions should test understanding and application, not just recall.
3. **Answer & grade** — user answers each question, then AI grades the response with a score and explanation of what was right/wrong
4. **Quiz results** — summary screen with overall score, per-question breakdown, and which topics need more work
5. **Weak spot feedback** — highlight topics where the user scored lowest and suggest reviewing those flashcards

### UI/UX Requirements

- **Tab or toggle** to switch between Flashcard and Quiz modes
- **Clean, focused design** — one card or question centered on screen, no clutter
- **Mobile-friendly** — responsive layout, touch targets
- **Topic/deck selector** — filter by topic in both modes
- **Progress indicator** — card counter in flashcard mode, question progress bar in quiz mode

## Best Practices

1. **Minimum information principle trumps everything** — when in doubt, split the card
2. **Cloze is the default for prose** — fastest path from notes to reviewable cards
3. **Never make set-enumeration cards** — "list all X" → overlapping cloze instead
4. **30 great cards > 100 mediocre ones** — review burden compounds; every bad card costs minutes over months
5. **Cap new cards at ~20/day** — the review debt from 100 new cards/day becomes unsustainable by week 3

## Limitations

- Cannot read existing `.apkg` files (genanki is write-only); cannot sync to AnkiWeb
- Cannot track review history across sessions unless building a persistent app
- Verify generated content for specialized domains — confident-sounding wrong cards are worse than no cards

```

---

## Secondary Skill: github-solution-finder

**Path:** `.local/secondary_skills/github-solution-finder/SKILL.md`

```markdown
---
name: github-solution-finder
description: Search GitHub for battle-tested open-source libraries and solutions
---

# GitHub Solution Finder

Find battle-tested libraries instead of building from scratch. Use GitHub's search operators — they're far more precise than plain Google.

## Search Operators (combine with spaces = AND)

| Operator | Example | Effect |
|---|---|---|
| `stars:>N` | `stars:>1000` | More than N stars |
| `stars:N..M` | `stars:100..500` | Between N and M |
| `language:X` | `language:python` | Primary language |
| `pushed:>DATE` | `pushed:>2025-06-01` | Commits after date — **the key freshness signal** |
| `created:>DATE` | `created:>2024-01-01` | Repo created after date |
| `topic:X` | `topic:cli` | Tagged with topic |
| `license:X` | `license:mit` | Specific license |
| `-X` | `-language:javascript` | Exclude (prefix any qualifier) |
| `archived:false` | | Exclude archived repos |
| `is:public fork:false` | | No forks |
| `in:name` / `in:readme` | `http in:name` | Restrict where term matches |
| `user:X` / `org:X` | `org:google` | Scope to owner |
| `"exact phrase"` | `"rate limiter"` | Phrase match |
| `NOT` | `redis NOT cache` | Exclude keyword (strings only) |

## High-Signal Query Templates

```text

# Baseline: established + actively maintained
<problem> language:<lang> stars:>500 pushed:>2025-06-01 archived:false

# Find the dominant library (only a few results = clear winner)
<problem> language:python stars:>5000

# Hidden gems (newer, not yet famous, but active)
<problem> language:go stars:50..500 pushed:>2025-09-01 fork:false

# Curated lists — these exist for almost every topic
awesome <topic> in:name stars:>1000

# CLI tools
<task> topic:cli stars:>200 pushed:>2025-01-01

# Commercial-safe only
<problem> license:mit OR license:apache-2.0 stars:>500

# Boolean grouping
(language:rust OR language:go) <problem> stars:>1000

# Code search (different syntax — searches file contents)
path:**/*.py "from fastapi import" symbol:RateLimiter

```

## Search Aggressively — webSearch Is Your Primary Tool

**Use webSearch extensively.** Do not rely on a single query or a single source. Every solution search should involve multiple rounds of web searching across different angles — GitHub, package registries, blog posts, Stack Overflow, and comparison articles. Cast a wide net before narrowing down.

### GitHub searches

```text
webSearch("site:github.com <problem> <language> stars")
webSearch("site:github.com awesome <topic>")
webSearch("site:github.com/issues <specific error message>")
webSearch("best <language> library for <problem> 2026")
```

Note: GitHub-specific qualifiers like `language:`, `stars:>`, and `pushed:>` only work on GitHub's own search engine. Through `webSearch`, use natural-language equivalents (e.g. "python" instead of `language:python`). For precise filtering, use `gh search repos` if the GitHub CLI is available (see below).

### Package registry searches

```text
webSearch("site:pypi.org <problem>")        # Python
webSearch("site:npmjs.com <problem>")        # Node
webSearch("site:crates.io <problem>")        # Rust
webSearch("site:pkg.go.dev <problem>")       # Go
```

### Community and comparison searches

```text
webSearch("<lib A> vs <lib B> <language>")
webSearch("<problem> <language> reddit")
webSearch("<problem> best library site:stackoverflow.com")
webSearch("<problem> comparison benchmark <language>")
webSearch("awesome <topic> list github")
```

### Read what you find

`webFetch` every promising repo URL to read the README directly. Don't just rely on search result snippets — actually read the README, check the examples, and look at the API surface before recommending anything. For comparison posts and blog articles, `webFetch` the full content to extract specific benchmarks and tradeoffs.

## GitHub CLI (if available)

```bash
gh search repos "rate limiter" --language=python --stars=">1000" \
  --sort=stars --limit=10 --json=name,stargazersCount,pushedAt,url,description

gh api repos/OWNER/REPO --jq '{stars:.stargazers_count, pushed:.pushed_at, issues:.open_issues_count, license:.license.spdx_id, archived:.archived}'

```

## Health Evaluation — Check These Fast

| Signal | Healthy | Walk away |
|---|---|---|
| Last commit | <3 months | >18 months |
| Stars | >1000 (lib), >100 (niche) | <20 |
| Open/closed issue ratio | <0.3 | >1.0 with no replies |
| Contributors | 5+ | 1 (bus factor) |
| "Used by" (sidebar) | >1000 | 0 |
| Releases | Tagged, semver, changelog | No tags |
| License | MIT, Apache-2.0, BSD | None, GPL/AGPL (if commercial) |
| CI badge | Green | Missing or red |
| `archived: true` banner | — | Instant no |

**Red flags in issues:** Search the issue tracker for `"memory leak"`, `"abandoned"`, `"unmaintained"`, `"alternative"`. If maintainer hasn't replied to anything in 6 months, the project is effectively dead regardless of star count.

**Download trend check:**

- Python: `https://pypistats.org/packages/<name>` — declining = dying
- npm: `https://npmtrends.com/<pkg1>-vs-<pkg2>` — compare candidates head-to-head
- Check bundle size: `https://bundlephobia.com/package/<name>` (frontend only)

## License TL;DR

| License | Commercial OK | Must open-source your code? |
|---|---|---|
| MIT, BSD, Apache-2.0, ISC | Yes | No |
| LGPL | Yes | Only if you modify the lib itself |
| GPL | Yes | **Yes, if you distribute** (viral) |
| AGPL | Yes | **Yes, even for SaaS** (network-viral) |
| No LICENSE file | **No** | default is all rights reserved |

## Awesome Lists (curated entry points)

`sindresorhus/awesome` — the root of all awesome lists. Then: `awesome-python`, `awesome-go`, `awesome-rust`, `awesome-react`, `awesome-selfhosted`, `awesome-nodejs`, `free-for-dev`, `build-your-own-x` (learn by reimplementing), `public-apis`.

## Comparison Output Template

````markdown

## pkg-name  [12.4k stars, pushed 2 weeks ago, MIT]
github.com/owner/pkg-name

**Does:** One-line pitch.
**Fit:** Why it matches this specific problem.
**Install:** `pip install pkg-name`

**Pro:** Active, typed, 89% test coverage.
**Con:** Pulls in 23 transitive deps; async-only API.

```python
from pkg import Thing
Thing().do(x)  # minimal working example
```

````

## Decision Rules

1. **Two libs within 2x stars of each other** → pick the one pushed more recently
2. **A lib with 50k stars but last commit 2023** → it's dead, find the fork (check "Forks" tab sorted by stars)
3. **Lib does 10x more than needed** → check if you can vendor the 200 lines you actually need (with attribution)
4. **Can't find anything with >100 stars** → problem may be too niche; search blog posts / Stack Overflow for how others solved it
5. **Found 3+ viable options** → npmtrends/pypistats comparison, then read the top 5 closed issues of each

## Output

Always present key findings and recommendations as a plaintext summary in chat, even when also generating files. The user should be able to understand the results without opening any files.

```

---

## Secondary Skill: insurance-optimizer

**Path:** `.local/secondary_skills/insurance-optimizer/SKILL.md`

```markdown
---
name: insurance-optimizer
description: Review insurance coverage and find opportunities to optimize premiums and reduce gaps.
---

# Insurance Optimizer

Review current insurance coverage, identify gaps or overpayment, and suggest strategies to optimize premiums. Covers auto, home/renters, health, and life insurance.

**DISCLAIMER: This provides general information only, not professional insurance or financial advice.**

## When to Use

- User wants to review if they're over- or under-insured
- User is paying too much and wants to save
- User wants to understand their coverage
- User is shopping for new insurance

## When NOT to Use

- Filing insurance claims
- Complex commercial insurance
- Specific policy interpretation (consult agent)

## Methodology

### Step 1: Gather Current Coverage

Ask the user for their current policies. For each, collect:

- **Type**: Auto, home/renters, health, life, umbrella, disability
- **Provider**: Who is the carrier?
- **Premium**: Monthly or annual cost
- **Deductible**: How much they pay before insurance kicks in
- **Coverage limits**: Maximum the policy will pay
- **Key features**: What's included, what's excluded

### Step 2: Assess Coverage by Type

#### Auto Insurance

**Minimum recommended coverage:**

| Coverage | Recommended Minimum | Notes |
|----------|-------------------|-------|
| Bodily injury liability | 100/300 ($100K per person, $300K per accident) | State minimums are dangerously low |
| Property damage liability | $100,000 | Covers damage to other vehicles/property |
| Uninsured/underinsured motorist | Match liability limits | Protects you from uninsured drivers |
| Collision | Based on car value | Consider dropping if car value < 10× annual premium |
| Comprehensive | Based on car value | Covers theft, weather, animals |
| Medical payments / PIP | $5,000-$10,000 | Covers your medical costs regardless of fault |

**Drop collision/comp test:** If car value (KBB private party) < 10× the annual collision+comp premium, OR < ~$4,000 outright → self-insure. A $3,000 car with a $1,000 deductible and $400/yr premium means best-case payout is $2,000 — you're paying 20%/yr to insure that.

**Liability floor:** 100/300/100 minimum. State minimums (often 25/50/25) won't cover a single hospital visit. If net worth >$500k, bump to 250/500/100 + umbrella.

#### Home / Renters Insurance

**Homeowners:**

| Coverage | Guideline |
|----------|-----------|
| Dwelling | Full replacement cost (NOT market value) |
| Personal property | Enough to replace belongings (do a home inventory) |
| Liability | $300,000-$500,000 minimum |
| Additional living expenses | 20% of dwelling coverage |
| Deductible | $1,000-$2,500 (higher = lower premium) |

**Commonly missed:** Flood (NOT in standard policies — check FEMA zone), earthquake (separate), scheduled riders for jewelry/art >$1,500-2,500, sewer backup, home business equipment.

**Renters:** $15-30/mo for $30-50k property + $100-300k liability. Best value in insurance — never skip.

#### Health Insurance

| | HMO | PPO | HDHP + HSA |
|---|---|---|---|
| Premium | Lower | Higher | Lowest |
| Deductible | Lower | Moderate | Highest ($1,650+ ind.) |
| Network | Referral needed | Any | Any |
| Best for | Low utilization | Frequent specialists | Healthy + want tax savings |

**HSA advantage:** Triple tax benefit — contributions deductible, growth tax-free, withdrawals tax-free for medical. 2026 limits: $4,400 individual / $8,750 family (+$1,000 if 55+). The only account in the tax code better than a Roth IRA. Save receipts — reimburse yourself decades later, tax-free.

**HDHP break-even math:** `(PPO premium − HDHP premium) × 12 + employer HSA contribution` = your buffer. If expected annual healthcare spending < buffer + tax savings on HSA contribution, HDHP wins. Most healthy people under 50 without chronic conditions come out ahead on HDHP.

#### Life Insurance

**How much:**

- Rule of thumb: 10-12× annual income
- More precise: Calculate total financial obligations (mortgage, debts, children's education, income replacement for X years) minus existing assets

**Term vs. Whole — run the math:**

| | Term (20yr, $500k) | Whole ($500k) |
|---|---|---|
| Monthly, healthy 30yo | ~$25-30 | ~$200-450 (8-15× term) |
| Cash value after 20yr | $0 | ~$50-80k (2-4% IRR after fees) |
| "Buy term, invest the difference" | $300/mo in index fund @ 7% real → **~$150k** after 20yr | — |

The salesperson's commission on whole life is typically 50-100% of the first-year premium — that's why it's pushed hard. Whole life makes sense only for: estate tax planning above the ~$15M exemption, special-needs trust funding, or maxed-out every other tax-advantaged account and still have excess.

**Term life is right for 90%+ of people.** Ladder policies (e.g., $500k/30yr + $500k/20yr) to match declining need as mortgage shrinks and kids age out.

#### Umbrella Insurance

**The $500k trigger:** Standard auto/home liability maxes out at ~$300-500k. Once your attachable net worth (home equity + taxable brokerage + savings — exclude 401k/IRA, they're federally protected from most judgments) crosses ~$500k, you're a lawsuit target without a shield.

- Coverage = total attachable net worth, rounded up to nearest $1M
- Cost: **~$150-300/yr for first $1M**, each additional $1M only ~$75-100/yr. $5M runs ~$500-700/yr. The cheapest insurance per dollar of coverage in existence.
- **Prerequisite:** most carriers require $250-300k underlying liability on auto/home before writing umbrella
- **Get it if:** net worth >$500k, rental properties, teenage drivers, pool/trampoline/dog, coach youth sports, high public profile, or you post opinions on the internet under your real name

### Step 3: Identify Gaps

Common coverage gaps to flag:

- [ ] Liability limits too low relative to net worth
- [ ] No umbrella policy
- [ ] No disability insurance (protects income — most overlooked insurance)
- [ ] No flood/earthquake in at-risk area
- [ ] Renters without renters insurance
- [ ] Life insurance insufficient for dependents
- [ ] Health plan doesn't cover needed specialists
- [ ] No scheduled coverage for high-value items

### Step 4: Find Savings

**Deductible break-even math (compute this, don't guess):**

```text
break_even_years = (high_deductible − low_deductible) / annual_premium_savings
```

- $500 → $1,000 deductible typically saves 15-30% on collision/comp (NOT proportional — doubling deductible does not halve premium)
- Avg driver files a claim every **6-8 years**. If break-even < 3 years and you have the emergency fund, raise it.
- Example: $500→$1,000 saves $200/yr → break-even 2.5yr → clearly worth it. Saves only $50/yr → 10yr break-even → skip.
- **Bank the savings** in a dedicated account until it equals your highest deductible — self-insure the gap.

**Shopping cadence — loyalty is a tax:**

- **Auto: re-quote every 6 months** (standard policy term). Carriers use "price optimization" — they raise rates on customers their models predict won't shop. ~22% of shoppers who compare find a cheaper rate. Early-shopper discounts: up to 10-15% for quoting before your current policy expires.
- **Home: re-quote every 2-3 years** or after any claim-free stretch
- **Life: re-quote after health improvements** — quit smoking 12+ months, lost significant weight, A1C normalized. Rates can drop 50%+.
- **Trigger events** that should always prompt a re-quote: birthday (esp. 25), violation falls off record (~3yr), credit score jump, marriage, move, paid off car

**Savings strategies by impact:**

| Strategy | Savings | Notes |
|---|---|---|
| Shop every 6mo (auto) | 15-30% | The Zebra, Insurify, or independent agent — get 3+ quotes |
| Raise deductibles | 10-25% | Only if emergency fund covers it; do break-even math |
| Bundle home + auto | 10-25% | But quote unbundled too — bundle discount sometimes masks one overpriced policy |
| Drop collision/comp | 100% of that premium | When car value < ~10× annual premium OR < $4,000 |
| Pay annually | 5-10% | Avoids monthly installment fees |
| Telematics (Progressive Snapshot etc.) | 10-30% for safe drivers | Can also RAISE rates — know your driving |
| Credit score improvement | 5-25% | Insurers use credit-based insurance scores in most states |

**Comparison sites:** The Zebra / Insurify (auto+home), Policygenius (life+disability), Healthcare.gov (ACA). All free. An independent broker who writes for multiple carriers beats a captive agent (State Farm/Allstate only sell their own).

### Step 5: Prioritize — Gaps Before Savings

Fix underinsurance first (existential risk), then optimize premiums (efficiency).

## Output Format

```text
# Insurance Review: [Name]

## Current Coverage Summary
| Type | Provider | Premium | Deductible | Coverage | Assessment |
|------|----------|---------|-----------|----------|------------|
| Auto | [co] | $X/mo | $Y | 100/300/100 | Adequate |
| Home | [co] | $X/mo | $Y | $Z dwelling | Gap: flood |
| ... | | | | | |

## Total Annual Cost: $X,XXX

## Gaps Identified
1. **[Gap]** — [risk explanation and recommendation]

## Savings Opportunities
1. **[Strategy]** — estimated savings: $X-Y/year

## Action Items
1. [ ] [Highest priority action]
2. [ ] [Next priority]
3. [ ] [Shop for quotes by date]

## Disclaimer
General information only. Consult a licensed insurance professional for specific policy advice.
```

## Best Practices

1. **Review annually** — needs, rates, and life circumstances change
2. **Shop around** — get 3+ quotes; loyalty rarely gets the best rate
3. **Understand deductibles** — ensure your emergency fund can cover them
4. **Don't underinsure to save** — $50/month savings isn't worth major exposure
5. **Ask about discounts** — most insurers have unadvertised discounts (ask explicitly)
6. **Read the exclusions** — know what's NOT covered, not just what is

## Limitations

- Cannot provide actual quotes or bind policies
- Cannot compare specific policy documents (recommend an independent agent for that)
- Cannot interpret specific policy language or coverage disputes
- Not a licensed insurance advisor
- Rates and regulations vary significantly by state

```

---

## Secondary Skill: interview-prep

**Path:** `.local/secondary_skills/interview-prep/SKILL.md`

```markdown
---
name: interview-prep
description: Prepare for job interviews with tailored questions, STAR answers, and company research. Builds interactive web apps for practice.
---

# Job Interview Prep Kit

Prepare for interviews with company-specific research, behavioral story banks, technical frameworks, and salary negotiation scripts. Always delivers as an interactive web app.

## When to Use

- Upcoming interview, mock question practice, salary negotiation prep, behavioral story coaching

## When NOT to Use

- Resume creation (resume-maker), broad career research (deep-research)

## Step 0: Ask the User — Mode Selection

Before doing anything else, ask the user:

1. **What role and company** are you interviewing for?
2. **Which prep mode do you want?**
   - **Voice mock interview** — AI-powered voice conversation simulating a real interview (uses OpenAI Realtime API for speech-to-speech)
   - **Text mock interview** — Chat-based interview simulator where the AI asks questions and gives feedback in real time
   - **Interview prep dashboard** — A reference website with expected questions, company intel, story frameworks, and negotiation scripts

All three modes are built as **web apps** deployed as artifacts. Do not output raw markdown — always build an interactive app.

## Step 1: Research the Role and Company

Before building anything, use `webSearch` to gather real intel. This data populates whichever mode the user chose.

| Source | Query | What you get |
|---|---|---|
| **Glassdoor** | `site:glassdoor.com [Company] interview questions [role]` | Actual questions asked, by round. Filter to last 6 months. |
| **Blind** | `site:teamblind.com [Company] interview` OR `[Company] onsite` | Unfiltered loop structure, which rounds matter, bar-raiser tells, comp bands |
| **levels.fyi** | `site:levels.fyi [Company]` | Real comp by level + location. Critical for negotiation anchoring. |
| **LeetCode Discuss** | `site:leetcode.com/discuss [Company] [role]` | Tagged coding problems actually asked |
| **LinkedIn** | `[Company] [team name]` → recent posts from hiring manager | What they're shipping, what they celebrate, vocabulary they use |
| **Eng blog / Newsroom** | `[Company] engineering blog` | System design context. Mentioning their published architecture in an interview is a strong signal. |

For Amazon specifically: each interviewer is assigned 1-3 Leadership Principles to probe. Map stories to LPs before the loop.

## Step 2: Build the Web App

### Mode A: Voice Mock Interview

Build a React web app that uses the **OpenAI Realtime API** for voice-to-voice interview simulation. The app should:

- Connect to OpenAI's Realtime API via WebSocket for low-latency speech-to-speech
- Configure the AI persona as an interviewer for the specific role/company
- Seed the system prompt with the researched questions from Step 1
- Include a **question queue** panel showing upcoming questions (behavioral, technical, situational) drawn from Glassdoor/Blind research
- Show a **live transcript** panel so the user can review what they said
- After each answer, provide **written feedback** on: STAR structure, specificity, quantification, and areas to improve
- Include a **timer** per question (recommended 2-3 min per behavioral, 15-20 min per system design)
- End with a **scorecard** summarizing performance across categories

```javascript
// OpenAI Realtime API connection pattern
const pc = new RTCPeerConnection();
const audioEl = document.createElement("audio");
audioEl.autoplay = true;

// Add local audio track for user's microphone
const ms = await navigator.mediaDevices.getUserMedia({ audio: true });
pc.addTrack(ms.getTracks()[0]);
pc.ontrack = (e) => { audioEl.srcObject = e.streams[0]; };

// Connect to OpenAI Realtime
const tokenRes = await fetch("/api/realtime-session", { method: "POST" });
const { client_secret } = await tokenRes.json();
const offer = await pc.createOffer();
await pc.setLocalDescription(offer);

const sdpRes = await fetch("https://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${client_secret.value}`,
    "Content-Type": "application/sdp",
  },
  body: offer.sdp,
});
await pc.setRemoteDescription({ type: "answer", sdp: await sdpRes.text() });
```

The backend route (`/api/realtime-session`) creates an ephemeral token via:

```javascript
const r = await fetch("https://api.openai.com/v1/realtime/sessions", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    model: "gpt-4o-realtime-preview",
    voice: "verse",
    instructions: `You are an interviewer for [Role] at [Company]. Ask behavioral and technical questions one at a time. After the candidate answers, give brief feedback, then move to the next question. Questions: [insert researched questions from Step 1]`,
  }),
});
const data = await r.json();
// Return data.client_secret to the frontend
```

### Mode B: Text Mock Interview

Build a React chat app that simulates a text-based interview. The app should:

- Present a chat interface styled like a messaging app
- AI asks one question at a time from the researched question bank
- After each user response, AI provides inline feedback (STAR structure check, specificity score, improvement suggestions)
- Include a **sidebar** with: question categories (behavioral / technical / situational), progress tracker, tips for the current question type
- Use the OpenAI Chat Completions API (not Realtime) via a backend route
- End with a **summary report** scoring each answer

System prompt for the interviewer AI:

```text
You are interviewing a candidate for [Role] at [Company]. Ask questions one at a time from this list: [researched questions]. After each answer, give brief, constructive feedback focusing on: specificity, use of "I" vs "we", quantified results, and STAR structure. Then ask the next question. Be professional but conversational.
```

### Mode C: Interview Prep Dashboard

Build a polished single-page React app with these sections:

1. **Company Intel Panel** — loop structure, recent news (from web search), team info, culture notes
2. **Question Bank** — categorized tabs (Behavioral, Technical, System Design, Culture Fit) with actual questions from Glassdoor/Blind research. Each question expandable to show:
   - Why they ask this
   - Framework to use (STAR, CAR, SOAR, STAR+L)
   - Example strong answer structure
3. **Story Builder** — interactive 6-story matrix (Leadership, Conflict, Failure, Ambiguity, Impact, Scope Creep). User fills in their STAR components; the app validates completeness and flags missing quantification
4. **Comp & Negotiation** — levels.fyi data, target/walk-away ranges, scripted negotiation lines
5. **Questions to Ask** — curated list with context on what each reveals
6. **Countdown Timer** — if the user has an interview date, show days remaining with a suggested daily prep schedule

## Behavioral Story Frameworks

**STAR is the baseline. Know the variants:**

- **STAR** — Situation (1-2 sent) → Task (1 sent) → Action (60% of airtime, use "I" not "we") → Result (quantified)
- **CAR** — Challenge → Action → Result. Tighter; better for rapid-fire rounds.
- **SOAR** — Situation → Obstacle → Action → Result. Use when the story's value is in what you overcame.
- **STAR+L** — Append Learning. Mandatory for failure questions.

**Build a 6-story matrix, not a script per question.** One well-told story covers 3-4 question variants.

| Category | Prepare 1 story each | Maps to questions like |
|---|---|---|
| Leadership | Stepped up without authority | "Influenced without authority," "led a project" |
| Conflict | Disagreed with manager/peer, resolved | "Difficult coworker," "disagree and commit" |
| Failure | Owned a mistake, quantify damage + fix | "Project that failed," "missed a deadline" |
| Ambiguity | Decided with incomplete info | "Moved fast," "prioritized under uncertainty" |
| Impact | Your single biggest measurable win | "Most proud of," "biggest accomplishment" |
| Scope creep | Did more than asked | "Exceeded expectations," "ownership" |

**"Tell me about yourself":** Present (current role + one win) → Past (how you got here, 1 pivot) → Future (why this role is the logical next step). 90 seconds.

## Technical Frameworks

**System design — RADIO:**

- **R**equirements — Functional + non-functional. Ask: scale? latency target? (~15% of time)
- **A**rchitecture — Boxes and arrows. Client, API layer, services, data stores, queues. (~20%)
- **D**ata model — Entities, fields, relationships. (~15%)
- **I**nterface — API contracts. REST vs GraphQL vs gRPC. (~15%)
- **O**ptimizations — Caching, CDN, sharding, read replicas. Senior signal lives here. (~35%)

**Coding pattern recognition:** ~75% of LeetCode-style questions reduce to: sliding window, two pointers, BFS/DFS, binary search on answer, heap for top-K, DP (1D/2D), union-find, monotonic stack.

## Salary Negotiation

1. **Never give a number first.** *"I'd want to learn more about the role before discussing comp — what range did you have budgeted?"*
2. **Only negotiate after a yes.** Once they want to hire you.
3. **BATNA is everything.** Competing offer > current job > nothing.
4. **Anchor with data.** levels.fyi for exact company + level + location. Quote 75th percentile.
5. **Negotiate the package, not the base.** Signing bonus, equity refresh, start date, remote days, title.
6. **The reframe script:** *"I'm really excited about this. Based on levels.fyi data for [level] at [company], I was expecting something closer to [X]. Is there flexibility?"*
7. **Silence is a tool.** State your number. Stop talking.
8. **Get it in writing.**

## Questions to Ask Interviewers

- "What's the one thing that, if it goes wrong in the next 6 months, keeps you up at night?"
- "What did the last person who was great in this role do differently?"
- "What's something the team tried recently that didn't work?"
- "How are decisions made when engineering and product disagree?"
- To the hiring manager: "What would make you say 'I'm so glad we hired them' at the 6-month mark?"

## Best Practices

1. **6 stories, not 30 answers** — depth beats breadth
2. **Quantify or it didn't happen** — "cut p99 from 340ms to 45ms" > "improved performance"
3. **Practice out loud** — written answers don't survive contact with your mouth
4. **"I don't have a great example" is fine** — better than a weak story. Pivot: "The closest I have is..."
5. **Failure questions: own it fully** — hedging is the most common disqualifier

## Limitations

- Voice mode requires user to provide their OpenAI API key (for Realtime API access)
- Comp data lags reality by ~3-6 months; cross-reference Blind for recency
- Company-specific intel quality depends on how much employees post publicly
- Cannot access internal question banks or recruiter portals

```

---

## Secondary Skill: invoice-generator

**Path:** `.local/secondary_skills/invoice-generator/SKILL.md`

```markdown
---
name: invoice-generator
description: Generate professional invoices as React web apps with auto-scaling layout and pixel-perfect PDF export via Puppeteer.
---

# Invoice Generator

Build invoices as React web artifacts that auto-scale to fit the page, then generate pixel-perfect PDFs via Puppeteer. The web page is the single source of truth — the PDF is a screenshot of it.

## Before You Start Building — Gather Information First

**Do NOT start building the invoice until you have enough information to populate real line items and details.** An invoice with placeholder data is useless.

### If the user provides complete invoice details

Go ahead and start building immediately. You have what you need.

### If the user asks to "make me an invoice" without providing details

You MUST ask clarifying questions before writing any code. Ask about:

1. **Seller info** — Business name, address, email, phone, logo (if any), VAT/tax ID (if applicable)
2. **Client info** — Client/company name, address, contact email, VAT number (if B2B in EU)
3. **Line items** — Description of each service/product, quantity, rate/price per unit
4. **Payment terms** — Net 30, due on receipt, etc. + preferred payment method (bank transfer, PayPal, Stripe, etc.)
5. **Invoice number** — Do they have an existing numbering scheme, or should you start one?
6. **Dates** — Invoice date, service/delivery date (if different), due date
7. **Tax** — What tax rate applies? (Sales tax, VAT, none?) This depends on jurisdiction.
8. **Where is the seller based?** — Determines required legal fields, page size (US = Letter, everyone else = A4), and tax handling

### How to ask

Start with the essentials:

> "To create your invoice, I need a few details:
>
> 1. Your business name and address (the seller)
> 2. Who you're billing — client name and address
> 3. What you're billing for — list each item/service with the quantity and price
> 4. Payment terms — when is it due, and how should they pay?"

Then follow up for tax details, numbering, branding, etc. based on what they share.

### If the invoice feels incomplete

If the user gives vague descriptions like "consulting work," push for specifics: *"Can you break that down into specific deliverables? e.g., 'Website redesign — 3 revision rounds' at $5,000. Specific line items look more professional and reduce client pushback."*

## Flag Guesses and Inferred Details

If you had to guess or infer any details — tax rates, payment terms, invoice numbers, dates — you MUST tell the user what you assumed. After presenting the first draft, explicitly list anything you weren't sure about. For example:

> "A few things I assumed — let me know if any need adjusting:
>
> - I used invoice number INV-2026-0001 — do you have an existing numbering scheme?
> - I set the tax rate to 0% since you didn't mention taxes — should I add sales tax or VAT?
> - I set payment terms to Net 30 with a due date of April 13 — is that right?"

Do NOT silently present fabricated details as fact. Getting invoice details wrong can cause real payment and legal issues.

## Build Order — PDF First, Website Last

Follow this exact order so the user gets fast results:

1. **Build the web artifact** with all invoice data and generate the PDF
2. **Present the PDF to the user in chat** — show the generated PDF immediately so they can see their invoice right away
3. **Finish the web app** — make sure the web preview looks correct and is browsable

The user cares most about seeing their invoice quickly. Get the PDF into their hands first. The web app is a bonus for previewing and iterating.

## Architecture

```text
artifacts/<client>-invoice/
  client/src/pages/Invoice.tsx   # Invoice data + component with auto-scale
  client/src/index.css           # Print-ready styles (A4 or Letter)
scripts/src/generate-invoice.ts  # Puppeteer PDF generator
output/                          # Generated PDF
```

### How it works

1. **Web page** renders the invoice at exactly 8.5in x 11in (Letter) or 210mm x 297mm (A4) with CSS
2. **Auto-scale hook** measures content height vs available height after fonts load; if content overflows, it applies `transform: scale()` to shrink everything to fit — content is never clipped
3. **PDF generation** uses Puppeteer to load the live web page, apply the same scale calculation, then `page.pdf()` with exact page dimensions
4. **Multi-page support** — unlike resumes, invoices can span multiple pages if the line items are long. For invoices with more than ~20 line items, don't aggressively shrink to one page — instead let the content flow naturally across pages with repeating table headers on each page

## Page Length Rules

- **Most invoices should fit on one page.** The auto-scale handles this for typical invoices.
- **It's OK to go multi-page** if the invoice has many line items. Don't shrink text to an unreadable size just to force everything onto one page.
- **If going multi-page**: repeat the table header (Description | Qty | Rate | Amount) on each page, and put the totals section on the final page.
- **Always put payment instructions and totals on the last page** so the client sees how much they owe and how to pay without hunting.

## Required Fields by Jurisdiction

**EU (VAT Directive 2006/112/EC, Article 226) — legally mandatory:**

- Sequential invoice number (gaps must be documented — auditors **will** assess VAT on missing numbers)
- Invoice date + date of supply (if different)
- Seller's full name, address, and **VAT number**
- Customer's name and address (and VAT number if B2B)
- Description of goods/services, quantity/extent
- Unit price excluding VAT, VAT rate per line, VAT amount **in the member state's currency** (even if invoice is in USD)
- **Reverse charge:** if selling B2B cross-border within EU, charge 0% VAT and add the notation `"Reverse charge — VAT to be accounted for by the recipient (Art. 196, Directive 2006/112/EC)"`. Include the customer's VAT number (validate via VIES).

**US — no federal invoice law.** Sequential numbering is best practice (IRS wants unique IDs for audit trail) but not legally required. Sales tax rules vary by state; many services are untaxed.

**Numbering scheme:** `{PREFIX}-{YYYY}-{SEQ:04d}` e.g. `INV-2026-0042`. Prefix can distinguish clients or entities. Never reuse or skip; if you void one, keep the voided record.

## Payment Terms Glossary

| Term | Meaning | Typical use |
|------|---------|-------------|
| Due on receipt | Pay immediately | Small amounts, new clients |
| Net 30 | Due 30 days from invoice date | Standard B2B |
| Net 60 / Net 90 | 60/90 days | Large enterprise (push back on this) |
| 2/10 Net 30 | 2% discount if paid in 10 days, else full in 30 | Incentivize fast payment |
| EOM | Due end of month | |
| 1.5% monthly late fee | Compounds on overdue balance | Check local usury caps — often ~18% APR max |

## Building the Invoice

### Invoice.tsx — React Component

The invoice component should include:

- `INVOICE_DATA` object at the top holding all content — line items, client info, seller info, tax rates, payment terms, dates
- `useEffect` with `scaleToFit()` that measures `scrollHeight` vs available height and applies `transform: scale()` if content overflows
- `document.fonts.ready.then(scaleToFit)` ensures scaling runs after web fonts load
- Multiple `setTimeout` calls as fallback for slow font/layout

**Layout structure:**

```tsx
const INVOICE_DATA = {
  invoiceNumber: "INV-2026-0042",
  issueDate: "2026-03-14",
  dueDate: "2026-04-13",
  seller: {
    name: "Your Company",
    address: "123 Main St, City, ST 12345",
    email: "billing@company.com",
    vatNumber: "", // EU only
  },
  client: {
    name: "Client Corp",
    address: "456 Oak Ave, City, ST 67890",
    vatNumber: "", // EU B2B only
  },
  items: [
    { description: "Homepage redesign — 3 rounds of revisions", qty: 1, rate: 5000 },
    { description: "Logo design and brand kit", qty: 1, rate: 2500 },
  ],
  taxRate: 0, // 0.20 for 20% VAT, etc.
  currency: "USD",
  paymentTerms: "Net 30",
  paymentInstructions: "Bank: ... | ACH Routing: ... | Account: ...",
  notes: "",
  lateFeePolicy: "1.5% monthly interest on overdue balances",
};
```

**Component structure:**

```text
<header>  Logo + "INVOICE" title + invoice number/dates  </header>
<section class="parties">  Two columns: From (seller) / Bill To (client)  </section>
<table>  Description | Qty | Rate | Amount  — with calculated line totals  </table>
<section class="totals">  Subtotal / Tax (X%) / Total Due — right-aligned, bold total  </section>
<footer>  Payment instructions · Bank/IBAN/SWIFT or payment link · Late fee policy  </footer>
```

The component should compute subtotal, tax, and total from the items array. Display the due date as an actual date ("Due: April 13, 2026") not just the payment term.

### index.css — Stylesheet

Key patterns:

- `@page { size: letter; margin: 0; }` for print (swap `letter` for `A4` for non-US)
- `.invoice-page` is exactly `8.5in x 11in` with `overflow: hidden`
- `@media print` hides Replit banners/iframes
- Clean sans-serif font (Inter, system fonts) — invoices should look professional but modern
- Table styling: light header row, subtle row borders, right-aligned numbers
- Totals section: right-aligned, bold total due with clear visual hierarchy
- Logo: `max-height: 48px` at top-left

### generate-invoice.ts — PDF Generator

```typescript
import puppeteer from "puppeteer-core";
import * as fs from "fs";
import * as path from "path";

const outDir = path.resolve(import.meta.dirname, "..", "..", "output");
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

// UPDATE THESE for each invoice:
// 1. Find Chromium path: ls /nix/store/*chromium*/bin/chromium
// 2. Set INVOICE_URL to the web artifact's URL
// 3. Set OUTPUT_NAME for the filename
const CHROMIUM_PATH = "/nix/store/FIND_YOUR_PATH/bin/chromium";
const INVOICE_URL = `https://${process.env.REPLIT_DEV_DOMAIN}/ARTIFACT-SLUG`;
const OUTPUT_NAME = "INV-2026-0042";

async function generatePDF() {
  const browser = await puppeteer.launch({
    executablePath: CHROMIUM_PATH,
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 816, height: 1056 });
  await page.goto(INVOICE_URL, { waitUntil: "networkidle0", timeout: 30000 });

  await page.waitForSelector(".invoice-page", { timeout: 10000 });
  await new Promise((r) => setTimeout(r, 2000));

  // Remove Replit dev UI and auto-scale content to fit one page
  await page.evaluate(() => {
    document.querySelectorAll('[class*="replit"], [class*="banner"], [id*="replit"], [id*="banner"], iframe').forEach(
      (el) => (el as HTMLElement).remove()
    );
    document.body.style.background = "#fff";
    document.body.style.margin = "0";
    document.body.style.padding = "0";

    const pg = document.querySelector(".invoice-page") as HTMLElement;
    if (!pg) return;
    pg.style.margin = "0";
    pg.style.boxShadow = "none";
    pg.style.width = "8.5in";
    pg.style.height = "11in";
    pg.style.overflow = "hidden";
    pg.style.position = "relative";

    const inner = pg.children[0] as HTMLElement;
    if (!inner) return;

    // Reset any existing transform to measure true height
    inner.style.transform = "none";
    inner.style.width = "100%";

    const padTop = parseFloat(getComputedStyle(pg).paddingTop);
    const padBot = parseFloat(getComputedStyle(pg).paddingBottom);
    const availH = pg.clientHeight - padTop - padBot;
    const contentH = inner.scrollHeight;

    // Scale down if content overflows available space
    if (contentH > availH) {
      const scale = availH / contentH;
      inner.style.transformOrigin = "top left";
      inner.style.transform = `scale(${scale})`;
      inner.style.width = `${100 / scale}%`;
    }
  });

  await new Promise((r) => setTimeout(r, 300));

  const pdfPath = path.join(outDir, `${OUTPUT_NAME}.pdf`);
  await page.pdf({
    path: pdfPath,
    width: "8.5in",
    height: "11in",
    printBackground: true,
    margin: { top: "0", bottom: "0", left: "0", right: "0" },
    preferCSSPageSize: false,
  });

  await browser.close();
  console.log("PDF saved:", pdfPath);
  return pdfPath;
}

await generatePDF();
console.log("Done!");
```

## Preventing Content Cutoff

The most common issue is content getting clipped at the bottom. Use a **two-layer defense**:

1. **React side** (for browser preview): The `scaleToFit` useEffect measures `scrollHeight` vs `clientHeight - padding` and applies CSS `transform: scale()`. This runs on mount, resize, font load, and via timeouts.

2. **Puppeteer side** (for PDF): The `page.evaluate()` block does the exact same measurement and scaling. This is necessary because Puppeteer's PDF renderer may not execute React effects reliably.

Both use the same formula:

```text
availH = container.clientHeight - paddingTop - paddingBottom
scale = availH / content.scrollHeight
content.style.transform = `scale(${scale})`
content.style.width = `${100 / scale}%`  // compensate for horizontal shrink
```

## Iteration and Changes

When the user requests changes (line items, amounts, branding, payment terms, etc.):

1. Make the requested changes in `Invoice.tsx`
2. **Re-run the PDF generation script** to produce an updated PDF
3. **Verify the output looks correct** — check that content isn't clipped, numbers are right-aligned, totals are correct
4. **Re-present the updated PDF** to the user in chat

Never deliver an updated invoice without re-generating the PDF. Every iteration cycle ends with the user seeing a fresh PDF.

## Best Practices

1. **Show the due date as an actual date** — "Due: April 13, 2026" not just "Net 30" (clients miscount)
2. **Specific line items** — "Homepage redesign — 3 rounds of revisions" not "Design services"
3. **Payment instructions on the invoice itself** — bank details, IBAN/SWIFT for international, payment link
4. **Ask the user's jurisdiction before building** — it changes required fields, page size, and tax display
5. **Right-align all numbers** — amounts, quantities, rates, totals
6. **Bold the total due** — it should be the most visually prominent number on the page

## Limitations

- Cannot send invoices, process payments, or track payment status
- Tax calculation is flat-rate per invoice — doesn't handle mixed VAT rates per line or US multi-state nexus
- Not a substitute for accounting software; no ledger integration

```

---

## Secondary Skill: legal-contract

**Path:** `.local/secondary_skills/legal-contract/SKILL.md`

```markdown
---
name: legal-contract
description: Draft and review legal documents like NDAs, contracts, and lease agreements with plain-language explanations.
---

# Legal Contract Assistant

Draft and review common legal documents including NDAs, service agreements, freelancer contracts, and lease reviews. Provide plain-language explanations and flag potential issues.

**IMPORTANT DISCLAIMER: This provides general information and templates only. It does NOT constitute legal advice. Always consult a qualified attorney for legal matters.**

## When to Use

- User needs a basic NDA, service agreement, or freelancer contract
- User wants a plain-language review of a contract they received
- User needs to understand specific legal terms or clauses
- User wants a lease or rental agreement reviewed for red flags

## When NOT to Use

- Complex litigation or regulatory compliance
- Employment law disputes
- International trade agreements
- Anything involving criminal law
- Situations requiring jurisdiction-specific legal analysis

## Open-Source Template Libraries (Use These First)

**Never draft from scratch.** Start from committee-vetted open-source agreements released under CC BY 4.0:

| Source | Documents | Style | Get it |
|--------|-----------|-------|--------|
| **Bonterms** | Mutual NDA, Cloud Terms (SaaS), SLA, DPA, PSA, AI Standard Clauses | US; "cover page + standard terms" | `github.com/Bonterms` |
| **Common Paper** | Mutual NDA, Cloud Service Agreement, DPA, Design Partner Agreement | US; standards committee of 40+ attorneys | `commonpaper.com/standards` |
| **oneNDA** | NDA (777 words), oneDPA | UK/EU; strict variable-only edits | `onenda.org` |

**Workflow:** `webFetch("https://bonterms.com/forms/mutual-nda/")` → extract the standard terms → build a cover page with the user's deal-specific variables (parties, effective date, term, governing law, jurisdiction). Don't modify the body; that's the whole point of standards.

## Red-Flag Language to Grep For

When reviewing, search the document text for these exact phrases — each is a known risk pattern:

| Phrase | Why it's dangerous | Suggested fix |
|--------|-------------------|---------------|
| `"any and all claims"` | Unlimited indemnity scope | "claims arising directly from [Party]'s breach of Section X" |
| `"indemnify, defend, and hold harmless"` | "Hold harmless" blocks your counterclaims even if they caused the loss | Strike "and hold harmless"; keep "indemnify and defend" |
| `"sole discretion"` / `"absolute discretion"` | One party can act arbitrarily (block settlements, reject deliverables) | "consent not to be unreasonably withheld, conditioned, or delayed" |
| `"including but not limited to"` in IP assignment | Open-ended IP grab beyond deliverables | Enumerate specific deliverables; add "excluding pre-existing IP" |
| No liability cap stated | Courts default to **unlimited** liability | "Aggregate liability capped at fees paid in the 12 months preceding the claim" |
| `"time is of the essence"` | Any delay = material breach | Delete, or limit to payment obligations only |
| Indemnity **carved out** of liability cap | Your cap doesn't protect you where exposure is highest | "Indemnification obligations are subject to the cap in Section X" |
| Auto-renewal with <30-day opt-out window | Easy to miss; locked in another term | 60–90 day notice window; email notice permitted |
| `"perpetual"` + `"irrevocable"` license | Can never be revoked even after breach | Term-limited; terminable on material breach |

**Indemnity forms (escalating risk):** *Limited* = you cover only your own negligence. *Intermediate* = everything except their sole negligence. *Broad* = you cover losses **even when caused entirely by them**. Flag intermediate and broad as Critical.

## Playbook Checks (What Harvey/Spellbook Actually Run)

AI contract tools run a fixed checklist per document type. For a **Service Agreement** run these checks and grade each Pass/Flag/Missing:

1. Is there a liability cap? Is it mutual? Is it tied to fees paid (1x, 2x)?
2. Is indemnity mutual or one-way? Subject to the cap or carved out?
3. Does IP assignment exclude contractor's pre-existing tools/libraries?
4. Is there a cure period (typically 30 days) before termination for breach?
5. Are "consequential damages" (lost profits, lost data) excluded? Mutually?
6. Payment terms: Net 30 or better? Late fee specified?
7. Can the client terminate for convenience? If so, is there a kill fee?
8. Governing law + venue: neutral, or the other party's home court?

## Review Output Format

```text

# Contract Review: [Document Type]
**NOT LEGAL ADVICE — for informational purposes only. Consult an attorney before signing.**

## Summary
[2–3 sentences: what this is, who it favors, biggest concern]

## Critical — Do Not Sign Without Addressing

1. **[Clause §X.Y]**: [quote the exact language]
   - **Risk**: [plain English]
   - **Suggested redline**: "[replacement text]"

## Warnings — Negotiate If You Have Leverage

## Notes — Standard But Be Aware

## Missing Protections
[clauses that should be here but aren't — e.g., no liability cap, no cure period]

## Overall: [Fair / Favors Counterparty / Consult Attorney Before Signing]

```

## Output: Always Produce PDF & DOCX

**Every drafted contract MUST be delivered as both a PDF and a DOCX file.** Clients need PDF for signing and DOCX for redlining — always provide both.

### Architecture: React + Vite → Puppeteer PDF + python-docx DOCX

Build the contract as a React web artifact first (source of truth for layout), then export:

**PDF via Puppeteer:**

```typescript
// generate-contract.ts
import puppeteer from 'puppeteer-core';

// Find Chromium: ls /nix/store/*chromium*/bin/chromium
const CHROMIUM_PATH = "/nix/store/FIND_YOUR_PATH/bin/chromium";
// Use the artifact's actual URL, not localhost
const CONTRACT_URL = `https://${process.env.REPLIT_DEV_DOMAIN}/ARTIFACT-SLUG`;

const browser = await puppeteer.launch({
  executablePath: CHROMIUM_PATH,
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});
const page = await browser.newPage();
await page.goto(CONTRACT_URL, { waitUntil: 'networkidle0' });
await page.pdf({
  path: 'contract.pdf',
  format: 'Letter',
  printBackground: true,
  margin: { top: '1in', bottom: '1in', left: '1.25in', right: '1.25in' },
});
await browser.close();
```

**DOCX via python-docx:**

```python
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)

# Set margins
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.25)
    section.right_margin = Inches(1.25)

# Title
title = doc.add_heading('MUTUAL NON-DISCLOSURE AGREEMENT', level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Preamble
doc.add_paragraph(
    'This Mutual Non-Disclosure Agreement ("Agreement") is entered into '
    'as of [DATE] by and between:'
)

# Parties table
table = doc.add_table(rows=2, cols=2)
table.style = 'Table Grid'
# ... populate with party details

# Sections with numbered clauses
doc.add_heading('1. Definition of Confidential Information', level=1)
doc.add_paragraph('...')

# Signature block
doc.add_paragraph('\n\n')
sig_table = doc.add_table(rows=4, cols=2)
# ... signature lines with name, title, date

doc.save('contract.docx')
```

### Styling for Legal Documents

- **Font**: Times New Roman 12pt (standard for legal docs) or similar serif
- **Margins**: 1" top/bottom, 1.25" left/right
- **Line spacing**: 1.5 or double-spaced (jurisdiction dependent)
- **Section numbering**: Use hierarchical numbering (1, 1.1, 1.1.1)
- **Page numbers**: Bottom center, "Page X of Y"
- **Headers**: Document title and date on each page
- **Signature blocks**: Two-column layout with lines for signature, printed name, title, date

### Contract Review Output

For **reviews** (not drafting), output the review analysis directly as text using the Review Output Format above. Do not generate PDF/DOCX for reviews — the review is commentary, not a document.

## Drafting Rules

1. **Always include the disclaimer** at the top of every output — this is not legal advice
2. Start from Bonterms/Common Paper, don't invent clause language
3. Quote exact problem text with section numbers, then give replacement language
4. Flag jurisdiction dependencies — non-compete enforceability, anti-indemnity statutes, and consumer protection vary wildly by state/country
5. When stakes are high (>$50K, equity, exclusivity, personal guarantees) → recommend attorney review explicitly

## Limitations

- NOT a substitute for legal advice from a licensed attorney
- Cannot account for jurisdiction-specific laws
- Cannot verify legal enforceability of any clause
- Cannot handle litigation, regulatory filings, or court documents
- Templates are starting points, not final legal documents

```

---

## Secondary Skill: meal-planner

**Path:** `.local/secondary_skills/meal-planner/SKILL.md`

```markdown
---
name: meal-planner
description: Create personalized meal plans with macros, shopping lists, and fitness schedules.
---

# Meal Planner & Fitness Schedule

Create personalized meal plans with calculated macro targets, shopping lists, and training schedules.

**DISCLAIMER: General nutrition and fitness information only — not medical or dietetic advice. Users with medical conditions, eating disorder history, pregnancy, or on medications should consult a registered dietitian or physician.**

## When to Use

- User wants a weekly meal plan hitting specific macros
- User needs a shopping list generated from a plan
- User wants a training split paired with nutrition

## When NOT to Use

- Medical dietary needs (renal, diabetic, celiac management) → refer to RD
- Single recipe creation → use recipe-creator skill
- Health data analysis → use personal-health skill

## Step 1: Gather Inputs

Required: goal (fat loss / maintenance / muscle gain), sex, age, height, weight, activity level, dietary restrictions, meals-per-day preference, cooking time available, budget.

If body fat % is known, use Katch-McArdle instead of Mifflin-St Jeor — it's more accurate for lean or obese individuals.

## Step 2: Calculate Energy Target

**Mifflin-St Jeor BMR** (validated as most accurate predictive equation for the general population, ±10% for most adults):

```text
Men:   BMR = (10 × weight_kg) + (6.25 × height_cm) − (5 × age) + 5
Women: BMR = (10 × weight_kg) + (6.25 × height_cm) − (5 × age) − 161
```

**Katch-McArdle** (use if body fat % is known — more accurate at body-composition extremes):

```text
BMR = 370 + (21.6 × lean_mass_kg)    where lean_mass_kg = weight_kg × (1 − bodyfat%)
```

**TDEE = BMR × activity multiplier:**

| Level | Multiplier | Description |
|---|---|---|
| Sedentary | 1.2 | Desk job, minimal deliberate exercise |
| Lightly active | 1.375 | 1–3 sessions/week |
| Moderately active | 1.55 | 3–5 sessions/week |
| Very active | 1.725 | 6–7 sessions/week |
| Extra active | 1.9 | Athlete or physical labor + training |

People consistently overestimate their activity — when in doubt, pick the lower multiplier and adjust upward after 2 weeks of real-world data.

**Goal adjustment:**

- Fat loss: TDEE − 20–25% (typically 400–600 kcal deficit). Targets ~0.5–1% bodyweight/week. Steeper deficits accelerate muscle loss.
- Maintenance: TDEE ± 0
- Muscle gain: TDEE + 10–15% (typically 200–400 kcal surplus). Larger surpluses mostly add fat, not muscle, in trained individuals.

## Step 3: Set Macros — Evidence-Based Targets

### Protein (set this first, in g/kg — not as a percentage)

| Goal | Target | Evidence |
|---|---|---|
| General health / sedentary | 0.8–1.2 g/kg | RDA is 0.8 g/kg — the minimum to prevent deficiency, not an optimum |
| Muscle gain + resistance training | **1.6–2.2 g/kg** | Morton et al. 2018 meta-analysis (49 RCTs, n=1,863, *BJSM*): gains in fat-free mass plateau at 1.62 g/kg/day (95% CI: 1.03–2.20). The upper CI bound (~2.2 g/kg) is recommended for those maximizing hypertrophy. Confirmed by Nunes et al. 2022 (74 RCTs). |
| Fat loss (preserving lean mass) | 1.8–2.7 g/kg | Higher end of range compensates for the muscle-sparing effect of protein during energy deficit |
| Endurance athletes | 1.2–1.6 g/kg | ISSN position stand |

In imperial: 1.6–2.2 g/kg ≈ 0.7–1.0 g/lb. Distribute across 3–5 meals at 0.3–0.4 g/kg per meal (~25–40 g) — muscle protein synthesis response plateaus per-sitting.

### Fat

Minimum ~0.5 g/kg bodyweight (hormone synthesis floor). Typical range 0.8–1.2 g/kg, or 20–35% of calories. Going below 20% long-term risks fat-soluble vitamin and hormone issues.

### Carbohydrates

Fill remaining calories after protein and fat are set. `carbs_g = (target_kcal − protein_g×4 − fat_g×9) / 4`

### Fiber

**14 g per 1,000 kcal** (Dietary Guidelines for Americans) — roughly 25 g/day for women, 38 g/day for men at maintenance. Most plans undershoot this. Check it explicitly.

## Step 4: Build the Plan

Rotate 3–4 breakfast templates, 4–5 lunch/dinner templates across the week — enough variety to prevent burnout, enough repetition to keep prep and shopping simple.

```text
## Monday — Target: 2,200 kcal | 165P / 220C / 73F

Breakfast (520 kcal): Greek yogurt 250g + berries 100g + granola 40g + chia 10g → 32P / 58C / 14F
Lunch (640 kcal): Chicken breast 170g + brown rice 200g cooked + roasted veg 200g + olive oil 10g → 48P / 62C / 16F
Snack (230 kcal): Apple + almond butter 20g → 5P / 28C / 12F
Dinner (630 kcal): Salmon 150g + sweet potato 250g + broccoli 150g → 42P / 56C / 22F
Pre-bed (180 kcal): Cottage cheese 180g → 22P / 7C / 4F

Daily total: 2,200 kcal | 149P / 211C / 68F | Fiber: ~31g ✓
```

**Nutrition data sources** — for accurate macros, query the USDA FoodData Central API rather than guessing:

- Base URL: `https://api.nal.usda.gov/fdc/v1/` — free API key from api.data.gov, 1,000 req/hr limit
- Search: `GET /foods/search?query=chicken breast&api_key=KEY`
- Lookup: `GET /food/{fdcId}?api_key=KEY` returns full nutrient profile per 100g
- Python clients on PyPI: `fooddatacentral` (simple), `usda-fdc` (includes DRI comparison + recipe aggregation)
- Data is public domain (CC0). Branded foods update monthly.

## Step 5: Shopping List

Aggregate ingredients across all days, round to purchasable units, organize by store section:

```text
PROTEINS: Chicken breast 1.2kg · Salmon 450g · Eggs 1 dozen · Greek yogurt 1.8kg · Cottage cheese 750g
PRODUCE: Broccoli 2 heads · Sweet potato 1.5kg · Mixed berries 700g · Spinach 300g · Apples 5
GRAINS/PANTRY: Brown rice 1kg · Oats 500g · Granola 300g · Almond butter 1 jar · Chia 100g
```

## Step 6: Meal Prep Logistics

**Single prep session (Sun, ~90 min):** Cook all grains. Roast two sheet-pans of proteins + veg. Portion into containers. Prep overnight oats for 3 days.

**USDA-backed refrigerated shelf life:** cooked poultry/meat 3–4 days · cooked fish 3–4 days · cooked grains 4–6 days · cut raw veg 3–5 days. Freeze anything for day 5+.

## Fitness Schedule (Condensed)

**Beginner (<6 mo): Full body 3×/week** (Mon/Wed/Fri). Each session: 1 squat pattern, 1 hinge, 1 push, 1 pull, 1 carry/core. 3×8–12. Simplest progression: add 2.5 kg when all sets hit the top of the rep range.

**Intermediate (6 mo–2 yr): Upper/Lower 4×/week.** Mon upper-push emphasis, Tue lower-quad, Thu upper-pull, Fri lower-hinge.

**Advanced: Push/Pull/Legs 5–6×/week.**

**Volume guidelines** (per muscle group per week, meta-analytic consensus): 10–20 hard sets for hypertrophy. Below 10 is maintenance; above 20 shows diminishing returns and rising injury risk for most.

**Rep ranges:** 3–6 strength-biased · 6–15 hypertrophy (all ranges build muscle if taken near failure; hypertrophy is not rep-range-specific) · 15+ endurance-biased.

**Progressive overload is mandatory** — log every session. No log → no plan.

**Recovery:** ≥1 full rest day/week. 7–9 hrs sleep. Deload (−40–50% volume) every 4–6 weeks.

**Cardio:** General health → 150 min/week moderate (WHO guideline). Fat-loss phase → add 2–3 × 20–30 min sessions, steady-state or intervals. Muscle-gain phase → keep cardio to 1–2 light sessions to minimize interference.

## Output: Always Build a Visual Web App

**Every meal plan MUST be delivered as an interactive React + Vite web app.** Do not output plans as plain text or markdown — always build and deploy a visual website.

### Core Layout: Week-by-Week Calendar View

The app should display the meal plan as a visual weekly calendar grid:

1. **Week selector** — tabs or navigation for Week 1, Week 2, etc. If the plan has cycling options (e.g., 2-week rotation, high/low carb days), show each cycle as a separate week tab.
2. **Day columns** — 7 columns (Mon–Sun), each showing all meals for that day as stacked cards.
3. **Meal cards** — each card shows:
   - Meal name (Breakfast, Lunch, Dinner, Snack)
   - Food items with portions
   - Per-meal macros: P / C / F / kcal
   - Color-coded macro bar (protein=blue, carbs=amber, fat=red)
4. **Daily summary row** — bottom of each column shows daily total kcal and macro breakdown vs target (with green/yellow/red indicator for on-target/close/off)

### Multiple Options & Cycling

- **Meal swaps** — for each meal slot, offer 2–3 alternatives the user can click to swap in. Show a small "swap" icon on each meal card that reveals alternatives in a dropdown or modal.
- **Rotation plans** — if the user wants variety (e.g., "don't repeat the same dinner twice in 2 weeks"), build a 2-week rotation with different week tabs.
- **High/low day cycling** — for carb cycling or calorie cycling plans, label each day (e.g., "High Day — 2,400 kcal" vs "Low Day — 1,800 kcal") and color-code the day header accordingly.

### Additional Views / Sections

- **Shopping list tab** — aggregated by store section (Proteins, Produce, Grains/Pantry, Dairy, Frozen), with quantities rounded to purchasable units. Checkboxes for each item.
- **Prep guide tab** — Sunday prep timeline as a visual step-by-step with estimated times.
- **Macro dashboard** — summary panel showing weekly averages vs targets: avg daily kcal, protein g/kg, fiber g, and a simple bar chart comparing planned vs target.
- **Training schedule** — if fitness plan is included, show as a sidebar or separate tab with day-by-day exercises.

### UI/UX Requirements

- **Clean, appetizing design** — warm color palette, rounded cards, readable portions
- **Mobile-responsive** — stack day columns vertically on mobile
- **Click to expand** — meal cards expand on click to show full ingredient list, cooking notes, and nutrition detail
- **Print-friendly** — `@media print` stylesheet that renders the week view cleanly on paper

### Data Architecture

Embed all plan data as JSON in the app:

```typescript
interface MealPlan {
  weeks: Week[];
  profile: { goal: string; tdee: number; target_kcal: number; macros: Macros };
  shoppingList: ShoppingSection[];
  prepGuide: PrepStep[];
}

interface Week {
  label: string;  // "Week 1", "High Carb Cycle", etc.
  days: Day[];
}

interface Day {
  name: string;  // "Monday"
  label?: string; // "High Day", "Rest Day", etc.
  target_kcal: number;
  meals: Meal[];
}

interface Meal {
  slot: 'breakfast' | 'lunch' | 'dinner' | 'snack' | 'pre-bed';
  name: string;
  items: { food: string; portion: string; }[];
  macros: Macros;
  alternatives?: Meal[];  // swap options
}

interface Macros { protein: number; carbs: number; fat: number; fiber: number; kcal: number; }
```

## Best Practices

1. **Adherence beats optimization** — a 90%-adhered B+ plan beats a 50%-adhered A+ plan. Build around foods the user already likes.
2. **Protein is the anchor macro** — set it in g/kg first, then fill carbs/fat by preference.
3. **Budget a 10% flex buffer** — plans that forbid all unplanned food get abandoned.
4. **Re-calculate TDEE after weight changes ~5 kg** — BMR shifts with body mass.
5. **Track for 2 weeks before adjusting** — daily weight fluctuates ±1–2 kg from water/glycogen/gut contents. Use a 7-day rolling average.

## Limitations

- Nutritional values are estimates (±10–15% even with USDA data — portion eyeballing adds more error)
- TDEE formulas are population averages with ~10% individual error — real-world tracking over 2–3 weeks is the only way to find someone's true maintenance
- Not a substitute for a registered dietitian, especially for medical conditions, disordered eating history, or pregnancy
- Training templates are generic — modify around injuries and individual response

```

---

## Secondary Skill: personal-shopper

**Path:** `.local/secondary_skills/personal-shopper/SKILL.md`

```markdown
---
name: personal-shopper
description: Research products, compare options, and find the perfect gift based on recipient and occasion.
---

# Personal Shopper & Gift Finder

Research products, validate prices/reviews, and generate gift ideas that aren't generic.

## When to Use

- "What's the best [X] under $[Y]?" / product comparison
- "Is this Amazon deal real?" / price validation
- Gift ideas for a specific person

## When NOT to Use

- Market research (deep-research), budgeting (budget-planner), used cars (used-car-advisor)

## Research Sources — Where to Actually Look

### Review & Research Sites

| Category | Best source | Why |
|----------|-------------|-----|
| Most consumer goods | Wirecutter (nytimes.com/wirecutter) | Long-term testing, updates picks when they fail |
| TVs, monitors, headphones, soundbars | `rtings.com` | Lab-measured data (input lag in ms, frequency response graphs), not vibes |
| Appliances, cars, mattresses | Consumer Reports (paywalled) — search `"consumer reports [product] reddit"` for summaries | |
| Enthusiast gear (knives, keyboards, flashlights, coffee, pens) | Product subreddit wiki/FAQ — `site:reddit.com/r/[hobby] wiki` | Actual users, not affiliate sites |
| Outdoor/camping | `outdoorgearlab.com` | Side-by-side field testing |
| Laptops | `notebookcheck.net` | Thermals, throttling, display calibration data |
| Skincare/cosmetics ingredients | `incidecoder.com` | Ingredient breakdown, no marketing |

### Curated & Boutique Sources

Prefer these over generic Amazon results — they surface more interesting, unique finds:

| Source | Best for | Why |
|--------|----------|-----|
| Wirecutter (nytimes.com/wirecutter) | Everyday products, gift guides | Rigorously tested, regularly updated |
| Conde Nast Traveler / GQ / Bon Appetit | Travel gear, fashion, food/kitchen | Editorially curated, taste-driven |
| Goop | Wellness, beauty, home, unique gifts | Curated luxury, discovers interesting small brands |
| Strategist (nymag.com/strategist) | Gift guides, home, fashion, wellness | Real-person recommendations, not algorithm-driven |
| Cool Material (`coolmaterial.com`) | Men's gifts, gear, home goods | Curated interesting finds |
| Uncommon Goods (`uncommongoods.com`) | Unique/artisan gifts | Handmade, small-batch, creative |
| Food52 (`food52.com`) | Kitchen, home, food gifts | Chef-tested, beautifully curated |
| Reddit gift threads | Any category | Search `site:reddit.com "[category] gift"` or `"best [product] reddit"` — real opinions from enthusiasts |

**Search pattern for honest reviews:** `"[product] reddit"` or `"[product] site:reddit.com"` — cuts through SEO affiliate spam. Also `"[product] long term"` or `"[product] after 1 year"`.

**Search pattern for curated finds:** `"[product/category] site:nymag.com/strategist"` or `"best [category] gifts site:goop.com"` — surfaces editorially picked items over algorithm-promoted ones.

## Price Validation — "Is This Deal Real?"

Amazon "40% off" is often off a fake inflated list price. Verify:

| Tool | Use | Access |
|------|-----|--------|
| **CamelCamelCamel** | Amazon price history chart — paste URL or ASIN | `camelcamelcamel.com` (free, webFetch works) |
| **Keepa** | Same but overlays directly on Amazon pages; more marketplaces | `keepa.com` (free tier sufficient) |

**Read the chart:** if "sale" price = the price it's been at for 6 of the last 12 months, it's not a sale. Real deals sit at or near the all-time low line. Flag any product where price spiked up right before the "discount."

**Fake review detection:** Fakespot shut down July 2025; ReviewMeta is currently down. Manual heuristics:

- Cluster of 5-star reviews in a 2-day window = paid review burst
- Reviews that mention "gift" / "haven't tried yet but looks great" = incentivized
- All reviews are 5 or 1 stars, nothing in between = manipulated
- Check reviewer profiles — dozens of 5-star reviews across random categories = fake account
- Sort by most recent, not "top" — recent reviews reveal quality decline after a product gets popular

## Product Recommendation Format

Always give 3 tiers so the user can self-select on budget:

- **Budget pick** — 80% of the performance at 40% of the price
- **Best overall** — the Wirecutter-style default
- **Upgrade** — only if the premium is justified by a specific use case; say what that use case is

For each: price, one-line "why this one," one-line "main tradeoff," and **always include direct links**:

- **Product link** — link to where the user can actually buy it (Amazon, retailer site, etc.). Search for the specific product and provide the real URL, not a homepage.
- **Review/source link** — link to the review, article, or Reddit thread that informed the recommendation
- **Price history link** — for Amazon products, include a CamelCamelCamel link so the user can check price history themselves

**Never recommend a product without at least a purchase link.** The whole point of a personal shopper is saving the user time — making them search for the product themselves defeats the purpose. Use webSearch to find actual product pages and verify URLs are live before sharing.

## Gift Framework — Beyond "Know the Person"

**The four gift modes** (pick one, don't blend):

1. **Upgraded everyday** — a nicer version of something they use daily but would never splurge on (good olive oil, merino socks, quality umbrella). Safest bet. Works for anyone.
2. **Experience** — class, tickets, tasting, subscription. No clutter. Good for people who "have everything."
3. **Consumable luxury** — fancy food/drink/candle they'll use up. Zero storage burden. Default for acquaintances, hosts, coworkers.
4. **Interest-deep-cut** — something only a real enthusiast would know about. Highest risk, highest reward. Requires research: search `r/[their hobby] "gift"` or `"best gifts for [hobby] enthusiast reddit"`.

**Extraction questions** (ask user, not recipient):

- What do they complain about? (Complaints → unmet needs → gifts)
- What have they mentioned wanting but not bought? (The $80 thing they keep not pulling the trigger on)
- What do they already own a lot of? (Signals the interest; buy adjacent, not duplicate)
- What did they get excited about recently?

**Variety rule — this is critical:**

Recommendations must span different categories. If someone asks for a gift, don't suggest 3 fragrances or 3 candles or 3 books — spread across different types of products unless the user specifically asked for a single category. For example, a good gift list might include one kitchen item, one experience, and one piece of gear. Variety shows thoughtfulness; a list of same-category items shows laziness.

**Hard rules:**

- Scented anything (candles, perfume, lotion) — only if you know their taste. Scent is personal.
- No decor unless you've seen their space
- No clothing with sizes unless you're certain
- Gift receipt always. Return window matters more than wrapping.

| Occasion | Default mode | Budget anchor |
|----------|--------------|---------------|
| Close friend birthday | Interest-deep-cut or upgraded-everyday | Whatever you'd spend on dinner together |
| Acquaintance / coworker | Consumable luxury | $20-40 |
| Housewarming | Consumable (nice pantry goods, wine) — no decor | $25-50 |
| Wedding | Registry. If off-registry, cash. | Cover your plate cost minimum |
| Thank-you | Consumable, handwritten note matters more than price | $15-30 |
| Host gift | Something they can use after you leave (not flowers — requires a vase and attention mid-hosting) | $15-30 |

**Gift recommendations must also include direct purchase links.** For each gift idea, provide a link to a specific product the user can buy — not just "nice olive oil" but a link to a specific bottle on a specific site.

## Limitations

- Can't see real-time stock/price — always tell user to verify before buying
- Can't access paywalled review sites directly (CR, some Wirecutter)
- Can't process transactions

```

---

## Secondary Skill: photo-editor

**Path:** `.local/secondary_skills/photo-editor/SKILL.md`

```markdown
---
name: photo-editor
description: Edit, resize, crop, filter, and optimize images using code-based image processing
---

# Photo Editor

Resize, crop, filter, and optimize images. Pillow for Python, sharp for Node. Clarify intent before starting.

## Clarify Intent First

When a user asks to "edit a photo" or "change an image," the request could mean two very different things. **Ask before proceeding** if it's ambiguous:

1. **Edit the existing image** — crop, resize, recolor, adjust brightness/contrast, add text, remove background, apply filters, watermark, etc. → Use the tools below (Pillow, sharp, OpenCV).
2. **Generate a new AI image** — create something from scratch or heavily reimagine the photo (e.g., "make this photo look like a painting," "put me on a beach," "create a logo from this concept"). → Use image generation tools instead, not this skill.

**When to ask:**

- "Can you fix this photo?" → Probably editing. Ask what specifically needs fixing.
- "Make this look better" → Ambiguous. Ask: "Do you want me to adjust the existing photo (brightness, contrast, cropping, etc.) or generate a new version with AI?"
- "Change the background" → Could be either. Ask: "Should I remove the current background (I can make it transparent or a solid color), or do you want an AI-generated scene behind you?"
- "Make a profile picture from this" → Likely crop/resize, but could mean AI enhancement. Clarify.

**Don't ask when it's obvious:**

- "Crop this to 1080x1080" → Just crop it.
- "Make this a PNG" → Just convert it.
- "Remove the background" → Use rembg.
- "Generate a photo of a sunset" → No existing photo to edit — use image generation.

## Tool Selection

| Tool | Use when | Install |
|---|---|---|
| **Pillow** | Default: resize, crop, filters, text, format conversion | `pip install Pillow` |
| **OpenCV** | Computer vision: face detection, perspective transform, contours | `pip install opencv-python` |
| **sharp** (Node) | High-volume pipelines — 4-5x faster than Pillow (libvips-backed) | `npm install sharp` |
| **rembg** | AI background removal | `pip install rembg` |
| **ImageMagick** | CLI batch ops, 200+ formats | `apt install imagemagick` |

## Open — ALWAYS Fix Orientation First

```python
from PIL import Image, ImageOps

img = Image.open("photo.jpg")
img = ImageOps.exif_transpose(img)   # CRITICAL: applies EXIF rotation, then strips tag

# Without this, phone photos appear sideways after processing

```

## Resize & Crop

```python
from PIL import Image, ImageOps

# --- Fit inside box, keep aspect ratio (shrink only) ---
img.thumbnail((1080, 1080), Image.Resampling.LANCZOS)  # modifies in place

# --- Exact size, keep aspect, center-crop overflow (best for thumbnails) ---
thumb = ImageOps.fit(img, (300, 300), Image.Resampling.LANCZOS, centering=(0.5, 0.5))

# --- Exact size, keep aspect, pad with color (letterbox) ---
padded = ImageOps.pad(img, (1920, 1080), color=(0, 0, 0))

# --- Exact size, ignore aspect (will distort) ---
stretched = img.resize((800, 600), Image.Resampling.LANCZOS)

# --- Scale by factor ---
half = img.resize((img.width // 2, img.height // 2), Image.Resampling.LANCZOS)

# --- Manual crop (left, upper, right, lower) — NOT (x, y, w, h) ---
cropped = img.crop((100, 50, 900, 650))

```

**Resampling filters:** `LANCZOS` for photo downscale (best quality), `BICUBIC` for upscale, `NEAREST` for pixel art/icons (no smoothing).

## Color & Exposure

```python
from PIL import ImageEnhance, ImageOps

# --- Enhancers: 1.0 = unchanged, <1 less, >1 more ---
img = ImageEnhance.Brightness(img).enhance(1.15)
img = ImageEnhance.Contrast(img).enhance(1.2)
img = ImageEnhance.Color(img).enhance(1.1)      # saturation
img = ImageEnhance.Sharpness(img).enhance(1.5)

# --- Quick ops ---
gray = ImageOps.grayscale(img)
inverted = ImageOps.invert(img.convert("RGB"))
auto = ImageOps.autocontrast(img, cutoff=1)     # stretch histogram, clip 1% extremes
equalized = ImageOps.equalize(img)              # flatten histogram

```

## Filters

```python
from PIL import ImageFilter

img.filter(ImageFilter.GaussianBlur(radius=5))
img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))  # better than SHARPEN
img.filter(ImageFilter.BoxBlur(10))
img.filter(ImageFilter.FIND_EDGES)
img.filter(ImageFilter.MedianFilter(size=3))    # denoise, removes salt-and-pepper

```

## Text & Watermark

```python
from PIL import Image, ImageDraw, ImageFont

draw = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)   # Linux default
except OSError:
    font = ImageFont.load_default()                        # fallback (tiny, ugly)

# --- Text with outline ---
draw.text((50, 50), "Caption", font=font, fill="white",
          stroke_width=3, stroke_fill="black")

# --- Centered text ---
bbox = draw.textbbox((0, 0), "Centered", font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
draw.text(((img.width - tw) // 2, (img.height - th) // 2), "Centered", font=font, fill="white")

# --- Watermark (semi-transparent PNG overlay) ---
logo = Image.open("logo.png").convert("RGBA")
logo.thumbnail((img.width // 5, img.height // 5))

# Fade to 40% opacity
alpha = logo.split()[3].point(lambda p: int(p * 0.4))
logo.putalpha(alpha)
pos = (img.width - logo.width - 20, img.height - logo.height - 20)
img.paste(logo, pos, logo)  # third arg = alpha mask — REQUIRED for transparency

```

## Save & Optimize

```python

# --- JPEG ---
img.convert("RGB").save("out.jpg", quality=85, optimize=True, progressive=True)

# convert("RGB") REQUIRED if source has alpha — JPEG can't store transparency

# --- PNG (lossless — quality param does nothing) ---
img.save("out.png", optimize=True, compress_level=9)

# --- WebP (best web format: ~30% smaller than JPEG at same quality) ---
img.save("out.webp", quality=85, method=6)   # method 0-6, 6=slowest/best compression

# --- AVIF (smallest files, Pillow 11+, slower encode) ---
img.save("out.avif", quality=75)             # 75 ≈ JPEG 85 visually, ~50% smaller

# --- Strip all metadata (privacy) ---
clean = Image.new(img.mode, img.size)
clean.putdata(list(img.getdata()))
clean.save("stripped.jpg", quality=85)

```

**Quality guide:** JPEG/WebP 85 = sweet spot. 90+ = diminishing returns. <70 = visible artifacts. Never re-save JPEGs repeatedly — each save degrades (generation loss).

## Batch Processing

```python
from pathlib import Path
from PIL import Image, ImageOps

out = Path("optimized"); out.mkdir(exist_ok=True)
for p in Path("photos").glob("*.[jJ][pP]*[gG]"):   # matches jpg, jpeg, JPG, JPEG
    img = ImageOps.exif_transpose(Image.open(p))
    img.thumbnail((1920, 1920), Image.Resampling.LANCZOS)
    img.convert("RGB").save(out / f"{p.stem}.webp", quality=85, method=6)

```

## sharp (Node.js — use for high throughput)

```javascript
const sharp = require('sharp');

// Resize + convert + optimize, streaming (flat memory)
await sharp('in.jpg')
  .rotate()                          // auto-rotate from EXIF (like exif_transpose)
  .resize(1080, 1080, { fit: 'cover', position: 'center' })  // = ImageOps.fit
  .webp({ quality: 85 })
  .toFile('out.webp');

// fit options: 'cover' (crop), 'contain' (letterbox), 'inside' (shrink to fit), 'fill' (stretch)

// Composite watermark
await sharp('photo.jpg')
  .composite([{ input: 'logo.png', gravity: 'southeast' }])
  .toFile('watermarked.jpg');

```

sharp strips all metadata by default. Use `.withMetadata()` to preserve EXIF/ICC.

## OpenCV (when Pillow isn't enough)

```python
import cv2

img = cv2.imread("in.jpg")                    # BGR order, not RGB!
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Face detection
cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imwrite("out.jpg", img)

# Pillow ↔ OpenCV
import numpy as np
cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
pil_img = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

```

## Platform Dimensions

| Platform | Size | Ratio |
|---|---|---|
| Instagram post | 1080×1080 | 1:1 |
| Instagram story / TikTok | 1080×1920 | 9:16 |
| Twitter/X | 1200×675 | 16:9 |
| YouTube thumbnail | 1280×720 | 16:9 |
| Open Graph (link preview) | 1200×630 | 1.91:1 |

## Gotchas

- **`img.crop()` box is `(left, top, right, bottom)`** — absolute coords, NOT `(x, y, width, height)`
- **`thumbnail()` mutates in place and returns `None`** — don't do `img = img.thumbnail(...)`
- **Paste with transparency** needs the image as the third (mask) arg: `bg.paste(fg, pos, fg)`
- **Palette mode ("P")** breaks many filters — `img.convert("RGB")` first
- **Fonts:** `ImageFont.truetype` needs a real font file. Linux: `/usr/share/fonts/truetype/dejavu/`. Ship a `.ttf` with your code for portability.

```

---

## Secondary Skill: podcast-generator

**Path:** `.local/secondary_skills/podcast-generator/SKILL.md`

```markdown
---
name: podcast-generator
description: Turn research or topics into podcast scripts and audio using ElevenLabs
---

# Podcast Generator

Turn research, articles, or topics into podcast-ready scripts and audio content. Generate conversational scripts with host/guest dynamics and produce audio using ElevenLabs text-to-speech.

## When to Use

- User wants to turn written content into a podcast episode
- User wants to create a podcast-style summary of a topic or paper
- User wants to generate audio content from research
- User mentions "AI Pods", podcast, or audio content creation

## When NOT to Use

- Music creation or sound effects
- Video content (use storyboard skill for planning)
- Written summaries only (use deep-research skill)

## Methodology

### Step 1: Content Ingestion

Gather the source material:

- Read provided documents, articles, or URLs
- Research the topic using webSearch if needed
- Identify key points, interesting angles, and narrative arc
- Note any technical terms that need explanation

### Step 2: Format Selection

Choose the podcast format:

| Format | Description | Best For |
|--------|-------------|----------|
| **Solo explainer** | One host walks through the topic | Tutorials, news summaries, deep dives |
| **Conversational duo** | Two hosts discuss and riff | Making complex topics accessible, entertainment |
| **Interview style** | Host asks questions, expert answers | Technical topics, research papers |
| **Debate** | Two perspectives argue a topic | Controversial or nuanced subjects |
| **Narrative** | Storytelling with narration | Case studies, historical events |

### Step 3: Script Writing — NotebookLM Pattern

The two-host format that works (reverse-engineered from Google's Audio Overviews):

- **Host A = "The Explainer"** — knows the material, breaks down concepts
- **Host B = "The Questioner"** — audience surrogate, asks the "wait, why?" questions
- **Dialog rhythm:** alternate short punchy lines with longer explanations. Sprinkle affirmations: "Right.", "Exactly.", "Okay so—"
- **Arc:** open with common misconception → introduce source that challenges it → unpack implications → "so what does this mean for you"
- **Transitions:** "And on that note..." / "Which brings us to..." / "Here's where it gets weird—"

**Structure (target ~150 words per minute of audio):**

1. **Cold open** (15–30s) — the single most surprising finding, stated as a question or contradiction
2. **Setup** (30–60s) — what we're covering, why it matters now
3. **Segments** (3–5 × 2–4 min) — one idea each; end each with a mini-hook into the next
4. **Takeaways** (1–2 min) — 3 things to remember
5. **Outro** (15s) — sign-off

**Write for ears, not eyes:** contractions always, no semicolons, no parentheticals. If you wouldn't say it out loud, rewrite it.

**Script format** — one line per utterance, speaker tag in brackets, blank line between speakers. This is the unit you'll chunk for TTS:

```text
[ALEX]: So today we're diving into something that honestly broke my brain a little.

[SAM]: Oh no. What now.

[ALEX]: Okay — you know how everyone says [common belief]? There's this paper from [source] that basically says... the opposite.

[SAM]: Wait. The *opposite* opposite?

```

### Step 4: Audio Generation — ElevenLabs

**Install:** `pip install elevenlabs pydub`

**Model choice:** `eleven_multilingual_v2` for quality (10K char limit per call); `eleven_turbo_v2_5` for speed/cost (40K char limit, ~300ms latency, ~3x faster).

**Voice IDs that work for duo podcasts** (from the default library — verify with `client.voices.search()`):

- `JBFqnCBsd6RMkjVDRZzb` (George — warm, mid-range male)
- `21m00Tcm4TlvDq8ikWAM` (Rachel — clear, measured female)
- `pNInz6obpgDQGcFmaJgB` (Adam — energetic narrator)
- `EXAVITQu4vr4xnSDxMaL` (Bella — conversational female)

**Settings for conversational podcast delivery:**

- `stability: 0.45` — lower = more expressive; below 0.3 gets inconsistent
- `similarity_boost: 0.8` — keeps voice consistent across chunks
- `style: 0.3` — mild exaggeration for energy (0 = flat)
- `use_speaker_boost: True`

```python
import os
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import io

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
VOICES = {"ALEX": "JBFqnCBsd6RMkjVDRZzb", "SAM": "21m00Tcm4TlvDq8ikWAM"}

def render_line(speaker: str, text: str) -> AudioSegment:
    audio = client.text_to_speech.convert(
        voice_id=VOICES[speaker],
        text=text,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        voice_settings={"stability": 0.45, "similarity_boost": 0.8,
                        "style": 0.3, "use_speaker_boost": True},
    )
    return AudioSegment.from_mp3(io.BytesIO(b"".join(audio)))

# parse script → list of (speaker, text) tuples, render each, concat
gap = AudioSegment.silent(duration=350)  # 350ms between speakers
episode = sum((render_line(s, t) + gap for s, t in lines), AudioSegment.empty())
episode.export("episode_raw.mp3", format="mp3", bitrate="128k")

```

**Chunking long utterances:** split at sentence boundaries (`.`, `?`, `!`), keep under ~800 chars per call. Pass `previous_text`/`next_text` params to preserve prosody across chunk boundaries.

### Step 5: Loudness Normalization

Podcast standard is **-16 LUFS** (stereo) per Apple/Spotify specs. pydub's `normalize()` is peak-only — not LUFS. Use ffmpeg's two-pass `loudnorm` via the `ffmpeg-normalize` wrapper:

```bash
pip install ffmpeg-normalize
ffmpeg-normalize episode_raw.mp3 -o episode.mp3 -c:a libmp3lame -b:a 128k \
    -t -16 -tp -1.5 -lra 11 --normalization-type ebu

```

`-t -16` = target LUFS, `-tp -1.5` = true-peak ceiling (prevents clipping), `-lra 11` = loudness range. This runs two passes automatically (analyze, then correct).

## Episode Length Guidelines

| Content Type | Target Length | Script Word Count |
|-------------|-------------|-------------------|
| News summary | 5-10 min | 750-1,500 words |
| Topic explainer | 10-20 min | 1,500-3,000 words |
| Deep dive | 20-40 min | 3,000-6,000 words |
| Research paper review | 15-25 min | 2,250-3,750 words |

Rule of thumb: ~150 words per minute of audio.

## Best Practices

1. **Hook early** — if the first 30 seconds aren't interesting, listeners skip
2. **One idea per segment** — don't cram too much; let ideas breathe
3. **Use stories and examples** — abstract concepts need concrete illustrations
4. **Vary pacing** — alternate between fast energy and slow, thoughtful moments
5. **End with value** — give listeners a clear takeaway or action item

## Limitations

- Requires `ELEVENLABS_API_KEY` env var
- Voices mispronounce technical terms/acronyms — spell phonetically in the script (`"Kubernetes"` → `"koo-ber-NET-eez"`) or use ElevenLabs pronunciation dictionaries
- `eleven_multilingual_v2` has known issues with very long single calls (voice drift, occasional stutter) — chunk at sentence boundaries, don't send 5K-char blobs
- Cost: ~$0.18–0.30 per 1000 characters depending on plan; a 20-min episode (~3000 words) ≈ $3–5

```

---

## Secondary Skill: product-manager

**Path:** `.local/secondary_skills/product-manager/SKILL.md`

```markdown
---
name: product-manager
description: Create PRDs, write user stories, prioritize features, and plan product roadmaps.
---

# Product Manager

Write PRDs, user stories, and roadmaps. Prioritize features. Default to real templates from top product orgs, not textbook generics.

## When to Use

- PRD, spec, or one-pager needed
- Backlog prioritization
- User stories + acceptance criteria
- Roadmap planning

## When NOT to Use

- Technical architecture (core agent capabilities)
- User research / discovery (design-thinker)

## PRD Formats — Pick by Context

The three most-copied templates in tech. Ask the user their team size and culture, then pick:

### Amazon PR/FAQ ("Working Backwards")

Write the press release *before* building. Used for every Amazon product since 2004 (AWS, Kindle, Prime). Format:

- **Press release (1 page, strict)**: Headline (`[Company] announces [product] to enable [customer] to [benefit]`), sub-headline, dated intro paragraph, problem paragraph (3-4 problems max), solution paragraph, customer quote, how to get started.
- **Internal FAQ**: Every hard question a VP would ask. "What's the BOM?" "Why won't [competitor] crush this?" "What's the failure mode?"

Why it works: the press-release frame forces customer language and ruthlessly exposes when you can't articulate the benefit. If the PR is boring, the product probably is too.

Source templates: Colin Bryar (ex-Bezos chief of staff) at `coda.io/@colin-bryar/working-backwards`, Ian McAllister's LinkedIn template, `github.com/Green-Software-Foundation/pr-faqs` for a real org using PR/FAQ on GitHub.

**Best for**: Big bets, new product lines, when you need exec alignment before committing eng resources.

### Intercom "Intermission" (1-page hard limit)

Paul Adams (VP Product): "An Intermission must always fit on a printed A4 page. If it does not, you haven't a clear enough view of the problem yet." Sections:

- **Problem**: What's broken, why now, links to customer conversations
- **Job Stories** (Intercom invented these — replaces user stories): `When [situation], I want to [motivation], so I can [expected outcome]`. Situation > persona. "When I'm on-call at 3am and an alert fires" beats "As a DevOps engineer."
- **Success criteria**: Qualitative + quantitative
- **NO solution section** — solutions go in Figma, not the PRD

**Best for**: Feature-level work, fast-moving teams, when scope creep is the enemy.

### Linear's Project Spec

Nan Yu (Head of Product at Linear). Short, outcome-focused: Problem → Proposed solution → Success metrics → Non-goals → Open questions. Non-goals are load-bearing — explicitly listing what you're *not* building is the single most effective scope-creep prevention.

**Best for**: Eng-heavy teams already in Linear, projects with clear shape.

Full template collection: `hustlebadger.com/what-do-product-teams-do/prd-template-examples/` (Figma, Asana, Shape Up, Lenny's 1-Pager all compared).

### Cross-template patterns (from analysis of 13+ company PRDs)

1. Problem strictly before solution — every high-performing template enforces this
2. Explicit "Non-goals" section — second most common element
3. Living docs — version + changelog, not write-once

## Prioritization

**RICE** (Intercom's framework — the de facto standard):

- **Reach**: Users affected per quarter. Use real numbers from analytics, not guesses.
- **Impact**: 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal
- **Confidence**: 100% = data-backed, 80% = strong intuition, 50% = guessing. This multiplier is what makes RICE better than ICE — it punishes wishful thinking.
- **Effort**: Person-months, all functions (PM + design + eng + QA)
- Score = (R × I × C) / E. Build as a spreadsheet — agent can generate CSV.

**When NOT to use RICE**: When effort estimates are garbage (early-stage), when one item is existential (just do it), when the list is >30 items (you have a strategy problem, not a prioritization problem).

**Cost of Delay / WSJF** (SAFe framework): (User value + Time criticality + Risk reduction) / Job size. Better than RICE when timing/sequencing matters (regulatory deadlines, market windows).

**Kano**: Survey users on each feature twice — "how would you feel if we had this?" and "how would you feel if we didn't?" Cross-tab reveals Basic/Performance/Delighter/Indifferent. Reference: `foldingburritos.com/blog/kano-model` for the full method + survey template.

## Roadmap Format

Now / Next / Later (GOV.UK popularized this — intentionally vague on dates to avoid roadmap-as-contract):

```text

## Theme: [one strategic bet this quarter]

### Now (committed, in flight)
| Initiative | Owner | Success metric | Status |

### Next (committed, not started)
| Initiative | Why now | Dependency |

### Later (directional, not committed)

- [bullets only — dates here are lies]

```

Public roadmap examples to reference: `github.com/github/roadmap` (GitHub's own), Buffer's transparent roadmap, Linear's changelog.

## Acceptance Criteria

Gherkin syntax (Given/When/Then) — directly executable as test cases:

```text
Given [precondition]
When [action]
Then [observable result]
And [additional result]

```

One scenario per acceptance criterion. If you can't write it as Given/When/Then, the requirement is ambiguous.

## Limitations

- Cannot integrate with Jira/Linear/Asana — deliver as markdown for copy-paste
- Cannot access user analytics — ask user for reach/retention numbers before RICE scoring
- Templates are starting points; teams should adapt

```

---

## Secondary Skill: programmatic-seo

**Path:** `.local/secondary_skills/programmatic-seo/SKILL.md`

```markdown
---
name: programmatic-seo
description: Build SEO-optimized pages at scale using templates and data (directories, comparisons, locations, integrations)
---

# Programmatic SEO

Build SEO-optimized pages at scale using templates and data. Create page generators that target keyword patterns and produce unique, valuable content for each variation.

## When to Use

- User wants to create many SEO-driven pages from a template (e.g., "[product] vs [competitor]", "[service] in [city]")
- User mentions programmatic SEO, template pages, directory pages, location pages, or comparison pages at scale
- User wants to build an "alternatives to X" page set, integrations directory, or glossary
- User has a data set they want to turn into individual landing pages

## When NOT to Use

- Auditing existing SEO issues (use seo-auditor skill)
- Writing a single blog post or landing page (use content-machine skill)
- One-off competitive analysis (use competitive-analysis skill)

## Core Principles

1. **Unique value per page** — Every page must provide value specific to that page, not just swapped variables in a template
2. **Proprietary data wins** — Hierarchy: proprietary > product-derived > user-generated > licensed > public (weakest)
3. **Subfolders, not subdomains** — `yoursite.com/templates/resume/` not `templates.yoursite.com/resume/`
4. **Match search intent** — Pages must actually answer what people are searching for
5. **Quality over quantity** — 100 great pages beat 10,000 thin ones

## Content Authenticity — Don't Hallucinate Business Data

When building programmatic SEO for **the user's own company**, you will not have access to their internal data (customer stories, case studies, testimonials, product metrics, pricing, team bios, etc.). **Do not fabricate this information.**

**Before generating any company-specific content, ask the user for:**

- Customer names, logos, or testimonials they want featured
- Case study data (metrics, outcomes, quotes)
- Product-specific details (features, pricing tiers, integrations list)
- Any proprietary data that should populate template variables

**If the user hasn't provided this data, default to safe content patterns:**

- Industry research and statistics (sourced via `webSearch`)
- General descriptions of the problem/solution category
- Feature explanations based on what's publicly visible on their site (use `webFetch` on their domain)
- Placeholder blocks clearly marked `[INSERT: customer testimonial]` or `[INSERT: case study metrics]`
- Comparison data pulled from public sources (G2, Capterra reviews via `webSearch`)

**Never generate:** fake customer quotes, fabricated ROI numbers, invented case studies, made-up testimonials, or fictional company metrics. These damage trust and can create legal liability.

For **generic/research topics** (e.g., "[city] cost of living", "[tool A] vs [tool B]", glossary terms), use `webSearch` to gather real data and cite sources.

## Proven Playbooks (Real Traffic Numbers)

| Playbook | URL pattern | Who does it | Scale |
|---|---|---|---|
| **Integrations** | `/apps/[A]/integrations/[B]` | **Zapier** — ~56k pages, 5.8M+ monthly organic visits, ranks for 1.3M keywords. Proprietary data (triggers/templates per app pair) no one else can replicate. | N² combinations |
| **Conversions** | `/currency-converter/[from]-to-[to]-rate` | **Wise** — 8.5M pages across locale subfolders, 60M+ monthly visits. Live exchange-rate data + fee calculators = unique value per page. | N² × locales |
| **Locations** | `/Restaurants-[city]`, `/[cuisine]-Restaurants-[city]`, `/Restaurants-[neighborhood]` | **Tripadvisor** — 700M+ pages, 226M+ monthly visits. UGC reviews keep pages fresh; layered matrix (city × cuisine × neighborhood). | city × category × modifier |
| **Data profiles** | `/[city-slug]` | **Nomad List** — cost-of-living, internet speed, safety scores per city. Pages are pure data tables — minimal prose, high value. | N entities |
| **Comparisons** | `/[A]-vs-[B]`, `/alternatives/[A]` | **G2, Capterra** — "vs" pages + "alternatives" pages, populated by user reviews. | N² / 2 |
| **Templates** | `/templates/[type]` | **Canva, Notion** — each template is a landing page. | N types |
| **Glossary** | `/learn/[term]` | **Ahrefs, HubSpot** — definition pages cluster topical authority. | N terms |
| **Personas** | `/[product]-for-[audience]` | "CRM for real estate agents" | N × M |

**The test:** If your data doesn't meaningfully change between page variations, don't build it. Zapier works because Slack+Asana genuinely differs from Slack+Trello. "Plumber in Austin" vs "Plumber in Dallas" with identical boilerplate = thin content penalty.

Layer playbooks for long-tail: Tripadvisor's "Best Italian Restaurants in Chinatown NYC" = curation × cuisine × neighborhood.

## Implementation

### Step 1: Keyword Pattern Research

- Identify the repeating structure and variables
- Count how many unique combinations exist
- Validate demand: aggregate search volume, distribution (head vs. long tail), trend direction

### Step 2: Data Requirements

- What data populates each page?
- Is it first-party, scraped, licensed, or public?
- How is it updated and maintained?

### Step 3: Template Design

**Page structure:**

- H1 with target keyword
- Unique intro (not just variables swapped — conditional content based on data)
- Data-driven sections with original insights/analysis per page
- Related pages / internal links
- CTAs appropriate to intent

**Ensuring uniqueness — critical to avoid thin content penalties:**

- Conditional content blocks that vary based on data attributes
- Calculated or derived data (not just raw display)
- Editorial commentary unique to each entity
- User-generated content where possible

### Step 4: Internal Linking Architecture

**Hub and spoke model:**

- Hub: Main category page (e.g., "/integrations/")
- Spokes: Individual programmatic pages (e.g., "/integrations/slack-asana/")
- Cross-links between related spokes

Every page must be reachable from the main site. Include XML sitemap and breadcrumbs with structured data.

### Step 5: Indexation Strategy

- Prioritize high-volume patterns for initial crawling
- Noindex very thin variations rather than publishing them
- Manage crawl budget (separate sitemaps by page type)
- Monitor indexation rate in Search Console

### Step 6: Build the Page Generator (Framework Patterns)

**Rendering strategy decision:**

| Page count | Data freshness | Strategy |
|---|---|---|
| <1,000 | Rarely changes | **SSG** — pre-render everything at build |
| 1,000-100,000 | Changes daily/weekly | **ISR** — pre-render popular subset, generate rest on-demand + cache |
| 100,000+ or live data | Real-time (prices, rates) | **ISR with short revalidate** or SSR |

SSG is fastest but build time scales linearly — 50k pages can mean 30+ min builds. ISR is the pSEO sweet spot: instant deploys, pages generate on first request then cache.

**Next.js App Router pattern (`app/[category]/[slug]/page.tsx`):**

```tsx
// Pre-render popular combos at build, generate rest on-demand
export async function generateStaticParams() {
  const popular = await db.query('SELECT slug FROM entities ORDER BY search_volume DESC LIMIT 500');
  return popular.map(e => ({ slug: e.slug }));
  // Return [] to skip build-time generation entirely — all pages ISR-on-demand
}

export const dynamicParams = true;  // allow slugs NOT in the list above (generate + cache on first hit)
export const revalidate = 3600;     // re-generate page at most once/hour when requested

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const entity = await getEntity(slug);
  return {
    title: `${entity.name} — ${entity.category} | Brand`,
    description: entity.summary,
    alternates: { canonical: `https://site.com/${entity.category}/${slug}` },
  };
}

export default async function Page({ params }) {
  const { slug } = await params;
  const entity = await getEntity(slug);
  if (!entity) notFound();  // 404 — don't serve thin pages for bad slugs
  // ... render template with entity data
}

```

**Critical ISR rules:** `generateStaticParams` is NOT re-run on revalidation. Must return an array (even `[]`) or the route becomes fully dynamic. Set `dynamicParams = false` only if you want 404s for anything not pre-generated. `fetch()` calls inside `generateStaticParams` are automatically deduplicated across layouts/pages.

**For nested routes** (`/apps/[appA]/integrations/[appB]`): child `generateStaticParams` receives parent params — generate appB list *per* appA rather than the full N² matrix upfront.

**Astro alternative** (better for content-heavy, less-interactive pages):

```js
// src/pages/[category]/[slug].astro
export async function getStaticPaths() {
  const entities = await loadEntities();
  return entities.map(e => ({ params: { category: e.cat, slug: e.slug }, props: { entity: e } }));
}

```

Astro ships zero JS by default — better Core Web Vitals for pure content pages. No native ISR; use on-demand rendering + CDN cache headers (`Cache-Control: s-maxage=3600, stale-while-revalidate`).

**Sitemaps at scale:** Google's limit is 50,000 URLs per sitemap file. Use `next-sitemap` (Next.js) or custom generation to shard into `sitemap-1.xml`, `sitemap-2.xml`... referenced by a sitemap index. For ISR sites, generate sitemaps server-side from the DB, not at build time. **Warning:** Google will NOT index all pages immediately — indexation at scale takes weeks/months. Prioritize high-volume slugs in the first sitemap.

## Quality Checks

### Pre-Launch

- [ ] Each page provides unique value beyond variable substitution
- [ ] Answers search intent for the target keyword
- [ ] Unique titles and meta descriptions per page
- [ ] Proper heading structure and schema markup
- [ ] Page speed acceptable
- [ ] Connected to site architecture (no orphan pages)
- [ ] In XML sitemap and crawlable

### Post-Launch Monitoring

Track: indexation rate, rankings by page type, traffic, engagement metrics, conversion rate

Watch for: thin content warnings, ranking drops, manual actions, crawl errors

## Common Mistakes

- **Thin content**: Just swapping city names in identical content (Google will deindex)
- **Keyword cannibalization**: Multiple pages targeting the same keyword
- **Over-generation**: Creating pages with no search demand
- **Poor data quality**: Outdated or incorrect information erodes trust
- **Ignoring UX**: Pages that exist for Google but not for users

## Output Format

Deliver both a strategy document and the actual implementation:

1. **Strategy**: Opportunity analysis, chosen playbook(s), keyword patterns, data sources, page count estimate
2. **Template**: URL structure, title/meta templates, content outline, schema markup
3. **Implementation**: Working web application that generates and serves the pages, deployed and accessible

## Limitations

- Cannot access Search Console data to monitor indexation
- Cannot check existing backlink profiles
- Data quality depends on the source — always validate before publishing
- Cannot guarantee rankings — SEO involves many factors beyond on-page optimization

```

---

## Secondary Skill: real-estate-analyzer

**Path:** `.local/secondary_skills/real-estate-analyzer/SKILL.md`

```markdown
---
name: real-estate-analyzer
description: Evaluate properties, neighborhoods, and investment returns for home buying
---

# Real Estate Analyzer

Analyze properties, neighborhoods, and real estate investment opportunities for home buyers and investors. Evaluate listings, estimate fair value, assess neighborhoods, and model investment returns.

## When to Use

- User wants to evaluate a property listing for purchase
- User asks about neighborhood quality, schools, or safety
- User wants to compare properties or neighborhoods
- User needs help estimating if a home is fairly priced
- User wants to analyze a property as an investment (rental yield, appreciation)

## When NOT to Use

- Apartment rental hunting (use apartment-finder skill)
- Mortgage or loan calculations only (use budget-planner skill)
- Legal review of purchase agreements (use legal-contract skill)

## Methodology

### Step 1: Property Assessment

Gather and evaluate listing details:

**Basic Details:**

- Address, price, square footage, lot size
- Bedrooms, bathrooms, year built
- Property type (single-family, condo, townhouse, multi-family)
- Days on market, price history, price reductions

**Condition Indicators:**

- Age of major systems (roof, HVAC, water heater, electrical)
- Recent renovations or updates
- Foundation type and condition
- Photos analysis — look for staging tricks, unflattering angles, missing rooms

**Red Flags:**

- Significantly below market price (could indicate undisclosed issues)
- Frequent ownership changes (flipped too fast?)
- "As-is" or "investor special" language
- Missing disclosures or incomplete listing info
- High DOM (days on market) without price reduction

### Step 2: Valuation Analysis

**Pull comps — specific sources:**

- `webFetch` Redfin sold filter: `redfin.com/city/{id}/filter/include=sold-6mo` — recently sold within 0.5mi, ±20% sqft, same beds
- Zillow Research (`zillow.com/research/data/`) — free CSV downloads of ZHVI (home value index) and ZORI (rent index) by ZIP, monthly back to 1996
- County assessor website — webSearch `"{county name} property assessor {address}"` for tax-assessed value, last sale price, permit history. Assessed value is typically 70-90% of market value.
- Adjust comps: ±$15-40/sqft for size delta, ±$5-15k per bedroom, ±10-20% for condition

**Affordability math (compute, don't estimate):**

```python

# PITI at 30yr fixed — webSearch current rates (use Freddie Mac PMMS)
# PMMS reports percentage (e.g. 6.76), so divide by 100 first
P, r, n = loan_amount, annual_rate/100/12, 360
monthly_PI = P * (r*(1+r)**n) / ((1+r)**n - 1)

# + property tax (county rate × assessed value / 12)

# + homeowners insurance (~$150-250/mo, varies wildly by state)

# + PMI if <20% down (~0.5-1.0% of loan/yr)

```

- 28/36 rule: PITI <28% gross income, total debt <36%. Lenders stretch to 43% DTI — don't.
- Closing costs: 2-5% of purchase. Maintenance reserve: 1-2% of home value/yr.

### Step 3: Neighborhood Analysis

**webSearch/webFetch targets (name the source, don't be vague):**

- Schools: `greatschools.org/{state}/{city}` — rating ≥7 protects resale value even if user has no kids
- Crime: `crimemapping.com` or `spotcrime.com/{city}` — check 6-month trend, not just snapshot. NeighborhoodScout for demographic overlay.
- Walk/Transit/Bike Score: `walkscore.com/score/{address}`
- Flood: `msc.fema.gov/portal/search` — Zone A/AE/V = mandatory flood insurance ($400-3,000+/yr, often kills deals)
- Market velocity: Redfin Data Center — median DOM, sale-to-list ratio, months of supply. <3 months supply = seller's market.
- Future development: webSearch `"{city} planning commission agenda"` + `"{city} zoning map"` — a highway expansion or apartment rezoning next door changes everything

### Step 4: Investment Analysis — Run the Numbers

**Quick-filter rules (kill deals fast):**

- **1% rule**: monthly rent ≥ 1% of purchase price. Dead in coastal/HCOL markets — there, 0.5-0.7% is realistic and you're betting on appreciation, not cash flow.
- **50% rule**: operating expenses (NOT mortgage) eat ~50% of gross rent. Vacancy + repairs + management + taxes + insurance + capex reserve. Beginners always underestimate this.
- **70% rule (flips/BRRRR)**: max offer = (ARV × 0.70) − rehab cost. ARV = after-repair value from renovated comps.

**Full underwriting (build in Python):**

```text
Gross rent (use Rentometer or Zillow ZORI for the ZIP)
− Vacancy (5-8% typical; 10% conservative)
− Property management (8-10% of collected rent)
− Repairs/maintenance (~8% of rent)
− CapEx reserve (~5% — roof/HVAC/water heater sinking fund)
− Taxes + insurance
= NOI (Net Operating Income)

Cap rate = NOI / purchase price
  → <4%: you're buying appreciation, not cash flow
  → 4-6%: typical for A/B-class in growth metros
  → 6-8%: solid cash flow, B/C-class
  → >10%: either a great deal or a war zone — verify crime data

NOI − annual debt service (P+I) = annual cash flow
Cash-on-cash = annual cash flow / total cash in (down pmt + closing + rehab)
  → Target 8%+ CoC. Below that, an index fund wins with zero tenants.

```

**DSCR (what lenders check for investment loans):**

- DSCR = NOI / annual debt service. Lenders want ≥1.20-1.25× (2025 standard). <1.0 means rent doesn't cover the mortgage.
- DSCR loans (2025): ~6.5-7.5% rate, qualify on property income not W-2, typical max 75% LTV. How investors scale past 10 conventional mortgages.

**BRRRR stack**: Buy distressed (hard money, 7-14 day close) → Rehab → Rent → Refinance at 75% of new ARV into DSCR loan → pull most capital out → Repeat. Only works if `ARV × 0.75 ≥ purchase + rehab + holding costs`.

**Rent comps:** webSearch Rentometer free tier, or pull Zillow rentals for the ZIP and compute median $/sqft for same bed count.

### Step 5: Due Diligence Checklist

Before making an offer:

- [ ] Pre-approval letter from lender
- [ ] Professional home inspection ($300-500)
- [ ] Pest/termite inspection
- [ ] Title search for liens or encumbrances
- [ ] Survey (if boundaries unclear)
- [ ] Flood zone check (FEMA maps)
- [ ] Environmental concerns (radon, lead paint for pre-1978 homes)
- [ ] HOA review (financials, rules, pending assessments)
- [ ] Property tax history and assessment

## Output Format

Always present key findings and recommendations as a plaintext summary in chat, even when also generating files. The user should be able to understand the results without opening any files.

```text

# Property Analysis: [Address]

## Summary

- Asking Price: $XXX,XXX
- Estimated Fair Value: $XXX,XXX — [Over/Under/Fair priced by X%]
- Recommendation: [Strong Buy / Buy / Hold / Pass]

## Property Details
[Key facts table]

## Valuation
[Comps analysis, price per sqft comparison]

## Neighborhood
[Schools, safety, livability scores]

## Financial Analysis
[Monthly payment breakdown, investment returns if applicable]

## Risks & Concerns
[Red flags, upcoming expenses, market risks]

## Verdict
[2-3 sentence recommendation]

```

## Best Practices

1. **Asking price is marketing** — only sold comps within 6 months matter
2. **Model three scenarios** — base case, 10% vacancy + 20% higher repairs, and "tenant trashes it year 1"
3. **Permit history is free alpha** — county assessor site shows pulled permits. No permits on an "updated kitchen" = unpermitted work = your liability.
4. **Price/sqft is a blunt tool** — lot size, corner lots, and basement finish skew it hard. Use for screening, not for offers.
5. **Cap rate without appreciation** — in a flat market, if cap rate < your mortgage rate, you're paying to own it

## Interactive Map — Web App Visualization

After analyzing properties, **build a web app** that displays properties and relevant neighborhood data on an interactive map.

### Property Markers

- **Color-coded by recommendation**: green = Strong Buy, blue = Buy, yellow = Hold, red = Pass
- **Popup on each marker** showing: address, asking price, estimated fair value, beds/baths, sqft, price/sqft, and recommendation
- **Click to expand** with key details: comp-adjusted value, cap rate (if investment), flood zone, school rating

### Neighborhood Context Layers

Display relevant context around the properties:

- **Sold comps** — recent comparable sales as smaller markers, with sale price and date
- **School locations** with GreatSchools ratings (color-coded: green ≥7, yellow 4-6, red <4)
- **Flood zones** if any properties are in or near FEMA Zone A/AE/V
- **Nearby amenities** — transit, grocery, parks when walkability matters to the user

### Geocoding

Use the free Nominatim API (OpenStreetMap) to convert addresses to lat/lng — no API key required:

```text
https://nominatim.openstreetmap.org/search?q={url_encoded_address}&format=json&limit=1
```

Rate limit: max 1 request/second. Batch geocode all addresses before building the map.

Always generate the map alongside the text-based analysis — the map is a visual complement, not a replacement for the detailed evaluation.

## Limitations & Disclaimer

- **This is NOT real estate, legal, or financial advice.** Informational analysis only. Always engage a licensed realtor, real estate attorney, and professional inspector before purchasing.
- Cannot access MLS — Redfin/Zillow public data lags and misses pocket listings
- Cannot provide appraisals (licensed appraiser required for lending)
- Cannot physically inspect — photos hide foundation cracks, mold, and grading issues
- Market snapshot only — rates and comps move weekly

```

---

## Secondary Skill: recipe-creator

**Path:** `.local/secondary_skills/recipe-creator/SKILL.md`

```markdown
---
name: recipe-creator
description: Create recipes, suggest meals from available ingredients, and provide nutritional guidance.
---

# Recipe Creator

Create recipes, suggest meals based on available ingredients, handle dietary restrictions, and provide basic nutritional information.

## When to Use

- User wants a recipe for a specific dish
- User has ingredients and wants meal ideas
- User needs recipes for dietary restrictions (vegan, gluten-free, keto)
- User wants to scale a recipe up or down
- User wants meal prep or batch cooking plans

## When NOT to Use

- Detailed meal planning with fitness goals (use meal-planner skill)
- Health data analysis (use personal-health skill)

## Methodology

### Output — Visual Recipe Card, Not Markdown

**Do not output recipes as plain markdown text.** Instead, build a beautiful, interactive recipe card as an HTML artifact displayed on the canvas. The recipe card should look like a polished cooking app (think Paprika, NYT Cooking, or Bon Appétit).

#### Recipe Card Requirements

1. **Generated hero image** — Use `generateImage` to create a photorealistic, appetizing hero image of the finished dish. Place it at the top of the card. Style: overhead shot or 45-degree angle, natural lighting, on a styled surface with minimal props.

2. **Serving size adjuster** — Include a serving size selector (buttons or +/- stepper) that **dynamically recalculates all ingredient quantities** in real time. Store the base recipe quantities in JavaScript and multiply on change:

```javascript
// Store base recipe for N servings
const baseServings = 4;
const ingredients = [
  { name: "chicken breast", qty: 2, unit: "lbs" },
  { name: "olive oil", qty: 2, unit: "Tbsp" },
  // ...
];

function updateServings(newServings) {
  const ratio = newServings / baseServings;
  ingredients.forEach(ing => {
    const scaled = ing.qty * ratio;
    // Display with smart fractions (¼, ½, ¾) for common amounts
  });
}
```

1. **Card layout** — Structure the visual card with:
   - Hero image (full-width, 16:9 or 4:3)
   - Recipe title (large, styled)
   - Metadata bar: prep time, cook time, total time, difficulty, servings adjuster
   - Ingredients list (left column or collapsible section) — checkboxes so users can tick off items
   - Step-by-step instructions (numbered, with visual/audio cues highlighted)
   - Nutrition facts panel (per serving, updates with serving size)
   - Notes section: storage, substitutions, allergen flags

2. **Styling** — Clean, modern, food-magazine aesthetic. Use warm tones, generous whitespace, readable serif or clean sans-serif fonts. Mobile-friendly layout. No cluttered sidebars.

Place the recipe card on the canvas as an iframe (1280x900 or similar).

### "What Can I Make?" Logic

Think in **formula + flavor profile**, not recipe lookup:

1. Bucket ingredients: protein / starch / veg / aromatic / fat / acid
2. Match a base formula (stir-fry, braise, grain bowl, frittata, soup, sheet-pan roast)
3. Assign a flavor direction based on what's in the pantry (soy+ginger+sesame → East Asian; cumin+lime+cilantro → Mexican; lemon+garlic+oregano → Mediterranean)
4. Every savory dish needs fat + acid + salt to taste finished. If it's "flat," it's missing acid 90% of the time — add lemon, vinegar, or pickled something
5. Rank suggestions by fewest missing ingredients

### Ratios — Cook Without a Recipe

From Ruhlman's *Ratio* (the CIA-derived reference). **All by weight**, not volume — this is why they work:

| Thing | Ratio | Notes |
|-------|-------|-------|
| Bread dough | 5 flour : 3 water (+yeast, salt 2% of flour wt) | Hydration % = water/flour. 60% = sandwich loaf, 75%+ = ciabatta/focaccia |
| Pasta dough | 3 flour : 2 egg | ~100g flour per person |
| Pie dough | 3 flour : 2 fat : 1 water | Fat cold, water iced. Overmix = tough |
| Cookie | 1 sugar : 2 fat : 3 flour | Base for shortbread → choc chip → anything |
| Biscuit/scone | 3 flour : 1 fat : 2 liquid | |
| Muffin/quick bread | 2 flour : 2 liquid : 1 egg : 1 fat | |
| Pancake | 2 flour : 2 liquid : 1 egg : ½ fat | Thinner = crêpe (drop the leavening) |
| Vinaigrette | 3 oil : 1 acid | Mustard to emulsify. Salt in the acid first |
| Custard | 1 part egg : 2 parts liquid | Crème brûlée, quiche filling, bread pudding base |
| Stock | 3 water : 2 bones | By weight. Simmer, never boil |
| Brine | 20 water : 1 salt (5% w/w) | |
| Rice (stovetop) | 1 rice : 1.5 water by volume | Less for jasmine, more for brown |

Knowing the ratio > knowing a recipe. Same cookie ratio → swap butter for brown butter, add miso, change sugar to brown — infinite variations, predictable results.

### Substitutions — With the Actual Conversion

| Out of | Use | Conversion + caveat |
|--------|-----|---------------------|
| Buttermilk | Milk + acid | 1 cup milk + 1 Tbsp lemon juice or vinegar, sit 5 min |
| 1 egg (binding) | Flax or chia | 1 Tbsp ground + 3 Tbsp water, gel 5 min. Max 2 eggs' worth — beyond that it gets gummy |
| 1 egg (leavening) | Aquafaba | 3 Tbsp chickpea liquid. Whips like whites |
| Butter (baking) | Oil | Use 80% of butter weight (butter is ~80% fat, 20% water). Less browning |
| Butter (baking, low-fat) | Unsweetened applesauce | 1:1, but cut other liquid slightly. Cakier texture |
| Heavy cream | Coconut cream (the solid part of the can) | 1:1. Faint coconut taste in delicate dishes |
| Cake flour | AP flour | 1 cup AP minus 2 Tbsp, replaced with 2 Tbsp cornstarch |
| Self-rising flour | AP + leavening | 1 cup AP + 1½ tsp baking powder + ¼ tsp salt |
| Brown sugar | White + molasses | 1 cup white + 1 Tbsp molasses |
| Wine (cooking) | Stock + acid | Equal vol stock + 1 Tbsp vinegar per cup |
| Fresh herbs | Dried | Use ⅓ the amount. Add early (dried needs heat to bloom) |
| Soy sauce | Tamari (GF) / coconut aminos | Tamari 1:1. Coconut aminos: use ~1.3× and add salt (it's sweeter, less salty) |

### Nutrition — Compute, Don't Guess

**USDA FoodData Central** (`fdc.nal.usda.gov`) — free API, no key needed for basic search. The authoritative macro/micro database.

```python

# webFetch or requests

# Search: https://api.nal.usda.gov/fdc/v1/foods/search?query=chicken%20breast&api_key=DEMO_KEY

# Returns per-100g: kcal, protein, fat, carbs, fiber, plus micros

# Scale by actual gram weight, sum across ingredients, divide by servings

```

For quick estimates without the API: protein ~4 kcal/g, carbs ~4 kcal/g, fat ~9 kcal/g, alcohol ~7 kcal/g.

**Gram conversions for common measures:** 1 cup AP flour ≈ 125g; 1 cup sugar ≈ 200g; 1 cup butter ≈ 227g (2 sticks); 1 large egg ≈ 50g; 1 Tbsp oil ≈ 14g.

### Best Practices

- **Visual/audio cues over times** — "onions translucent and soft" beats "5 min" (stove strength varies 2×). "Oil shimmers." "Garlic fragrant, ~30 sec." "Dough springs back slowly."
- **Salt in layers** — season at each stage, not all at the end
- **Rest meat** — 5 min for steaks, 15+ for roasts. Skipping this is the #1 reason home-cooked meat is dry
- Ingredients listed in order of use; prep notes inline ("1 onion, diced")
- Flag top-9 allergens: milk, egg, fish, shellfish, tree nuts, peanuts, wheat, soy, sesame

## Limitations

- Nutrition is computed from generic USDA data — brand variance is real
- Baking ratios assume weight measurement; volume introduces 10-20% error
- Not medical dietary advice

```

---

## Secondary Skill: repl-seo-optimizer

**Path:** `.local/secondary_skills/repl-seo-optimizer/SKILL.md`

```markdown
---
name: repl-seo-optimizer
description: Review and fix SEO issues in your Replit app's code before launch (meta tags, Open Graph, sitemap, structured data, SPA fixes)
---

# Repl SEO Optimizer

Review a Replit-built website or web app and implement SEO improvements directly in the code before launch.

## When to Use

- User wants to make sure their site is SEO-ready before deploying
- User asks to "optimize for SEO" or "make this searchable"
- User is about to launch and wants a pre-flight SEO check
- User notices their deployed site isn't showing up in search results

## When NOT to Use

- Auditing an external website the user didn't build (use seo-auditor skill)
- Building SEO landing pages at scale (use programmatic-seo skill)
- Content strategy or keyword research without a live codebase

## Approach

This is a hands-on skill. Don't just list recommendations — read the code, identify what's missing, and implement the fixes directly.

### Step 1: Scan the Project

Read the project structure to identify:

- Framework (React/Vite, Next.js, Express, Flask, static HTML, etc.)
- Entry point HTML file(s) — `index.html`, `public/index.html`, etc.
- Routing setup — client-side (React Router) vs. server-rendered
- Existing `<head>` content — meta tags, title, Open Graph tags
- Any existing sitemap or robots.txt

### Step 2: Fix Critical SEO Foundations

**Title & Meta Description:**

- Every page needs a unique `<title>` (50-60 chars) with primary keyword near the start
- Every page needs a `<meta name="description">` (150-160 chars) with a clear value proposition
- For SPAs: implement dynamic titles per route (e.g., `document.title` or `react-helmet` / `react-helmet-async`)

**Heading Structure:**

- Exactly one `<h1>` per page/route containing the primary keyword
- Logical hierarchy — no skipping from H1 to H3
- Check that headings aren't used purely for styling

**Semantic HTML:**

- Replace generic `<div>` wrappers with `<header>`, `<main>`, `<nav>`, `<footer>`, `<article>`, `<section>` where appropriate
- Use `<a>` for navigation links, not click-handler divs
- Use `<button>` for actions, `<a>` for navigation

### Step 3: Open Graph & Social Sharing

Add to `<head>` on every page (or the SPA shell):

```html
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Page description">
<meta property="og:image" content="https://yourdomain.com/og-image.png">
<meta property="og:url" content="https://yourdomain.com/page">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Page description">
<meta name="twitter:image" content="https://yourdomain.com/og-image.png">

```

For SPAs, these must be set server-side or via pre-rendering for crawlers to see them.

### Step 4: Technical SEO in Code

**Image Optimization:**

- All `<img>` tags need `alt` attributes (descriptive, not "image1")
- Add `width` and `height` attributes to prevent CLS
- Use `loading="lazy"` on below-the-fold images
- Prefer WebP format where possible

**Link Quality:**

- Internal links use descriptive anchor text, not "click here"
- External links use `rel="noopener noreferrer"` and consider `target="_blank"`
- No broken internal links — check route references match actual routes

**Performance (SEO-impacting):**

- Fonts: use `font-display: swap` in `@font-face` rules
- Defer non-critical JS: `<script defer>` or dynamic imports
- Inline critical CSS or ensure CSS loads early
- Avoid render-blocking resources in `<head>`

### Step 5: Crawlability Setup

**robots.txt** — create at project root / public directory:

```text
User-agent: *
Allow: /
Sitemap: https://yourdomain.com/sitemap.xml

```

**sitemap.xml** — create listing all public pages:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://yourdomain.com/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <!-- Add all public routes -->
</urlset>

```

For dynamic sites, generate the sitemap from your routes programmatically.

**Canonical URLs:**

- Add `<link rel="canonical" href="https://yourdomain.com/current-page">` to each page
- Prevents duplicate content issues between www/non-www, trailing slashes, query params

### Step 6: SPA-Specific Issues

Single-page apps (React, Vue, etc.) have unique SEO challenges:

**Problem:** Crawlers may not execute JavaScript, so they see an empty `<div id="root">`.

**Solutions (in order of preference):**

1. **Pre-rendering:** Use a build-time tool to generate static HTML for each route (e.g., `react-snap`, `prerender-spa-plugin`)
2. **Server-side rendering:** If using Next.js or Remix, SSR is built in — verify pages render server-side
3. **Meta tag injection:** At minimum, ensure the HTML shell has good default meta tags

**SPA Routing:**

- If using hash routing (`/#/about`), switch to browser history routing (`/about`) — search engines ignore hash fragments
- Ensure the server returns the SPA shell for all routes (catch-all / wildcard route) so direct URL access works

### Step 7: Structured Data

Add JSON-LD schema markup in a `<script type="application/ld+json">` block. Choose based on site type:

| Site Type | Schema |
|-----------|--------|
| Business / SaaS | `Organization`, `WebSite`, `WebApplication` |
| Blog / Content | `Article`, `BlogPosting`, `BreadcrumbList` |
| Product / Store | `Product`, `Offer`, `AggregateRating` |
| Portfolio | `Person`, `CreativeWork` |
| Local business | `LocalBusiness`, `PostalAddress` |

Example for a SaaS landing page:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "App Name",
  "description": "What the app does",
  "url": "https://yourdomain.com",
  "applicationCategory": "Category",
  "operatingSystem": "Web"
}
</script>

```

## Pre-Launch Checklist

Run through before deploying:

- [ ] Every page has a unique `<title>` and `<meta name="description">`
- [ ] One `<h1>` per page with relevant keyword
- [ ] Open Graph and Twitter Card meta tags present
- [ ] All images have descriptive `alt` text and dimensions
- [ ] Semantic HTML elements used (`<main>`, `<nav>`, `<header>`, `<footer>`)
- [ ] `robots.txt` exists and allows crawling
- [ ] `sitemap.xml` exists and lists all public pages
- [ ] Canonical URLs set on each page
- [ ] No broken internal links
- [ ] Fonts use `font-display: swap`
- [ ] Below-fold images use `loading="lazy"`
- [ ] Structured data (JSON-LD) added for site type
- [ ] SPA routes work with direct URL access (no 404s)
- [ ] Page loads in under 3 seconds on mobile

## Output

Always present key findings and recommendations as a plaintext summary in chat, even when also generating files. The user should be able to understand the results without opening any files.

## Best Practices

1. **Implement, don't just recommend** — read the actual code and make the changes
2. **Start with the highest-impact fixes** — title tags and meta descriptions matter more than schema markup
3. **Don't over-optimize** — keyword stuffing hurts rankings; write naturally
4. **Test after changes** — run the app and verify pages render correctly with the new tags
5. **Respect the user's content** — improve SEO without changing their messaging or design intent

```

---

## Secondary Skill: resume-maker

**Path:** `.local/secondary_skills/resume-maker/SKILL.md`

```markdown
---
name: resume-maker
description: Build a professional resume web app with viewable HTML page and downloadable PDF/DOCX files. Use when the user asks to create, generate, or build a resume, CV, or curriculum vitae with web preview and file exports.
---

# Resume Maker

Build a resume as a React web page backed by a generation script that produces pixel-perfect PDF and DOCX files from a single data source. The web page reads spacing values from the same JSON so the HTML preview closely matches the generated documents.

## Before You Start Building — Gather Information First

**Do NOT start building the resume until you have enough information to write meaningful, specific content.** A resume with placeholder text or vague bullets is useless. You need real details to create something valuable.

### If the user provides a complete resume or detailed background

Go ahead and start building immediately. You have what you need.

### If the user asks to "make me a resume" without providing details

You MUST ask clarifying questions before writing any code. Ask about:

1. **Target role** — What job or type of role are they applying for? (This shapes the entire resume's framing)
2. **Work experience** — For each role: job title, company name, dates, location, and what they accomplished (not just responsibilities — ask for specific achievements, numbers, outcomes)
3. **Education** — Degree(s), school(s), graduation year(s), honors/GPA if notable
4. **Skills** — Technical skills, tools, languages, frameworks, certifications
5. **Contact info** — Full name, email, phone, LinkedIn, location, portfolio/website
6. **Optional extras** — Publications, talks, awards, volunteer work, projects

### How to ask

Don't dump all questions at once. Start with the most critical:

> "To build you a great resume, I need some info. Let's start with the basics:
>
> 1. What's your full name and contact info (email, phone, LinkedIn, location)?
> 2. What type of role are you targeting?
> 3. Walk me through your work history — for each job, give me the title, company, dates, and your biggest accomplishments with specific numbers if possible."

Then follow up for education, skills, and anything else based on what they share. If they give vague bullets like "managed a team," push back and ask for specifics: *"How large was the team? What did you deliver? Any measurable outcomes?"*

### If the resume feels thin

If the user doesn't have enough experience to fill a page, ask about additional material: volunteer work, side projects, open-source contributions, certifications, coursework, publications, talks, or awards. Proactively suggest these categories — don't just leave the page half-empty.

### If the user provides a job posting

Ask them for their background details, then tailor the resume to match the posting's keywords and requirements. Mirror the posting's language.

## Build Order — Files First, Website Last

Follow this exact order so the user gets fast, tangible results:

1. **Write the generation script** (`generate-resume-files.ts`) with all resume content and run it to produce the PDF, DOCX, and `resume-data.json`
2. **Present the PDF to the user in chat** — show the generated PDF file immediately so they can see their resume right away
3. **Present the DOCX file to the user in chat** — make the DOCX available for download so they can grab it
4. **Build the web app last** — set up the React artifact and API routes that serve the resume page and download endpoints

The user cares most about seeing their resume quickly. The PDF and DOCX are the primary deliverables — get those into the user's hands first. The web app is a nice-to-have that comes after. Do NOT spend time building the web app before the user has seen their PDF and downloaded their DOCX.

## Architecture

```text
scripts/src/generate-resume-files.ts   ← single source of truth for content + layout
  └─ output/
       ├─ resume-data.json             ← consumed by the web frontend
       ├─ <name>-resume.pdf            ← downloadable PDF
       └─ <name>-resume.docx           ← downloadable DOCX

artifacts/<name>/src/pages/resume.tsx   ← React page, reads resume-data.json via API
artifacts/api-server/src/routes/download.ts ← serves PDF, DOCX, and JSON
```

### Data flow

1. `generate-resume-files.ts` holds all resume content in a `getResumeData()` function.
2. The script renders the PDF with jsPDF, measures content height, and auto-adjusts spacing to fill exactly one US Letter page (612×792pt, 36pt margins).
3. It writes the computed spacing values into `resume-data.json` alongside the content.
4. The React page fetches `resume-data.json` at runtime and uses the spacing values (converted pt→px via `96/72`) to render a matching HTML preview.

## Content Rules

- **Summary/blurb**: If you include a personal summary at the top, keep it to 2 sentences max. Long plaintext paragraphs waste prime real estate and recruiters skip them.
- **One page hard limit**: The resume MUST fit on exactly one US Letter page (612×792pt). The auto-fit algorithm handles this, but be mindful when writing content — more bullets doesn't mean better.

## Flag Guesses and Inferred Details

If you had to guess or infer any details — dates, job titles, specific contributions, metrics, technologies — you MUST tell the user what you made up. After presenting the first draft, explicitly list anything you weren't sure about and ask if they want to correct it. For example:

> "I made a few assumptions I want to flag:
>
> - I estimated your dates at Company X as 2021–2023 — are those right?
> - I wrote that you 'reduced API latency by 40%' based on your mention of performance work — is that accurate, or should I adjust the number/framing?
> - I guessed TypeScript and Python for your skills — anything to add or remove?"

Do NOT silently present fabricated details as fact. The user trusts you to be honest about what you know vs. what you inferred.

## Iteration and Changes

When the user requests changes (rewording bullets, adding/removing sections, reordering, etc.):

1. Make the requested changes in `generate-resume-files.ts`
2. **Re-run the generation script** to produce updated PDF, DOCX, and JSON
3. **Verify the output still fits on one page** — if the changes pushed content past the page boundary, the auto-fit algorithm should handle it, but visually confirm. If content is getting clipped or the scale factor is too aggressive (text becoming unreadably small), trim lower-priority bullets or reduce spacing before delivering.
4. **Re-present the updated PDF and DOCX** to the user in chat

Never deliver an updated resume without re-running the generation script. The PDF/DOCX must always reflect the latest content. Every iteration cycle ends with the user seeing a fresh PDF and having a fresh DOCX to download.

## Critical Unit Rules

### DOCX (`docx` npm package)

The `docx` package uses two different unit systems — mixing them up causes 10× sizing bugs:

- **`TextRun.size`** = **half-points**: `ptToHalfPt = pt * 2` (e.g., 11pt → 22)
- **Spacing, margins, page dimensions** = **twips**: `ptToTwip = pt * 20` (e.g., 36pt → 720)

Always define separate converter functions:

```typescript
const ptToHalfPt = (pt: number) => Math.round(pt * 2);
const ptToTwip = (pt: number) => Math.round(pt * 20);
```

### jsPDF baseline rule

`doc.text(text, x, y)` draws text with `y` as the **baseline** — the text body extends upward from y. When placing a horizontal rule after text:

- **Wrong**: `y += 2` after drawing a rule — text overlaps the line
- **Right**: `y += lineHeight` after drawing a rule — full clearance before next text

```typescript
doc.line(MARGIN, y, PAGE_W - MARGIN, y);
y += lineHeight;  // NOT y += 4
```

### Web CSS alignment

When using `borderBottom` as a section divider:

- Put the border directly on the element (e.g., `h2`) rather than a separate `<div>`
- Use `paddingBottom` to separate text from the line
- Use `marginBottom` with at least `lineHeight` to separate the line from content below

## One-Page Auto-Fit Algorithm

The generation script measures content height, then adjusts spacing to fill the target:

```text
1. Render with BASE_SPACING → measure finalY
2. If finalY > TARGET_Y: shorten bullets until it fits
3. If finalY < TARGET_Y: distribute slack across sectionGap, roleGap, bulletGap, lineHeight
4. Re-render with adjusted spacing → write final files
```

Slack distribution weights: `sectionGap: 3, roleGap: 2, bulletGap: 1, lineHeight: 0.5`

## Skeleton: Generation Script

```typescript
import { jsPDF } from "jspdf";
import {
  Document, Packer, Paragraph, TextRun, BorderStyle,
  TabStopPosition, TabStopType, AlignmentType,
} from "docx";
import fs from "fs";
import path from "path";

// --- Interfaces ---
interface ResumeRole {
  title: string;
  company: string;
  location: string;
  startDate: string;
  endDate: string;
  bullets: string[];
}

interface Spacing {
  sectionGap: number;
  roleGap: number;
  bulletGap: number;
  lineHeight: number;
  bodyFontSize: number;
  headlineFontSize: number;
}

interface ResumeData {
  name: string;
  headline: string;
  contact: { email: string; phone: string; location: string; linkedin: string; website: string };
  summary: string;
  roles: ResumeRole[];
  skills: { category: string; items: string }[];
  education: { degree: string; school: string; location: string; dates: string }[];
  spacing: Spacing;
}

// --- Constants ---
const PAGE_W = 612;   // US Letter width in points
const PAGE_H = 792;   // US Letter height in points
const MARGIN = 36;     // 0.5 inch margins
const CONTENT_W = PAGE_W - 2 * MARGIN;
const TARGET_Y = PAGE_H - MARGIN;

const BASE_SPACING: Spacing = {
  sectionGap: 8,
  roleGap: 4,
  bulletGap: 1,
  lineHeight: 14,
  bodyFontSize: 11,
  headlineFontSize: 11,
};

// --- Unit converters (DOCX) ---
const ptToHalfPt = (pt: number) => Math.round(pt * 2);   // TextRun.size
const ptToTwip = (pt: number) => Math.round(pt * 20);     // spacing/margins

// --- Resume data ---
function getResumeData(): Omit<ResumeData, "spacing"> {
  return {
    name: "FULL NAME",
    headline: "Title | Specialty",
    contact: {
      email: "email@example.com",
      phone: "",
      location: "City, State",
      linkedin: "linkedin.com/in/handle",
      website: "example.com",
    },
    summary: "Professional summary paragraph.",
    roles: [
      {
        title: "Job Title",
        company: "Company",
        location: "City, State",
        startDate: "MM/YYYY",
        endDate: "Present",
        bullets: ["Achievement or responsibility"],
      },
    ],
    skills: [
      { category: "Category", items: "Skill1, Skill2, Skill3" },
    ],
    education: [
      {
        degree: "Degree",
        school: "University",
        location: "City, Country",
        dates: "YYYY - YYYY",
      },
    ],
  };
}

// --- PDF rendering ---
function renderPDF(doc: jsPDF, data: Omit<ResumeData, "spacing">, spacing: Spacing): number {
  let y = MARGIN;
  const { bodyFontSize, headlineFontSize, lineHeight, sectionGap, roleGap, bulletGap } = spacing;

  // Header
  doc.setFont("helvetica", "bold");
  doc.setFontSize(20);
  doc.text(data.name, PAGE_W / 2, y, { align: "center" });
  y += 16;

  doc.setFont("helvetica", "normal");
  doc.setFontSize(headlineFontSize);
  doc.text(data.headline, PAGE_W / 2, y, { align: "center" });
  y += lineHeight;

  // Contact line
  const contactParts = [data.contact.location, data.contact.email, data.contact.linkedin, data.contact.website].filter(Boolean);
  doc.setFontSize(9);
  doc.text(contactParts.join("  |  "), PAGE_W / 2, y, { align: "center" });
  y += lineHeight + 2;

  // Divider — use lineHeight gap after rule, NOT a small constant
  doc.setDrawColor(0);
  doc.setLineWidth(0.5);
  doc.line(MARGIN, y, PAGE_W - MARGIN, y);
  y += lineHeight;

  // Summary
  doc.setFont("helvetica", "normal");
  doc.setFontSize(bodyFontSize);
  const summaryLines = doc.splitTextToSize(data.summary, CONTENT_W) as string[];
  for (const line of summaryLines) {
    doc.text(line, MARGIN, y);
    y += lineHeight;
  }

  // Section header helper
  function renderSectionHeader(title: string) {
    y += sectionGap;
    doc.setFont("helvetica", "bold");
    doc.setFontSize(11);
    doc.text(title.toUpperCase(), MARGIN, y);
    y += 3;
    doc.setLineWidth(0.3);
    doc.line(MARGIN, y, PAGE_W - MARGIN, y);
    y += lineHeight;  // full lineHeight after rule
  }

  // Experience, Skills, Education sections...
  // (render each section using the spacing values)

  return y;
}

// --- DOCX rendering ---
function buildDocx(data: Omit<ResumeData, "spacing">, spacing: Spacing): Document {
  const { bodyFontSize, headlineFontSize, lineHeight, sectionGap, roleGap, bulletGap } = spacing;

  // Use ptToHalfPt() for ALL TextRun.size values
  // Use ptToTwip() for ALL spacing.before, spacing.after, margins, page dimensions

  const doc = new Document({
    sections: [{
      properties: {
        page: {
          size: { width: ptToTwip(PAGE_W), height: ptToTwip(PAGE_H) },
          margin: {
            top: ptToTwip(MARGIN),
            bottom: ptToTwip(MARGIN),
            left: ptToTwip(MARGIN),
            right: ptToTwip(MARGIN),
          },
        },
      },
      children: [
        // Build paragraphs here using the data
      ],
    }],
  });

  return doc;
}

// --- Auto-fit and generate ---
async function main() {
  const data = getResumeData();
  const outputDir = path.resolve(import.meta.dirname, "..", "output");
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  // Measure with base spacing
  let spacing = { ...BASE_SPACING };
  let doc = new jsPDF({ unit: "pt", format: "letter" });
  let finalY = renderPDF(doc, data, spacing);

  // Auto-fit: distribute slack
  const slack = TARGET_Y - finalY;
  if (slack > 0) {
    const weights = { sectionGap: 3, roleGap: 2, bulletGap: 1, lineHeight: 0.5 };
    const totalWeight = Object.values(weights).reduce((a, b) => a + b, 0);
    // Count occurrences of each spacing type to distribute evenly
    // Adjust spacing values proportionally
  }

  // Final render
  doc = new jsPDF({ unit: "pt", format: "letter" });
  finalY = renderPDF(doc, data, spacing);

  // Write files
  const pdfBuffer = Buffer.from(doc.output("arraybuffer"));
  fs.writeFileSync(path.join(outputDir, "person-name-resume.pdf"), pdfBuffer);

  const docxDoc = buildDocx(data, spacing);
  const docxBuffer = await Packer.toBuffer(docxDoc);
  fs.writeFileSync(path.join(outputDir, "person-name-resume.docx"), docxBuffer);

  const jsonData: ResumeData = { ...data, publications: [], spacing };
  fs.writeFileSync(path.join(outputDir, "resume-data.json"), JSON.stringify(jsonData, null, 2));

  console.log("All files generated successfully!");
}

main().catch(console.error);
```

## Skeleton: React Resume Page

```tsx
import { useState, useEffect } from "react";

const PT_TO_PX = 96 / 72;

interface ResumeData { /* same interfaces as generation script */ }

function SectionHeader({ title, lineHeightPx }: { title: string; lineHeightPx: number }) {
  return (
    <h2 style={{
      fontSize: "11pt",
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: "0.5px",
      margin: 0,
      padding: 0,
      paddingBottom: "4px",
      marginBottom: `${lineHeightPx}px`,
      borderBottom: "1px solid #1a1a2e",
      color: "#1a1a2e",
    }}>
      {title}
    </h2>
  );
}

export default function ResumePage() {
  const [data, setData] = useState<ResumeData | null>(null);

  useEffect(() => {
    const basePath = import.meta.env.BASE_URL;
    fetch(`${basePath}api/resume-data`)
      .then((r) => r.json())
      .then(setData);
  }, []);

  if (!data) return <p>Loading...</p>;

  const sp = data.spacing;
  const sectionGapPx = sp.sectionGap * PT_TO_PX;
  const roleGapPx = sp.roleGap * PT_TO_PX;
  const bulletGapPx = sp.bulletGap * PT_TO_PX;
  const lineHeightPx = sp.lineHeight * PT_TO_PX;
  const bodyFontPx = sp.bodyFontSize * PT_TO_PX;

  return (
    <div style={{ background: "#f0f0f0", minHeight: "100vh" }}>
      <div style={{
        width: "816px",       // 8.5in at 96dpi
        minHeight: "1056px",  // 11in at 96dpi
        margin: "0 auto",
        background: "#fff",
        padding: "48px",      // 0.5in margins at 96dpi
        fontFamily: "'Calibri', 'Arial', sans-serif",
        fontSize: `${bodyFontPx}px`,
        lineHeight: `${lineHeightPx}px`,
      }}>
        {/* Header, summary, experience, skills, education */}
        {/* Use SectionHeader with lineHeightPx for each section */}
        {/* Use spacing values from sp for all gaps */}
      </div>
    </div>
  );
}
```

## Skeleton: API Routes

```typescript
import { Router } from "express";
import path from "path";
import fs from "fs";

const router = Router();
const outputDir = path.resolve(import.meta.dirname, "..", "..", "..", "..", "output");

router.get("/download/pdf", (_req, res) => {
  const filePath = path.join(outputDir, "person-name-resume.pdf");
  if (!fs.existsSync(filePath)) {
    res.status(404).json({ error: "PDF not found. Run the generation script first." });
    return;
  }
  res.setHeader("Content-Disposition", "attachment; filename=person-name-resume.pdf");
  res.setHeader("Content-Type", "application/pdf");
  res.sendFile(filePath);
});

router.get("/download/docx", (_req, res) => {
  const filePath = path.join(outputDir, "person-name-resume.docx");
  if (!fs.existsSync(filePath)) {
    res.status(404).json({ error: "DOCX not found. Run the generation script first." });
    return;
  }
  res.setHeader("Content-Disposition", "attachment; filename=person-name-resume.docx");
  res.setHeader("Content-Type", "application/vnd.openxmlformats-officedocument.wordprocessingml.document");
  res.sendFile(filePath);
});

router.get("/resume-data", (_req, res) => {
  const filePath = path.join(outputDir, "resume-data.json");
  if (!fs.existsSync(filePath)) {
    res.status(404).json({ error: "Resume data not found. Run the generation script first." });
    return;
  }
  res.json(JSON.parse(fs.readFileSync(filePath, "utf-8")));
});

export default router;
```

## Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| DOCX text is 10× too large | Used `ptToTwip` (×20) for `TextRun.size` | Use `ptToHalfPt` (×2) for font sizes |
| PDF text overlaps horizontal rule | Used `y += 4` after `doc.line()` | Use `y += lineHeight` after any rule |
| Web section header line cuts through text | Border on a sibling `<div>` instead of the `<h2>` | Put `borderBottom` on the `<h2>` with `paddingBottom` |
| Downloads fail in Replit preview iframe | Proxy blocks file downloads in iframe | Use `target="_blank"` on download links, or present files directly |
| Web spacing doesn't match PDF | Hardcoded px values in CSS | Convert all pt values via `PT_TO_PX = 96/72` |

## Dependencies

- `jspdf` — PDF generation
- `docx` — DOCX generation
- `tsx` — TypeScript script runner (dev dependency)

```

---

## Secondary Skill: seo-auditor

**Path:** `.local/secondary_skills/seo-auditor/SKILL.md`

```markdown
---
name: seo-auditor
description: Audit websites for SEO issues and optimize content for search engine visibility.
---

# SEO Auditor & Content Optimizer

Audit websites for technical SEO issues, analyze on-page optimization, and provide actionable recommendations to improve search engine visibility and rankings.

## When to Use

- User wants an SEO audit of their website
- User asks how to improve search rankings
- User wants to optimize content for specific keywords
- User needs meta tag, title, or description improvements
- User wants to compare their SEO against competitors

## When NOT to Use

- Paid advertising strategy (use ad-creative skill)
- Social media content creation (use content-machine skill)
- General competitive analysis without SEO focus (use competitive-analysis)
- Building pages at scale for SEO (use programmatic-seo skill)

## Methodology

### Audit Priority Order

1. **Crawlability & Indexation** (can Google find and index it?)
2. **Technical Foundations** (is the site fast and functional?)
3. **On-Page Optimization** (is content optimized?)
4. **Content Quality** (does it deserve to rank?)
5. **Authority & Links** (does it have credibility?)

### Step 1: Crawlability & Indexation

**Robots.txt:**

- Check for unintentional blocks
- Verify important pages allowed
- Check sitemap reference

**XML Sitemap:**

- Exists and accessible
- Contains only canonical, indexable URLs
- Updated regularly

**Site Architecture:**

- Important pages within 3 clicks of homepage
- Logical hierarchy
- No orphan pages (pages with no internal links)

**Index Status:**

- site:domain.com check
- Compare indexed vs. expected page count

**Indexation Issues:**

- Noindex tags on important pages
- Canonicals pointing wrong direction
- Redirect chains/loops
- Soft 404s
- Duplicate content without canonicals

**Canonicalization:**

- All pages have canonical tags
- HTTP → HTTPS canonicals
- www vs. non-www consistency
- Trailing slash consistency

### Step 2: Technical Foundations

**Core Web Vitals (2025-2026):**

- **LCP** (Largest Contentful Paint): < 2.5s
- **INP** (Interaction to Next Paint): < 200ms — replaced FID in 2025 as the responsiveness metric
- **CLS** (Cumulative Layout Shift): < 0.1

**Speed Factors:**

- Server response time (TTFB)
- Image optimization and modern formats (WebP)
- JavaScript execution and bundle size
- CSS delivery
- Caching headers and CDN usage
- Font loading strategy

**Mobile-Friendliness:**

- Responsive design (not separate m. site)
- Tap target sizes
- Viewport configured
- No horizontal scroll
- Mobile-first indexing readiness

**Security:**

- HTTPS across entire site
- Valid SSL certificate
- No mixed content
- HSTS header

**URL Structure:**

- Readable, descriptive URLs
- Keywords where natural
- Consistent structure (lowercase, hyphen-separated)
- No unnecessary parameters

**Note:** Google now excludes pages returning non-200 status codes (4xx, 5xx) from the rendering queue entirely — critical for SPAs.

### Step 3: On-Page SEO

**Title Tags:**

- Unique per page, 50-60 characters
- Primary keyword near beginning
- Compelling and click-worthy
- Brand name at end
- Common issues: duplicates, too long/short, keyword stuffing, missing

**Meta Descriptions:**

- Unique per page, 150-160 characters
- Includes primary keyword
- Clear value proposition with CTA
- Common issues: duplicates, auto-generated, no compelling reason to click

**Heading Structure:**

- One H1 per page containing primary keyword
- Logical hierarchy (H1 → H2 → H3, no skipping)
- Headings describe content, not used just for styling

**Content Optimization:**

- Keyword in first 100 words
- Related keywords naturally used
- Sufficient depth for topic
- Answers search intent
- Better than current top-ranking competitors

**Image Optimization:**

- Descriptive file names and alt text
- Compressed file sizes, modern formats (WebP)
- Lazy loading, responsive images

**Internal Linking:**

- Important pages well-linked with descriptive anchor text
- No broken internal links
- No orphan pages

**Keyword Targeting (per page):**

- Clear primary keyword target
- Title, H1, URL aligned with keyword
- Content satisfies search intent
- Not competing with other pages (cannibalization)

### Step 4: Content Quality — E-E-A-T Signals

**Experience:** First-hand experience demonstrated, original insights/data, real examples
**Expertise:** Author credentials visible, accurate and detailed information, properly sourced claims
**Authoritativeness:** Recognized in the space, cited by others, industry credentials
**Trustworthiness:** Accurate information, transparent about business, contact info available, privacy policy, HTTPS

### Step 5: Bot Governance & AI Readiness

- Review robots.txt to differentiate between beneficial retrieval agents (OAI-SearchBot, Googlebot) and non-beneficial training scrapers
- Use structured data (schema.org) as the language of LLMs
- Use "BLUF" (Bottom Line Up Front) formatting to help content get cited in AI Overviews

**Schema Markup Detection Warning:** `webFetch` and `curl` cannot reliably detect structured data — many CMS plugins inject JSON-LD via client-side JavaScript. Never report "no schema found" based solely on webFetch. Recommend using Google Rich Results Test or browser DevTools for accurate schema verification.

### Step 6: Competitor SEO Comparison

- Search for target keywords and analyze top-ranking pages
- Identify content gaps and opportunities
- Compare meta tags, content depth, structure, and E-E-A-T signals

## Common Issues by Site Type

**SaaS/Product Sites:** Product pages lack content depth, blog not integrated with product pages, missing comparison/alternative pages, thin feature pages
**E-commerce:** Thin category pages, duplicate product descriptions, missing product schema, faceted navigation creating duplicates
**Content/Blog Sites:** Outdated content not refreshed, keyword cannibalization, no topical clustering, poor internal linking
**Local Business:** Inconsistent NAP, missing local schema, no Google Business Profile optimization

## Output Format

### SEO Audit Report Structure

```text

# SEO Audit Report: [Website]

## Executive Summary

- Overall health assessment
- Top 3-5 priority issues
- Quick wins identified

## Critical Issues (Fix Immediately)
| Issue | Page | Impact | Evidence | Fix |
|-------|------|--------|----------|-----|

## High-Impact Improvements
| Issue | Page | Impact | Evidence | Fix |
|-------|------|--------|----------|-----|

## Quick Wins
| Opportunity | Page | Potential Impact |
|------------|------|-----------------|

## Page-by-Page Analysis

### [Page URL]

- **Title**: Current | Recommended
- **Meta Description**: Current | Recommended
- **H1**: Current | Recommended
- **Content Score**: X/10
- **Issues**: [list]

## Prioritized Action Plan

1. Critical fixes (blocking indexation/ranking)
2. High-impact improvements
3. Quick wins (easy, immediate benefit)
4. Long-term recommendations

```

## Tools

**Free:** Google Search Console, Google PageSpeed Insights, Rich Results Test (use for schema validation — it renders JavaScript), Mobile-Friendly Test, Schema Validator
**Paid (if available):** Screaming Frog, Ahrefs / Semrush, Sitebulb

## Best Practices

1. **Prioritize by impact** -- fix critical issues before optimizing nice-to-haves
2. **Write for humans first** -- keyword-stuffed content hurts rankings
3. **Check actual SERPs** -- search for target keywords to understand what Google currently rewards
4. **Focus on search intent** -- match content type to what users actually want
5. **Monitor competitors** -- see what top-ranking pages do well and identify gaps

## Limitations

- Cannot access Google Search Console or Analytics data
- Cannot measure actual page speed (use Google Lighthouse separately)
- Cannot check backlink profiles (recommend Ahrefs, Semrush, or Moz)
- Cannot run full site crawls (recommend Screaming Frog or Sitebulb)
- Cannot guarantee ranking improvements -- SEO involves many factors
- Cannot access pages behind authentication or paywalls

```

---

## Secondary Skill: stock-analyzer

**Path:** `.local/secondary_skills/stock-analyzer/SKILL.md`

```markdown
---
name: stock-analyzer
description: Analyze stocks and companies with fundamental analysis, technical indicators, and risk assessment
---

# Stock & Investment Analyzer

Analyze stocks, companies, and investment opportunities using financial market data. Provide company profiles, technical analysis, fundamental analysis, and portfolio insights.

## When to Use

- User wants to analyze a specific stock or company
- User asks about financial metrics, earnings, or valuations
- User wants to compare investment options
- User needs portfolio analysis or allocation advice
- User asks about market trends or sector performance

## When NOT to Use

- Tax-specific questions (use tax-reviewer skill)
- Personal budgeting (use budget-planner skill)
- Insurance coverage (use insurance-optimizer skill)

## Data Sources (Use These — Don't Guess)

**Python libs (run directly, no API key):**

```python
import yfinance as yf
t = yf.Ticker("AAPL")
t.info              # P/E, market cap, beta, 52w range, margins
t.financials        # income statement (4yr)
t.balance_sheet     # debt, cash, equity
t.cashflow          # FCF, capex
t.history(period="1y")  # OHLCV for technicals
t.institutional_holders # 13F ownership

```

**Screening:** `finvizfinance` lib — filter S&P 500 by sector/valuation/signals. Finviz.com directly for heatmaps and insider tables.

**Primary filings:** Start from the EDGAR filing index: `webFetch("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}&type=10-K")`. This returns a list of filings — find the most recent 10-K and `webFetch` its "Documents" link to reach the actual filing. Read Item 1A (Risk Factors) and Item 7 (MD&A) — this is where management admits problems.

**Insider activity:** `webFetch("http://openinsider.com/screener?s={ticker}")` — look for **cluster buys** (multiple execs buying same week) and **P-code** open-market purchases (insider paid cash at market price — strongest signal). Ignore option exercises (M-code) and 10b5-1 scheduled sales.

**Short interest:** webSearch `"{ticker} short interest fintel"` — >20% of float = crowded short, squeeze risk either direction.

## Research First — Mandatory Before Any Output

**Never show financials, tables, or a report to the user without thoroughly researching first.** Before generating any Excel model, PDF, or web preview, you must:

1. **Load the `deep-research` skill** for comprehensive web research. This is not optional — every stock analysis must use deep research to gather real data before producing any deliverable.
2. **Pull actual financials** from yfinance AND cross-reference with SEC EDGAR filings (10-K, 10-Q). Do not rely on a single source.
3. **Search for every company mentioned** — if the user's request involves multiple companies or peers, pull financials on ALL of them, not just the primary ticker.
4. **Bias towards tables and numbers from actual public filings.** Every financial figure in the report must be traceable to a real source (SEC filing, earnings release, or yfinance data pull). Do not estimate or round when real numbers are available.

If you cannot verify a financial figure from at least one real source, flag it explicitly as unverified. Never present guessed or hallucinated numbers as fact.

## Methodology

### Step 1: Pull the Data (Python)

Run `yfinance` to get fundamentals + 1yr price history. Compute 50/200 SMA, RSI(14), and current price vs 52w high. Takes 10 lines of pandas.

### Step 2: Fundamental Analysis

**Valuation (compare to sector median, not S&P):**

- P/E — meaningless alone; flag if >2× sector median
- PEG — <1.0 = growth at reasonable price; >2.0 = priced for perfection
- EV/EBITDA — better than P/E for capital-intensive or leveraged cos
- P/S — only metric for unprofitable growth; >20× = needs hypergrowth to justify
- FCF yield (FCF/market cap) — >5% = genuinely cheap; negative = burning cash

**Quality red lines (practitioner heuristics):**

- Revenue growing but FCF shrinking → earnings quality problem, dig into receivables
- Debt/EBITDA >4× → one bad year from covenant breach
- Gross margin compressing 3+ quarters → losing pricing power
- Stock-based comp >15% of revenue → dilution machine (common in SaaS)
- Goodwill >50% of assets → acquisition-heavy, writedown risk

### Step 3: Technical Context (Not Prediction)

Compute in pandas — don't just describe:

- Price vs 50/200 SMA: below both = downtrend, don't catch knives
- Golden cross (50 crosses above 200) = trend confirmation, not entry signal
- RSI(14): >70 overbought / <30 oversold — only useful at extremes + divergence
- Volume: moves on 2×+ avg volume are real; low-volume moves fade
- % off 52w high: >30% drawdown in an uptrending market = something broke

### Step 4: The Retail Edge — Signals Institutions Ignore

- **Insider cluster buys** (OpenInsider): 3+ insiders open-market buying within 2 weeks is the single highest-conviction public signal. Research shows insider buys outperform; sells mean nothing (taxes/divorces/yachts).
- **Buying the dip**: insider P-code purchase after >10% drop = management disagrees with the market
- **Short squeeze setup**: short interest >20% + days-to-cover >5 + any positive catalyst
- **Unusual options**: webSearch `"{ticker} unusual options activity"` — large OTM call sweeps before earnings sometimes leak info

### Step 5: Comparative Table

Build a pandas DataFrame with peers side-by-side: P/E, PEG, rev growth, gross margin, FCF yield, debt/EBITDA. The outlier in either direction is your thesis. **Pull yfinance data for every peer company** — do not leave cells blank or use estimates when real data is available. Every company in the comparison must have actual financials pulled and verified.

## Step 6: Web Research — Find Existing Analyst Reports and News

**Use web search aggressively via the `deep-research` skill.** Before writing the report, gather real external research to cite:

```text
webSearch("[ticker] analyst report 2026")
webSearch("[ticker] earnings analysis site:seekingalpha.com")
webSearch("[ticker] bull case bear case site:seekingalpha.com OR site:fool.com")
webSearch("[company] investor presentation 2026 filetype:pdf")
webSearch("[ticker] price target consensus")
webSearch("[ticker] industry outlook [sector]")
webSearch("[company] competitive landscape")
webSearch("[ticker] short interest thesis")
```

**Source hierarchy (cite all of these in the report):**

| Source | What you get | How to cite |
|--------|-------------|-------------|
| **SEC EDGAR** (10-K, 10-Q, 8-K) | Primary financials, risk factors, MD&A | "Source: [Company] 10-K FY2025, Item 7" |
| **Earnings call transcripts** | Management commentary, guidance | "Source: Q4 2025 Earnings Call, CEO remarks" |
| **Sell-side research** (via SeekingAlpha, TipRanks) | Price targets, consensus estimates | "Source: TipRanks consensus, 12 analysts" |
| **Industry reports** | TAM, growth rates, competitive dynamics | "Source: [Firm] [Industry] Report, [Date]" |
| **Company investor presentations** | Management's own bull case, KPIs | "Source: [Company] Investor Day 2025" |
| **News** (Reuters, Bloomberg, CNBC) | Catalysts, M&A, regulatory | "Source: Reuters, [Date]" |

Use `webFetch` to pull actual content from SeekingAlpha articles, earnings transcripts, and investor presentations. Extract specific data points, quotes, and estimates to cite in the report.

## Build Order — Excel First, Then PDF Report, Website Last

Follow this exact order so the user gets fast, tangible results. You MUST produce **both** the Excel model AND the PDF report — they are not optional or interchangeable.

### Step 1: Build the Excel financial model

**Load the `excel-generator` skill** and generate a professional `.xlsx` file containing all financial models, comp tables, DCF spreadsheets, and data-heavy outputs. The Excel file is the working analytical model — it should have real formulas, charts, conditional formatting, and data validation. Present the Excel file to the user in chat immediately after generating it.

### Step 2: Generate the PDF research report

Write a generation script (`generate-report.ts`) that produces a polished, multi-page equity research PDF using **jsPDF**. This is the primary deliverable — the report the user would hand to someone. **Do not output a markdown summary as a substitute. Do not skip the PDF.** The PDF must be generated and presented to the user in chat before building any web app.

### Step 3: Build the web app last

Build a React web artifact that renders the same report data as an HTML preview — a page-by-page view that visually matches the PDF. The web app is a nice-to-have preview that comes after the PDF and Excel are already in the user's hands. **Do NOT spend time on the web app before the user has seen their PDF and Excel file.**

The user cares most about the Excel model and PDF report. Get those into the user's hands first. The web app is a visual complement, not a replacement.

## Excel Output — Financial Models & Data Tables

The `.xlsx` file should include:

- DCF model with editable assumptions (WACC, terminal growth, revenue CAGR)
- Comparable company analysis table with live formulas
- Historical financials (income statement, balance sheet, cash flow) — 4+ years
- Peer comparison metrics (P/E, EV/EBITDA, revenue growth, margins)
- Charts: revenue trend, margin trends, valuation multiples
- Conditional formatting on key metrics (green/red for above/below thresholds)

## PDF Report — Professional Research Report (Sell-Side Format)

The PDF should look like a sell-side initiation note from Goldman, Morgan Stanley, or JP Morgan. **This is mandatory — every stock analysis must produce this PDF.**

### Report Structure

**Page 1 — Cover / Executive Summary:**

- Company name, ticker, exchange, current price, market cap
- **Rating**: Buy / Hold / Sell with price target and upside/downside %
- **Investment thesis** in 3-4 bullet points (the "elevator pitch")
- Key metrics snapshot: P/E, EV/EBITDA, revenue growth, FCF yield
- A **1-year price chart** (generated via matplotlib/plotly, embedded as image)

**Pages 2-3 — Investment Thesis:**

- Bull case (with probability weighting if possible)
- Bear case (required — what kills this trade?)
- Key catalysts with expected timeline
- Competitive positioning / moat analysis

**Pages 3-4 — Financial Analysis:**

- Revenue breakdown by segment (with a **stacked bar chart**)
- Margin trends over 4+ quarters (with a **line chart**)
- FCF bridge / waterfall
- Balance sheet health (debt maturity, liquidity)
- Peer comparison table (pulled from yfinance for 3-5 peers)

**Page 5 — Valuation:**

- DCF model summary (show assumptions: WACC, terminal growth, revenue CAGR)
- Comparable company analysis table
- Historical valuation range (P/E or EV/EBITDA band chart)
- Price target derivation

**Page 6 — Technical Analysis:**

- Price chart with 50/200 SMA overlay (generated via matplotlib)
- Volume analysis
- Key support/resistance levels
- RSI chart

**Page 7 — Risks:**

- Ranked by probability × impact
- Regulatory, competitive, execution, macro risks
- Specific to this company, not generic boilerplate

**Final Page — Sources:**

- Full citation list with dates for every external source referenced
- Disclaimer / not financial advice

### Charts and Visualizations

Generate charts using **matplotlib** or **plotly** in Python, save as PNG, and embed in both the PDF and the web preview:

```python
import matplotlib.pyplot as plt
import yfinance as yf

# Price chart with SMAs
df = yf.Ticker("AAPL").history(period="1y")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df.index, df['Close'], label='Price', color='#1a1a2e')
ax.plot(df.index, df['Close'].rolling(50).mean(), label='50 SMA', color='#e94560', linestyle='--')
ax.plot(df.index, df['Close'].rolling(200).mean(), label='200 SMA', color='#0f3460', linestyle='--')
ax.set_title("AAPL — 1 Year Price History")
ax.legend()
ax.grid(alpha=0.3)
fig.savefig("price_chart.png", dpi=150, bbox_inches='tight')

# Revenue by segment bar chart
# Margin trend line chart
# Valuation band chart
# RSI chart
```

Generate **at least 4 charts** for the report: price history with SMAs, revenue/margin trends, peer valuation comparison, and one more relevant to the thesis.

### PDF Generation (jsPDF)

Use **jsPDF** (same approach as the resume skill) to generate the PDF with explicit point-based layout:

- `new jsPDF({ unit: "pt", format: "letter" })` — US Letter: 612×792pt
- Use 36pt margins (0.5in). Content area: 540w × 720h points.
- **Track Y position** as you render each element. When the next element would exceed `PAGE_H - MARGIN`, call `doc.addPage()` and reset Y to the top margin. Never let content silently overflow — always check before rendering.
- Embed chart PNGs via `doc.addImage()` — scale each chart to fit the content width while respecting remaining page height. If a chart won't fit on the current page, start a new page.
- Add a **header** (company name, ticker, page number) and **footer** on each page by hooking into page creation.
- Use a clean sans-serif font, navy/dark blue headers, and consistent spacing.

### Avoiding Blank Pages — Two Common Causes

Blank pages in multi-page jsPDF reports almost always come from one of two bugs:

1. **Footer hijacking the cursor.** If you draw a footer at the bottom of the page (e.g., y=720) and leave the cursor there, the next section thinks it's already at the bottom and forces a new page — leaving the previous page blank except for the footer. **Fix:** save the Y position before drawing the footer, then restore it afterward so content flow isn't disrupted.

2. **Double page breaks.** If you have both automatic page breaks (when content nears the bottom) and manual `doc.addPage()` calls at section transitions, both can fire in sequence — producing a blank page between them. **Fix:** before any manual page break, check whether a fresh page was already added (e.g., track an `isNewPage` flag). Only add a page if you're not already on a fresh one.

**Required before presenting:** After generating the PDF, verify there are no blank pages before showing it to the user. Open the generated PDF and check every page for content. If any page is blank, fix the page-break logic and regenerate. Do not present a PDF with blank pages.

### Web Preview — Page-by-Page HTML That Matches the PDF

The React web artifact reads the same report data (via a JSON endpoint, same pattern as the resume skill) and renders an HTML version that **visually mirrors the PDF page-by-page**. Each "page" in the web preview should be a fixed-size container (816×1056px — US Letter at 96dpi) with the same margins, typography, and chart placement as the PDF.

### Styling Guidelines

- **Header bar** on each page with company name, ticker, and page number
- **Data tables** with alternating row shading, right-aligned numbers
- **Charts** at full column width with clear titles and axis labels
- **Callout boxes** for key insights ("Management guided 15% revenue growth in Q4 call")
- **Source citations** as footnotes or inline parenthetical references
- **Professional typography**: 11pt body, 14pt section headers, consistent spacing

## Best Practices

1. **Timestamp everything** — state data pull date; yfinance prices are ~15min delayed
2. **Sector-relative only** — a 30 P/E is cheap in software, expensive in utilities
3. **Label facts vs thesis** — "FCF yield is 6%" (fact) vs "undervalued" (opinion)
4. **Bear case required** — every analysis must include: what kills this trade?
5. **Position sizing reality** — no single stock >5% for most retail portfolios; if conviction demands 20%, the conviction is the problem

## Limitations & Disclaimer

- **This is NOT financial advice.** Informational analysis only. User is responsible for all investment decisions. Recommend consulting a licensed financial advisor before acting.
- yfinance scrapes Yahoo — occasionally breaks, data may lag filings
- Cannot access Bloomberg/FactSet/real-time Level 2
- Cannot execute trades or provide personalized portfolio allocation
- Past performance does not indicate future results; all equities can go to zero

```

---

## Secondary Skill: storyboard

**Path:** `.local/secondary_skills/storyboard/SKILL.md`

```markdown
---
name: storyboard
description: Create storyboards for social media videos, UGC content, and short-form video campaigns.
---

# Storyboarding for Social Content

Shot-by-shot storyboards for TikTok, Reels, YouTube Shorts, and UGC ad scripts. Built around retention physics, not film-school conventions.

## When to Use

- TikTok / Reel / YouTube Short planning
- UGC ad scripts (creator briefs, testimonial mashups)
- Multi-platform video campaigns

## When NOT to Use

- Static ads (ad-creative) · Written posts (content-machine) · Slide decks (use slides skill)

## Platform Specs (2025-2026)

| Platform | Ratio | Resolution | Max duration | Sweet spot | File |
|---|---|---|---|---|---|
| TikTok | 9:16 | 1080×1920 | 10 min in-app / 60 min upload | **21-34 sec** | MP4/MOV, H.264, 287MB mobile / 500MB web |
| Instagram Reels | 9:16 | 1080×1920 | 3 min in-app / 15 min upload | **<90 sec** for Explore boost | MP4/MOV, 4GB |
| YouTube Shorts | 9:16 | 1080×1920 (up to 4K) | **3 min** | 15-60 sec | MP4 |
| YouTube long-form | 16:9 | 1920×1080+ | unlimited | 8-12 min (mid-roll ads) | — |

**Universal safe zone for cross-posting:** Keep all text, faces, logos inside the **center 900×1400** of the 1080×1920 frame. Top 14% + bottom 20-35% are covered by UI on at least one platform.

## The 3-Second Rule (Data-Backed)

TikTok's algorithm scores hook retention **separately** from total watch time. 2025 creator analytics:

| 3-sec retention | View multiplier | Outcome |
|---|---|---|
| **85%+** | 2.8× | Viral tier — FYP push |
| **70-85%** | 2.2× | Optimal reach |
| **60-70%** | 1.6× | Average |
| **<60%** | baseline | Minimal distribution |

**Target: keep ≥65% of viewers past 0:03.** If you're losing >35% in 3 seconds, the hook is broken — rewrite the opening, not the body. 84% of viral TikToks in 2025 used an identifiable psychological trigger in the first 3 seconds.

## Named Hook Formulas

The scroll-stopping element must fire in **0-2 seconds**. Seconds 3-5 expand it. **Never introduce — interrupt.** Banned openers: "Hey guys," "Welcome back," "So today I'm gonna..."

| Hook | Template | Trigger |
|---|---|---|
| **POV** | "POV: you just found out [revelation]" | Puts viewer inside the scenario; personal relevance |
| **Stop-scrolling callout** | "Stop scrolling if you're a [role] who [pain]" | Audience self-selects; filters for high-intent |
| **Contrarian** | "Everyone says X. That's completely wrong." | Cognitive dissonance demands resolution |
| **Unfinished story** | "I almost [drastic action] until I found..." | Open loop — Zeigarnik effect |
| **Negative listicle** | "3 [category] mistakes that are costing you [outcome]" | Loss aversion > gain framing |
| **Number hook** | "$47,000 in 30 days — here's the exact breakdown" | Specificity = credibility |
| **Secret reveal** | "What [authority] doesn't want you to know about X" | Insider info promise |
| **Surprise reaction** | Open on a shocked face, silent beat, then reveal | Viewer's brain asks "what are they reacting to?" |
| **Visual interrupt** | Start mid-action, mid-motion, mid-chaos | Pattern break — no static frame 1 |

**The silent test:** Watch your first 3 seconds on mute. If text overlay + visual alone don't communicate the promise, it fails — ~85% of social video is watched muted.

## Script Structure by Video Type

### Organic short-form (15-60s) — Hook → Value → Loop

```text
0:00-0:02  HOOK         Visual interrupt + text overlay with the promise
0:02-0:05  EXPAND       Why this matters to YOU (the viewer)
0:05-0:XX  DELIVER      The value. Pattern-interrupt every 3-5s: cut, zoom, text pop, angle change
0:XX-end   LOOP/CTA     End mid-sentence OR loop back to frame 1 for rewatch. Soft CTA in caption, not in video.

```

Mid-video retention hooks at ~15s and ~30s ("but here's the part nobody talks about...").

### UGC ad (15-30s) — Direct Response formula

The proven DR structure: **Hook → Problem → Agitate → Solution → Proof → CTA**

```text
0:00-0:02  HOOK      "I was about to [give up on X]..."
0:02-0:05  PROBLEM   Show/say the pain. Be specific.
0:05-0:08  AGITATE   "And it just kept getting worse — [consequence]"
0:08-0:20  SOLUTION  Product in hand. Demo it working. Lo-fi > polished.
0:15-0:22  PROOF     Green-screen reviews behind you, or "my [authority figure] friend told me..."
0:22-0:30  CTA       Verbal + text overlay. "Link in bio" / "Use code X"

```

**UGC ad writing rules:**

- Write like you text a friend — contractions, "literally," "obsessed," imperfect grammar
- One emotion per script (relief / excitement / transformation — pick one)
- Modular shooting: film hook, problem, demo, CTA as separate clips → mix-and-match 3 hooks × 1 body × 2 CTAs = 6 ad variants
- For TikTok Spark Ads, script must feel organic — get creator authorization codes; Spark Ads keep organic engagement metrics
- Research pain points in TikTok comments / Amazon reviews / Reddit before writing — use their exact words

**Vertical-specific angles:** Beauty → before/after transformation. Fitness → "30 days with X" challenge. SaaS → screen recording solving the problem in <10s. Ecom → unboxing + speed-of-delivery.

## Shot-by-Shot Storyboard Format

| # | Time | Shot | Visual | On-screen text | VO / Audio | Retention device |
|---|---|---|---|---|---|---|
| 1 | 0:00-0:02 | CU face | Shocked expression, product out of frame | "I was today years old..." | [silence / gasp] | Surprise reaction hook |
| 2 | 0:02-0:05 | MS | Hold up product | "...when I learned THIS" | "So I've been doing X wrong for 3 years" | Text reveal |
| 3 | 0:05-0:08 | POV | Hands demo the product | — | VO continues | Angle change = pattern interrupt |
| 4 | 0:08-0:12 | Split screen | Before / After | "BEFORE → AFTER" | — | Visual proof |
| 5 | 0:12-0:15 | CU face | Direct to camera | "Link in my bio" | "Code SAVE20 — thank me later" | CTA |

**Shot types:** CU (close-up), MS (medium), WS (wide), POV, OTS (over-the-shoulder), Screen recording, Green-screen, B-roll.

## Visual Output — Always Use the Design Canvas

**Always render the storyboard visually on the design canvas** using the `canvas` skill. Do not just output a text table — build a real, visual storyboard with a generated image for every shot.

### Generated Shot Images

Use the `media-generation` skill to **generate an image for every shot** in the storyboard. Each image should visualize exactly what the camera sees for that shot — match the shot type (CU, MS, WS, POV, etc.), framing, subject, and mood described in the storyboard. These are the storyboard frames, not placeholders.

### Canvas Layout

Each shot is a vertical stack on the canvas, arranged left-to-right as a horizontal timeline:

1. **Shot image** (`image` shape, 400w × 300h) — the generated frame for this shot
2. **Metadata bar** (`geo` shape, 400w × 60h) — shot number, timestamp, and shot type. Color-coded by purpose: red/orange for hook shots, blue for value delivery, green for CTA.
3. **Script/VO bar** (`geo` shape, 400w × 80h) — the voiceover line, on-screen text, or audio direction for this shot

Use 440px horizontal spacing between shot columns. Add a **title shape** across the top with the video concept, platform, and target duration.

For long storyboards (>8 shots), wrap to a second row.

## Production Notes

- **Cuts:** Every 1.5-3 sec on TikTok, every 3-5 sec on YouTube. Static shots >5s bleed viewers.
- **Captions:** Always burned-in. Platform auto-captions are unreliable and can't be styled.
- **Audio:** Trending sound at low volume under VO > original audio only. Use `webSearch` for "[platform] trending sounds this week" — shelf life is ~7-14 days.
- **UGC aesthetic:** Phone camera, natural light, slightly messy background. Ring lights and DSLRs read as "ad" and tank trust. Authenticity converts 3-4× polished.
- **Research:** `webSearch` for current top-performing ad hooks — e.g. `webSearch("[industry] TikTok ad hooks 2026")` or `webSearch("[industry] viral ad examples")`. The TikTok Creative Center (ads.tiktok.com/business/creativecenter) is a useful reference but requires direct browser interaction to filter; search for articles and breakdowns that cite its data.

## A/B Testing Plan

Always deliver 3 hook variants for the same body. Variables to test (change one at a time): Hook type (problem vs. outcome), Proof timing (early vs. late), CTA hardness (soft "check it out" vs. hard "buy now"). Run 7-14 days before picking a winner.

## Limitations

- Produces scripts/storyboards only — no video rendering
- Cannot access live trending sounds (suggest mood + search query)
- Cannot measure retention curves

```

---

## Secondary Skill: supplier-research

**Path:** `.local/secondary_skills/supplier-research/SKILL.md`

```markdown
---
name: supplier-research
description: Research, evaluate, and compare suppliers and vendors for B2B procurement
---

# Supplier & Vendor Research

Research, evaluate, and compare suppliers and vendors for B2B procurement. Build vendor shortlists, evaluation matrices, and RFP frameworks.

## When to Use

- User needs to find suppliers for a product, service, or component
- User wants to evaluate and compare vendors
- User needs an RFP or vendor evaluation framework
- User asks about procurement best practices
- User wants to assess supplier risk or negotiate better terms

## When NOT to Use

- Personal product shopping (use personal-shopper skill)
- Competitive market analysis (use competitive-analysis skill)
- Software/SaaS evaluation only (use deep-research skill)

## Methodology

### Step 1: Requirements Definition

Before researching suppliers, clarify:

**What you need:**

- Product/service specification (be specific)
- Volume/quantity requirements
- Quality standards and certifications needed
- Timeline and delivery requirements

**Constraints:**

- Budget range
- Geographic preferences (domestic, nearshore, offshore)
- Compliance requirements (ISO, SOC2, GDPR, industry-specific)
- Minimum order quantities
- Payment terms preferences

### Step 2: Supplier Discovery

Match the directory to the sourcing geography. Use `webSearch` + `webFetch` against these:

| Platform | Coverage | Best for | Caveat |
|----------|----------|----------|--------|
| **Thomasnet** | 500k+ North American suppliers | US/Canada industrial — machinery, plastics, metals, custom components. Free for buyers. Filter by ISO certs + CAD availability. | US-only; no pricing shown |
| **Alibaba** | 200k+ suppliers, 200M+ SKUs | China/Asia, prototype sampling, MOQ benchmarking across 5,900 categories | Many "manufacturers" are trading companies — verify with customs data |
| **Global Sources** | Asia, audited | Electronics, consumer goods. Stronger supplier audits than Alibaba. | Smaller catalog |
| **IndiaMART** | India | Textiles, chemicals, pharma intermediates, generics | Data quality varies widely |
| **Kompass / Europages** | EU | EU-based sourcing when GDPR/CE compliance matters | Limited free tier |
| **ImportYeti** (free) | US ocean freight records | **Verification, not discovery.** Look up a supplier to see real US customs shipment history — who they actually ship to, how often, what volume. Exposes trading companies posing as factories. | Sea freight only, US imports only |
| **Panjiva / ImportGenius** | Global trade data | Competitor supply chain mapping — find out who your competitors buy from | Paid, learning curve |

**Agent search patterns:**

- `site:thomasnet.com "[product] manufacturer" [state]` — direct directory scrape
- `site:alibaba.com "[product]" "verified supplier" "trade assurance"` — pre-filtered for badges
- `webFetch: importyeti.com/company/[supplier-name]` — verify real export activity before engaging
- `"[competitor product name]" "made in" OR "manufactured by"` — reverse-engineer competitor supply chains
- `site:alibaba.com "[product]" MOQ` — quickly benchmark minimum order quantities across suppliers

**2025 geography shift:** Vietnam, India, and Mexico are the primary China+1 alternatives. Mexico benefits from USMCA (no tariffs, 3-5 day freight vs 30+ from Asia). Vietnam is strong in furniture/electronics assembly. India is strong in textiles/pharma/software.

Target: 8-12 candidates for RFI, narrow to 3-5 for RFQ.

### Step 3: Vendor Evaluation Matrix

Score each vendor across weighted criteria:

| Category | Weight | Criteria |
|----------|--------|----------|
| **Quality** | 25% | Certifications, defect rates, QC processes, samples |
| **Cost** | 20% | Unit price, total cost of ownership, volume discounts, hidden fees |
| **Delivery** | 20% | Lead times, on-time delivery rate, shipping methods, inventory |
| **Capability** | 15% | Production capacity, scalability, technology, R&D |
| **Reliability** | 10% | Financial stability, years in business, references, insurance |
| **Compliance** | 10% | Regulatory compliance, certifications, ESG practices, data security |

**Scoring scale:** 1 (poor) to 5 (excellent) per criterion.

**Total Cost of Ownership (TCO):**
Don't just compare unit prices. Include:

- Purchase price
- Shipping and logistics
- Import duties and taxes
- Quality inspection costs
- Inventory carrying costs
- Switching costs
- Risk costs (what if they fail to deliver?)

### Step 4: Verification & Risk Assessment

**Verify the factory is real (the #1 failure mode in overseas sourcing):**

- **Customs data cross-check**: `webFetch` the supplier on ImportYeti — consistent monthly shipments to recognizable brands = real factory. Zero export history or shipments only to shell companies = trading company or fraud.
- **Certificate verification**: Don't trust uploaded PDFs. ISO 9001 certs have a cert number — verify on the issuing body's site (SGS, BV, TÜV, Intertek all have public lookup tools). `webSearch: "[cert body] certificate verification [cert number]"`.
- **Business license**: For China, request the Unified Social Credit Code (18 digits) — verifiable on the National Enterprise Credit system. For US, check state Secretary of State filings.
- **Address verification**: `webSearch` the factory address — Google Maps satellite view should show an industrial facility, not a residential block or office tower.
- **Alibaba badges**: "Verified Supplier" means a third party (SGS/BV) physically visited. "Gold Supplier" just means they paid a fee — it verifies nothing.

**Risk dimensions:**

| Risk type | Check | Red flags |
|-----------|-------|-----------|
| **Financial** | D&B report, years in business, customer concentration | <3 years operating, >40% revenue from one customer, requests 100% upfront payment |
| **Operational** | Factory count, capacity utilization, QC process docs | Single facility, no in-house QC team, won't allow video factory tour |
| **Geopolitical** | Tariff exposure (Section 301 for China), sanctions lists (OFAC SDN list), port stability | Sourcing region on UFLPA entity list, currency controls, single-port dependency |
| **Compliance** | UFLPA (Xinjiang forced labor — US *presumes* guilt for flagged regions), EU CSDDD due-diligence rules (2024+), conflict minerals (3TG) | Can't provide tier-2 supplier list, cotton/polysilicon from Xinjiang, no chain-of-custody docs |
| **Supply chain** | Tier-2 dependencies, raw material source, seasonal capacity (Chinese New Year = 4-6 wk shutdown) | Won't name their material suppliers, capacity claims exceed facility size |

### Step 5: RFP/RFQ Process

If conducting a formal selection:

**RFP structure:**

1. Company overview and project background
2. Scope of work / product specifications
3. Volume and timeline requirements
4. Quality and compliance requirements
5. Pricing format (line item breakdown)
6. References (3+ similar clients)
7. Evaluation criteria and weights
8. Timeline for responses and decision

**Evaluation process:**

1. Distribute RFP to shortlisted vendors (3-5)
2. Allow Q&A period
3. Score responses against evaluation matrix
4. Conduct reference checks for top 2-3
5. Request samples or pilot project
6. Negotiate final terms with preferred vendor
7. Award and onboard

### Step 6: Negotiation Preparation

**Levers ranked by typical yield:**

1. **Volume commitment** — annual forecast (even non-binding) usually unlocks 8-15% off spot pricing
2. **Payment terms** — overseas default is 30% deposit / 70% pre-shipment. Pushing to 30/70 *after* delivery, or Net 30 from shipment, is worth 2-5% of unit cost in cash flow
3. **Incoterms** — know the difference: FOB (you pay freight + insurance from port), CIF (supplier pays to your port, but *you* bear risk in transit — worst of both), DDP (supplier handles everything including customs — most expensive, least risk). FOB is the standard for experienced buyers.
4. **MOQ flexibility** — first-order MOQ is almost always negotiable down 30-50% if you frame it as a paid trial. "We'll pay the higher per-unit price on 500 units to validate, then commit to your 2,000 MOQ."
5. **Tooling/mold ownership** — for custom parts, negotiate that *you* own the mold after paying for it. Otherwise you're locked in forever.

**Contract terms that matter most:**

- **Price escalation clause** — cap annual increases at a named index (e.g., PPI for the material category), not "supplier discretion"
- **Quality SLA with teeth** — define AQL (Acceptable Quality Level — typically 2.5 for general goods, 1.0 for critical components), specify who pays for third-party inspection (QIMA, SGS), and define the remedy (rework at supplier cost, not just credit)
- **Lead time + late penalties** — industry norm: 1-2% of order value per week late, capped at 10%
- **IP protection** — NNN agreement (Non-disclosure, Non-use, Non-circumvention) for China, not a US-style NDA — US NDAs are unenforceable in Chinese courts
- **Exit clause** — right to terminate with 60-90 days notice, obligation to complete in-flight orders, tooling transfer terms

## Output Format

Always present key findings and recommendations as a plaintext summary in chat, even when also generating files. The user should be able to understand the results without opening any files.

```text

# Vendor Evaluation: [Category]

## Requirements Summary
[Key specs, volume, timeline, constraints]

## Shortlisted Vendors

### 1. [Vendor Name]

- Website: [url]
- Location: [city, country]
- Specialization: [what they do]
- Key Strengths: [2-3 points]
- Concerns: [1-2 points]
- Estimated Cost: [range]

### 2. [Vendor Name]
...

## Evaluation Matrix
| Criteria (Weight) | Vendor A | Vendor B | Vendor C |
|-------------------|----------|----------|----------|
| Quality (25%) | 4/5 | 3/5 | 5/5 |
| Cost (20%) | 5/5 | 4/5 | 3/5 |
| ... | | | |
| **Weighted Total** | **X.X** | **X.X** | **X.X** |

## Recommendation
[Top pick with reasoning, runner-up, and suggested next steps]

```

## Best Practices

1. **Never single-source critical components** — maintain a qualified backup at 10-20% of volume even if unit cost is higher
2. **Sample → pilot → scale** — paid samples first, then a pilot run of 5-10% of target volume, then commit. Never skip to full MOQ.
3. **Third-party inspection before final payment** — QIMA, SGS, or Bureau Veritas run pre-shipment inspections for ~$300. Cheaper than one bad container.
4. **Back-channel references** — find their customers via ImportYeti shipment records and cold-email them. Supplier-provided references are curated.
5. **Plan around Chinese New Year** — factories shut 4-6 weeks (late Jan/Feb). Orders placed in December ship in March. Build buffer inventory by November.
6. **Landed cost, not unit cost** — a $2.00 unit from China can land at $3.50 after freight, 25% Section 301 tariff, duty, and inspection. A $2.80 unit from Mexico under USMCA might land at $3.10.

## Limitations

- Cannot access paid databases (Panjiva, D&B, ImportGenius full data) — ImportYeti free tier is the workaround for US import verification
- Cannot physically inspect facilities or samples — always recommend third-party audit for orders >$10k
- Cannot verify certificate authenticity directly — provides the lookup URLs for the user to check
- Tariff rates and trade rules change frequently (Section 301, UFLPA scope) — verify current rates at time of order
- Pricing from directory listings is indicative only — real quotes require RFQ with full specs

```

---

## Secondary Skill: tax-reviewer

**Path:** `.local/secondary_skills/tax-reviewer/SKILL.md`

```markdown
---
name: tax-reviewer
description: Review tax returns, identify missed deductions, and suggest strategies to reduce tax liability.
---

# Tax Reviewer

Review tax returns and identify potential savings. Flag commonly missed deductions, suggest tax-advantaged strategies, and help with year-round planning.

**IMPORTANT DISCLAIMER: This provides general tax information only, NOT professional tax advice. Always consult a qualified CPA or tax professional before making tax decisions.**

## When to Use

- User wants a review of their tax return
- User asks about commonly missed deductions
- User wants tax planning strategies
- User is self-employed and needs deduction guidance

## When NOT to Use

- Filing taxes (use actual tax software)
- State-specific tax law questions (recommend a local CPA)
- International tax situations
- Business entity tax structuring

## 2026 Key Numbers (verify with webSearch — these change annually)

| Item | 2026 Limit | Notes |
|---|---|---|
| Standard deduction | $16,100 single / $32,200 MFJ / $24,150 HoH | Most filers don't itemize |
| 401(k)/403(b)/TSP employee | $24,500 | +$8,000 catch-up (50+); +$11,250 (age 60-63) |
| IRA (Trad + Roth combined) | $7,500 | +$1,100 catch-up (50+) |
| Roth IRA phase-out | $153k-168k single / $242k-252k MFJ | Above → backdoor Roth |
| HSA | $4,400 single / $8,750 family | +$1,000 (55+). Requires HDHP. |
| SIMPLE IRA | $17,000 | +$4,000 (50+) |
| Section 179 | $2,500,000 | Immediate expensing |
| Standard mileage | $0.70/mi (2025) — webSearch 2026 rate | Must keep contemporaneous log |
| QBI threshold (Form 8995) | $197,300 single / $394,600 MFJ | Above → Form 8995-A with wage/capital limits |

**Always verify:** `webSearch("IRS {year} contribution limits")` — numbers above are Tax Year 2026.

## Commonly Missed Deductions by Filer Type

**W-2 Employees** (limited since TCJA):

- Student loan interest — up to $2,500, above-the-line (no itemizing needed), phases out ~$80-95k single
- Educator expenses — $300 above-the-line for K-12 teachers
- HSA contributions made outside payroll — deductible on Schedule 1
- Traditional IRA — deductible if no workplace plan, or under phase-out ($81-91k single with plan)
- Saver's Credit — up to $1,000 credit (not deduction) for retirement contributions if AGI <~$39k single
- NEW 2025+: qualified overtime deduction (up to $12,500) and personal-use car loan interest — Schedule 1-A

**Self-Employed / Schedule C** (every missed $1 costs ~30-40¢ in income+SE tax):

- **QBI (Form 8995) — #1 most missed.** 20% of qualified business income, off the top. Check the return: if there's Schedule C/E/K-1 income and NO Form 8995, thousands were left on the table. Amendable 3 years back.
- **Half of SE tax** — Schedule 1 line 15. Auto-computed by software but verify it's there.
- **Self-employed health insurance** — 100% of premiums (self + spouse + dependents), Schedule 1 line 17. Above-the-line.
- **Solo 401(k) / SEP-IRA** — Solo 401(k) allows employee ($24,500) + employer (25% of net SE income) contributions. SEP is simpler, 25% of net up to ~$70k.
- **Home office** — simplified: $5/sqft × up to 300 sqft = $1,500 max. Regular method (Form 8829): actual % of rent/mortgage/utilities/insurance. Regular method also reduces SE tax — shifts expense from Schedule A to Schedule C.
- **100% bonus depreciation** — restored for assets placed in service after Jan 19, 2025. Full first-year write-off for equipment.
- **Business % of phone/internet, software subs, business meals (50%), professional development**
- **Tax prep fees** — the portion for business forms (Schedule C, SE) is deductible on Schedule C itself

**Investors:**

- Tax-loss harvesting — realize up to $3,000/yr net capital loss against ordinary income; carry forward indefinitely. Mind 30-day wash-sale rule.
- Qualified dividends + LTCG — 0% rate up to ~$48k single / ~$96k MFJ taxable income. Tax-gain harvesting in low-income years.
- Foreign tax credit (Form 1116) — commonly missed on international ETF dividends
- Rental real estate: depreciation (27.5-yr straight line on building basis), and QBI may apply under the 199A safe harbor

**Homeowners (only if itemizing > standard deduction — most don't):**

- Mortgage interest (first $750k of acquisition debt), points in purchase year
- SALT up to $10k (property + state income/sales)
- Residential clean energy credit — 30% of solar/battery/geothermal cost, no cap (Form 5695)
- Energy efficient home improvement credit — 30% up to $1,200/yr for insulation/windows/doors, $2,000 for heat pumps

## Tax-Advantaged Account Priority

1. **HSA** — triple tax-free (deduct in, grow free, withdraw free for medical). Acts as stealth IRA after 65.
2. **401(k) to match** — 50-100% instant return
3. **Roth IRA** (if in 12-22% bracket) / **Traditional** (if 32%+). Over income limit → backdoor Roth (nondeductible Trad → convert).
4. **Max 401(k)** — mega backdoor Roth if plan allows after-tax contributions + in-service conversions
5. **529** — state deduction varies (some states give nothing); tax-free growth for education

## Output Format

```text
# Tax Review Summary

## Filing Overview
| Item | Current | Notes |

## Potential Savings

### High Confidence
1. **[Deduction]**: Potential savings $X,XXX

### Worth Investigating
1. **[Strategy]**: Potential savings $X,XXX

## Recommended Actions

## Disclaimer
Consult a CPA for personalized advice.
```

## Review Checklist When User Shares a Return

1. **Filing status** — MFJ vs MFS (MFS rarely wins; check if student loans on IBR). HoH if unmarried with dependent.
2. **Standard vs itemized** — if Schedule A total < standard deduction, they itemized wrong (or could bunch charity/medical into alternate years)
3. **Form 8995 present?** — If Schedule C, E (rental), or K-1 income exists and no 8995, QBI was missed. Biggest dollar finding.
4. **Schedule 1 adjustments** — SE tax ÷ 2, SE health insurance, HSA, IRA, student loan interest all present?
5. **Retirement contributions maxed?** — If refund is large and 401(k)/IRA room remains, they're over-withholding instead of investing pre-tax
6. **Credits vs deductions** — Child Tax Credit, Saver's Credit, education credits (AOTC > LLC for undergrads), EV credit
7. **Carryforwards applied?** — prior-year capital losses, NOLs, unused credits

## Best Practices

1. **Lead with the disclaimer** — this is education, not advice
2. **Quantify every finding** — "missed QBI" means nothing; "missed ~$4,200 deduction ≈ $925 refund at 22% bracket" means something
3. **Flag aggressive positions** — home office for W-2, hobby-loss rules, meals >50%: "discuss with a CPA, this gets audited"
4. **Second-order effects** — lowering AGI can unlock Roth eligibility, ACA subsidies, Saver's Credit. Model the cascade.
5. **webSearch current-year limits** — do not trust memorized numbers; the IRS adjusts annually

## Limitations

- **NOT professional tax advice.** General information only. Always consult a CPA or EA before filing or amending — especially for self-employment, rentals, K-1s, or state issues.
- Cannot file or amend returns
- Cannot model all state rules (state conformity to federal law varies wildly)
- Tax law changes yearly — all figures require current-year verification

```

---

## Secondary Skill: translation

**Path:** `.local/secondary_skills/translation/SKILL.md`

```markdown
---
name: translation
description: Translate text and documents between languages with cultural and contextual adaptation
---

# Translation

Translate text, documents, and content between languages with attention to context, tone, and cultural nuance.

## When to Use

- User wants text translated between languages
- User needs a document, email, or webpage localized
- User wants to understand foreign-language content
- User needs culturally adapted content (not just word-for-word translation)
- User wants multilingual versions of their content

## When NOT to Use

- Code localization / i18n implementation (use the `artifacts` skill)
- Writing original content in a specific language (use content-machine skill)

## Methodology

### Step 1: Understand the Context

Before translating, clarify:

- **Source and target language(s)**
- **Content type**: Casual text, business document, marketing copy, technical/legal, creative/literary
- **Audience**: Who will read the translation? (formal vs. informal register)
- **Purpose**: Information transfer, marketing impact, legal accuracy, or cultural adaptation?
- **Tone**: Should the translation match the original tone or adapt for the target culture?

### Step 2: Translation Approach

**Choose the right approach for the content type:**

| Content Type | Approach | Priority |
|-------------|----------|----------|
| **Technical/Legal** | Precise, terminology-consistent | Accuracy over fluency |
| **Business** | Professional, clear | Balance accuracy and fluency |
| **Marketing/Creative** | Transcreation — adapt the message | Impact over literal accuracy |
| **Casual/Chat** | Natural, colloquial | Fluency over formality |
| **UI/UX** | Concise, action-oriented | Brevity and clarity |

### Step 3: Translate

**Translation principles:**

- Translate meaning, not words — convey the intent, not a word-for-word mapping
- Preserve tone and register — formal stays formal, casual stays casual
- Handle idioms properly — find equivalent expressions in the target language, don't translate literally
- Maintain formatting — preserve bullet points, headers, bold/italic, links
- Keep proper nouns as-is unless there's a standard localized form
- Preserve technical terms — use established translations from the field, don't invent new ones

### Formality — The T-V Distinction

Many languages force you to pick a formality register for "you." Get this wrong and the whole translation reads off. **Ask the user or default to formal for business.**

| Language | Informal (T) | Formal (V) | Notes |
|----------|-------------|------------|-------|
| Spanish | tú / vos | usted | LatAm vs. Spain differ; Argentina uses *vos* |
| French | tu | vous | *vous* is also plural — context disambiguates |
| German | du | Sie | *Sie* is capitalized; verbs conjugate differently |
| Portuguese | tu / você | o senhor / a senhora | Brazil: *você* is default-neutral |
| Russian | ты | вы | |
| Japanese | — | — | No T-V; uses **keigo** — three honorific systems (*teineigo* polite, *sonkeigo* respectful, *kenjōgo* humble). In-group vs out-group matters more than hierarchy: you humble *your own boss* when talking to a client. |
| Korean | 반말 | 존댓말 | Six speech levels; verb endings change completely |

### Locale Data — Don't Guess, Use CLDR

Dates, numbers, and currencies follow **Unicode CLDR** (Common Locale Data Repository — what every OS and browser uses). Don't hardcode formats; look them up per locale:

| Locale | Date | Number | Notes |
|--------|------|--------|-------|
| en-US | 3/14/2026 | 1,234.56 | 12-hour clock default |
| en-GB | 14/03/2026 | 1,234.56 | 24-hour clock |
| de-DE | 14.03.2026 | 1.234,56 | Comma is decimal separator |
| fr-FR | 14/03/2026 | 1 234,56 | Thin-space thousands separator |
| ja-JP | 2026年3月14日 | 1,234.56 | Year-month-day, era names possible (令和8年) |
| ar-SA | ١٤/٠٣/٢٠٢٦ | ١٬٢٣٤٫٥٦ | RTL, Arabic-Indic digits, Hijri calendar option |

In Python: `babel.dates.format_date(d, locale='de_DE')` handles this correctly.

### Text Expansion — Plan for It

English → other languages changes length. Critical for UI strings, button labels, and anything with character limits:

| Target | Expansion vs. English | Watch out for |
|--------|----------------------|---------------|
| German | +35% | Compound words don't wrap: `Eingabeverarbeitungsfunktionen` |
| French, Spanish | +20–25% | |
| Russian | +15% | Plus Cyrillic glyphs are often wider |
| Finnish, Dutch | +30% | Agglutinative compounds |
| Chinese, Japanese, Korean | −10% to −30% (shorter) | But need larger font sizes for legibility |

**UI rule of thumb:** design with 35% horizontal slack. Tell the user if their 12-char button label becomes 22 chars in German.

### Tooling — When to Use What

| Tool | Use when | Don't use when |
|------|----------|----------------|
| **LLM (you)** | Context matters, tone adaptation, idioms, marketing copy, anything needing judgment | You need 10,000 strings translated identically |
| **`deep-translator` (Python)** | Bulk throughput, wrapping Google/DeepL/Microsoft APIs, simple string-in-string-out | You need glossary enforcement (it doesn't expose DeepL's glossary API) |
| **`deepl` official SDK** | Need glossary/termbase support — it actually exposes this | |
| **`translate-toolkit`** | Parsing XLIFF/TMX/TBX/PO files — the standard localization formats | |

### QA — Back-Translation

For high-stakes content (legal, medical, safety warnings): translate source→target, then independently translate target→source, then diff semantically against the original. Divergences flag ambiguity or drift. Don't use the same model/prompt for both directions — you'll get confirmation bias. This catches errors but is NOT proof of correctness; it's a smell test.

### Glossary Injection

For multi-document projects, build a termbase (JSON of `{source_term: target_term}`) and inject it into your system prompt. Forces consistency across documents — "dashboard" shouldn't be *tablero* on page 1 and *panel de control* on page 5.

## Best Practices

1. **Specify the locale, not just the language** — `es-MX` ≠ `es-ES` ≠ `es-AR` (vocabulary, formality, *vos* vs *tú*)
2. **Flag transcreation** — when you significantly adapt rather than translate (slogans, jokes), tell the user what you changed and why
3. **Preserve placeholders exactly** — `{name}`, `%s`, `{{count}}` must survive unchanged and in grammatically valid positions
4. **Pluralization is hard** — English has 2 forms (1 item / 2 items); Russian has 3; Arabic has 6. CLDR plural rules define these.
5. **RTL is layout, not translation** — Arabic/Hebrew/Persian text is RTL but numbers and embedded Latin stay LTR. Flag it; don't try to "fix" it in the text.

## Limitations

- AI translation may miss subtle cultural nuances a native speaker would catch
- Legal and medical translations should be reviewed by a certified professional
- Poetry, humor, and wordplay may lose their effect — note this when it happens
- Cannot verify pronunciation for audio/speech contexts
- Some specialized terminology may not have established translations

```

---

## Secondary Skill: travel-assistant

**Path:** `.local/secondary_skills/travel-assistant/SKILL.md`

```markdown
---
name: travel-assistant
description: Plan trips, create itineraries, estimate budgets, and research destinations.
---

# Travel Assistant

Plan trips, build paced itineraries, find flight deals, and catch visa/entry issues before they ruin a trip.

## When to Use

- Itinerary building, flight/accommodation strategy, budget estimation
- "What do I need to enter [country]?" — visa/vaccine/ETIAS checks

## When NOT to Use

- Booking (can't transact); travel insurance (insurance-optimizer)

## Step 0: Ask Before You Plan

Before producing any itinerary or recommendations, ask the user:

- **Where are you traveling from?** (origin city/airport — required for flight search)
- **Destination(s)**
- **Dates** (or flexible?)
- **Number of travelers** (solo, couple, family with kids?)
- **Budget level** (budget, mid-range, luxury?)
- **Trip style** (relaxation, culture, adventure, foodie, nightlife?)
- **Must-dos** (any specific activities, restaurants, or experiences?)

Do NOT search for flights without knowing the origin city — you will get it wrong.

## Output Structure

Organize the trip plan into these sections, in this order:

### 1. Flights

Search for flights using `webSearch` with queries like `"Google Flights [origin] to [destination] [dates]"`, `"Skyscanner [origin] to [destination] [month]"`.

Present options with **direct links** to booking/search pages:

```text
**Option 1: [Airline] — $XXX roundtrip**
- Outbound: [date], [time] [origin] → [time] [dest] (Xh Xm, nonstop/1 stop)
- Return: [date], [time] [dest] → [time] [origin] (Xh Xm, nonstop/1 stop)
- [Google Flights link](URL) | [Book direct with airline](URL)

**Option 2: [Airline] — $XXX roundtrip**
...
```

Include at least 3 options when possible: cheapest, best schedule, best airline. Note open-jaw options if doing a multi-city trip.

**Flight search tools — use multiple, they surface different fares:**

| Tool | What it's best at |
|------|-------------------|
| Google Flights | Speed; calendar price grid; search up to 7 origin + 7 destination airports at once; price-history graph shows if "now" is cheap |
| Skyscanner | "Everywhere" destination (cheapest places from your airport, sorted by price); "Whole month" date view; surfaces budget carriers Google misses |
| Skiplagged | Hidden-city fares — flight A→C with layover at B is cheaper than A→B, so you get off at B. Savings up to 60%. **Constraints:** carry-on only (checked bags go to C), one-way only (skipping a leg cancels the rest), don't do it repeatedly on the same airline (they ban accounts) |
| Going.com / Secret Flying | Error fares, mistake prices — time-sensitive |

**Booking rules:**

- Find the fare on an aggregator → **book direct with the airline.** OTAs (Expedia etc.) are useless when flights get cancelled — airline agents will say "call Expedia"
- Domestic sweet spot: 1-3 months out. International: 2-6 months. Last-minute is almost always worse except on empty routes
- Tuesday/Wednesday/Saturday departures are typically cheapest
- Open-jaw (fly into city A, out of city B) via multi-city search — often cheaper than round-trip + ground transport

### 2. Hotels / Accommodations

Search using `webSearch` for hotels in the destination area with queries like `"best hotels [neighborhood] [city] [budget level]"`, `"[city] hotels [dates] site:booking.com"`, `"[city] airbnb [neighborhood]"`.

Present options with **direct links**:

```text
**[Hotel Name]** — $XXX/night | [neighborhood] | [rating] stars
- [Key feature 1], [key feature 2] (e.g., rooftop pool, walkable to old town, free breakfast)
- [Booking.com link](URL) | [Hotel website](URL)

**[Hotel/Airbnb Name]** — $XXX/night | [neighborhood] | [rating]
...
```

Include 3-5 options spanning the user's budget range. Note the neighborhood and why it's a good base. For multi-city trips, list accommodations per city.

| Platform | Best for |
|----------|----------|
| Booking.com | Widest hotel inventory, free cancellation options, price match |
| Airbnb | Apartments, longer stays, groups, kitchens |
| Hostelworld | Budget/social travelers |
| Hotel direct sites | Loyalty perks, best-rate guarantees |

### 3. Day-by-Day Itinerary

Structure each day with anchor activities and restaurant recommendations with links:

```text
## Day X — [Neighborhood/Theme]

**Anchor (AM):** [Activity] — book ahead? y/n — ~$XX — nearest metro: [station]
**Lunch:** [Restaurant name](URL) — [cuisine, 1-line description] — ~$XX/person
**Anchor (PM):** [Activity]
**Dinner:** [Restaurant name](URL) — [cuisine, 1-line description] — ~$XX/person
**Alt dinner:** [Restaurant name](URL) — [backup option]
**Transit:** [A→B method, ~time, ~cost]
**If it rains / you're tired:** [one swap]
**Day est:** $XX
```

For restaurant links, search with `webSearch` for `"best [cuisine] restaurant [neighborhood] [city]"` or `"[city] [neighborhood] restaurants site:google.com/maps"`. Link to Google Maps, Yelp, or the restaurant's website.

### 4. Web App — Map + Itinerary

**Always build a web app** that combines two views the user can switch between:

1. **Map view** — all locations plotted on an interactive map with color-coded markers by type (airports, hotels, activities, restaurants). Each marker has a popup with name, time, and links. Connect same-day stops with route lines so the user can see the flow.

2. **Itinerary view** — a beautiful, card-based day-by-day layout. Each day is a card with the day number, neighborhood/theme, and a timeline of activities, meals, and transit. Include photos or icons for each stop, estimated costs, and direct links to book or learn more.

Use the **Nominatim API** (OpenStreetMap) for geocoding addresses to lat/lng — no API key required.

The user should be able to toggle between map and itinerary views. Clicking a day in the itinerary should highlight that day's markers on the map.

### 5. Budget Summary

| Category | Est. Total |
|----------|-----------|
| Flights | $XXX |
| Accommodation (X nights) | $XXX |
| Food | $XXX |
| Activities/Entries | $XXX |
| Local Transport | $XXX |
| **Trip Total** | **$X,XXX** |

## Entry Requirements — Check Before Anything Else

Getting this wrong ends the trip at the airport. webSearch every time — rules change.

| Check | Source | Notes |
|-------|--------|-------|
| Visa requirements | `travel.state.gov` (US citizens) or `[passport country] [destination] visa requirements` | |
| Schengen 90/180 (Europe) | `ec.europa.eu` calculator or `schengenvisainfo.com/visa-calculator` | 90 days in any rolling 180-day window. Does NOT reset on exit. Count days not months. Entry + exit days both count as full days. Schengen ≠ EU (UK, Ireland out; Switzerland, Norway in) |
| ETIAS (Europe) | `etias.com` | Pre-authorization now required even for visa-free travelers |
| Passport validity | — | Many countries require 6 months validity beyond your departure date. Check blank pages too (some need 2+) |
| Vaccines | `cdc.gov/travel` | Yellow fever is mandatory (with certificate) for some countries if arriving from an endemic zone |
| Onward ticket proof | — | Some countries (Thailand, Philippines, Indonesia, Costa Rica, Peru) won't let you board without proof you're leaving |
| Safety advisories | `travel.state.gov/content/travel/en/traveladvisories` | |

## Itinerary Pacing — The #1 Mistake Is Overplanning

**Hard limits:**

- **Max 1 anchor activity per half-day.** One museum in the morning, one neighborhood in the afternoon. Hour-by-hour schedules fall apart by day 2.
- **Transit tax:** every change of location costs 30-60 min more than Google Maps says (finding the entrance, ticketing, getting lost once). Budget it.
- **Day 1 after a long-haul flight is dead.** Plan a walk and an early dinner, nothing with a timed entry.
- **3-night minimum per city** for multi-city trips. 2 nights = 1 real day. Fewer cities, done well, beats a checklist.
- **One unplanned afternoon per 3 days.** The best travel moments are unscheduled.
- **Cluster by geography** — plot everything on a map first, then group by neighborhood. Never cross the city twice in a day.

**Known closure patterns:**

- Europe: many museums closed Mondays (Louvre, Prado) or Tuesdays (Italy). Always verify.
- Japan: many restaurants/shops closed one weekday (often Mon or Wed). Golden Week (late Apr-early May) = everything packed.
- Middle East: Friday is the weekend day; expect closures.
- Siesta countries (Spain, Greece, parts of Italy): 2-5pm dead zone outside tourist cores.

## Budget Estimation

| Category | Budget | Mid | High | Notes |
|----------|--------|-----|------|-------|
| Sleep /night | $25-50 | $80-180 | $250+ | Hostels/guesthouses → 3-star → boutique |
| Food /day | $15-30 | $40-80 | $120+ | Street + one sit-down → restaurants → tasting menus |
| Local transit /day | $5-15 | $15-30 | $50+ | Metro pass → occasional taxi → car+driver |
| Activities /day | $0-20 | $30-60 | $100+ | Free walking tours → paid entries → private guides |

Southeast Asia / Central America / Eastern Europe: use the low end. Western Europe / Japan / Australia: mid-to-high. Switzerland / Norway / Iceland: add 30% to whatever you estimated.

**Always add:** intercity transport (trains/flights between cities — often the hidden budget killer), travel insurance (~4-8% of trip cost), SIM/eSIM (~$20-40), visa fees, 10-15% buffer.

## Useful lookups (webSearch)

- `"[city] 3 day itinerary reddit"` — real traveler pacing, not SEO content
- `"rome2rio [city A] to [city B]"` — compares train/bus/flight/ferry with rough prices
- `"numbeo cost of living [city]"` — meal/taxi/beer price baselines
- `"seat61 [country]"` — train travel bible, especially Europe/Asia
- `"[attraction] skip the line"` — whether advance booking is actually necessary

## Limitations

- Can't see live prices/availability — user must verify before booking
- Visa rules change — always confirm on official government sites
- Can't book anything

```

---

## Secondary Skill: used-car-advisor

**Path:** `.local/secondary_skills/used-car-advisor/SKILL.md`

```markdown
---
name: used-car-advisor
description: Evaluate used car listings, estimate fair prices, and guide purchasing decisions.
---

# Used Car Advisor

Evaluate used car listings, estimate fair value, flag known-problem models, and coach negotiation.

## When to Use

- "Find me the best [car] under $X" — search for real listings first, then evaluate
- Evaluating a specific listing or comparing options
- "Is this a fair price?" / "What's wrong with this model year?"
- Negotiation prep before contacting a dealer

## When NOT to Use

- New car purchasing, repair diagnosis, insurance (use insurance-optimizer)

## Listing Search Workflow

When a user asks to find a car, follow these steps in order:

**Step 1: Search for real listings across multiple platforms.** Use specific price, mileage, and location filters. Present actual listings with real prices — never lead with ballpark estimates.

**Step 2: Collect and organize results.** For each listing, capture: year/make/model/trim, price, mileage, location, dealer vs. private, and listing URL.

**Step 3: Evaluate and compare.** Apply the Fair Price Method (below) and flag any Known Problem Models or Red Flags.

**Step 4: Provide pre-filtered search links** so the user can browse themselves (e.g., `cars.com/shopping/ferrari-california/price-under-80000/`). Don't just link site homepages.

## Research Sources (use webSearch/webFetch)

### Inventory / Listing Search

| Source | Best for | Notes |
|--------|----------|-------|
| `cargurus.com` | Deal ratings, days-on-market | Shows "great/good/fair/overpriced" vs. market |
| `cars.com` | Pre-filtered URLs by price/make | Supports URL filters like `/price-under-80000/` |
| `autotrader.com` | Broad dealer inventory | Good trim-level filtering |
| `edmunds.com` | Listings + TMV pricing | Combines inventory with valuation |
| `autolist.com` | Savings vs. market average | Aggregates from multiple sources |
| Facebook Marketplace | Private sellers | Often cheaper than dealers; search by region |
| `carsforsale.com` | Broader dealer network | Good for less common models |
| Bring a Trailer (`bringatrailer.com`) | Specialty/enthusiast/exotic cars | Auction format with sold-price history |
| Hemmings (`hemmings.com`) | Classic and collector cars | Specialty listings |
| DuPont Registry (`dupontregistry.com`) | Luxury and exotic cars | High-end inventory |
| `preowned.ferrari.com` | CPO Ferraris | Factory-certified pre-owned |

### Valuation & Reliability Research

| Need | Source | Query pattern |
|------|--------|---------------|
| Recalls by VIN | `nhtsa.gov/recalls` | Fetch directly with 17-char VIN |
| Complaint clusters | `carcomplaints.com` | `"[year] [model] problems site:carcomplaints.com"` |
| Repair cost estimates | `repairpal.com` | `"[model] [repair] cost repairpal"` |
| Fair market value | KBB, Edmunds, `cargurus.com` (shows days-on-market + deal rating) | |
| TSBs (technical service bulletins) | `nhtsa.gov` or `"[model] TSB [symptom]"` | |
| Long-term reliability | `dashboard-light.com`, Consumer Reports (paywalled — search `"consumer reports [model] reliability reddit"` for summaries) | |

## Known Problem Models — Flag These Immediately

When user mentions any of these, warn before discussing price:

| Avoid | Years | Issue | Failure cost |
|-------|-------|-------|--------------|
| Ford Focus/Fiesta | 2011-2016 | PowerShift DCT — shudder, slip, class-action settled | $3-4k transmission |
| Nissan Altima/Sentra/Rogue/Pathfinder/Versa | 2013-2017 (worst) | Jatco CVT — overheats, limp mode, ~120k mi lifespan | $3.5-5k |
| Subaru (most) | 2012-2017 | CVT (warranty extended); also head gasket <2012 | $2-7k |
| BMW/Audi/Mercedes | Any out of warranty | Normal wear = premium parts/labor; depreciates 50%+ by yr 5 | Budget $2-3k/yr |
| Hyundai/Kia 2.0/2.4L Theta II | 2011-2019 | Rod bearing failure, engine seizure (recall) | Engine replacement |
| Chevy Cruze | 2011-2015 | Coolant leaks, turbo failure | $1-2k recurring |

**CVT buying rule:** Demand transmission fluid service records. No CVT service by 60k mi (4-cyl) or 80k mi (6-cyl) → walk away. Metal belt on metal pulleys — old fluid = cooked transmission.

**Safe defaults:** Toyota Corolla/Camry, Honda Civic/Accord (Honda's CVT is the exception — reliable), Mazda3/6, Lexus anything. Toyota Prius 2009-2020: 5/5 CR reliability every year.

## Exotic & Luxury Cars — Different Rules Apply

Exotic and high-performance cars (Ferrari, Lamborghini, Porsche, McLaren, Aston Martin, Maserati, etc.) operate on completely different cost structures. Flag this immediately when a user asks about these brands.

| Item | Mainstream | Exotic/Luxury |
|------|-----------|---------------|
| Pre-purchase inspection | $100-200 | $300-500+ (specialist required) |
| Annual maintenance budget | $500-1,500 | $5,000-10,000+ |
| Transmission repair | $2-5K | $15-25K+ |
| Engine work | $3-8K | $15-50K+ |
| Brake job (all 4) | $300-800 | $3,000-8,000 (carbon ceramics: $15K+) |
| Tires | $400-800/set | $1,500-4,000/set |

**Exotic car buying rules:**

- Always use a marque specialist for PPI, not a general mechanic
- Search sold listings on Bring a Trailer for real transaction prices — asking prices on exotics are often negotiable by 10-20%
- Check brand-specific CPO programs (Ferrari Approved, Porsche CPO, Lamborghini Selezione) — CPO warranty can save tens of thousands
- Service history is everything. Incomplete records on an exotic = walk away
- Join model-specific forums (FerrariChat, Rennlist, Lamborghini-Talk) for ownership cost reality checks

## Listing Red Flags

| Flag | What it means |
|------|---------------|
| Salvage/rebuilt/"clean rebuilt" title | Totaled once. Insurance may refuse comprehensive. -40% value |
| Price 20%+ below CarGurus "great deal" | Scam or undisclosed damage |
| "Runs great, just needs [X]" | If it were cheap to fix, they'd have fixed it |
| Odometer ends in 000 / round number | Possible rollback; cross-check Carfax mileage entries |
| No cold-start video on request | Hiding startup rattle (timing chain) or blue smoke (rings) |
| Dealer add-ons mandatory (nitrogen tires, VIN etching, "protection package") | Junk fees — refuse or walk |

## Fair Price Method

1. Pull KBB private-party + Edmunds TMV + 3 comparable CarGurus listings (same trim, ±15k miles, ±100 mi radius)
2. Average them, then adjust: below-avg miles +5-10%, accident on Carfax -10-25%, one-owner +$500, new tires +$400-800
3. Check days-on-market (CarGurus shows this). >45 days = dealer is motivated
4. Subtract cost of any needed work (use RepairPal estimates)

## Negotiation Playbook

**Before contact:**

- Get pre-approved financing from a credit union — removes dealer's biggest profit lever
- Find 2-3 competing listings for the same model. Screenshot them.

**The ask:**

- Email/text only until price is locked. Never negotiate on the lot.
- Ask for **out-the-door (OTD) price** — tax, title, doc fee, everything. "What's the OTD on stock #____?" Refuse to discuss monthly payments.
- Open at 10-15% below ask (dealer) or 15-20% (private). Anchor with KBB private-party number even at a dealer.
- After your offer: **stop talking.** First to fill silence loses.

**Timing:** Last 2-3 days of the month, weekday morning. Salespeople under quota will eat margin. (Caveat: if they already hit quota this does nothing.)

**Trade-in:** Get it appraised separately (CarMax/Carvana give free written offers). Never let them bundle trade-in value into the purchase — it obscures both numbers.

**Before signing:** Read every line of the buyer's order. Reject "market adjustment," "dealer prep," mandatory add-ons. Verify VIN on contract = VIN on door jamb.

## Pre-Purchase Inspection — Non-Negotiable

$100-200 at an independent shop ($300-500 for exotics — use a marque specialist). NOT the seller's mechanic. Any seller who refuses → walk. Specifically request:

- Compression test (engine health) — all cylinders within 10% of each other
- Scan for stored/pending OBD codes (some sellers clear codes before showing)
- Lift inspection: frame rust, leaks, CV boot tears, uneven tire wear (alignment/suspension)
- **Cold start** — arrive before the seller warms it up. Listen for rattle (timing chain), watch for blue smoke (oil burning) or white smoke that lingers (head gasket)

## Regional Search Strategy

Regional pricing differences can be significant — always search multiple regions:

| Region | Tends to be cheaper for | Watch out for |
|--------|------------------------|---------------|
| Midwest / South | Luxury & exotic cars (lower demand) | Hail damage (Midwest), flood titles (Gulf states) |
| Southwest (AZ, NV, NM) | Older cars (no rust) | Sun damage to paint/interior |
| Northeast / Rust Belt | Nothing specific | Frame rust, salt corrosion — get underbody inspection |
| Florida | High supply of luxury/exotic | Flood damage, hurricane salvage titles |
| California | High supply overall | Higher prices due to demand; emissions compliance |

**Tip:** Search nationwide first to establish fair market price, then narrow by region. A $5K price difference can justify shipping ($500-1,500 depending on distance).

## Comparison Web App

After finding the best options, **build a web app** that displays a visual comparison page so the user can evaluate listings side-by-side.

### Each listing card should show

- **Car image** — use the actual photo scraped from the listing URL. **Never generate, synthesize, or use placeholder images.** Only display real photos from the source listing. If no image can be scraped, show a text-only card instead.
- **Year / Make / Model / Trim**
- **Price** (with deal rating if available: great/good/fair/overpriced)
- **Mileage**
- **Location** (city, state, distance from user)
- **Dealer vs. private seller**
- **Key flags** (known problems, red flags, or positive signals like one-owner/no accidents)
- **Direct link** to the original listing

### Layout

- Card grid or side-by-side layout, sortable by price, mileage, or deal rating
- Highlight the best-value picks visually (border, badge, or background color)
- Include a summary section at the top with the recommendation and why

Always generate the comparison page alongside the text-based analysis — the web app is a visual complement, not a replacement for the detailed evaluation.

## Limitations

- Can't pull VIN history directly (user must buy Carfax/AutoCheck, ~$25-40)
- Regional price variance is real — rust-belt vs. southwest vs. PNW differ 10-15%
- Not a substitute for a physical PPI

```

---

## Secondary Skill: website-cloning

**Path:** `.local/secondary_skills/website-cloning/SKILL.md`

```markdown
---
name: website-cloning
description: Clone any website as a deployable React + Vite web app with real scraped content (images, text, structure, colors, fonts). Use when the user asks to clone, replicate, copy, or rebuild an existing website.
---

# Website Cloning

Clone a website's design and layout into a React + Vite web app using real scraped content from the target site.

## Legitimate Use Policy

**Before cloning, you MUST confirm the user's intent is legitimate.** Ask the user directly:

1. **"Is this your own website or your client's website?"** — Cloning your own site (e.g., to rebuild on a new stack, create a staging copy, or migrate platforms) is always fine.
2. **"What is this clone for?"** — Acceptable purposes include:
   - Rebuilding your own site on a new framework
   - Creating a design reference/inspiration starting point (with significant modifications planned)
   - Learning how a layout or component works
   - Building a staging/test version of a site you own
   - Migrating a client's site to a new platform with their permission

**REFUSE to proceed if any of these apply:**

- The user wants to impersonate another business or individual
- The clone will be used to collect credentials, payment info, or personal data from visitors who believe they're on the original site (phishing)
- The user wants to create a lookalike site to redirect or steal traffic from the original
- The clone copies trademarked branding (logos, brand names) of a business the user does not own, without plans to replace them
- The user explicitly states intent to deceive visitors about who operates the site

**When in doubt, ask.** A simple "What's this clone for?" usually clarifies intent. Most users have perfectly legitimate reasons — rebuilding their own site, learning from good design, or migrating platforms. Don't be overly suspicious, but do confirm before proceeding.

**Required modifications for non-owned sites:** If the user is cloning a site they don't own (for design inspiration), remind them to:

- Replace all logos, brand names, and trademarks with their own
- Replace product data, pricing, and business-specific content
- Change contact information, social links, and legal pages
- Treat the clone as a design template, not a finished product

## Overview

This skill uses Playwright (system Chromium) to scrape a target website's visual structure, content, images, colors, fonts, and layout — then builds a faithful React + Vite clone using that data. The clone uses real CDN image URLs, real text, real navigation links, and real design tokens extracted from the live site.

## Prerequisites

- **Chromium**: Use the system Chromium at the Nix store path. Run `find /nix/store -name chromium -type f 2>/dev/null | head -5` to locate the exact path. Cache it for all subsequent scripts.
- **Playwright**: Install via `pip install playwright` (no need for `playwright install` — use the system Chromium directly via `executable_path`).
- **Artifact**: Use the `artifacts` skill to scaffold a React + Vite web app artifact before building components.

## Phase 1: Visual Reconnaissance

Capture a full-page screenshot and extract design tokens before scraping content.

```python
from playwright.sync_api import sync_playwright

def recon(url, chromium_path, out_dir="clone"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=chromium_path)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(url, wait_until="networkidle", timeout=60000)

        # Force lazy content to load by scrolling the full page
        page.evaluate("""
          async () => {
            await new Promise(r => {
              let y = 0;
              const t = setInterval(() => {
                window.scrollBy(0, 300);
                y += 300;
                if (y >= document.body.scrollHeight) { clearInterval(t); r(); }
              }, 100);
            });
          }
        """)
        page.wait_for_timeout(3000)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(1000)

        # Full-page screenshot for visual reference
        page.screenshot(path=f"{out_dir}/full_page.png", full_page=True)

        # Extract design tokens
        tokens = page.evaluate("""
          () => {
            const body = document.body;
            const cs = getComputedStyle(body);
            return {
              bgColor: cs.backgroundColor,
              textColor: cs.color,
              fontFamily: cs.fontFamily,
              fontSize: cs.fontSize,
              // Extract CSS custom properties from :root
              cssVars: [...document.styleSheets].flatMap(sheet => {
                try {
                  return [...sheet.cssRules].filter(r => r.selectorText === ':root')
                    .flatMap(r => [...r.style].map(prop => [prop, r.style.getPropertyValue(prop)]));
                } catch { return []; }
              })
            };
          }
        """)
        # Save tokens as JSON
        import json
        open(f"{out_dir}/tokens.json", "w").write(json.dumps(tokens, indent=2))
        browser.close()
```

Key extractions:

- Background color, text color, font families
- CSS custom properties / design tokens
- Full-page screenshot as visual reference

## Phase 2: Deep Content Scrape

Extract all content from the rendered page. Critical: modern sites are SPAs — the raw HTML is often empty. You MUST use Playwright's `page.evaluate()` to extract content from the rendered DOM.

```python
def scrape_content(url, chromium_path, out_dir="clone"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=chromium_path)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(url, wait_until="networkidle", timeout=60000)

        # IMPORTANT: Scroll the full page to trigger lazy loading
        for _ in range(8):
            page.evaluate("window.scrollBy(0, 1500)")
            page.wait_for_timeout(1500)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(1000)

        data = page.evaluate("""
          () => {
            const result = {};

            // 1. Top banner / announcement bar
            // Look for common patterns: fixed top bars, rotating promos
            const banner = document.querySelector(
              '[class*="banner"], [class*="announcement"], [class*="promo-bar"], [class*="top-bar"]'
            );
            if (banner) {
              result.banner = {
                bgColor: getComputedStyle(banner).backgroundColor,
                text: banner.innerText.trim(),
                slides: [...banner.querySelectorAll('[class*="slide"], [class*="message"]')].map(s => ({
                  text: s.innerText.trim(),
                  link: s.querySelector('a')?.href || ''
                }))
              };
            }

            // 2. Header / Navigation
            const header = document.querySelector('header') || document.querySelector('[class*="header"], nav');
            if (header) {
              result.header = {
                height: header.offsetHeight,
                bgColor: getComputedStyle(header).backgroundColor,
                navLinks: [...header.querySelectorAll('a')].map(a => ({
                  text: a.innerText.trim(),
                  href: a.getAttribute('href') || ''
                })).filter(l => l.text && l.text.length < 50)
              };
            }

            // 3. All visible sections in DOM order
            const main = document.querySelector('main') || document.body;
            result.sections = [...main.children].map(child => {
              const rect = child.getBoundingClientRect();
              if (rect.height < 20) return null;
              const cs = getComputedStyle(child);
              if (cs.display === 'none' || cs.visibility === 'hidden') return null;
              return {
                tag: child.tagName.toLowerCase(),
                classes: child.className.toString().slice(0, 200),
                top: Math.round(rect.top + window.scrollY),
                height: Math.round(rect.height),
                bg: cs.backgroundColor,
                bgImage: cs.backgroundImage !== 'none' ? cs.backgroundImage : null,
                text: child.innerText.slice(0, 1500),
                images: [...child.querySelectorAll('img')].slice(0, 30).map(img => ({
                  src: img.src,
                  alt: img.alt,
                  w: img.offsetWidth,
                  h: img.offsetHeight
                })).filter(i => i.src && i.w > 30),
                links: [...child.querySelectorAll('a')].slice(0, 30).map(a => ({
                  text: a.innerText.trim(),
                  href: a.getAttribute('href') || ''
                })).filter(l => l.text)
              };
            }).filter(Boolean);

            // 4. Product/card data (e-commerce sites)
            const productLinks = document.querySelectorAll('a[href*="/product"], a[href*="/shop"], a[href*="/item"]');
            const seen = new Set();
            result.products = [...productLinks].map(link => {
              const href = (link.getAttribute('href') || '').split('?')[0];
              if (seen.has(href) || !href) return null;
              seen.add(href);
              const img = link.querySelector('img');
              const heading = link.querySelector('h2, h3, h4');
              const spans = link.querySelectorAll('span, div');
              let price = '';
              for (const s of spans) {
                if (s.innerText.match(/^\\$\\d/)) price = s.innerText.trim();
              }
              return {
                href,
                image: img?.src || '',
                imageAlt: img?.alt || '',
                title: heading?.innerText?.trim() || '',
                price,
                fullText: link.innerText.trim().slice(0, 300)
              };
            }).filter(Boolean);

            // 5. Footer
            const footer = document.querySelector('footer');
            if (footer) {
              result.footer = {
                text: footer.innerText.trim(),
                links: [...footer.querySelectorAll('a')].map(a => ({
                  text: a.innerText.trim(),
                  href: a.href
                })).filter(l => l.text),
                socialLinks: [...footer.querySelectorAll(
                  'a[href*="instagram"], a[href*="tiktok"], a[href*="pinterest"], a[href*="facebook"], a[href*="twitter"], a[href*="youtube"], a[href*="linkedin"]'
                )].map(a => ({ href: a.href }))
              };
            }

            // 6. Fonts (from Google Fonts links or @font-face)
            const fontLinks = [...document.querySelectorAll('link[href*="fonts.googleapis"], link[href*="fonts.gstatic"]')]
              .map(l => l.href);
            result.fonts = fontLinks;

            return result;
          }
        """)

        import json
        open(f"{out_dir}/content.json", "w").write(json.dumps(data, indent=2))
        browser.close()
```

## Phase 3: Image URL Verification

**Critical step.** Scraped image URLs are frequently truncated, expired, or incorrect. Always verify every image URL before using it.

```python
import subprocess

def verify_images(urls):
    """Returns dict of url -> status_code. Fix any non-200."""
    results = {}
    for url in urls:
        try:
            r = subprocess.run(
                ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '-L', url],
                capture_output=True, text=True, timeout=10
            )
            results[url] = r.stdout.strip()
        except:
            results[url] = 'TIMEOUT'
    return results
```

### Common Image URL Problems & Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Truncated filename | Playwright serialized long filename | Re-scrape with full `img.src` extraction |
| Wrong extension | Site serves `.png` but URL says `.jpg` | Check actual Content-Type header |
| Missing query params | Shopify/CDN URLs need `&width=` / `&crop=` | Add sizing params back |
| 403 Forbidden | Hotlink protection | Download image locally to `public/images/` |
| Expired signed URL | Temporary CDN token | Download and serve locally |

### Re-scrape strategy for broken images

If URLs are truncated, run a targeted re-scrape that extracts the full `img.src` property:

```python
# Target specific broken images by their alt text or position
data = page.evaluate("""
  () => [...document.querySelectorAll('img')]
    .filter(img => img.offsetWidth > 30)
    .map(img => ({
      src: img.src,              // Full URL from DOM
      srcset: img.srcset || '',  // May have higher-res versions
      alt: img.alt,
      width: img.offsetWidth,
      top: Math.round(img.getBoundingClientRect().top + window.scrollY)
    }))
""")
```

### Upgrading image resolution

CDN images often have size params you can modify:

```python
# Shopify CDN
url = url.replace("width=100", "width=800").replace("height=100", "height=800")

# Sanity CDN
url = url.replace("w=100", "w=1200").replace("h=100", "h=1200")

# General pattern: find width/height params and increase them
import re
url = re.sub(r'width=\d+', 'width=800', url)
url = re.sub(r'height=\d+', 'height=800', url)
```

## Phase 4: Build the Clone

### Project structure

```text
artifacts/{clone-name}/
  client/src/
    components/
      TopBanner.tsx       # Announcement/promo bar
      Header.tsx          # Logo + nav + icons
      HeroSection.tsx     # Hero images/video
      ProductCarousel.tsx # Scrollable product cards
      EditorialSections.tsx # Full-width editorial imagery
      Footer.tsx          # Footer columns + newsletter + social
    pages/
      home.tsx            # Assembles all components with real data
    index.css             # Design tokens, fonts, utilities
```

### Design token mapping

Extract these from the scrape and set as CSS custom properties:

```css
:root {
  --background: /* body background-color from scrape */;
  --foreground: /* body color from scrape */;
  --border: /* border color observed */;
  --top-banner: /* banner background-color */;
  --font-sans: /* primary font family */;
  --font-serif: /* heading/display font */;
}
```

### Data architecture

Keep scraped product/content data in the page file (e.g., `home.tsx`) as typed arrays, not in separate JSON files. This keeps the clone self-contained and avoids fetch complexity:

```tsx
const products = [
  {
    image: "https://cdn.shopify.com/...",  // Verified CDN URL
    name: "PRODUCT NAME",
    badge: "BEST-SELLER",
    retailPrice: "$192",
    salePrice: "$144",
    href: "/products/slug"
  },
  // ...
];
```

### Font loading

Add Google Fonts in `index.html`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&family=EB+Garamond:ital@0;1&display=swap" rel="stylesheet">
```

## Phase 5: Validation Checklist

After building, verify:

1. **All images load** — Run the URL verification script against every image URL in your components
2. **No console errors** — Check browser console logs via the refresh logs tool
3. **Responsive layout** — Test at 1440px (desktop), 768px (tablet), 375px (mobile)
4. **Visual fidelity** — Compare your clone's screenshot against the scraped `full_page.png`
5. **Real content** — No placeholder text ("Lorem ipsum"), no stock photos (Unsplash), no made-up prices
6. **Scroll behavior** — Sticky header, smooth scroll, proper z-indexing
7. **Hover states** — Image zoom, link opacity changes, button transitions

## Gotchas & Lessons Learned

### SPA sites (React, Next.js, Shopify)

- The raw HTML (`curl` output) is typically empty — just a `<div id="root">` or `<div id="app">`
- You MUST use Playwright with `wait_until="networkidle"` and scroll the page before extracting
- Content is rendered client-side — only `page.evaluate()` can access it

### Lazy-loaded content

- Scroll the ENTIRE page before extracting. Use multiple scroll passes with delays (see example below)
- Some content loads only when scrolled into viewport — a single `scrollTo(bottom)` may not trigger it

```python
for _ in range(8):
    page.evaluate("window.scrollBy(0, 1500)")
    page.wait_for_timeout(1500)
```

### Image URL truncation

- The most common scrape failure. Playwright's DOM serialization and JSON output can silently truncate very long URLs
- Always verify with `curl -s -o /dev/null -w '%{http_code}'` before using any URL
- When truncated: re-scrape specifically targeting that image's `img.src` property

### Hotlink protection

- Some sites block external embedding of their images (403 responses)
- Solution: Download images to `public/images/` and serve them locally
- This is also a good fallback for any URL that might expire

### Dynamic pricing / variant data

- Product prices and variant names often render via JavaScript after the card enters viewport
- Extract `innerText` from the product link container — prices are usually in nested spans
- Check for `text-decoration: line-through` to identify retail vs sale prices

### CDN URL patterns

- **Shopify**: `cdn.shopify.com/s/files/...?width=X&height=Y&crop=center`
- **Sanity**: `cdn.sanity.io/images/{project}/{dataset}/{hash}.{ext}?w=X&h=Y&q=80&auto=format`
- **Contentful**: `images.ctfassets.net/{space}/{id}/{name}?w=X&h=X`
- **Cloudinary**: `res.cloudinary.com/{cloud}/image/upload/w_X,h_Y/{path}`

## Quick Start

```bash
# 1. Find Chromium
find /nix/store -name chromium -type f 2>/dev/null | head -5

# 2. Install Playwright
pip install playwright

# 3. Run recon
python3 scripts/recon.py https://target-site.com

# 4. Run deep scrape
python3 scripts/scrape_content.py https://target-site.com

# 5. Verify images
python3 scripts/verify_images.py

# 6. Create artifact and build components
# Use the artifacts skill, then build components from scraped data

# 7. Final verification
# Check all images load, no console errors, responsive layout
```

```

---

