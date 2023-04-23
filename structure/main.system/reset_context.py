import argparse
import poe

# define command-line arguments
parser = argparse.ArgumentParser(description='Reset the context of the Poe.com client')
parser.add_argument('--model-type', type=str, choices=['logical', 'creative'],
                    help='The model to use for resetting the context', required=True)
args = parser.parse_args()

# extract arguments
MODEL = args.model_type

# read credentials from config file
with open('structure/main.system/config.ini') as f:
    lines = f.readlines()
    credentials = [line.strip().split(":") for line in lines]

api_key = next(item[1] for item in credentials if item[0] == 'api')
logical_model = next(item[1] for item in credentials if item[0] == 'logical')
creative_model = next(item[1] for item in credentials if item[0] == 'creative')

# create Poe.com client
client = poe.Client(api_key)

# select model based on user input
if MODEL == 'logical':
    model = logical_model
else:
    model = creative_model

# reset context using selected model
client.send_chat_break(model)