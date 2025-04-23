# Chatbot Testing Demonstration & Analysis

This document outlines test cases designed to evaluate the chatbot's performance in key areas, including knowledge accuracy, conversational handling, rule adherence, and user engagement within the **"Upstander"** learning module.

---

## Test Case 1: Core Knowledge & Definition

**Objective:**  
To assess the chatbot's ability to provide an accurate, clear, and appropriately toned definition of a core concept ("upstander").

**User Input:**  
“What is an upstander?”

**Chatbot Response:**  
An upstander is someone who recognizes when something is wrong and acts to make it right. Unlike a bystander, who might witness injustice without intervening, an upstander takes action. Upstanders can:

- **Speak out**: They voice their concerns and challenge unfair behavior.  
- **Support others**: They offer help and comfort to those who are being mistreated.  
- **Educate**: They inform others about injustice and how to prevent it.  
- **Intervene**: They safely step in to stop harmful actions.  
Would you like to learn more about upstanders, or perhaps about the Canadian Human Rights Museum?

**Evaluation:**
- **Accuracy & Completeness**: Clear, correct definition with effective contrast to "bystander" and actionable examples.  
- **Clarity**: Accessible language and improved readability through bullet points.  
- **Tone**: Informative and encouraging, aligned with Upstander program goals.  
- **Relevance & Engagement**: On-topic with a prompt for further learning (though the museum mention may benefit from better contextual framing).

---

## Test Case 2: Off-Topic Response Handling

**Objective:**  
To evaluate the chatbot's adherence to predefined rules for managing off-topic user input and redirecting the conversation gently.

**Rules Tested:**
- Stay focused on the current stage's objectives.  
- Acknowledge user responses in the context of the stage.  
- Gently guide back if the user goes off-topic.  
- Only progress stages when stage objectives are met.

**User Input:**  
“I wanna skydive”

**Chatbot Response:**  
Skydiving sounds like an amazing experience! However, this learning journey is about becoming an upstander. Let's get back on track. Upstanders are people who stand up for others and for what is right, even when it's difficult. Would you like to learn more about what it means to be an upstander, explore the Human Rights Museum, or something else?

**Evaluation:**
- Successfully acknowledges and redirects off-topic input.
- Maintains focus and does not advance prematurely.
- Balances politeness with educational intent.

---

## Test Case 3: Empathetic Response & Stage Progression

**Objective:**  
To assess the chatbot's ability to handle user-shared experiences relevant to the topic, respond empathetically, and manage progression within the learning flow.

**User Input:**  
“I will notice my friend are sad and when they are depressed ill talk and actively listen to them”

**Chatbot Response:**  
That's a wonderful example of empathy in action! Noticing when your friends are down and offering a listening ear is a great way to support them. It shows you care and creates a safe space for them to share their feelings. Now that you've described one of your strengths as a potential upstander in detail, let's move on to the next step. Click the "Next" button at the top right to continue your learning journey!

**Evaluation:**
- **Tone & Empathy**: Warm and affirming, validates user's actions.  
- **Relevance**: Ties the user’s story directly to upstander traits.  
- **Engagement & Progression**: Guides user smoothly to the next stage after reflecting back input.

---

## Test Case 4: Input Robustness & Information Retrieval

**Objective:**  
To evaluate the chatbot's ability to handle potentially ambiguous or misspelled input, retrieve relevant information, and present it clearly.

**User Input:**  
“crag” (Intended: Craig Kielburger)

**Chatbot Response:**  
I see you're interested in learning more about Craig Kielburger. He's a great example of an upstander!

**Craig Kielburger:**

- **Story**: At age 12, Craig was moved by the story of a child laborer who was murdered for speaking out. He founded *Free The Children* (now *WE Charity*) to fight child labor and promote education.  
- **Impact**: His empathy for other children's suffering led to a global movement empowering youth to make positive social change.

Craig demonstrated empathy by understanding and sharing the feelings of the child laborer. His actions show how recognizing the suffering of others can inspire someone to stand up and create positive change. Would you like to learn about upstanders who demonstrated: **courage**, **empathy**, or **persistence**? Or, are you ready to move on to the next section?

**Evaluation:**
- **Robustness**: Interpreted "crag" as "Craig" correctly.  
- **Clarity & Structure**: Clean formatting, bolded headings, concise bullets.  
- **Relevance & Tone**: Content is well-matched to user intent and topic.  
- **Engagement**: Offers options for exploration or progression.

---

## Summary

This testing highlights the chatbot's:

- Strong grasp of core concepts.
- Ability to maintain focus and handle unexpected input gracefully.
- Empathetic engagement with users.
- Structured delivery of information.
- Support for flexible, user-driven learning paths.

