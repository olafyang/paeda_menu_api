import boto3
from boto3.dynamodb.conditions import Key
from io import BytesIO
from paeda_menu_reader.get_menu import scrap_pdf
from paeda_menu_reader.read_menu import ReadFromMenu
from datetime import date
from app.s3_upload import upload_obj_to_pdf_bucket


class ObjectDoesNotExist(Exception):
    pass


dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
table = dynamodb.Table('paeda_menu')


def get_menu_by_day(day):
    week_number_of_given_day = date.isocalendar(day)[1]
    week_name_of_given_day = f'{date.isocalendar(day)[0]}W{date.isocalendar(day)[1]}'

    # detect invalid input
    current_week_number = date.isocalendar(date.today())[1]
    # if week of given day is in future
    if week_number_of_given_day > current_week_number:
        raise ObjectDoesNotExist

    query_response = table.query(KeyConditionExpression=Key('year_week').eq(week_name_of_given_day))

    # if no entry in db
    if query_response['Count'] == 0:
        # detect invalid input
        # if day is in the past and no records are found
        if week_number_of_given_day < current_week_number:
            raise ObjectDoesNotExist

        pdf_obj = BytesIO(scrap_pdf())
        menu = ReadFromMenu(pdf_obj)
        lunch_list = menu.get_lunch_list()
        dinner_list = menu.get_dinner_list()

        week = {
            'meals': {}
        }

        for i in range(7):
            week['meals'][str(i)] = {
                'lunch': lunch_list[i],
                'dinner': dinner_list[i],
            }

        meals_of_week = week['meals']

        # create item in ddb table
        table.put_item(
            Item={
                'year_week': week_name_of_given_day,
                'week': meals_of_week
            }
        )

        upload_obj_to_pdf_bucket(pdf_obj, week_name_of_given_day + '.pdf')

        weekday_of_given_day = str(date.weekday(day))

        lunch_of_given_day = meals_of_week[weekday_of_given_day]['lunch']
        dinner_of_given_day = meals_of_week[weekday_of_given_day]['dinner']

        return lunch_of_given_day, dinner_of_given_day

    # object exist in db
    else:
        meals_of_given_week = query_response['Items'][0]['week']
        weekday_of_given_day = str(date.weekday(day))

        lunch_of_given_day = meals_of_given_week[weekday_of_given_day]['lunch']
        dinner_of_given_day = meals_of_given_week[weekday_of_given_day]['dinner']
        return lunch_of_given_day, dinner_of_given_day


def get_week(week_name):
    query_response = table.query(KeyConditionExpression=Key('year_week').eq(week_name))

    if query_response['Count'] == 0:
        raise ObjectDoesNotExist
    else:
        return query_response['Items'][0]['week']
