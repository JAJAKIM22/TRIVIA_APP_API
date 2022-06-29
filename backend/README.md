# Backend - Trivia API

## Setting up the Backend
From the backend folder run `pip install -r requirements.txt.` All required packages are included in the requirements file.
To run the application, run the following commands:
​
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flak run

### Frontend
​
From the frontend folder, run the following commands to start the client:
​
```
npm install // only once to install the dependencies
npm start### Frontend
​
From the frontend folder, run the following commands to start the client:
​
```
npm install // only once to install the dependencies
npm start

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints
### Endpoints
​
#### `GET "/categories"`
​
- General:
  - Returns a dictionary of categories in which the key is of id and the values are the corresponding string of category, success value, and total categories
- Sample: `curl http://127.0.0.1:5000/categories`
​
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_category": 6
}
```
​
#### `GET "/questions"`
​
- General:
  - Returns a paginated set of questions, all categories, total_questions and success value.
- Sample `curl http://127.0.0.1:5000/questions`
​
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 22
}
```
​
#### `DELETE "/questions/{question_id}"`
​
- General:
  - Deletes the question of the given ID if it exists. Returns the id of the deleted question and success value
- `curl -X DELETE http://127.0.0.1:5000/questions/31`
​
```json
{
  "deleted": 31,
  "success": true,
  "total_questions": 22
}
```
​
#### `POST "/questions"`
​
- General:
​
  - Sends a post request in order to add a new question
​
- Sample `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who is going to apply for a Full Stack Job", "answer":"Me", "difficulty":"1", "category": "5"}'`
​
```
{
    "created": 32,
    "questions": [
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
    ],
    "success": true,
    "total_questions": 23
}
```
​
#### `POST "/questions"`
​
- General:
  - Sends a post request in order to search for a specific question by search term
- Sample `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "trees"}'`
​
- Returns: any array of questions, a number of totalQuestions that met the search term. and success value
​
```json
{
  "questions": [
    {
      "answer": "Canada",
      "category": 5,
      "difficulty": 2,
      "id": 24,
      "question": "Which country is the largest exporter of christmas trees?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```
​
#### `GET "/categories/{category_id}/questions"`
​
- General:
​
  - Fetches questions for a category specified by id request argument
​
- Sample `curl http://127.0.0.1:5000/categories/1/questions`
- Returns: An object with questions for the specified category, total questions, and success value.
​
```json
{
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```
​
#### `POST "/quizzes"`
​
- General:
​
  - Sends a post request in order to get the next question
  - Request Body:
​
    ```json
    {
      "previous_questions": [1, 4, 12],
      "quiz_category": {
        "id": 0,
        "type": "science"
      }
    }
    ```
​
  - Returns: a single new question object
​
  ```json
  {
    "question": {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  }
  ```
​
## Deployment N/A
​
## Authors
​
`Peter KImani`
​
# Acknowledgements
​
The awesome team at Udacity.

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
