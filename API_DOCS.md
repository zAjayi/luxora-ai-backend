# LuxoraAI API Documentation

This document outlines all currently implemented endpoints in the LuxoraAI FastAPI backend.

## Repurpose

### POST `/api/v1/repurpose/stream`
**Summary:** Repurpose Content Stream

**Request Body:**
- Content-Type: `application/json`
  - Schema:
    - `source_text` (string)
    - `platforms` (array)
    - `tone` (any)
    - `brand_voice_description` (any)
    - `brand_voice_id` (any)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error

---

## Brand Voices

### GET `/api/v1/brand-voices/`
**Summary:** List Brand Voices

**Responses:**
- `200`: Successful Response

---

### POST `/api/v1/brand-voices/`
**Summary:** Create Brand Voice

**Request Body:**
- Content-Type: `application/json`
  - Schema:
    - `name` (string)
    - `description` (any)
    - `style_guide_text` (string)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error

---

### GET `/api/v1/brand-voices/{id}`
**Summary:** Get Brand Voice

**Parameters:**
- `id` (path, required=True)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error

---

## Jobs

### GET `/api/v1/jobs/`
**Summary:** Get Jobs

**Parameters:**
- `skip` (query, required=False)
- `limit` (query, required=False)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error

---

### GET `/api/v1/jobs/{id}`
**Summary:** Get Job

**Parameters:**
- `id` (path, required=True)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error

---

## Outputs

### POST `/api/v1/outputs/{id}/regenerate`
**Summary:** Regenerate Output

**Parameters:**
- `id` (path, required=True)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error

---

## Other

### GET `/`
**Summary:** Read Root

**Responses:**
- `200`: Successful Response

---

