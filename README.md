# IdeaEvaluator

## 1. Project summary
IdeaEvaluator is a lightweight, interactive web application built with Streamlit that allows users to submit their early-stage startup ideas and receive instant, AI-driven feedback. The tool leverages OpenAI's language models to assess the viability of the idea, providing a brief summary of its pros and cons (whether it's a good or bad idea) and assigning an arbitrary qualitative score out of 10.

## 2. Codebase/Architecture discussion
The codebase is currently a single-file Streamlit application (`demo.py`). 
- **Frontend/UI:** Handled entirely by Streamlit, featuring a tabbed layout to separate the tool ("Evaluate Your Idea") from project documentation and context ("About the Project").
- **Backend/Logic:** There is no complex backend server yet. The application runs synchronously, capturing user input and making an HTTP request to the OpenAI API using the official `openai` Python client.
- **Future Architecture (Custom LLM & Idea Library):** We plan to evolve this architecture by implementing an "idea library"—a database of historically proven good and bad startup ideas. The system will use a customized LLM approach to pull opinions and context directly from this library. By referencing these real-world examples, the AI's evaluations and scoring will become much more precise and grounded.

## 3. Demo of current UI and functionality
The current UI is structured into two main tabs:
- **About the Project:** Explains the purpose of the IdeaScore, personal doubts/hypotheses about the product, and details the factors the AI considers (demand, competition, viability).
- **Evaluate Your Idea:** Provides a text box where users can type their idea. Upon clicking "Evaluate Idea", a loading spinner appears, and the app connects to the OpenAI API.
- **Results Display:** The AI returns structured markdown containing a **Summary**, **Pros & Cons**, and the final **IdeaScore (out of 10)** with a brief justification.

## 4. Discussion of remaining tasks for final demonstration.
To prepare for a final, production-ready demonstration, the following tasks remain:
- **Implement the "Idea Library":** Curate a robust database of good and bad startup ideas. We will connect the custom LLM to this library so it can draw comparisons and base its feedback on this specific dataset, significantly increasing the accuracy of the IdeaScore.
- **Error Handling & Rate Limiting:** Improve the resiliency of the app by gracefully handling potential OpenAI API limits (e.g., HTTP 429).
- **Prompt Engineering Refinement:** Fine-tune the system and user prompts to seamlessly integrate data from the new idea library.
