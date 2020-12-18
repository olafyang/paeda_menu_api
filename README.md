# paeda_menu_api
An API for my school that pulls PDF files of weekly lunch and dinner menu and returns daily and weekly menu in JSON.
The API is hosted on AWS Lambda in a docker container with AWS API Gateway as the trigger.

# Useage
## API url:
`https://rk41bvtelc.execute-api.eu-central-1.amazonaws.com/paeda_menu_api/get`

Make query by adding either one of following parameters to the url:

- **`method=today`**: return today's menu
  - For example:
  `https://rk41bvtelc.execute-api.eu-central-1.amazonaws.com/paeda_menu_api/get?method=today`
  will return the following JSON:
  
     `{"date": "2020-12-16", "meals": {"lunch": "Bratwurst mit Kartoffelsalat", "dinner": "Chinabuffet"}}`



- **`method=date`**: return menu based on specified date
  - To query with `date` method, add the `day=(desired date)` parameter with date in [ISO 8601 date format](https://en.wikipedia.org/wiki/ISO_8601) (YYYY-MM-DD)
  
  - For example:
  `https://rk41bvtelc.execute-api.eu-central-1.amazonaws.com/paeda_menu_api/get?method=date&day=2020-11-29`
  will return the following JSON:
  
     `{"date": "2020-11-29", "meals": {"lunch": "Brunch 10.00 bis 11.00 Uhr", "dinner": "Schaschlikpfanne"}}`
     
- **`method=week`**: return menu of the entire week based on week name
  - To query with `week` method, add the `name=(week name)` parameter in following format
    - `(YYYY)W(WW)`
    - For example: `2020W51` means the 50th week of 2020
    - For weeks in singular digit, formats like `2020W5` and `2020W05` will both work
  
  - For example:
  `https://rk41bvtelc.execute-api.eu-central-1.amazonaws.com/paeda_menu_api/get?method=week&name=2020W50`
  will return the following JSON:
  
     `{"week": "2020W50", "meals": {"0": {"dinner": "Ofenfeta", "lunch": "Linsensuppe mit W\u00fcrstchen"}, "1": {"dinner": "Kartoffeltaschen mit Frischk\u00e4se", "lunch": "Fischst\u00e4bchen mit Dillsauce Salzkartoffeln und Salat"}, "2": {"dinner": "Chinabuffet", "lunch": "Paprikaschnitzel (H\u00e4hnchenbrust) dazu Reis und Salat"}, "3": {"dinner": "Pizza", "lunch": "Spaghetti mit Tomate-Mozzarella-Sauce"}, "4": {"dinner": "Chinabuffet", "lunch": "Schweinelachsschnitzel mit Brokkoli Sauce Hollandaise"}, "5": {"dinner": "Rahmgeschnetzeltes", "lunch": "Brunch 10.00 bis 11.00 Uhr"}, "6": {"dinner": "Schlemmerfilet \"Bordelaise\"", "lunch": "Brunch 10.00 bis 11.00 Uhr"}}}`
     
     
# Example Code
https://gist.github.com/olafyang/40d12ae42710a48a90c60a3874cc7ce8
