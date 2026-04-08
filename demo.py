import streamlit as st
import google.genai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv() 

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Biblioteca de Ideias - Exemplos para comparação
IDEA_LIBRARY = {
    "good_ideas": [
        {
            "name": "AI-powered resume optimizer",
            "keywords": ["ai", "resume", "job", "optimization", "career"],
            "score": 8.5,
            "pros": [
                "Massive target market (millions of job seekers)",
                "Clear monetization (B2C subscription or B2B licensing)",
                "Low infrastructure costs, high margins"
            ],
            "cons": [
                "Competition from LinkedIn and other platforms",
                "User acquisition can be expensive"
            ]
        },
        {
            "name": "Real-time team collaboration tool",
            "keywords": ["collaboration", "team", "real-time", "remote", "productivity"],
            "score": 7.8,
            "pros": [
                "Post-pandemic demand for remote work tools",
                "Easy to integrate with existing workflows",
                "Network effects increase with adoption"
            ],
            "cons": [
                "Dominated by Slack, Microsoft Teams, and Notion",
                "Customer retention depends on continuous innovation"
            ]
        },
        {
            "name": "Blockchain-based supply chain tracker",
            "keywords": ["blockchain", "supply", "chain", "tracking", "transparency"],
            "score": 7.5,
            "pros": [
                "Growing regulatory demand for transparency",
                "Enterprise clients willing to pay premium prices",
                "Addresses real pain point in logistics"
            ],
            "cons": [
                "Blockchain scalability challenges",
                "Long B2B sales cycles",
                "Technical complexity"
            ]
        },
        {
            "name": "Personalized AI fitness coach app",
            "keywords": ["fitness", "ai", "health", "personalization", "wellness"],
            "score": 7.2,
            "pros": [
                "Health & wellness is a multi-billion dollar market",
                "Recurring revenue from subscriptions",
                "Can leverage wearable data for personalization"
            ],
            "cons": [
                "Strong competition from Peloton, Apple Fitness",
                "Requires gym partnerships for monetization",
                "Churn rate typically high in fitness apps"
            ]
        }
    ],
    "bad_ideas": [
        {
            "name": "Another social media platform",
            "keywords": ["social", "media", "social network", "instagram clone"],
            "score": 3.2,
            "pros": [
                "Large addressable market"
            ],
            "cons": [
                "Network effects heavily favor incumbents",
                "Impossible to compete with Facebook, TikTok, Instagram",
                "User acquisition costs would be astronomical",
                "No clear differentiation or monetization path"
            ]
        },
        {
            "name": "Generic todo list app",
            "keywords": ["todo", "task", "list", "productivity", "notes"],
            "score": 2.8,
            "pros": [
                "Easy to build"
            ],
            "cons": [
                "Market saturated with Todoist, Microsoft To Do, Notion",
                "Very low barriers to entry = intense competition",
                "Users don't switch due to switching costs",
                "Difficult to differentiate on features alone"
            ]
        },
        {
            "name": "App that tells you weather",
            "keywords": ["weather", "app", "forecast"],
            "score": 2.1,
            "pros": [
                "Simple to understand"
            ],
            "cons": [
                "Everyone has a weather app already",
                "Weather data is commoditized and free",
                "No monetization path",
                "Impossible to build a defensible moat"
            ]
        }
    ]
}

def analyze_idea_similarity(user_idea, library_idea):
    """Calcula similaridade entre a ideia do usuário e uma ideia da biblioteca."""
    user_idea_lower = user_idea.lower()
    keywords = library_idea["keywords"]
    
    matches = sum(1 for keyword in keywords if keyword in user_idea_lower)
    similarity = matches / len(keywords) if keywords else 0
    return similarity

def generate_mock_evaluation(idea_input):
    """Gera uma avaliação simulada baseada em comparação com biblioteca de ideias."""
    # Encontra ideias similares na biblioteca
    all_ideas = IDEA_LIBRARY["good_ideas"] + IDEA_LIBRARY["bad_ideas"]
    similarities = [(idea, analyze_idea_similarity(idea_input, idea)) for idea in all_ideas]
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Pega as 2 ideias mais similares
    most_similar = similarities[0][0]
    similarity_score = similarities[0][1]
    second_similar = similarities[1][0] if len(similarities) > 1 else None
    
    # Base score na similaridade e na ideia mais próxima
    base_score = most_similar["score"]
    
    # Ajusta score com base em palavras-chave
    user_idea_lower = idea_input.lower()
    bonus_keywords = {
        "ai": 0.5, "machine learning": 0.5, "blockchain": 0.3,
        "sustainable": 0.3, "eco": 0.2, "renewable": 0.3,
        "saas": 0.4, "subscription": 0.3, "recurring": 0.2
    }
    
    bonus = sum(bonus for keyword, bonus in bonus_keywords.items() if keyword in user_idea_lower)
    final_score = min(9.5, base_score + bonus)
    
    # Determina tom baseado no score mais similar
    if most_similar["score"] >= 7:
        tone = "promising"
        summary_intro = "This is a **promising startup concept** with solid market potential."
    elif most_similar["score"] >= 5:
        tone = "moderate"
        summary_intro = "This idea has **moderate potential**, but faces some significant challenges."
    else:
        tone = "challenging"
        summary_intro = "This idea faces **significant challenges** and may struggle in the market."
    
    # Combina pros e cons de ideias similares
    pros = list(set(most_similar["pros"][:2]))
    if second_similar and second_similar["score"] >= 6:
        pros.extend(second_similar["pros"][:1])
    
    cons = list(set(most_similar["cons"][:2]))
    if second_similar:
        cons.extend(second_similar["cons"][:1])
    
    pros_text = "\n".join([f"- {pro}" for pro in pros[:3]])
    cons_text = "\n".join([f"- {con}" for con in cons[:3]])
    
    # Gera justificativa baseada na comparação
    comparison_msg = f"Similar to *{most_similar['name']}* (Score: {most_similar['score']}/10)"
    if similarity_score < 0.3:
        comparison_msg += " - but with some unique aspects"
    
    evaluation = f"""### Summary
{summary_intro} Your concept shares characteristics with successful market examples. Focus on execution quality and customer validation to succeed.

**Comparison:** {comparison_msg}

### Pros & Cons

**Pros:**
{pros_text}

**Cons:**
{cons_text}

### IdeaScore: {final_score:.1f}/10
Based on market analysis and comparison with similar ideas, this concept shows {'strong' if final_score >= 7 else 'moderate' if final_score >= 5 else 'limited'} viability. Success will depend heavily on execution, team quality, and market timing."""
    
    return evaluation

st.set_page_config(page_title="IdeaEvaluator", layout="wide")

# Title and header
st.title("IdeaEvaluator — AI Startup Idea Checker")
st.markdown("---")

# Layout: Tabs para separar a funcionalidade principal das explicações
tab_evaluate, tab_about = st.tabs(["💡 Evaluate Your Idea", "📖 About the Project"])

with tab_about:
    st.header("About IdeaEvaluator")
    left, right = st.columns([1, 1])
    
    with left:
        st.subheader("Why use IdeaEvaluator?")
        st.markdown(
            "- It gives data-backed (via AI) insights into the potential of an early-stage startup idea, even before any product is built.\n"
            "- It offers an **IdeaScore**, an arbitrary but indicative score out of 10 based on AI heuristics.\n"
            "- It quickly highlights the main **Pros** and **Cons** of your concept to help you pivot or validate.\n"
        )

    with right:
        st.subheader("What is the IdeaScore?")
        st.markdown(
            "The **IdeaScore** is a heuristic metric (1 to 10) generated by the AI model analyzing various factors such as:\n"
            "- **Potential market demand:** Is there a clear problem being solved?\n"
            "- **Level of competition:** Is the market too saturated?\n"
            "- **Overall viability:** Does the solution make technical and business sense?\n\n"
            "*Note: This score is a simulated evaluation generated by an LLM and should be used as a starting point for real-world validation, not as a definitive proof of success.*"
        )

with tab_evaluate:
    st.header("Submit and Evaluate")
    st.write(
        "Enter your startup idea below. Our AI will analyze your concept, outline its strengths and weaknesses, "
        "and provide an **IdeaScore** to help you gauge its potential."
    )

    idea_input = st.text_area(
        "Describe your idea (one or two sentences)", 
        height=120, 
        placeholder="e.g., An AI tool that predicts startup success using public data and provides an IdeaScore."
    )

    if st.button("Evaluate Idea", type="primary"):
        if not idea_input.strip():
            st.warning("Please enter an idea to evaluate.")
        elif GEMINI_API_KEY is None:
            st.error("Please configure your Google Gemini API key via environment variable (GEMINI_API_KEY) to run the evaluation.")
        else:
            with st.spinner("Analyzing your idea... This may take a few seconds."):
                try:
                    client = genai.Client(api_key=GEMINI_API_KEY)
                    
                    prompt = (
                        f"You are an expert startup advisor and experienced venture capitalist. "
                        f"Evaluate the following startup idea: '{idea_input}'.\n\n"
                        "Please provide your evaluation structured EXACTLY as follows:\n\n"
                        "### Summary\n"
                        "(Provide a brief summary of whether it is a good idea or a bad idea and why)\n\n"
                        "### Pros & Cons\n"
                        "(List 2-3 bullet points for Pros, and 2-3 bullet points for Cons)\n\n"
                        "### IdeaScore: [Score]/10\n"
                        "(Give an arbitrary score out of 10 based on market viability, followed by a 1-sentence justification for the score.)"
                    )
                    
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=prompt,
                    )
                    
                    evaluation = response.text
                    
                    st.markdown("---")
                    st.subheader("📊 Evaluation Results")
                    
                    with st.container():
                        st.markdown(evaluation)
                        
                    st.success("Analysis complete!")
                    st.info("💡 **Next Steps:** Use these insights to validate your idea with real users. Remember, the IdeaScore is just a guide, execution is what matters!")
                    
                except Exception as e:
                    error_str = str(e)
                    
                    # Exceded quota handling
                    if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                        st.warning(
                            "⚠️ **API Quota Exceeded** - Your free tier quota has been reached. "
                            "Please upgrade your plan or try again later. "
                            "For now, showing a sample evaluation:"
                        )
                        
                        # Fallback
                        mock_evaluation = generate_mock_evaluation(idea_input)
                        
                        st.markdown("---")
                        st.subheader("📊 Sample Evaluation Results")
                        st.info("💡 **This is a simulated example** - To get real AI-powered insights, please upgrade your Gemini API plan.")
                        
                        with st.container():
                            st.markdown(mock_evaluation)
                    else:
                        st.error(f"An error occurred while connecting to the Google Gemini API: {e}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.9em;'>"
    "🔗 <a href='https://github.com/felipebns/demo_project_babson' target='_blank'>View on GitHub</a>"
    "</div>",
    unsafe_allow_html=True
)

