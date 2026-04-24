import requests
from config import Config

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_headers():
    """Get request headers with API key"""
    return {
        "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "FlavorForge"
    }

def generate_recipe(ingredients, allergy="None"):
    """Generate recipes using AI"""
    ingredients = ingredients.strip()
    
    if not ingredients:
        return "ERROR: No ingredients provided"
    
    # Sanitize allergy input
    if allergy and allergy.lower() != "none":
        allergy_text = f"STRICTLY avoid these allergies: {allergy}"
    else:
        allergy_text = "No specific allergies to avoid"
    
    prompt = f"""
You are a professional chef and nutrition expert.

Generate EXACTLY 3 unique recipes based on the user's ingredients.

For EACH recipe, use this STRICT format:

RECIPE:
Dish Name: [Creative name]
Cooking Time: [X minutes]
Servings: [X servings]
Difficulty: [Easy/Medium/Hard]

Ingredients:
- [ingredient 1 with quantity]
- [ingredient 2 with quantity]
- [etc.]

Instructions:
1. [First step]
2. [Second step]
3. [Continue with clear numbered steps]

Estimated Nutrition (per serving):
- Calories: [X kcal]
- Protein: [X g]
- Carbs: [X g]
- Fat: [X g]
-Vitamins & Minerals: [Brief summary in mgh]

Chef's Tip: [One helpful tip for this recipe]

---

IMPORTANT RULES:
- {allergy_text}
- NEVER mention or include allergic ingredients
- Use ONLY the provided ingredients as the main components
- Keep instructions clear, concise, and numbered
- Provide realistic nutrition estimates
- Make each recipe unique and different from the others

User's Available Ingredients:
{ingredients}
"""

    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct",
        "messages": [
            {
                "role": "system", 
                "content": "You are an expert chef who creates structured, safe, and delicious recipes. You always follow the specified format and never include allergenic ingredients when allergies are mentioned."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "temperature": 0.8,
        "max_tokens": 1200,
        "top_p": 0.9
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=get_headers(),
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            error_msg = response.json().get('error', {}).get('message', response.text)
            return f"ERROR: API request failed - {error_msg}"

        content = response.json()["choices"][0]["message"]["content"]
        return content

    except requests.exceptions.Timeout:
        return "ERROR: Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"ERROR: Network error - {str(e)}"
    except KeyError as e:
        return f"ERROR: Unexpected API response format - {str(e)}"
    except Exception as e:
        return f"ERROR: {str(e)}"