from secrets import dbname, username, password, recipes_table, drink, ingredients, alcohol_type, ingredients_table, bit_string, ingredient, bit_shift
import psycopg2
import psycopg2.extras
import requests



# sets up the connection to a database where recipes and ingredients are stored
def getConnection():
    try:
        _connection = psycopg2.connect(f"dbname = {dbname} user = {username} password = {password}")
        return _connection
    except:
        raise("Error while connecting to database of recipes.")


# creates the database connection and cursor
connection = getConnection()
cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# list of the subset of drinks we are targeting
drinks = ["rum", "vodka", "whiskey", "tequila", "brandy", "gin"]
cur_ingredient_bit = 0

# retrieves data for each type of drink
for item in drinks:
    # retrieves json data
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={item}"
    r = requests.get(url)
    drinks_info = r.json()['drinks']
    # identifies the ingredients for each beverage associated with a given type of alcohol
    for beverage in drinks_info:

        drink_name = beverage['strDrink'] # beverage name
        drink_type = item # beverage type
        drink_ingredients = [] # list of ingredients for the beverage

        cur_num = 1 # identifies maximum number of potential ingredients so far 
        ingredient_key = f'strIngredient{cur_num}'

        # identifies the ingredients for a given beverage
        cur_beverage_bit_shift = 0 # unique decimal value that represents the ingredients associated with the given beverage in binary (by position in the binary number)
        while beverage[ingredient_key]:
            cur_ingredient = str(beverage[ingredient_key]).lower()
            drink_ingredients.append(cur_ingredient)
            cur_num += 1
            ingredient_key = f'strIngredient{cur_num}'

            postgreSQL_select_Query = f"""SELECT * FROM "{ingredients_table}" WHERE "{ingredient}" = '{cur_ingredient}'"""

            cur.execute(postgreSQL_select_Query)

            ingredient_info = cur.fetchall()
            if len(ingredient_info) == 0:
                # assigns each unique ingredient an integer value
                postgreSQL_insert_Query = f"""INSERT INTO "{ingredients_table}" ("{ingredient}", "{bit_shift}") VALUES ('{cur_ingredient}', '{cur_ingredient_bit}')"""
                
                cur.execute(postgreSQL_insert_Query)

                cur_ingredient_bit += 1
            
            postgreSQL_select_Query = f"""SELECT * FROM "{ingredients_table}" WHERE "{ingredient}" = '{cur_ingredient}'"""

            cur.execute(postgreSQL_select_Query)

            ingredient_info = cur.fetchall()

            cur_beverage_bit_shift += 2**ingredient_info[0][f'{bit_shift}']


        # inserts the beverage into the database
        postgreSQL_insert_Query = f"""INSERT INTO "{recipes_table}" ("{drink}", "{ingredients}", "{alcohol_type}", "{bit_string}") VALUES ('{drink_name}', ARRAY{drink_ingredients}, '{drink_type}', '{cur_beverage_bit_shift}')"""

        cur.execute(postgreSQL_insert_Query)


# commits all insertions
connection.commit()


    

    

