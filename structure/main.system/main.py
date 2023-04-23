import argparse
import configparser
import os
import poe


# define command-line arguments
parser = argparse.ArgumentParser(description='Take a prompt from the user')
parser.add_argument('--prompt', type=str,
                    help='The prompt to take from the user', required=True)
parser.add_argument('--model-type', type=str, choices=['logical', 'creative'],
                    help='The type of model to use for generating the response', required=True)
args = parser.parse_args()

# extract arguments
PROMPT = args.prompt
MODEL_TYPE = args.model_type

# read credentials from config file
with open('structure/main.system/config.ini') as f:
    lines = f.readlines()
    credentials = [line.strip().split(":") for line in lines]

api_key = next(item[1] for item in credentials if item[0] == 'api')
logical = next(item[1] for item in credentials if item[0] == 'logical')
creative = next(item[1] for item in credentials if item[0] == 'creative')

# create Poe.com client
CLIENT = poe.Client(api_key)

# select model based on user input
if MODEL_TYPE == 'logical':
    MODEL = logical
else:
    MODEL = creative


# define function to send message
def send_message(prompt):
    for chunk in CLIENT.send_message(MODEL, prompt):
        pass
    response = chunk["text"]
    with open("structure/main.system/response.txt", "w") as f:
        f.write(response)
    with open("structure/main.system/check.txt", "w") as f:
        f.write("1")
    return response

send_message(PROMPT)