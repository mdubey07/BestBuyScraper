import requests
import fpdf
import os
import re
import string

import json

# Set the request parameters
url = 'https://legsline.zendesk.com/api/v2/tickets.json?page='
url2 = 'https://legsline.zendesk.com/api/v2/tickets/389/comments.json'
user = ''
pwd = ''

# Do the HTTP get request
# response = requests.get(url, auth=(user, pwd))
fpdf.set_global("SYSTEM_TTFONTS", os.path.join(os.path.dirname(__file__), 'fonts'))

print(os.path.join(os.path.dirname(__file__), 'fonts'))


def format_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ', '_')  # I don't like spaces in filenames.
    return filename


def ticket_comments(ticket_id):
    left_url = 'https://legsline.zendesk.com/api/v2/tickets/'
    right_url = '/comments.json'
    t_url = left_url + str(ticket_id) + right_url
    response2 = requests.get(t_url, auth=(user, pwd))

    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    data2 = response2.json()
    # data2 = json.dumps(response2.json())
    comment_list = data2['comments']
    count = 1
    # comments = []
    # comments_date = []
    comments_data = []
    for comment in comment_list:
        # print('\ncomment ' + str(count) + ': ' + comment['plain_body'])
        # count = count + 1

        # comment_text = comment['plain_body'].replace("’", "'").replace("‘", "'")
        # comment_text = comment_text.replace(u"\u2018", "'").replace(u"\u2019", "'")
        # comments.append(comment_text.encode('ascii', 'ignore').decode('latin-1'))
        # comments.append(comment['plain_body'])
        # comments_date.append(comment['created_at'])
        c_data = {
            'comments': emoji_pattern.sub(r'', comment['plain_body']),
            'comments_date': comment['created_at']
        }
        comments_data.append(c_data)
    return comments_data


def create_pdf(pdf_name):
    pdf = fpdf.FPDF()

    ticket_creation_date = str(pdf_name['created_at']).split('T')[0].strip()
    ticket_status = pdf_name['status'].strip()
    t_pdf_name = str(pdf_name['id']) + '-' + ticket_creation_date + '-' + str(pdf_name['from_name']) + '-' + str(
        pdf_name['status'])

    pdf.add_font("NotoSans", style="", fname="NotoSans-Regular.ttf", uni=True)
    pdf.add_page()
    pdf.set_font("NotoSans", size=14)

    pdf.set_text_color(7, 177, 190)
    pdf.cell(200, 10, txt='#' + str(pdf_name['id']), ln=1, align='C')
    pdf.cell(200, 10, txt=pdf_name['subject'], ln=1, align='C')

    from_txt = pdf_name['from_name'] + '( ' + pdf_name['from_address'] + ' )'
    to_txt = pdf_name['to_name'] + '( ' + pdf_name['to_address'] + ' )'

    pdf.set_font("NotoSans", size=8)
    pdf.set_text_color(81, 81, 81)
    pdf.cell(0, 10, txt=from_txt, ln=0, align='L')
    pdf.cell(0, 10, txt=to_txt, ln=2, align='R')

    pdf.ln(3)
    pdf.set_font("NotoSans", size=12)
    pdf.set_text_color(7, 177, 190)
    pdf.cell(0, 10, txt='Ticket Creation Date: ' + str(pdf_name['created_at']), ln=1, align='L')
    pdf.cell(0, 10, txt='Ticket Status: ' + str(pdf_name['status']), ln=1, align='L')

    pdf.set_text_color(7, 177, 190)
    pdf.cell(200, 10, txt='All Comments', ln=1, align='C')
    pdf.ln(4)

    if pdf_name['comments']:
        count = 1
        for comment in pdf_name['comments']:
            h2 = 'Comment ' + str(count) + ': ' + comment['comments_date']
            pdf.set_text_color(7, 177, 190)
            pdf.cell(200, 10, txt=h2, ln=1, align='L')
            pdf.ln(2)

            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 5, re.sub(r'\n\s*\n', '\n\n', comment['comments'].replace('&nbsp;', ' ')))
            pdf.ln(2)
            count = count + 1

    pdf.output(format_filename(str(t_pdf_name).strip()) + '.pdf')


# Check for HTTP codes other than 200
# if response.status_code != 200:
#     print('Status:', response.status_code, 'Problem with the request. Exiting.')
#     exit()

# Decode the JSON response into a dictionary and use the data
def get_tickets():
    page_count = 1
    while True:
        m_url = url + str(page_count)
        response = requests.get(m_url, auth=(user, pwd))
        print("Page " + str(page_count))
        if response.status_code != 200:
            print('Status:', response.status_code, 'Problem with the request. Exiting.')
            exit()
        data = response.json()
        tickets_list = data['tickets']
        for ticket in tickets_list:
            print(ticket['id'])

            # ticket_data = {}
            t_id = ticket['id']
            t_subject = ticket['subject']
            try:
                if ticket['via']['source']['from']['address']:
                    t_from_add = ticket['via']['source']['from']['address']
                else:
                    t_from_add = 'NA'
            except KeyError:
                t_from_add = 'NA'

            try:
                if ticket['via']['source']['from']['name']:
                    t_from_name = ticket['via']['source']['from']['name']
                else:
                    t_from_name = 'NA'
            except KeyError:
                t_from_name = 'NA'

            try:
                if ticket['via']['source']['to']['address']:
                    t_to_add = ticket['via']['source']['to']['address']
                else:
                    t_to_add = 'NA'
            except KeyError:
                t_to_add = 'NA'

            try:
                if ticket['via']['source']['to']['name']:
                    t_to_name = ticket['via']['source']['to']['name']
                else:
                    t_to_name = 'NA'
            except KeyError:
                t_to_name = 'NA'

            if ticket_comments(ticket['id']):
                t_comments = ticket_comments(ticket['id'])
            else:
                t_comments = 'NA'

            ticket_data = {
                'id': t_id,
                'created_at': ticket['created_at'],
                'status': ticket['status'],
                'subject': t_subject,
                'from_address': t_from_add,
                'from_name': t_from_name,
                'to_address': t_to_add,
                'to_name': t_to_name,
                'comments': t_comments,

            }
            create_pdf(ticket_data)
            # exit(123)
        page_count = page_count + 1
    # exit(123)


# Example 1: Print the name of the first group in the list
# print('First group = ', data['groups'][0]['name'])

# Example 2: Print the name of each group in the list
# group_list = data['groups']
# for group in group_list:
#     print(group['name'])

get_tickets()
