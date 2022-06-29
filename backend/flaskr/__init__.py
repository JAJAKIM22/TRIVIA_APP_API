import os
from typing import List
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
from settings import DB_NAME, DB_USER, DB_PASSWORD

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. DONE
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        formatted_categories = {category.id:category.type for category in categories}
        return jsonify({
            'success': True,
            'categories':formatted_categories,
            'total_categories':len(formatted_categories)
        })
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """
    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        questions=Question.query.join(Category, Question.category==Category.id).all()

        categories=[]

        for question in questions:
         categories.append(question.category)

         unique_cat=set(categories)

         category_type=Category.query.all()
         formatted_categories = {category.id:category.type for category in category_type}
         current_category=formatted_categories
         formatted_questions =[question.format() for question in questions]
         if len(current_category)== 0:
            abort(404)

         return jsonify({
            'success': True,
            'questions':formatted_questions[start:end],
            'total_questions':len(formatted_questions),
            'categories': formatted_categories,
            'current_category': current_category
            
        })
    """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            questions = Question.query.order_by(Question.id).all()
            formatted_questions =[question.format() for question in questions]

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    'questions':formatted_questions,
                    'total_questions':len(formatted_questions)
                }
            )

        except:
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=["POST"])
    def create_questions():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)

        try:
            question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
            question.insert()

            questions = Question.query.order_by(Question.id).all()
            formatted_questions =[question.format() for question in questions]
            return jsonify(
                {
                    "success": True,
                    'questions':formatted_questions,
                    'total_questions':len(Question.query.all())
                }
            )

        except:
            abort(405)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=["POST"])
    def search_questions():
        body = request.get_json()
        search_term = body.get("searchTerm", None)
        if search_term:
            search_questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

            return jsonify({
                'success': True,
                'questions': [question.format() for question in search_questions],
                'total_questions': len(search_questions),
                'current category': None
            })
        else:
            abort(400)  
     
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def question_category(category_id):
        categories = Category.query.filter(Category.id == category_id).one_or_none()
        if categories is None:
            abort(404)
        try:
            questions = Question.query.filter(Question.category == category_id).all()
            formatted_questions =[question.format() for question in questions]
            return jsonify({
               "success": True,
               "questions": formatted_questions,
               "total_questions": len(questions) 
            })
        except:
            abort(400)


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def random_quizzes():

        data = request.get_json()

        quiz_category = data.get("quiz_category", None)
        previous_questions = data.get("previous_questions", None)
        
        try:
            if quiz_category['id'] == 0:
                question_list = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                question_list = Question.query.filter(Question.category == quiz_category['id']).filter(Question.id.notin_(previous_questions)).all()

            formatted_question = [question.format() for question in question_list]
            randomIndex = random.randint(0, len(formatted_question) - 1)
            nextQuestion = formatted_question[randomIndex]
            return jsonify({
                "success": True,
                "question": nextQuestion
            })
        except:
            abort(400)    

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return(
            jsonify({"success": False, "error": 400, "message": "bad request"}), 
            400
        )
    @app.errorhandler(500)
    def server_error(error):
        return(
            jsonify({"success": False, "error": 500, "message": "server_error"}), 
            500
        )

    return app


    return app

