from flask import Flask,jsonify,request,render_template
import requests

app=Flask(__name__)

# recipes = [
#     {
#         "name": "Coffee",
#         "ingredients": ["water", "coffee grounds", "milk", "sugar"]
#     },
#     {
#         "name": "Omelette",
#         "ingredients": ["eggs", "milk", "salt", "pepper", "butter"]
#     },
#     {
#         "name": "Waffles",
#         "ingredients": ["flour", "milk", "eggs", "butter", "sugar"]
#     },
#     {
#         "name": "Pancakes",
#         "ingredients": ["flour", "milk", "eggs", "sugar", "baking powder"]
#     },
#     {
#         "name": "Toast",
#         "ingredients": ["bread", "butter"]
#     },
#     {
#         "name": "Sandwich",
#         "ingredients": ["bread", "lettuce", "tomato", "cheese", "ham"]
#     }
# ]

ingredient_list=[]



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ingredients',methods=['POST'])
def add_ingredients():
    new_ingredients=request.get_json()
    ingredient_list.append(new_ingredients["name"].lower())
    return jsonify(ingredient_list)

@app.route('/ingredients',methods=['GET'])
def get_ingredients():
    return jsonify(ingredient_list)

# @app.route('/recipes',methods=['GET'])
# def check_recipes():
#     matching_recipes=[]
#     # can_make = all(ingredient in ingredient_list for ingredient in recipe['ingredients'])
#     #Above commented code is a simple way to write the below block of code
#     for  recipe in recipes:
#         can_make=True
#         for ingredient in recipe['ingredients']:
#             if ingredient not in ingredient_list:
#                 can_make=False
#                 break
#         if can_make:
#             matching_recipes.append(recipe)

#     return jsonify(matching_recipes)


@app.route('/test_api',methods=['GET'])
def get_recipe():
    if not ingredient_list:
        return jsonify({"error":"No ingredients added"}),400
    ingredients_param=",".join(ingredient_list)
    spoonacular_api=f"https://api.spoonacular.com/recipes/findByIngredients?apiKey=c9bd552d386546a6b1ae06a831b318e9&ingredients={ingredients_param}&number=5"
    response=requests.get(spoonacular_api)
    data=response.json()
    return jsonify(data)

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    url=f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey=c9bd552d386546a6b1ae06a831b318e9"
    response=requests.get(url)
    if response.status_code != 200:
     return f"Error: {response.status_code}", response.status_code

    recipe=response.json()
    return render_template('recipe.html',recipe=recipe)
        

if __name__=="__main__":
    app.run(debug=True)