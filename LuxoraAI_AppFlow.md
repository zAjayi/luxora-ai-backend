# **LuxoraAI — App Flow Document (v1.0)**

## **1\. High-Level Flow Overview**

Entry → Input Content → Configure Repurpose → Submit Job → AI Processing (Streaming) → View Results → Edit/Copy/Export → Save to Library → Reuse/Search  
---

## **2\. Core User Journeys**

### **2.1 Primary Flow (Phase 1 — MVP)**

**Goal:** Repurpose content in \< 2 minutes

Dashboard  
  ↓  
New Repurpose Page  
  ↓  
\[Input Content\]  
  ↓  
\[Select Platforms \+ Options\]  
  ↓  
Submit Job  
  ↓  
Streaming Results Page  
  ↓  
Edit / Copy / Regenerate  
  ↓  
Auto-save to Library  
---

### **2.2 Secondary Flow (History Reuse)**

Dashboard / Library  
  ↓  
Select Past Job  
  ↓  
View Outputs  
  ↓  
Edit / Copy / Regenerate  
---

### **2.3 Phase 2 (Auth \+ SaaS Flow)**

Landing Page  
  ↓  
Register / Login  
  ↓  
Dashboard  
  ↓  
Usage Check (Free/Pro Limits)  
  ↓  
Repurpose Flow  
  ↓  
Billing Prompt (if limit reached)  
---

## **3\. Screen-Level App Flow**

---

## **3.1 Dashboard**

**Purpose:** Entry point \+ quick actions

### **UI Components:**

* Recent Jobs List  
* “New Repurpose” CTA  
* Quick stats (jobs count — Phase 2\)  
* Search bar (Phase 2\)

### **Actions:**

* Click “New Repurpose” → Navigate to Input Screen  
* Click Job → Open Results View

---

## **3.2 New Repurpose Screen (Core Engine Entry)**

### **Sections:**

#### **1\. Content Input**

* Text Area (Primary)  
* URL Input (scraper trigger)  
* File Upload (Phase 2\)

#### **2\. Configuration Panel**

* Platform Selector (multi-select)  
* Tone Selector  
* Brand Voice (optional)  
* Toggles:  
  * Hashtags ON/OFF  
  * Emojis ON/OFF  
* CTA Input Field

#### **3\. Submission**

* “Generate Content” Button

---

### **Flow:**

User Input → Validate → Submit → POST /repurpose → Redirect to Results (Streaming Mode)  
---

## **3.3 AI Processing (Streaming State)**

### **Behavior:**

* Transition immediately after submission  
* Display loading \+ streaming outputs per platform

### **UI States:**

1. **Initializing**  
2. **Streaming Output (per platform)**  
3. **Completed**

---

### **Streaming Flow:**

Frontend (EventSource)  
  ← SSE stream  
Backend (FastAPI)  
  ← AI Layer (Gemma)  
---

## **3.4 Results View (Core Experience)**

**Most important screen in the app**

---

### **Layout:**

Platform Group (e.g., Twitter/X)  
  ├── Variant 1  
  ├── Variant 2  
  ├── Variant 3

Platform Group (LinkedIn)  
  ├── Variants...  
---

### **Per Output Actions:**

* ✏️ Edit (inline)  
* 📋 Copy  
* 🔁 Regenerate (single output)  
* ⭐ Favourite (Phase 2\)

---

### **Page-Level Actions:**

* Export All (.txt / .csv)  
* Back to Dashboard

---

### **Flow:**

Streaming Complete  
  ↓  
User interacts with outputs  
  ↓  
Optional edits/regeneration  
  ↓  
Saved automatically  
---

## **3.5 Content Library**

### **Purpose:**

Central storage of all jobs

---

### **Features:**

* List of all repurpose jobs  
* Filters:  
  * Platform  
  * Tone  
  * Date  
* Search (keyword-based)

---

### **Flow:**

Library → Select Job → Results View  
---

## **3.6 Brand Voice Management**

### **Features:**

* Create brand voice profile  
* Edit/Delete profile

---

### **Flow:**

Create Profile  
  ↓  
Stored in DB  
  ↓  
Selectable in New Repurpose  
---

## **3.7 Account & Settings (Phase 2\)**

* Profile info  
* Default tone  
* Default platforms  
* Plan info

---

## **3.8 Billing (Phase 2\)**

### **Flow:**

User hits limit  
  ↓  
Upgrade Prompt Modal  
  ↓  
Stripe Checkout  
  ↓  
Webhook → Update Plan  
---

## **3.9 Auth Flow (Phase 2\)**

Register → Login → JWT Issued → Access App  
---

## **4\. System Interaction Flow**

---

## **4.1 Repurpose Job Lifecycle**

Frontend  
  ↓ POST /repurpose  
Backend  
  ↓ Validate input  
  ↓ Save job (DB)  
  ↓ Call AI Service  
AI Layer (Gemma)  
  ↓ Generate structured JSON  
Backend  
  ↓ Stream results (SSE)  
Frontend  
  ↓ Render progressively  
Backend  
  ↓ Save outputs  
---

## **4.2 Regeneration Flow**

User clicks Regenerate  
  ↓  
POST /outputs/{id}/regenerate  
  ↓  
AI call (single output)  
  ↓  
Replace output  
---

## **4.3 Search Flow**

User types query  
  ↓  
GET /content/search  
  ↓  
Return filtered jobs/outputs  
---

## **5\. Navigation Structure**

/dashboard  
/new  
/results/:jobId  
/library  
/brand-voices  
/settings  
/billing (P2)  
/login (P2)  
/register (P2)  
---

## **6\. State Management (Frontend \- React)**

### **Global State (Zustand):**

* User (Phase 2\)  
* Current Job  
* Streaming State  
* Selected Platforms  
* Brand Voice

---

### **Server State (React Query):**

* Jobs  
* Outputs  
* Profile  
* Subscription

---

## **7\. Key UI States & Edge Cases**

---

### **7.1 Empty States**

* No jobs → “Create your first repurpose”  
* No outputs → fallback message

---

### **7.2 Error States**

* AI timeout (\>30s)  
* Invalid URL scrape  
* File parsing failure

---

### **7.3 Loading States**

* Skeleton loaders for results  
* Streaming indicators per platform

---

### **7.4 Limit Enforcement (Phase 2\)**

If usage \>= limit:  
  Show soft block  
  Allow upgrade  
  Prevent new job submission  
---

## **8\. Phase-Based Flow Differences**

---

### **Phase 1 (MVP)**

* No authentication  
* Single user  
* Local storage  
* No billing  
* Focus: speed \+ output quality

---

### **Phase 2 (SaaS)**

* Auth required  
* Multi-user  
* Usage limits  
* Billing integration  
* Async queue (Celery)

---

## **9\. Critical UX Flows (Must Be Perfect)**

These are your **make-or-break flows**:

### **1\. Repurpose Flow**

* Input → Generate → Results  
* Must feel **instant \+ intelligent**

### **2\. Streaming Experience**

* Outputs appear progressively  
* Gives perception of speed

### **3\. Copy UX**

* One-click copy must be flawless

### **4\. Regeneration**

* Fast \+ targeted (no full refresh)

---

## **10\. Developer Handoff Notes**

### **Frontend Priorities:**

* Streaming via EventSource  
* Component structure:  
  * `PlatformGroup`  
  * `OutputCard`  
  * `StreamingBlock`

### **Backend Priorities:**

* SSE implementation  
* Prompt builder abstraction  
* Modular AI service layer

---

## **11\. Suggested Component Tree (React)**

App  
├── Layout  
├── Dashboard  
├── NewRepurpose  
│     ├── InputPanel  
│     ├── ConfigPanel  
│     └── SubmitButton  
├── Results  
│     ├── PlatformGroup  
│     │     └── OutputCard  
├── Library  
├── BrandVoices  
├── Settings  
---

## **12\. Final Summary**

LuxoraAI’s app flow is built around **one dominant loop**:

**Input once → Generate many → Refine quickly → Reuse forever**

Everything in the system reinforces:

* Speed  
* Output quality  
* Minimal friction

