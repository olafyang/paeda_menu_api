import json
from app import app
from datetime import date, datetime
import re


def handler(event, context):
    params = event['queryStringParameters']

    try:
        params_method = params['method']
    except KeyError:
        response = phrase_error('invalid parameters')
        return json.dumps(response)

    if params_method == 'today':
        today = date.today()
        lunch = app.get_menu_by_day(today)[0]
        dinner = app.get_menu_by_day(today)[1]

        response = phrase_response_day(today, lunch, dinner)

    elif params_method == 'date':
        try:
            day_obj = datetime.fromisoformat(params['day'])
            lunch = app.get_menu_by_day(day_obj)[0]
            dinner = app.get_menu_by_day(day_obj)[1]

            response = phrase_response_day(day_obj, lunch, dinner)

        except KeyError:
            response = phrase_error('No date given')

        except ValueError:
            response = phrase_error('Invalid date format')

        except app.ObjectDoesNotExist:
            response = phrase_error('Object does not exist in database')

    elif params_method == 'week':
        try:
            week_name = params['name']

            re_pattern = r'(\d{4})W(\d{1,2})'
            re_search = re.search(re_pattern, week_name)
            if re_search:
                year_number_int = int(re_search.group(1))
                week_number_int = int(re_search.group(2))
                if week_number_int > 53:
                    raise ValueError
                if week_number_int < 10:
                    week_name = f'{year_number_int}W{week_number_int}'
                response = phrase_response_week(week_name, app.get_week(week_name))
            else:
                response = phrase_error('Invalid week parameter format')

        except KeyError:
            response = phrase_error('No week parameter given')

        except ValueError:
            response = phrase_error('Invalid week parameter format')

        except app.ObjectDoesNotExist:
            response = phrase_error('Object does not exist in database')

    else:
        response = phrase_error('invalid method')

    return response


def phrase_response_day(day_obj, lunch, dinner):

    body = {
        'date': date.isoformat(day_obj),
        'meals': {
            'lunch': lunch,
            'dinner': dinner
        }
    }
    response_meal = {
        'statusCode': 200,
        'body': json.dumps(body)
        }

    return response_meal


def phrase_response_week(week_name, meals):

    body = {
        'week': week_name,
        'meals': meals,
    }

    response = {
        'statusCode': 200,
        'body': json.dumps(body)
    }

    return response


def phrase_error(error_msg):
    response_err = {
        'message': '400 Bad Request: ' + error_msg
    }
    response = {
        'statusCode': 400,
        'body': json.dumps(response_err)
    }
    return response
