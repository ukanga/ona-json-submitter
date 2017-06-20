import argparse
import codecs
import json
import requests

ONA_API_URL = "https://api.ona.io/api/v1/"


def user(username, password):
    response = requests.get(ONA_API_URL + "user", auth=(username, password))
    return response.json()


def submit_json(data, id_string, username, password):
    submission_data = {
        'id': id_string,
        'submission': data,
    }

    response = requests.post(ONA_API_URL + "submissions",
                             data=json.dumps(submission_data),
                             auth=(username, password),
                             headers={'Content-Type': 'application/json'})

    return response.status_code in [201, 202]


def process_json(filename, id_string, username, password):
    json_file = codecs.open(filename, 'rb', encoding='utf-8')
    data = json.load(json_file)
    success = 0
    failed = 0
    for row in data:
        status = submit_json(row, id_string, username, password)
        if status:
            success += 1
        else:
            failed += 1

    print("Processed %d records successfully, %d failed." % (success, failed))


class Config:
    pass


if __name__ == '__main__':
    params = Config()
    parser = argparse.ArgumentParser(prog='submitter')
    parser.add_argument('id_string', help='Ona form_id')
    parser.add_argument('jsonfile', help='JSON file of data to be submitted.')
    parser.add_argument('--username', help='Ona username')
    parser.add_argument('--password', help='Ona password')
    parser.parse_args(namespace=params)

    username = params.username
    password = params.password
    filename = params.jsonfile
    id_string = params.id_string

    if not username and not password:
        print("Username and password are required.\n")
        parser.print_usage()
    else:
        user_data = user(username, password)
        print("User Account: ", user_data.get('name'))

        process_json(filename, id_string, username, password)
