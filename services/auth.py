import bcrypt
from services.database import DatabaseService
from typing import Optional, Dict

class AuthService:
    def __init__(self):
        self.db = DatabaseService()
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def login(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user login"""
        user = self.db.get_user_by_email(email)
        if user and self.verify_password(password, user['password_hash']):
            # Remove password hash from returned user data
            user_data = user.copy()
            del user_data['password_hash']
            return user_data
        return None
    
    def register(self, email: str, password: str, full_name: str, age: int, 
                gender: str, height_cm: Optional[float] = None, 
                weight_kg: Optional[float] = None) -> Optional[Dict]:
        """Register a new user"""
        # Check if user already exists
        existing_user = self.db.get_user_by_email(email)
        if existing_user:
            return None
        
        # Hash password and create user
        password_hash = self.hash_password(password)
        user = self.db.create_user(
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            age=age,
            gender=gender,
            height_cm=height_cm,
            weight_kg=weight_kg
        )
        
        if user:
            # Remove password hash from returned user data
            user_data = user.copy()
            del user_data['password_hash']
            return user_data
        return None
    
    def user_exists(self, email: str) -> bool:
        """Check if a user exists by email"""
        user = self.db.get_user_by_email(email)
        return user is not None