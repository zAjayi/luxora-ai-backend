# **LuxoraAI — Tech Stack Document (v1.0)**

---

## **1\. Overview**

LuxoraAI is built as a **modern AI-powered SaaS platform** using a **decoupled architecture**:

* **Frontend:** Reactive, fast, streaming-first UI  
* **Backend:** API-first, modular FastAPI service  
* **AI Layer:** OpenRouter API for LLM inference  
* **Database:** Relational, structured storage for jobs and outputs

---

## **2\. High-Level Architecture Stack**

Frontend (React \+ Vite)  
       ↓  
Backend API (FastAPI)  
       ↓  
AI Orchestration Layer  
       ↓  
LLM (Gemma via Ollama / Cloud)  
       ↓  
PostgreSQL Database  
---

## **3\. Frontend Stack**

### **3.1 Core Framework**

* **React 18 (Vite)**  
  * Fast dev server  
  * Optimized build output  
  * Ideal for SPA architecture

---

### **3.2 Styling & UI**

* **Tailwind CSS**  
  * Utility-first styling  
  * Rapid UI development  
* **shadcn/ui**  
  * Accessible component primitives  
  * Clean, minimal design (fits Luxora brand)

---

### **3.3 State Management**

* **Zustand**  
  * Lightweight global state  
  * No boilerplate  
  * Perfect for:  
    * Current job state  
    * Streaming state  
    * UI preferences

---

### **3.4 Server State & Data Fetching**

* **TanStack Query (React Query v5)**  
  * API caching  
  * Background refetching  
  * Mutation handling

---

### **3.5 Routing**

* **React Router v6**  
  * Declarative routing  
  * Nested layouts support

---

### **3.6 Streaming (Critical Feature)**

* **EventSource API (SSE)**  
  * Real-time AI output streaming  
  * Low overhead vs WebSockets  
  * Native browser support

---

### **3.7 Form Handling**

* **React Hook Form**  
  * High performance  
  * Minimal re-renders  
* **Zod**  
  * Schema validation  
  * Shared validation with backend (optional)

---

### **3.8 Optional Enhancements**

* **Framer Motion** → Smooth UI transitions  
* **React Hot Toast** → Notifications (copy success, errors)

---

## **4\. Backend Stack**

---

### **4.1 Core Framework**

* **FastAPI (Python 3.11+)**  
  * High performance (async)  
  * Automatic OpenAPI docs  
  * Native support for SSE

---

### **4.2 API Layer**

* RESTful architecture:  
  * `/repurpose`  
  * `/jobs`  
  * `/outputs`  
  * `/auth` (Phase 2\)  
  * `/billing` (Phase 2\)

---

### **4.3 Data Validation**

* **Pydantic**  
  * Request/response schemas  
  * Strong typing

---

### **4.4 ORM / Database Access**

* **SQLAlchemy (2.0)**  
  * ORM for PostgreSQL  
  * Async support  
* **Alembic**  
  * Database migrations

---

### **4.5 Background Processing (Phase 2\)**

* **Celery**  
  * Async job queue  
  * Offload AI processing  
* **Redis**  
  * Message broker for Celery  
  * Caching layer (optional)

---

### **4.6 Authentication (Phase 2\)**

* **JWT (JSON Web Tokens)**  
  * Access token (24h)  
  * Refresh token (7 days)  
* **Passlib (bcrypt)**  
  * Secure password hashing  
* **OAuth (Google Login)**  
  * Optional login method

---

### **4.7 File Handling (Phase 2\)**

* **Python Libraries**  
  * `python-docx` → DOCX parsing  
  * `PyPDF2` / `pdfplumber` → PDF parsing  
  * `markdown` → MD parsing

---

### **4.8 Web Scraping**

* **BeautifulSoup \+ Requests**  
  * Extract content from URLs  
* Optional:  
  * `newspaper3k` (better article extraction)

---

## **5\. AI Layer**

---

### **5.1 Core Model**

* **Google Gemma 4 31B (Instruction-tuned)**

---

### **5.2 Local Inference (Phase 1\)**

* **OpenRouter**  
  * Run model locally  
  * No external API dependency  
  * Privacy-first

---

### **5.3 Cloud Inference (Phase 2\)**

* **Vertex AI (Google Cloud)**  
   OR  
* **Together AI**

---

### **5.4 Prompt Engineering Layer**

Custom service:

app/ai/  
├── prompt\_builder.py  
├── platform\_configs.py  
├── inference\_client.py

Responsibilities:

* Build system prompt  
* Inject platform rules  
* Apply brand voice  
* Format structured JSON output

---

### **5.5 Streaming Output**

* SSE from backend → frontend  
* Token-by-token or chunk streaming

---

## **6\. Database Stack**

---

### **6.1 Core Database**

* **PostgreSQL 16**

---

### **6.2 Key Tables**

* `users`  
* `repurpose_jobs`  
* `repurposed_outputs`  
* `brand_voices`  
* `subscriptions`

---

### **6.3 Features Used**

* Full-text search (for content library)  
* JSON fields (optional for flexible metadata)  
* Indexing for fast queries

---

## **7\. Storage (Phase 2\)**

* **S3-Compatible Storage**  
  * AWS S3 / Cloudflare R2 / MinIO

Used for:

* Uploaded files  
* Large content blobs

---

## **8\. DevOps & Deployment**

---

### **8.1 Development Environment**

* **Docker (recommended)**  
  * Backend \+ DB \+ Redis  
* **Docker Compose**  
  * Local orchestration

---

### **8.2 Backend Deployment**

* **Cloud VPS (DigitalOcean / AWS EC2 / Hetzner)**  
* ASGI Server:  
  * **Uvicorn**  
  * **Gunicorn (with Uvicorn workers)**

---

### **8.3 Frontend Deployment**

* **Vercel** or **Netlify**  
  * Fast global CDN  
  * Easy CI/CD

---

### **8.4 Reverse Proxy**

* **Nginx**  
  * HTTPS  
  * Routing  
  * Rate limiting

---

### **8.5 CI/CD**

* **GitHub Actions**  
  * Linting  
  * Tests  
  * Deploy automation

---

## **9\. Observability & Monitoring**

---

### **9.1 Logging**

* Python `logging`  
* Structured logs (JSON)

---

### **9.2 Monitoring**

* **Prometheus \+ Grafana** (optional)  
* Or simpler:  
  * Log-based monitoring

---

### **9.3 Error Tracking**

* **Sentry**

---

## **10\. Security Stack**

---

### **10.1 Core Measures**

* HTTPS (TLS)  
* JWT authentication  
* Bcrypt password hashing

---

### **10.2 API Protection**

* Rate limiting (FastAPI middleware)  
* Input sanitization  
* CORS restrictions

---

### **10.3 Data Privacy**

* No third-party AI APIs in Phase 1  
* Local inference via Ollama

---

## **11\. Performance Optimization**

---

### **11.1 Backend**

* Async endpoints (FastAPI)  
* Connection pooling (PostgreSQL)  
* Caching (Redis optional)

---

### **11.2 AI**

* Quantized model (Q4\_K\_M)  
* Streaming responses (SSE)

---

### **11.3 Frontend**

* Code splitting  
* Lazy loading routes  
* Skeleton loaders

---

## **12\. Phase-Based Stack Evolution**

---

### **Phase 1 (MVP)**

* React \+ Tailwind  
* FastAPI  
* PostgreSQL  
* Ollama (local AI)  
* No auth, no billing

---

### **Phase 2 (SaaS)**

* Add:  
  * JWT Auth  
  * Stripe Billing  
  * Redis \+ Celery  
  * Cloud AI fallback  
  * S3 storage

---

## **13\. Recommended Folder Structure**

---

### **Backend**

app/  
├── api/  
├── core/  
├── models/  
├── schemas/  
├── services/  
├── ai/  
└── main.py  
---

### **Frontend**

src/  
├── components/  
├── pages/  
├── hooks/  
├── store/  
├── services/  
├── routes/  
└── utils/  
---

## **14\. Key Design Decisions**

---

### **1\. SSE over WebSockets**

* Simpler  
* Perfect for one-way streaming (AI → UI)

---

### **2\. Local-first AI**

* Privacy advantage  
* Cost control  
* Better positioning for “luxury AI tool”

---

### **3\. Modular AI Layer**

* Easily switch between:  
  * Ollama  
  * Vertex AI  
  * Future models

---

### **4\. Lightweight State (Zustand)**

* Avoid Redux complexity  
* Faster development

---

## **15\. Future Stack Additions**

* **React Native** → Mobile app  
* **Chrome Extension APIs** → In-browser repurposing  
* **Zapier / Webhooks** → Automation  
* **Vector DB (Pinecone / Weaviate)** → Semantic search (future AI features)

---

## **Final Summary**

LuxoraAI’s tech stack is designed to be:

* ⚡ **Fast** (React \+ FastAPI \+ SSE)  
* 🧠 **AI-first** (Gemma with strong prompt architecture)  
* 🔒 **Private** (local inference)  
* 📈 **Scalable** (cloud \+ queue in Phase 2\)
