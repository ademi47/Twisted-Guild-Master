import os
import json
from datetime import datetime, date
from openai import OpenAI
from models import get_db_session, AIUsage
from sqlalchemy import func

# AI Configuration
DAILY_USER_LIMIT = 25
DAILY_SERVER_LIMIT = 500
OPENAI_MODEL = "gpt-4o-mini"
MAX_INPUT_CHARS = 4000
MAX_OUTPUT_TOKENS = 600

class AIService:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = OpenAI(api_key=self.openai_api_key)
    
    def check_usage_limits(self, guild_id: int, user_id: int) -> tuple[bool, str]:
        """Check if user and server are within daily limits"""
        session = get_db_session()
        try:
            today = date.today().strftime('%Y-%m-%d')
            
            # Check user daily limit
            user_usage = session.query(func.count(AIUsage.id)).filter(
                AIUsage.user_id == user_id,
                AIUsage.date_only == today
            ).scalar() or 0
            
            if user_usage >= DAILY_USER_LIMIT:
                return False, f"You've reached your daily limit of {DAILY_USER_LIMIT} AI requests. Try again tomorrow!"
            
            # Check server daily limit
            server_usage = session.query(func.count(AIUsage.id)).filter(
                AIUsage.guild_id == guild_id,
                AIUsage.date_only == today
            ).scalar() or 0
            
            if server_usage >= DAILY_SERVER_LIMIT:
                return False, f"This server has reached its daily limit of {DAILY_SERVER_LIMIT} AI requests. Try again tomorrow!"
            
            return True, f"Usage: {user_usage}/{DAILY_USER_LIMIT} personal, {server_usage}/{DAILY_SERVER_LIMIT} server"
            
        except Exception as e:
            return False, f"Error checking usage limits: {str(e)}"
        finally:
            session.close()
    
    def trim_prompt(self, prompt: str) -> str:
        """Trim prompt to max character limit"""
        if len(prompt) <= MAX_INPUT_CHARS:
            return prompt
        
        trimmed = prompt[:MAX_INPUT_CHARS-50]  # Leave room for truncation message
        return f"{trimmed}... [Message trimmed to {MAX_INPUT_CHARS} characters]"
    
    def log_usage(self, guild_id: int, user_id: int, prompt_chars: int, output_tokens: int):
        """Log AI usage for tracking"""
        session = get_db_session()
        try:
            usage = AIUsage(
                guild_id=guild_id,
                user_id=user_id,
                prompt_chars=prompt_chars,
                output_tokens=output_tokens,
                model_used=OPENAI_MODEL,
                date_only=date.today().strftime('%Y-%m-%d')
            )
            session.add(usage)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error logging AI usage: {e}")
        finally:
            session.close()
    
    async def ask_ai(self, guild_id: int, user_id: int, prompt: str) -> tuple[bool, str]:
        """Process AI request with all safety checks"""
        try:
            # Check usage limits first
            can_use, limit_msg = self.check_usage_limits(guild_id, user_id)
            if not can_use:
                return False, limit_msg
            
            # Trim prompt if too long
            original_length = len(prompt)
            trimmed_prompt = self.trim_prompt(prompt)
            
            # Make OpenAI API call
            # the newest OpenAI model is "gpt-4o-mini" which is cost-effective for conversations
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant in a Discord server. Keep responses concise and friendly."
                    },
                    {"role": "user", "content": trimmed_prompt}
                ],
                max_tokens=MAX_OUTPUT_TOKENS,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            output_tokens = response.usage.completion_tokens
            
            # Log usage for tracking
            self.log_usage(guild_id, user_id, len(trimmed_prompt), output_tokens)
            
            # Add usage info to response
            usage_info = f"\n\n*{limit_msg}*"
            if original_length > MAX_INPUT_CHARS:
                usage_info += f"\n*Note: Your message was trimmed from {original_length} to {MAX_INPUT_CHARS} characters*"
            
            return True, answer + usage_info
            
        except Exception as e:
            error_msg = str(e)
            if "insufficient_quota" in error_msg:
                return False, "OpenAI API quota exceeded. Please check your API key billing."
            elif "invalid_api_key" in error_msg:
                return False, "Invalid OpenAI API key. Please check the configuration."
            else:
                return False, f"AI service error: {error_msg[:100]}..."

# Global AI service instance
ai_service = None

def get_ai_service():
    """Get or create AI service instance"""
    global ai_service
    if ai_service is None:
        try:
            ai_service = AIService()
        except ValueError as e:
            print(f"AI Service initialization failed: {e}")
            return None
    return ai_service