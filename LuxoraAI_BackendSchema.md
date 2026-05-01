# **LuxoraAI — Backend Schema Document (v1.0)**

---

## **1\. Overview**

The LuxoraAI backend schema is designed to support:

* AI-powered content repurposing workflows  
* Multi-platform output generation  
* Scalable SaaS evolution (Phase 2\)  
* Efficient querying for history, search, and analytics

---

## **2\. Database Technology**

* **Database:** PostgreSQL 16  
* **ORM:** SQLAlchemy 2.0 (async)  
* **Migrations:** Alembic

---

## **3\. Core Design Principles**

### **3.1 Normalization with Practical Flexibility**

* Structured relational schema  
* Optional JSON fields for flexible metadata

---

### **3.2 Job-Centric Architecture**

Everything revolves around a **Repurpose Job**

User → Repurpose Job → Outputs  
---

### **3.3 Scalability for Phase 2**

* Multi-user support  
* Billing integration  
* Search & filtering

---

## **4\. Entity Relationship Overview**

users  
 ├── repurpose\_jobs  
 │       └── repurposed\_outputs  
 ├── brand\_voices  
 └── subscriptions  
---

## **5\. Core Tables**

---

## **5.1 Users Table**

### **Purpose:**

Stores user account information (Phase 2\)

---

### **Schema:**

users (  
 id UUID PRIMARY KEY,  
 email VARCHAR(255) UNIQUE NOT NULL,  
 hashed\_password TEXT,  
 name VARCHAR(255),  
 brand\_name VARCHAR(255),

 plan VARCHAR(50) DEFAULT 'free', \-- free | pro  
 is\_active BOOLEAN DEFAULT TRUE,

 created\_at TIMESTAMP DEFAULT NOW(),  
 updated\_at TIMESTAMP DEFAULT NOW()  
)  
---

### **Notes:**

* `hashed_password` nullable (for OAuth users)  
* `plan` drives usage limits

---

## **5.2 Repurpose Jobs Table**

### **Purpose:**

Represents a single content transformation request

---

### **Schema:**

repurpose\_jobs (  
 id UUID PRIMARY KEY,  
 user\_id UUID REFERENCES users(id) ON DELETE CASCADE,

 source\_text TEXT,  
 source\_url TEXT,  
 source\_type VARCHAR(50), \-- text | url | file | transcript

 tone VARCHAR(50),  
 platforms TEXT\[\], \-- \['twitter', 'linkedin', ...\]

 cta TEXT,  
 include\_hashtags BOOLEAN DEFAULT TRUE,  
 include\_emojis BOOLEAN DEFAULT TRUE,

 status VARCHAR(50) DEFAULT 'pending', \-- pending | processing | completed | failed

 created\_at TIMESTAMP DEFAULT NOW(),  
 updated\_at TIMESTAMP DEFAULT NOW()  
)  
---

### **Notes:**

* `platforms` stored as array for flexibility  
* `status` supports async processing (Phase 2\)

---

## **5.3 Repurposed Outputs Table**

### **Purpose:**

Stores AI-generated outputs per platform and variant

---

### **Schema:**

repurposed\_outputs (  
 id UUID PRIMARY KEY,  
 job\_id UUID REFERENCES repurpose\_jobs(id) ON DELETE CASCADE,

 platform VARCHAR(50), \-- twitter, linkedin, etc.  
 variant\_index INTEGER, \-- 1, 2, 3

 content TEXT NOT NULL,

 is\_favourite BOOLEAN DEFAULT FALSE,

 created\_at TIMESTAMP DEFAULT NOW(),  
 updated\_at TIMESTAMP DEFAULT NOW()  
)  
---

### **Notes:**

* One job → multiple outputs  
* Supports regeneration per output

---

## **5.4 Brand Voices Table**

### **Purpose:**

Stores reusable writing styles

---

### **Schema:**

brand\_voices (  
 id UUID PRIMARY KEY,  
 user\_id UUID REFERENCES users(id) ON DELETE CASCADE,

 name VARCHAR(255),  
 description TEXT,  
 style\_guide\_text TEXT,

 created\_at TIMESTAMP DEFAULT NOW(),  
 updated\_at TIMESTAMP DEFAULT NOW()  
)  
---

### **Notes:**

* Injected into AI prompt  
* Can be selected per job

---

## **5.5 Subscriptions Table (Phase 2\)**

### **Purpose:**

Tracks billing and subscription status

---

### **Schema:**

subscriptions (  
 id UUID PRIMARY KEY,  
 user\_id UUID REFERENCES users(id) ON DELETE CASCADE,

 stripe\_customer\_id TEXT,  
 stripe\_subscription\_id TEXT,

 plan VARCHAR(50), \-- free | pro  
 status VARCHAR(50), \-- active | canceled | past\_due

 current\_period\_start TIMESTAMP,  
 current\_period\_end TIMESTAMP,

 created\_at TIMESTAMP DEFAULT NOW(),  
 updated\_at TIMESTAMP DEFAULT NOW()  
)  
---

### **Notes:**

* Stripe is source of truth  
* This table mirrors subscription state

---

## **6\. Supporting Tables (Optional / Future)**

---

## **6.1 Usage Tracking Table**

usage\_logs (  
 id UUID PRIMARY KEY,  
 user\_id UUID REFERENCES users(id),

 job\_id UUID REFERENCES repurpose\_jobs(id),

 action VARCHAR(50), \-- create\_job, regenerate, export

 created\_at TIMESTAMP DEFAULT NOW()  
)  
---

---

## **6.2 File Uploads Table (Phase 2\)**

uploads (  
 id UUID PRIMARY KEY,  
 user\_id UUID REFERENCES users(id),

 file\_url TEXT,  
 file\_type VARCHAR(50),

 created\_at TIMESTAMP DEFAULT NOW()  
)  
---

## **7\. Indexing Strategy**

---

### **Critical Indexes:**

\-- Jobs per user  
CREATE INDEX idx\_jobs\_user\_id ON repurpose\_jobs(user\_id);

\-- Outputs per job  
CREATE INDEX idx\_outputs\_job\_id ON repurposed\_outputs(job\_id);

\-- Search optimization  
CREATE INDEX idx\_jobs\_created\_at ON repurpose\_jobs(created\_at);

\-- Platform filtering  
CREATE INDEX idx\_outputs\_platform ON repurposed\_outputs(platform);  
---

### **Full-Text Search (PostgreSQL)**

ALTER TABLE repurpose\_jobs  
ADD COLUMN search\_vector tsvector;

CREATE INDEX idx\_search ON repurpose\_jobs USING GIN(search\_vector);  
---

## **8\. Data Relationships**

---

### **8.1 One-to-Many**

* User → Repurpose Jobs  
* Repurpose Job → Outputs  
* User → Brand Voices

---

### **8.2 One-to-One**

* User → Subscription

---

## **9\. Data Flow Mapping**

---

## **9.1 Job Creation Flow**

User submits content  
  ↓  
Create repurpose\_job  
  ↓  
AI generates outputs  
  ↓  
Insert repurposed\_outputs  
---

## **9.2 Output Regeneration**

User selects output  
  ↓  
AI generates new variant  
  ↓  
Update repurposed\_outputs  
---

## **10\. Constraints & Validation**

---

### **Enforced at DB Level:**

* Foreign key constraints  
* NOT NULL (critical fields)  
* Unique email (users)

---

### **Enforced at App Level:**

* Platform validation  
* Tone validation  
* Usage limits

---

## **11\. Soft vs Hard Deletes**

---

### **Strategy:**

* Use **hard deletes** for:  
  * Jobs  
  * Outputs  
* Optional future:  
  * Add `deleted_at` for soft delete

---

## **12\. Performance Considerations**

---

### **Key Optimizations:**

* Index frequently queried fields  
* Limit output payload size  
* Paginate job history

---

### **Query Patterns:**

* Fetch jobs with outputs (JOIN)  
* Filter by:  
  * Date  
  * Platform  
  * Tone

---

## **13\. Security Considerations**

---

* Use UUIDs (not incremental IDs)  
* Prevent SQL injection via ORM  
* Encrypt sensitive data (if added later)

---

## **14\. Schema Evolution Strategy**

---

### **Phase 1:**

* Minimal schema  
* Single-user

---

### **Phase 2:**

* Add:  
  * Users  
  * Subscriptions  
  * Usage tracking

---

### **Migration Tool:**

* Alembic

---

## **15\. Example SQLAlchemy Models (Simplified)**

class RepurposeJob(Base):  
   \_\_tablename\_\_ \= "repurpose\_jobs"

   id \= Column(UUID, primary\_key=True)  
   user\_id \= Column(UUID, ForeignKey("users.id"))

   source\_text \= Column(Text)  
   tone \= Column(String)  
   platforms \= Column(ARRAY(String))

   status \= Column(String, default="pending")  
---

## **16\. Future Enhancements**

* Vector embeddings table (semantic search)  
* Analytics tables (engagement tracking)  
* Team collaboration tables

---

## **Final Summary**

The LuxoraAI backend schema is:

* 🧱 **Structured** → clean relational design  
* ⚡ **Efficient** → optimized for fast queries  
* 📈 **Scalable** → ready for SaaS expansion  
* 🧠 **AI-ready** → built around content generation workflows