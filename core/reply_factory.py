
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    session["answers"] = {}
    session["answers"][current_question_id] = answer
    session.save()
    return True, None


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        question_index = 0
    else:
        question_index = int(current_question_id) + 1
    # question_index = current_question_id + 1
    if question_index < len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[question_index]['question_text'], question_index
    return None, -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    answers = session.get("answers")
    if answers:
        # Calculate the score based on user answers (assuming a simple calculation)
        score = sum(len(answer) for answer in answers.values())
        result_message = f"Congratulations! Your final score is {score}. Thanks for using the Python Quiz Bot!"
    else:
        result_message = "It seems there was an issue calculating your score. Please try again later."

    return result_message
