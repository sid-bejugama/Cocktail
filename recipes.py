from secrets import dbname, username, password, recipes_table, drink, ingredients_table, bit_string, ingredient, bit_shift
import psycopg2
import psycopg2.extras


# sets up the connection to a database where recipes and ingredients are stored
def getConnection():
    try:
        _connection = psycopg2.connect(f"dbname = {dbname} user = {username} password = {password}")
        return _connection
    except:
        raise("Error while connecting to database of recipes.")

# gets connection and cursor
connection = getConnection()
cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# asks for first ingredient
ingredient_input = input("What ingredients will you be using? Type in your first ingredient to get started and type 'Done' when finished.")

ingredient_list = []

# continuously asks for ingredients until user is finished
while ingredient_input != 'Done':
    ingredient_list.append(ingredient_input.lower())
    ingredient_input = input("Please type your next ingredient. Type 'Done' if finished.")

# calculates the unique binary number resulting from ingredients passed in
cur_recipe_bit = 0
for item in ingredient_list:
    postgreSQL_select_Query = f"""SELECT * FROM "{ingredients_table}" WHERE "{ingredient}" = '{item}'"""

    cur.execute(postgreSQL_select_Query)

    ingredient_info = cur.fetchall()

    if len(ingredient_info) == 0: continue

    cur_recipe_bit += 2**ingredient_info[0][f"{bit_shift}"]
    


postgreSQL_select_Query = f'SELECT * FROM "{recipes_table}"'
cur.execute(postgreSQL_select_Query)
recipe_info = cur.fetchall()

# retrieves all viable recipes based on received ingredients

# if the bitwise and of the calculated value from the received ingredients with the value associated with a given beverage equals to the value associated with a given beverage, then the ingredients of the given beverage are a subset of the received ingredients
viable_recipes = []
for recipe in recipe_info:
    if cur_recipe_bit&int(recipe[f'{bit_string}'])==int(recipe[f'{bit_string}']):
        viable_recipes.append(recipe[f'{drink}'])

if len(viable_recipes) == 0:
    print("You cannot make any drinks with those ingredients")
else:
    print("These are the drinks that you can make:")
    for recipe in viable_recipes:
        print(recipe)







