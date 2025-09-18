# 📘 Pydantic: `BaseModel` vs `@pydantic.dataclasses.dataclass`

Pydantic models provide **automatic data validation** using Python type hints.  
There are two main approaches:  

1. **BaseModel** → Strict validation (creation + updates).  
2. **@pydantic.dataclasses.dataclass** → Lightweight, validation only at creation.  

---

## 🔹 1. BaseModel

### ✅ Features
- Inherits from `pydantic.BaseModel`.  
- Validates **both at creation and on updates**.  
- Rich API in Pydantic v2:  
  - `.model_dump()` → Convert to dict  
  - `.model_dump_json()` → Convert to JSON  
  - `.model_copy()` → Clone model  
  - `.model_json_schema()` → Generate JSON schema  
- Use when you need **strict validation** (APIs, configs, structured data).  

### 📌 Example

```python
from pydantic import BaseModel, EmailStr, ConfigDict, ValidationError

class User(BaseModel):
    # validate_assignment=True → validation on updates also
    model_config = ConfigDict(validate_assignment=True)
    
    name: str
    age: int
    email: EmailStr

# ✅ Case 1: Valid creation
user = User(name="Areeba", age=22, email="areeba@example.com")
print(user.model_dump())
# {'name': 'Areeba', 'age': 22, 'email': 'areeba@example.com'}

# ❌ Case 2: Invalid creation (string instead of int)
try:
    user_invalid = User(name="Areeba", age="Twenty Two", email="areeba@example.com")
except ValidationError as e:
    print("❌ Creation Error:\n", e)
    # age
    #   Input should be a valid integer, unable to parse string as an integer

# ❌ Case 3: Invalid update
try:
    user.age = "Twenty Three"  # Raises error
except ValidationError as e:
    print("❌ Update Error:\n", e)
    # age
    #   Input should be a valid integer, unable to parse string as an integer

# ✅ Still holds last valid state
print(user.model_dump())
# {'name': 'Areeba', 'age': 22, 'email': 'areeba@example.com'}

```

## 🔹 2. @pydantic.dataclasses.dataclass
### ✔ Features

- Built on `Python’s` native `dataclasses`.

- Validation happens only at creation.

- After creation, updates do not trigger validation.

- Serialization via `dataclasses.asdict()` ~~(not .model_dump())~~.

- Lightweight and good for when libraries/frameworks expect dataclasses.

### 📌 Example

```python
from pydantic.dataclasses import dataclass
from typing import Optional
from dataclasses import asdict

@dataclass
class UserData:
    name: str
    age: int
    email: Optional[str] = None

# ✅ Case 1: Valid creation
user = UserData(name="Areeba", age=22)
print(user)
# UserData(name='Areeba', age=22, email=None)

# ❌ Case 2: Invalid creation
# user = UserData(name="Areeba", age="Twenty Two")
# Raises ValidationError: Input should be a valid integer

# ✅ Convert to dict
print(asdict(user))
# {'name': 'Areeba', 'age': 22, 'email': None}

# ⚠️ Case 3: No validation on update
user.age = "Twenty Three"  # Allowed, no error
print(user)
# UserData(name='Areeba', age='Twenty Three', email=None)
```

## 🔎 Comparison Table

| Feature             | BaseModel ✅                        | @dataclass ⚡                   |
|---------------------|-------------------------------------|---------------------------------|
| **Validation**      | At creation + update                | At creation only                |
| **Serialization**   | `.model_dump()`, `.model_dump_json()` | `dataclasses.asdict()`          |
| **Assignment checks** | Yes (if `validate_assignment=True`) | No                              |
| **API methods**     | Rich (copy, schema, etc.)           | Limited                         |
| **Performance**     | Slightly heavier                    | Lightweight                     |
| **Use case**        | APIs, configs, JSON schemas         | Native dataclass compatibility  |

---

## ⚖️ Rule of Thumb

✅ **Use `BaseModel` when:**
- You need strict validation.  
- You’re working with APIs, configs, or nested models.  
- You want built-in serialization & schema generation.  

⚡ **Use `@dataclass` when:**
- You want lightweight models.  
- A library/framework requires dataclasses.  
- You don’t need validation on updates.  
