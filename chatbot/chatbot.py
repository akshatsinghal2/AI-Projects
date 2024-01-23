import openai
import gradio

openai.api_key = " "

messages = [{"role": "system", "content": "You are a Psychologist"}]

def CustomChatGPT(user_input):
    # Check if the user input contains keywords related to psychology
    psychology_keywords = ["psychology", "therapist", "mental health", "counseling",
    "emotions", "therapy", "cognitive", "behavior", "depression",
    "anxiety", "stress", "trauma", "PTSD", "self-esteem", "well-being",
    "mindfulness", "psychiatry", "psychologist", "counselor", "diagnosis",
    "treatment", "therapy", "phobia", "addiction", "recovery",
    "personality", "disorder", "OCD", "Bipolar", "Schizophrenia",
    "suicide", "self-harm", "relationship", "family therapy",
    "group therapy", "child psychology", "adolescent psychology",
    "positive psychology", "abnormal psychology", "forensic psychology",
    "neuropsychology", "educational psychology", "social psychology",
    "industrial-organizational psychology", "sports psychology",
    "clinical psychology", "health psychology", "human behavior",
    "mental disorders", "psychotherapy", "cognitive-behavioral therapy",
    "talk therapy", "medication", "therapy session", "psychoanalysis",
    "mind-body connection", "subconscious", "consciousness",
    "self-awareness", "self-help", "therapy techniques",
    "mental health diagnosis", "mental health awareness",
    "positive thinking", "psychological research", "brain function",
    "neuroscience", "emotional intelligence", "stress management"]
    
    if any(keyword in user_input.lower() for keyword in psychology_keywords):
        # If the input is related to psychology, proceed with the conversation
        messages.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        return reply
    else:
        # If the input is not related to psychology, provide a specific message
        return "As an AI Psychologist, I can only give you information about the Psychological field."

demo = gradio.Interface(fn = CustomChatGPT, inputs = "text", outputs = "text", title = "AI Psychologist")

demo.launch()
