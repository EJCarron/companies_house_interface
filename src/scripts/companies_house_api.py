import datetime
import time
import requests
import json
from .config import config

base_url = 'https://api.company-information.service.gov.uk/'


def get_officer(officer_id, appointments_limit, requests_count):
    url = 'https://api.company-information.service.gov.uk/officers/{officer_id}/appointments'.format(
        officer_id=officer_id)

    return get_with_paging(url=url, requests_count=requests_count,
                           appointments_limit=appointments_limit,
                           )


def requests_check(requests_count):
    print(requests_count)
    if requests_count > 599:
        print('rate limit hit. Wait 5 mins')
        countdown(h=0, m=5, s=0)
        requests_count = 0
    else:
        requests_count += 1
    return requests_count


# Create class that acts as a countdown
def countdown(h, m, s):
    # Calculate the total number of seconds
    total_seconds = h * 3600 + m * 60 + s

    # While loop that checks if total_seconds reaches zero
    # If not zero, decrement total time by one second
    while total_seconds > 0:
        # Timer represents time left on countdown
        timer = datetime.timedelta(seconds=total_seconds)

        # Prints the time left on the timer
        print(timer, end="\r")

        # Delays the program one second
        time.sleep(1)

        # Reduces total time by one second
        total_seconds -= 1

    print("Bzzzt! The countdown is at zero seconds!")


def get_company_officer_ids(company_number, appointments_limit, requests_count):
    url = base_url + '/company/{company_number}/officers'.format(
        company_number=company_number)
    result, requests_count = get_with_paging(url=url, requests_count=requests_count,
                                             appointments_limit=appointments_limit)
    if result is None:
        return None

    ids = []

    for item in result['items']:
        officer_id = item['links']['officer']['appointments'].split('/')[2]
        if officer_id in ids:
            continue
        ids.append(officer_id)

    return ids, requests_count


def get_company(company_number, requests_count):
    requests_count = requests_check(requests_count)

    url = base_url + '/company/{companyNumber}'.format(companyNumber=company_number)
    print(url)
    response = requests.get(url=url, headers=config.header)
    print(response.status_code)
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        return None

    result = json.loads(response.text)
    return result, requests_count


def get_with_paging(url, appointments_limit, requests_count):
    items_per_page = 35
    start_index = 0

    go = True

    final_result = None
    items = []

    while go:
        requests_count = requests_check(requests_count)

        print('items_per_page: {items_per_page}, start_index: {start_index}'.format(items_per_page=items_per_page,
                                                                                    start_index=start_index))
        params = {'items_per_page': items_per_page, 'start_index': start_index}

        response = requests.get(url=url, headers=config.header, params=params)

        print(response.status_code)
        if response.status_code != 200:
            print(response.text)
            return None, requests_count

        result = json.loads(response.text)

        if appointments_limit != -1 and result['total_results'] >= appointments_limit:
            print("APPOINTMENT LIMIT BREACHED officer {officer} has {num} appointments"
                  .format(officer=result['name'], num=result['total_results']))
            final_result = result
            final_result['items'] = items
            break

        items += result['items']
        if (start_index + items_per_page) >= result['total_results']:
            go = False
            final_result = result
            final_result['items'] = items

        start_index += items_per_page

    return final_result, requests_count


def extract_id_from_link(link):
    return link.split('/')[2]
