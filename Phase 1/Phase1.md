# Phase 1 - AI Upstander

## Research and Planning

### Introduction
This document outlines the findings from the research and planning phase of the project aimed at enhancing the **Canadian Museum for Human Rights (CMHR) Upstander Program** through **AI-driven personalization**. The goal is to create a tailored, interactive experience that deepens users’ connection with human rights issues and empowers them to take action.

### Kick-off Meeting Feedback
**Key Takeaways:**
- Focus on MVP rather than an overly ambitious scope
- Prioritize a single critical feature for effectiveness
- AI should enhance engagement, not be added for novelty

**Incorporation into Project Phases:**
- Focused on a chatbot-based interactive journey
- Prioritized personalization & user engagement

### Initial Findings from CMHR Consultation and Web Content
- The **Upstander Program** inspires individuals, particularly youth, to recognize injustices, identify their strengths, and take action.
- AI should enhance the program by providing **tailored content** and guiding users through the **three core components** of the program.
- Users find the stories of upstanders (e.g., **Malala Yousafzai, Viola Desmond**) inspiring but desire a **more interactive experience**.
- **Personalization** based on interests and strengths would increase engagement.
- **In-gallery experiences** could be enriched with **location-specific information** and **interactive elements**.

## AI Techniques for Personalization

### **Natural Language Processing (NLP)**
- Used to create a **conversational AI chatbot** that guides users through the Upstander Program.
- **Example:** The chatbot asks users about their interests, personal strengths, and provides **personalized recommendations**.

### **Tools and Libraries**

#### Backend Implementation (Python)
- **Flask** - Micro web framework for building RESTful API endpoints.
- **Flask-CORS** - Extension for handling Cross-Origin Resource Sharing.
- **Pandas** - Data manipulation and analysis of CSV datasets.
- **Requests** - HTTP client for external API communication.
- **Python-dotenv** - Environment variable management.
- **Re** - Regular expressions for string processing *(Python standard library)*.
- **Random** - Random data generation *(Python standard library)*.
- **OS** - Operating system interaction *(Python standard library)*.

#### Frontend Implementation
- **Google Fonts** - `Montserrat` font for modern typography.
- **Animate.css** - Cross-browser CSS animations.

#### AI Service Integration
- **Hugging Face API** - Cloud-hosted inference endpoint for:
  - Model: `Mistral-7B-Instruct-v0.2` LLM.
  - *Requires API key for authentication*.

#### Data Formats
- **CSV** - Primary storage format for UAP location datasets.
- **JSON** - Standard format for API request/response payloads.

> **Note:** Items marked *(Python standard library)* require no additional installation.

## Data Review

### **Available Data Sources**
1. **Upstander Program Content** (Website)
   - Stories of notable upstanders (e.g., **Malala Yousafzai, Viola Desmond**).
   - Self-reflection activities and calls to action.
2. **Universal Access Points (UAPs)**
   - **250204_UAP Locations and Alignments.pdf** – Contains detailed information about UAP locations and alignments in the museum.

### **Key Findings**
- The **UAP data** will be utilized to provide **location-specific information** in the chatbot, enhancing the **in-gallery experience**.

## Scope
The goal is to develop a **Minimum Viable Product (MVP)** with the following core features:
- **AI-driven chatbot**.
- **Personalized recommendations**.
- **Integration with UAP locations**.

## Conclusion
The **research and planning phase** has provided a clear understanding of the project’s requirements and available resources. Although educational content from the museum’s education team is unavailable, the **Upstander Program content and UAP data** offer a strong foundation for the **AI-driven journey**. 

The next step is **Phase 2: Initial Development and Prototyping**, where the foundational features of the AI system will be built.
