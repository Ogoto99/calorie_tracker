from django.shortcuts import render
import requests

def home(request):
    api_result = []
    warning_messages = []

    if request.method == 'POST':
        query = request.POST.get('query')
        url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
        headers = {
            "x-app-id": "11213701",
            "x-app-key": "954720163566c3669a7f61c9d59fe1b8",
            "Content-Type": "application/json"
        }
        payload = {
            "query": query
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            foods = data.get('foods', [])
            if not foods:
                api_result = "oops! There was an error"
            else:
                for food in foods:
                    calories = food.get('nf_calories') or 0
                    sugar = food.get('nf_sugars') or 0
                    sodium = food.get('nf_sodium') or 0
                    cholesterol = food.get('nf_cholesterol') or 0
                    saturated_fat = food.get('nf_saturated_fat') or 0
                    total_fat = food.get('nf_total_fat') or 0

                    result = {
                        'name': food.get('food_name', 'Unknown').capitalize(),
                        'calories': calories,
                        'carbohydrates_total_g': food.get('nf_total_carbohydrate') or 0,
                        'cholesterol_mg': cholesterol,
                        'fat_saturated_g': saturated_fat,
                        'fat_total_g': total_fat,
                        'fiber_g': food.get('nf_dietary_fiber') or 0,
                        'potassium_mg': food.get('nf_potassium') or 0,
                        'protein_g': food.get('nf_protein') or 0,
                        'sodium_mg': sodium,
                        'sugar_g': sugar,
                    }

                    # Add warnings
                    if sodium > 1000:
                        warning_messages.append(
                            f"⚠️ {result['name']} contains a high amount of sodium. High sodium causes dehydration and water retention.")
                    if sugar > 20:
                        warning_messages.append(
                            f"⚠️ {result['name']} contains a high amount of sugar. Sugar causes insulin spikes and contributes to obesity.")
                    if cholesterol > 100:
                        warning_messages.append(
                            f"⚠️ {result['name']} has high cholesterol content, which may contribute to heart disease.")
                    if saturated_fat > 5:
                        warning_messages.append(
                            f"⚠️ {result['name']} is high in saturated fat, which can raise bad cholesterol.")
                    if total_fat > 15:
                        warning_messages.append(
                            f"⚠️ {result['name']} is high in fat. Excess fat intake can lead to obesity.")

                    api_result.append(result)

        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            api_result = "oops! There was an error"

    return render(request, 'home.html', {
        'api': api_result,
        'warnings': warning_messages
    })
