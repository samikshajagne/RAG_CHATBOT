# 🏦 Banking Chatbot 

<img width="950" height="902" alt="image" src="https://github.com/user-attachments/assets/1e373e80-c8d7-4bd0-a067-47f2bf015fa5" />


> An intelligent banking chatbot built using **Sentence Transformers** for semantic retrieval and a **Large Language Model (LLM)** for natural answer generation.

---

## Overview

This project implements a simple **RAG (Retrieval-Augmented Generation)** pipeline that:
1. Converts banking Q&A data into **semantic embeddings**
2. Finds the most **relevant context** for any user query using cosine similarity
3. Passes the context to an **LLM** to generate a fluent, accurate answer

--

## Tech Stack

| Component        | Technology                          |
|-----------------|-------------------------------------|
| Embeddings       | `sentence-transformers` (all-MiniLM-L6-v2) |
| Retrieval        | Cosine Similarity (NumPy)           |
| LLM Backend      | Groq API (LLaMA 3) / OpenAI GPT-3.5 |
| Interface        | Command-Line (CLI)                  |
| Dataset Format   | JSON                                |

---

## Project Structure

```
banking-chatbot/
├── banking_qa.json      # 10 banking Q&A entries
├── chatbot.py               # Core chatbot logic (RAG pipeline)
├── app.py                   # Streamlit Web UI  ←  NEW
├── main.py                  # CLI entry point
├── requirements.txt
└── README.md
```

---

##  Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/your-username/banking-chatbot.git
cd banking-chatbot
pip install -r requirements.txt
```

### 2. Set Your API Key

**Option A — Groq (Free, Recommended):**
Get a free key at [console.groq.com](https://console.groq.com)
```bash
export GROQ_API_KEY=""
export LLM_BACKEND=groq
```

**Option B — OpenAI:**
```bash
export OPENAI_API_KEY="your_openai_api_key"
export LLM_BACKEND=openai
```

**Option C — No API Key (Fallback):**
```bash
export LLM_BACKEND=fallback
```

### 3. Run the Chatbot

**Option A — Streamlit Web UI (Recommended):**
```bash
streamlit run app.py
```
Opens automatically at [http://localhost:8501](http://localhost:8501)

**Option B — Command-Line Interface:**
```bash
python main.py
```

---

## Sample Interaction

```
 You: What is KYC?
Bot: KYC stands for Know Your Customer. It is a mandatory process used
        by banks to verify the identity of clients, helping prevent fraud
        and money laundering. It typically requires a government-issued ID,
        proof of address, and a recent photograph.

 You: How does UPI work?
 Bot: UPI (Unified Payments Interface) enables instant bank-to-bank
        transfers via smartphone. You link your bank account to a UPI app
        (like Google Pay or PhonePe), set a UPI PIN, and can then send or
        receive money 24x7 using a UPI ID or QR code.
```

---

## How It Works

```
User Query
    │
    ▼
[Sentence Transformer]  →  Query Embedding (384-dim vector)
    │
    ▼
[Cosine Similarity]     →  Match against 10 pre-embedded Q&A entries
    │
    ▼
[Top Match Retrieved]   →  Relevant context passed to LLM
    │
    ▼
[LLM (Groq/OpenAI)]     →  Natural language answer generated
    │
    ▼
Final Answer displayed in CLI
```

---

## Dataset

The dataset (`data/banking_qa.json`) contains **10 banking Q&A entries** covering:
- KYC, Savings Account, FD, Home Loans
- NEFT, UPI, Credit Score
- Debit vs Credit Cards, Banking Fraud Prevention
- Account Opening Documents

---

