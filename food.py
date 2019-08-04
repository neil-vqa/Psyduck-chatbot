
import requests, json


def claim_search(find):
    extend = '&self=false&branded=false&common=true&claims=true'
    url = 'https://trackapi.nutritionix.com/v2/search/instant?query=' + find + extend

    res = requests.get(url, headers={'x-app-id':'fb3d9559', 'x-app-key':'728834e1a4f80b073dfeace223703259', 
        'Content-Type':'application/json'})

    result = json.loads(res.text)
    payload = result['common'][0]
    claims = payload['claims']

    return claims

def nutri_search(find):
    url2 = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    query = {'query': find}

    res = requests.post(url2, headers={'x-app-id':'fb3d9559', 'x-app-key':'728834e1a4f80b073dfeace223703259', 
        'Content-Type':'application/json'}, json=query)
    
    result = json.loads(res.text)
    name = result['foods'][0]['food_name']
    quantity = str(result['foods'][0]['serving_qty'])
    unit = result['foods'][0]['serving_unit']
    grams = str(result['foods'][0]['serving_weight_grams']) + ' grams'
    calories = str(result['foods'][0]['nf_calories']) + ' kcal'
    fat = str(result['foods'][0]['nf_total_fat']) + ' grams'
    chol = str(result['foods'][0]['nf_cholesterol']) + ' mg'
    sugar = str(result['foods'][0]['nf_sugars']) + ' grams'
    protein = str(result['foods'][0]['nf_protein']) + ' grams'
    photo = result['foods'][0]['photo']['highres']

    return name, quantity, unit, grams, calories, fat, chol, sugar, protein, photo
