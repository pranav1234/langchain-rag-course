"""
Prompt Chains for Generation and Reflection

This module defines the LLM chains for:
1. Generating initial content
2. Reflecting on and critiquing content
3. Refining content based on feedback
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.7)


# Generation Prompt
GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert content creator. Your task is to create high-quality, 
engaging content based on the user's request.

Guidelines:
- Be concise and impactful
- Use appropriate tone and style
- Include relevant emojis when appropriate
- Make it engaging and shareable

If you receive feedback, incorporate it to improve the content."""),
    ("user", "{input}")
])

# Refinement Prompt (when we have reflection feedback)
REFINEMENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert content creator. You previously created this content:

{draft}

You received this feedback:

{reflection}

Your task is to refine the content based on the feedback. Address all the points raised
while maintaining the core message."""),
    ("user", "Please create an improved version.")
])

# Reflection Prompt
REFLECTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert content critic. Your task is to provide constructive,
specific feedback on the given content.

Evaluate the content based on:
1. Clarity - Is the message clear and easy to understand?
2. Impact - Is it engaging and memorable?
3. Tone - Is the tone appropriate for the audience?
4. Structure - Is it well-organized?
5. Completeness - Does it cover all necessary points?

Provide specific, actionable feedback. Be constructive but honest."""),
    ("user", "Please critique this content:\n\n{draft}")
])


# Create chains
generation_chain = GENERATION_PROMPT | llm
refinement_chain = REFINEMENT_PROMPT | llm
reflection_chain = REFLECTION_PROMPT | llm


def generate_content(input_text: str) -> str:
    """
    Generate initial content based on user input.
    
    Args:
        input_text: User's content request
        
    Returns:
        Generated content
    """
    result = generation_chain.invoke({"input": input_text})
    return result.content


def refine_content(draft: str, reflection: str) -> str:
    """
    Refine content based on reflection feedback.
    
    Args:
        draft: Current draft
        reflection: Critique/feedback
        
    Returns:
        Refined content
    """
    result = refinement_chain.invoke({
        "draft": draft,
        "reflection": reflection
    })
    return result.content


def reflect_on_content(draft: str) -> str:
    """
    Provide critique and feedback on content.
    
    Args:
        draft: Content to critique
        
    Returns:
        Reflection/critique
    """
    result = reflection_chain.invoke({"draft": draft})
    return result.content


if __name__ == "__main__":
    """Demo: Test the chains"""
    print("=" * 70)
    print("Chains Demo")
    print("=" * 70 + "\n")
    
    # Test generation
    print("1. GENERATION")
    print("-" * 70)
    input_text = "Make this tweet better: LangChain is cool"
    draft = generate_content(input_text)
    print(f"Input: {input_text}")
    print(f"Generated: {draft}\n")
    
    # Test reflection
    print("2. REFLECTION")
    print("-" * 70)
    reflection = reflect_on_content(draft)
    print(f"Reflection: {reflection}\n")
    
    # Test refinement
    print("3. REFINEMENT")
    print("-" * 70)
    refined = refine_content(draft, reflection)
    print(f"Refined: {refined}\n")
