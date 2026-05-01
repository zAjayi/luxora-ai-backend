  **LUXORAAI**  

  AI-Powered Content Repurposing Platform  

  *Product Requirements Document*


| Document Version | v1.0 |
| :---- | :---- |
| **Status** | Draft — Ready for Review |
| **Date** | April 30, 2026 |
| **Owner** | Product Owner / Founder |
| **AI Engine** | Google Gemma 4 31B (via OpenRouter) |
| **Tech Stack** | FastAPI (Python) · PostgreSQL · React |
| **Target Audience** | Personal Use (Phase 1\) → Limited Paid Public Access (Phase 2\) |
| **Classification** | Confidential |

# **1\. Executive Summary**

LuxoraAI is an AI-powered content repurposing platform designed to help content creators, marketers, and solopreneurs transform existing content into platform-optimized social media posts — effortlessly and at scale. Built around Google’s Gemma 4 31B model, LuxoraAI understands the nuances of tone, platform conventions, character limits, and audience engagement to produce high-quality repurposed content on demand.

The product launches as personal-use software for the founder, with a clear upgrade path to a limited paid public access model (SaaS), enabling monetization without over-engineering in the early phase.

# **2\. Problem Statement**

Content creators produce long-form material — blogs, videos, newsletters, podcasts, threads — but lack the time and resources to consistently adapt that content across multiple social media platforms, each requiring different formats, tones, and lengths. The result is:

* Inconsistent posting cadence across platforms

* Missed engagement opportunities from existing high-value content

* Time lost manually rewriting the same ideas for Twitter/X, LinkedIn, Instagram, and more

* Content fatigue from producing net-new posts for every channel

LuxoraAI solves this by providing a single intelligent workspace where one piece of content becomes many, tailored perfectly for each platform.

# **3\. Goals & Success Metrics**

## **3.1 Product Goals**

* Reduce time to repurpose content from hours to under 2 minutes per piece

* Support all major social platforms with platform-aware output formatting

* Deliver a personal-use MVP within 6 weeks of development start

* Establish a monetizable SaaS foundation for Phase 2 public access

## **3.2 Key Success Metrics**

| Metric | Phase 1 Target | Phase 2 Target |
| :---- | :---- | :---- |
| Repurpose Generation Time | \< 30 seconds | \< 20 seconds |
| Platforms Supported | 5 platforms | 8+ platforms |
| User Satisfaction (quality rating) | \> 4/5 self-rating | \> 4/5 user rating |
| API Uptime | 99% | 99.5% (hosted) |
| Monthly Active Users | 1 (founder) | 50–200 beta users |
| Monthly Recurring Revenue | N/A | $500–$2,000 |

# **4\. User Personas**

|   Persona 1: The Founder (Phase 1\)   Name: Alex   Role: Content creator, solopreneur   Pain Points: Spends 3+ hours/week adapting content Inconsistent posting schedule Wants tools that actually understand context |   Persona 2: The Power User (Phase 2\)   Name: Jordan   Role: Marketing manager, small agency   Pain Points: Manages 3–5 client content pipelines Needs bulk repurposing with brand voice control Requires export and scheduling integrations |
| :---- | :---- |

# **5\. Scope & Phasing**

## **Phase 1 — Personal MVP (Weeks 1–6)**

Goal: A fully functional local/self-hosted tool for the founder’s personal content workflow.

## **Phase 2 — Limited Public SaaS (Weeks 7–16)**

Goal: Harden the platform for external users with auth, billing, usage limits, and improved UX.

# **6\. Functional Requirements**

## **6.1 Content Input**

* FR-01: Accept long-form text input (blog posts, articles, scripts, transcripts) via text area

* FR-02: Support URL input — system scrapes and extracts article content for processing

* FR-03: Accept file uploads: .txt, .md, .pdf, .docx (Phase 1: text/md; Phase 2: all formats)

* FR-04: Allow users to paste YouTube or podcast transcript URLs for extraction

* FR-05: Support bulk input (multiple content pieces in one session) — Phase 2

## **6.2 Platform Targeting**

* FR-06: User selects one or more target platforms per repurpose job

* FR-07: Supported platforms (Phase 1): Twitter/X, LinkedIn, Instagram, Facebook, Threads

* FR-08: Additional platforms (Phase 2): TikTok captions, YouTube Shorts description, Pinterest, Bluesky

* FR-09: Each platform profile includes: character limit, tone guide, hashtag style, formatting rules

## **6.3 AI Repurposing Engine**

* FR-10: Generate platform-specific repurposed content using Google Gemma 4 31B

* FR-11: Support tone selection: Professional, Casual, Witty, Inspirational, Educational, Conversational

* FR-12: Allow custom tone/brand voice input as a free-text style guide (per job or saved profile)

* FR-13: Generate multiple variations per platform (default: 3 variants)

* FR-14: Include hashtag generation, relevant to platform and content (configurable on/off)

* FR-15: Support call-to-action injection — user defines CTA text appended to relevant outputs

* FR-16: Thread generation for Twitter/X (auto-splits into numbered tweet thread)

* FR-17: Emoji injection toggle for platforms where emojis are appropriate

* FR-18: Preserve key statistics, quotes, and data points from source content in outputs

## **6.4 Output Management**

* FR-19: Display all generated outputs on a structured results page, grouped by platform

* FR-20: Inline editing of any generated output before saving or copying

* FR-21: One-click copy to clipboard per output

* FR-22: Export outputs as .txt or .csv bundle (all platforms in one file)

* FR-23: Regenerate individual outputs without re-processing the full job

* FR-24: Save output history to user’s account with tagging and search — Phase 2

## **6.5 Content Library & History**

* FR-25: Store all repurpose jobs with source content, settings, and outputs in PostgreSQL

* FR-26: Search and filter past jobs by date, platform, tone, or keyword

* FR-27: Favourite/bookmark outputs for quick retrieval

* FR-28: Delete individual outputs or full jobs

## **6.6 User & Account Management**

* FR-29: Phase 1: Single-user local mode (no auth required)

* FR-30: Phase 2: Email/password registration and login (JWT auth)

* FR-31: OAuth login via Google (Phase 2\)

* FR-32: User profile with name, brand name, default tone preference, default platforms

* FR-33: Saved brand voice profiles: users define persona-based writing styles

## **6.7 Subscription & Billing (Phase 2\)**

* FR-34: Free tier: 10 repurpose jobs/month, 3 platforms per job, no history export

* FR-35: Pro tier ($12–19/month): Unlimited jobs, all platforms, full history, bulk input, CSV export

* FR-36: Usage dashboard showing current month’s job count vs. limit

* FR-37: Stripe integration for subscription management and billing

* FR-38: Graceful limit enforcement with upgrade prompts (no hard failures)

# **7\. Non-Functional Requirements**

| ID | Category | Requirement | Target |
| :---- | :---- | :---- | :---- |
| NFR-01 | Performance | End-to-end generation time | \< 30s for 5 platforms |
| NFR-02 | Performance | API response (non-AI endpoints) | \< 500ms (p95) |
| NFR-03 | Scalability | Concurrent users supported | 1 (Phase 1\) / 50 (Phase 2\) |
| NFR-04 | Reliability | API uptime target | 99% (P1) / 99.5% (P2) |
| NFR-05 | Security | JWT token expiry | 24h access / 7d refresh |
| NFR-06 | Security | Passwords stored as | Bcrypt hash (cost 12\) |
| NFR-07 | Security | HTTPS enforcement | All environments (P2) |
| NFR-08 | Privacy | AI prompt data retention | Not sent to 3rd party APIs |
| NFR-09 | UX | Mobile responsiveness | Fully responsive React UI |
| NFR-10 | UX | First meaningful paint | \< 2 seconds |
| NFR-11 | Maintainability | Test coverage target | \> 70% unit (backend) |
| NFR-12 | Observability | Structured logging | All FastAPI endpoints |

# **8\. System Architecture**

## **8.1 High-Level Architecture**

LuxoraAI follows a clean client-server architecture with a decoupled AI inference layer:

* Frontend: React SPA (Vite) — communicates with backend exclusively via REST API

* Backend: FastAPI (Python 3.11+) — handles all business logic, auth, and AI orchestration

* Database: PostgreSQL 16 — stores users, jobs, content, outputs, and subscription data

* AI Layer: Google Gemma 4 31B — invoked via Ollama (local) or Vertex AI endpoint (cloud)

* Queue (Phase 2): Celery \+ Redis for async job processing at scale

* Storage (Phase 2): S3-compatible object store for uploaded file handling

## **8.2 Backend Structure (FastAPI)**

  app/

  ├── api/           \# Route handlers (v1)  
  │   ├── repurpose.py  \# Core repurposing endpoints  
  │   ├── auth.py       \# Login, register, refresh  
  │   ├── content.py    \# Library, history, search  
  │   └── billing.py    \# Stripe webhooks, plans  
  ├── core/          \# Config, DB, security  
  ├── models/        \# SQLAlchemy ORM models  
  ├── schemas/       \# Pydantic request/response models  
  ├── services/      \# Business logic layer  
  └── ai/            \# Gemma prompt builder \+ inference client

## **8.3 Database Schema (Core Tables)**

* users — id, email, hashed\_password, name, brand\_voice, plan, created\_at

* repurpose\_jobs — id, user\_id, source\_text, source\_url, tone, platforms, created\_at

* repurposed\_outputs — id, job\_id, platform, variant\_index, content, is\_favourite

* brand\_voices — id, user\_id, name, description, style\_guide\_text

* subscriptions — id, user\_id, stripe\_customer\_id, plan, status, current\_period\_end

# **9\. AI Engine Specification**

## **9.1 Model: Google Gemma 4 31B**

| Model | google/gemma-4-31b-it (instruction-tuned variant) |
| :---- | :---- |
| **Context Window** | 128K tokens (source content \+ system prompt \+ outputs) |
| **Inference Mode** | Phase 1: Ollama (local GPU/CPU) — Phase 2: Vertex AI or Together AI endpoint |
| **Temperature** | 0.75 (creative but coherent) |
| **Max Output Tokens** | 2,048 per generation call |
| **Streaming** | Streamed responses to frontend via SSE (Server-Sent Events) |

## **9.2 Prompt Architecture**

* System Prompt: Defines LuxoraAI’s role, platform rules, tone instructions, and output format

* User Prompt: Injects source content, selected platforms, tone, CTA, hashtag preferences

* Output Format: Structured JSON — each platform maps to an array of variant strings

* Platform Configs: Embedded in system prompt as a structured lookup (char limits, conventions)

* Brand Voice: Appended to system prompt when a saved brand voice profile is selected

## **9.3 Platform Output Rules**

| Platform | Char Limit | Hashtags | Special Rules |
| :---- | :---- | :---- | :---- |
| Twitter/X | 280 chars | 1–3 | Thread mode available; hooks required on tweet 1 |
| LinkedIn | 3,000 chars | 3–5 | Professional tone; line breaks after every sentence; strong opener |
| Instagram | 2,200 chars | 5–15 | Story-driven; CTA in last line; hook in first line |
| Facebook | 63,206 chars | 0–2 | Conversational; question-based CTAs; avoid link-in-post penalty |
| Threads | 500 chars | 0–2 | Casual, authentic; first-person; no corporate tone |

# **10\. Core API Endpoints**

| Method | Endpoint | Description |
| :---- | :---- | :---- |
| **POST** | /api/v1/repurpose | Submit a repurpose job; returns job ID and streamed outputs |
| **GET** | /api/v1/jobs | List all repurpose jobs for the authenticated user |
| **GET** | /api/v1/jobs/{id} | Retrieve a specific job with all outputs |
| **DELETE** | /api/v1/jobs/{id} | Delete a job and its associated outputs |
| **POST** | /api/v1/outputs/{id}/regenerate | Regenerate a single output variant |
| **PATCH** | /api/v1/outputs/{id} | Edit or favourite/unfavourite an output |
| **GET** | /api/v1/content/search | Full-text search across past jobs and outputs |
| **POST** | /api/v1/auth/register | Create a new user account (Phase 2\) |
| **POST** | /api/v1/auth/login | Authenticate and receive JWT tokens |
| **POST** | /api/v1/auth/refresh | Refresh access token using refresh token |
| **GET** | /api/v1/profile | Get current user profile and plan info |
| **PUT** | /api/v1/profile/brand-voice | Update or create brand voice profile |
| **POST** | /api/v1/billing/checkout | Create Stripe checkout session (Phase 2\) |
| **POST** | /api/v1/billing/webhook | Handle Stripe subscription events |

# **11\. Frontend UI Screens**

## **11.1 Screen Inventory**

* Dashboard — Recent jobs, quick stats, quick repurpose shortcut

* New Repurpose — Primary content input form with all configuration options

* Results View — Platform-grouped outputs with edit, copy, regenerate, favourite controls

* Content Library — Searchable history of all past jobs and saved outputs

* Brand Voices — Create and manage saved writing style profiles

* Account / Settings — Profile, preferences, API usage, plan management

* Billing (Phase 2\) — Plan selection, subscription status, usage meter

* Auth Screens (Phase 2\) — Login, Register, Forgot Password

## **11.2 Design Principles**

* Clean, minimal UI — content is the focus; no unnecessary decoration

* Dark mode support from day one

* Streaming output display — results appear progressively as Gemma generates

* Mobile-first responsive layout — usable on smartphone for quick repurposing on the go

* Keyboard-friendly — power users can navigate and copy without a mouse

## **11.3 Tech Choices (Frontend)**

* Framework: React 18 with Vite

* State Management: Zustand (lightweight, no boilerplate)

* Styling: Tailwind CSS with shadcn/ui components

* Data Fetching: TanStack Query (React Query v5)

* Streaming: EventSource API for SSE output streaming

* Routing: React Router v6

# **12\. Security & Privacy**

* All user passwords hashed with bcrypt (cost factor 12\) — never stored in plain text

* JWT-based authentication — short-lived access tokens (24h) \+ refresh tokens (7d)

* HTTPS enforced on all Phase 2 deployments via TLS/SSL certificate

* Rate limiting on AI endpoints — prevent abuse and control inference costs

* Source content is NOT sent to third-party AI APIs — Gemma runs locally or on private infra

* Database credentials managed via environment variables — never hardcoded

* CORS configured to allow only frontend origin in production

* SQL injection prevention via SQLAlchemy ORM parameterized queries

* Input sanitization on all user-submitted text fields

* Phase 2: Stripe handles all payment data — LuxoraAI stores no raw card information

# **13\. Development Roadmap**

| Phase | Timeline | Deliverables |
| :---- | :---- | :---- |
| **Phase 1Sprint 1** | Weeks 1–2 | Project scaffolding (FastAPI \+ React \+ PostgreSQL), Gemma 4 integration via Ollama, Core /repurpose endpoint, Basic React UI with text input and platform selector |
| **Phase 1Sprint 2** | Weeks 3–4 | Full platform output generation (5 platforms), Results page with copy/edit/regenerate, Job history storage and retrieval, URL scraper for content input |
| **Phase 1Sprint 3** | Weeks 5–6 | Brand voice profiles, Tone selector, Hashtag generation, Thread mode for Twitter/X, Content library with search |
| **Phase 2Sprint 4** | Weeks 7–9 | JWT auth (register/login/refresh), User profiles, Plan/tier system (Free vs Pro), Usage tracking and enforcement |
| **Phase 2Sprint 5** | Weeks 10–12 | Stripe billing integration, File upload support (PDF, DOCX), Bulk repurpose mode, CSV export |
| **Phase 2Sprint 6** | Weeks 13–16 | Production deployment (Docker \+ cloud VPS), Monitoring and logging, Beta user onboarding, Performance optimization, Bug fixes |

# **14\. Risks & Mitigations**

| Risk | Severity | Mitigation |
| :---- | :---- | :---- |
| Gemma 4 31B too slow on local hardware | **High** | Quantized model (Q4\_K\_M via Ollama); fallback to cloud endpoint if latency \> 30s |
| AI output quality below expectations | **Medium** | Prompt engineering iteration; few-shot examples in system prompt; user rating feedback loop |
| Scope creep delays Phase 1 MVP | **Medium** | Strict feature lock for Phase 1 sprints; defer anything not in FR-01 to FR-28 |
| PostgreSQL data loss (local mode) | **Low** | Daily automated backups via pg\_dump cron job; WAL logging enabled |
| Stripe payment disputes (Phase 2\) | **Low** | Clear billing terms; usage logs as evidence; automated receipt emails |
| Platform API policy changes | **Low** | No direct API integrations; content is generated text; user posts manually |

# **15\. Future Considerations (Post-Phase 2\)**

* Direct social media scheduling integrations (Buffer, Hootsuite API, or native platform APIs)

* Analytics dashboard: track which repurposed content performs best per platform

* Team workspaces: shared brand voices, collaborative content pipelines

* Chrome extension: highlight any web article and repurpose in one click

* Mobile app (React Native): full repurposing from iOS/Android

* Webhook / Zapier integration: trigger repurposing from external tools

* Image caption and alt-text generation for accessibility

* White-label version: agencies license LuxoraAI under their brand

# **16\. Glossary**

| Repurpose Job | A single content transformation request containing a source text and target platforms |
| :---- | :---- |
| **Output Variant** | One of 3 generated text options per platform per repurpose job |
| **Brand Voice** | A saved writing style profile describing tone, persona, and language conventions |
| **Platform Config** | Internal rules defining character limits, hashtag norms, and formatting for each social network |
| **Gemma 4 31B** | Google’s open-weight instruction-tuned large language model with 31 billion parameters |
| **Ollama** | A local model runtime that allows Gemma to run on the founder’s hardware without cloud API calls |
| **SSE** | Server-Sent Events — a protocol for streaming AI-generated text progressively to the frontend |
| **JWT** | JSON Web Token — a compact, self-contained token used for stateless API authentication |
| **CTA** | Call to Action — a phrase appended to content that prompts audience engagement |

  LuxoraAI PRD v1.0  ·  Confidential  ·  © 2026 LuxoraAI  
