# -------------------------------- BASEMODEL ---------------------------------------------

from pydantic import BaseModel, EmailStr, ConfigDict, ValidationError

class User(BaseModel):
    # validate_assignment=True ka matlab:
    # update (assignment) karte waqt bhi validation hoga
    model_config = ConfigDict(validate_assignment=True)
    
    name: str
    age: int
    email: EmailStr


# ✅ Case 1: Valid creation (sab types sahi hain → no error)
user = User(name="Areeba", age=22, email="areeba@example.com")
print(user.model_dump())
# Output: {'name': 'Areeba', 'age': 22, 'email': 'areeba@example.com'}


# ❌ Case 2: Invalid creation (age string diya hai → error at creation)
try:
    user_invalid = User(name="Areeba", age="Twenty Two", email="areeba@example.com")
except ValidationError as e:
    print("❌ Creation Error:\n", e)
    # Output:
    # age
    #   Input should be a valid integer, unable to parse string as an integer


# ❌ Case 3: Invalid update (assignment par bhi error aayega)
try:
    user.age = "Twenty Three"   # Error because validate_assignment=True
except ValidationError as e:
    print("❌ Update Error:\n", e)
    # Output:
    # age
    #   Input should be a valid integer, unable to parse string as an integer


# ✅ User object abhi bhi valid data hold karega (previous correct state)
print(user.model_dump())
# Output: {'name': 'Areeba', 'age': 22, 'email': 'areeba@example.com'}


# --------------------------- DATACLASSES -------------------------------------------

from pydantic.dataclasses import dataclass
from typing import Optional
from dataclasses import asdict

@dataclass
class UserData:
    name: str
    age: int
    email: Optional[str] = None


# ✅ Case 1: Valid creation (age int hai → no error)
user = UserData(name="Areeba", age=22)
print(user)
# Output: UserData(name='Areeba', age=22, email=None)


# ❌ Case 2: Invalid creation (age string diya hai → error at creation)
# Yeh line run hote hi ValidationError raise karegi
# user = UserData(name="Areeba", age="Twenty Two")  
# Output: ValidationError: Input should be a valid integer


# ✅ Convert to dictionary
print(asdict(user))
# {'name': 'Areeba', 'age': 22, 'email': None}


# ⚠️ No validation on update
# Dataclass creation time par validate karta hai,
# lekin update karte waqt type check nahi hota
user.age = "Twenty Three"   # Allowed, koi error nahi aayega
print(user)
# Output: UserData(name='Areeba', age='Twenty Three', email=None)
