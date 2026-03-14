import os
import uuid
from datetime import datetime
from supabase import create_client, Client
from typing import Optional, Dict, List

class DatabaseService:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        # Strip any whitespace that might cause issues
        url = url.strip()
        key = key.strip()
        
        self.supabase: Client = create_client(url, key)
    
    def create_user(self, email: str, password_hash: str, full_name: str, 
                   age: int, gender: str, height_cm: Optional[float] = None, 
                   weight_kg: Optional[float] = None) -> Dict:
        """Create a new user in the database"""
        user_data = {
            "user_id": str(uuid.uuid4()),
            "email": email,
            "full_name": full_name,
            "password_hash": password_hash,
            "age": age,
            "gender": gender,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "created_at": datetime.now().isoformat()
        }
        
        result = self.supabase.table("users").insert(user_data).execute()
        return result.data[0] if result.data else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        result = self.supabase.table("users").select("*").eq("email", email).execute()
        return result.data[0] if result.data else None
    
    def update_user_measurements(self, user_id: str, height_cm: Optional[float] = None, 
                               weight_kg: Optional[float] = None) -> bool:
        """Update user's height and weight"""
        update_data = {}
        if height_cm is not None:
            update_data["height_cm"] = height_cm
        if weight_kg is not None:
            update_data["weight_kg"] = weight_kg
        
        if update_data:
            result = self.supabase.table("users").update(update_data).eq("user_id", user_id).execute()
            return len(result.data) > 0
        return False
    
    def create_test_session(self, user_id: str) -> str:
        """Create a new test session"""
        session_data = {
            "session_id": str(uuid.uuid4()),
            "user_id": user_id,
            "session_date": datetime.now().date().isoformat(),
            "created_at": datetime.now().isoformat()
        }
        
        result = self.supabase.table("test_sessions").insert(session_data).execute()
        return result.data[0]["session_id"] if result.data else None
    
    def save_test_result(self, session_id: str, test_type: str, value_1: float, 
                        value_2: Optional[float] = None, status: str = "normal") -> bool:
        """Save a test result"""
        result_data = {
            "result_id": str(uuid.uuid4()),
            "session_id": session_id,
            "test_type": test_type,
            "value_1": value_1,
            "value_2": value_2,
            "status": status,
            "created_at": datetime.now().isoformat()
        }
        
        result = self.supabase.table("test_results").insert(result_data).execute()
        return len(result.data) > 0
    
    def get_user_test_history(self, user_id: str, test_type: Optional[str] = None) -> List[Dict]:
        """Get user's test history"""
        query = self.supabase.table("test_results").select("""
            *, test_sessions!inner(session_date, user_id)
        """).eq("test_sessions.user_id", user_id)
        
        if test_type:
            query = query.eq("test_type", test_type)
        
        result = query.order("created_at", desc=True).execute()
        return result.data if result.data else []
    
    def get_latest_session_for_user(self, user_id: str) -> Optional[str]:
        """Get the latest session ID for a user (for today)"""
        today = datetime.now().date().isoformat()
        result = self.supabase.table("test_sessions").select("session_id").eq("user_id", user_id).eq("session_date", today).order("created_at", desc=True).limit(1).execute()
        return result.data[0]["session_id"] if result.data else None