import math

COMMON_PASSWORDS = [
    "123456", "password", "12345678", "qwerty", "12345", "123456789", "iloveyou", "admin", "admin123"
]

def calculate_entropy(password):
    pool_size = 0
    if any(c.islower() for c in password):
        pool_size += 26
    if any(c.isupper() for c in password):
        pool_size += 26
    if any(c.isdigit() for c in password):
        pool_size += 10
    if any(c in "!@#$%^&*()_+{}:\"<>?|[];',./`~" for c in password):
        pool_size += 32
        
    if pool_size == 0:
        return 0
    
    entropy = len(password) * math.log2(pool_size)
    return entropy

def estimate_crack_time(entropy):
    # Assume attackers can try 10^10 hashes per second
    guesses = 2 ** entropy
    seconds = guesses / (10**10)
    
    if seconds < 1:
        return "Instantly"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds/60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds/3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds/86400)} days"
    else:
        return f"{int(seconds/31536000)} years"

def audit_password(password):
    if password.lower() in COMMON_PASSWORDS:
        return {
            "score": 0,
            "feedback": "This is a very common password! Change it immediately.",
            "crack_time": "Instantly",
            "entropy": 0,
            "risk": "Critical"
        }
    
    entropy = calculate_entropy(password)
    crack_time = estimate_crack_time(entropy)
    
    score = min(100, int((entropy / 100) * 100))
    
    if entropy < 40:
        risk = "High"
        feedback = "Weak password. Add uppercase letters, numbers, and symbols."
    elif entropy < 60:
        risk = "Medium"
        feedback = "Moderate password. Make it longer for better security."
    elif entropy < 80:
        risk = "Low"
        feedback = "Strong password."
    else:
        risk = "None"
        feedback = "Excellent password."
        
    return {
        "score": score,
        "feedback": feedback,
        "crack_time": crack_time,
        "entropy": round(entropy, 2),
        "risk": risk
    }
