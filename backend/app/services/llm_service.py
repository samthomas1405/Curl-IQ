"""
LLM Service for AI-Powered Insights
Uses Groq API (free, fast) to generate natural language explanations of patterns and insights
Also supports OpenAI and Anthropic as fallbacks
"""
import os
from typing import Dict, List, Optional
import httpx
from app.core.config import settings


class LLMInsightService:
    """Service for generating AI-powered insights using LLMs"""
    
    def __init__(self):
        # Prioritize Groq (free and fast), then OpenAI, then Anthropic
        self.api_key = (
            os.getenv("GROQ_API_KEY") or 
            os.getenv("OPENAI_API_KEY") or 
            os.getenv("ANTHROPIC_API_KEY")
        )
        self.provider = (
            "groq" if os.getenv("GROQ_API_KEY") else
            "openai" if os.getenv("OPENAI_API_KEY") else
            "anthropic" if os.getenv("ANTHROPIC_API_KEY") else None
        )
    
    def generate_insight_explanation(self, insight_data: Dict) -> Optional[str]:
        """
        Generate natural language explanation of an insight
        
        Args:
            insight_data: Dictionary with insight information
        
        Returns:
            Natural language explanation or None if API unavailable
        """
        if not self.api_key:
            return None
        
        try:
            if self.provider == "groq":
                return self._generate_groq_insight(insight_data)
            elif self.provider == "openai":
                return self._generate_openai_insight(insight_data)
            elif self.provider == "anthropic":
                return self._generate_anthropic_insight(insight_data)
        except Exception as e:
            print(f"Error generating LLM insight: {e}")
            return None
    
    def _generate_groq_insight(self, insight_data: Dict) -> str:
        """Generate insight using Groq API (free and fast)"""
        prompt = self._build_insight_prompt(insight_data)
        
        response = httpx.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",  # Fast, free model
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful hair care assistant that explains data-driven insights about curly hair routines. Be concise, friendly, and data-driven."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 200,
                "temperature": 0.7
            },
            timeout=10.0
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        return None
    
    def _generate_openai_insight(self, insight_data: Dict) -> str:
        """Generate insight using OpenAI API"""
        prompt = self._build_insight_prompt(insight_data)
        
        response = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful hair care assistant that explains data-driven insights about curly hair routines. Be concise, friendly, and data-driven."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 200,
                "temperature": 0.7
            },
            timeout=10.0
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        return None
    
    def _generate_anthropic_insight(self, insight_data: Dict) -> str:
        """Generate insight using Anthropic API"""
        prompt = self._build_insight_prompt(insight_data)
        
        response = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            },
            json={
                "model": "claude-3-haiku-20240307",
                "max_tokens": 200,
                "messages": [
                    {
                        "role": "user",
                        "content": f"You are a helpful hair care assistant. {prompt}"
                    }
                ]
            },
            timeout=10.0
        )
        
        if response.status_code == 200:
            return response.json()["content"][0]["text"].strip()
        return None
    
    def _build_insight_prompt(self, insight_data: Dict) -> str:
        """Build prompt for insight generation"""
        insight_type = insight_data.get("type", "pattern")
        message = insight_data.get("message", "")
        confidence = insight_data.get("confidence", "medium")
        sample_size = insight_data.get("sample_size", 0)
        
        prompt = f"""Based on this data insight, provide a friendly, concise explanation:

Insight Type: {insight_type}
Finding: {message}
Confidence: {confidence}
Sample Size: {sample_size} data points

Explain what this means for the user's hair care routine in 2-3 sentences. Be encouraging and actionable."""
        
        return prompt
    
    def generate_routine_suggestion(self, user_profile: Dict, context: Dict) -> Optional[str]:
        """
        Generate AI-powered routine suggestion
        
        Args:
            user_profile: User's hair profile
            context: Context about their goals/current routine
        
        Returns:
            Suggestion text or None
        """
        if not self.api_key:
            return None
        
        try:
            prompt = f"""Based on this hair profile, suggest a routine improvement:

Hair Type: {user_profile.get('curl_pattern', 'unknown')}
Porosity: {user_profile.get('porosity', 'unknown')}
Current Challenge: {context.get('challenge', 'general maintenance')}
Goal: {context.get('goal', 'better definition and less frizz')}

Provide a brief, actionable suggestion for their routine (2-3 sentences)."""
            
            if self.provider == "groq":
                response = httpx.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-8b-instant",
                        "messages": [
                            {"role": "system", "content": "You are a curly hair care expert."},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": 150,
                        "temperature": 0.8
                    },
                    timeout=10.0
                )
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"].strip()
            elif self.provider == "openai":
                response = httpx.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {"role": "system", "content": "You are a curly hair care expert."},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": 150,
                        "temperature": 0.8
                    },
                    timeout=10.0
                )
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Error generating suggestion: {e}")
        
        return None


# Singleton instance
llm_service = LLMInsightService()
