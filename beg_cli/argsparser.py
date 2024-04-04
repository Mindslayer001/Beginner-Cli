import json
import google.generativeai as genai
import os
import configparser
import typer
from tabulate import tabulate

# Define the configuration file path
CONFIG_FILE = 'config.ini'

# Load or create the configuration file
config = configparser.ConfigParser()

# If the configuration file exists, load it
if os.path.exists(CONFIG_FILE):
    config.read(CONFIG_FILE)

# If the configuration file doesn't exist or doesn't contain the API key, prompt the user to enter it
if 'GENAI' not in config or 'api_key' not in config['GENAI']:
    api_key = input("Enter your GenAI API key: ")
    config['GENAI'] = {'api_key': api_key}

    # Write the API key to the configuration file
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
else:
    # Get the API key from the configuration file
    api_key = config['GENAI']['api_key']

genai.configure(api_key=api_key) 
model = genai.GenerativeModel('gemini-pro')

app = typer.Typer()

# Error message format
ERROR_MESSAGE = "The command you provided does not appear to be a Linux command. Please check for spelling mistakes or provide a valid Linux command."

def parse_json(json_data, parser_function, query):
    print("""
 _______                       __                                                 ______   __       ______ 
/       \                     /  |                                               /      \ /  |     /      |
$$$$$$$  |  ______    ______  $$/  _______   _______    ______    ______        /$$$$$$  |$$ |     $$$$$$/ 
$$ |__$$ | /      \  /      \ /  |/       \ /       \  /      \  /      \       $$ |  $$/ $$ |       $$ |  
$$    $$< /$$$$$$  |/$$$$$$  |$$ |$$$$$$$  |$$$$$$$  |/$$$$$$  |/$$$$$$  |      $$ |      $$ |       $$ |  
$$$$$$$  |$$    $$ |$$ |  $$ |$$ |$$ |  $$ |$$ |  $$ |$$    $$ |$$ |  $$/       $$ |   __ $$ |       $$ |  
$$ |__$$ |$$$$$$$$/ $$ \__$$ |$$ |$$ |  $$ |$$ |  $$ |$$$$$$$$/ $$ |            $$ \__/  |$$ |_____ _$$ |_ 
$$    $$/ $$       |$$    $$ |$$ |$$ |  $$ |$$ |  $$ |$$       |$$ |            $$    $$/ $$       / $$   |
$$$$$$$/   $$$$$$$/  $$$$$$$ |$$/ $$/   $$/ $$/   $$/  $$$$$$$/ $$/              $$$$$$/  $$$$$$$$/$$$$$$/ 
                    /  \__$$ |                                                                             
                    $$    $$/                                                                              
                     $$$$$$/                                                                               
""")
    print("Author: https://github.com/Mindslayer001")
    try:
        data = json.loads(json_data)
        parser_function(data, query)
    except Exception as e:
        print(f"An error occurred while parsing JSON data: {e}")

def info_parser(data, query):
    try:
        command_data = data[query][0]
        table_data = []
        table_data.append(["Syntax", command_data["syntax"]])
        table_data.append(["Description", command_data["description"]])
        print(tabulate(table_data, tablefmt="fancy_grid"))

        # Adding options to the table
        table_data = []
        options = command_data["options"]
        for option, description in options.items():
            table_data.append([option, description])
        print(tabulate(table_data, headers=["Option", "Description"], tablefmt="grid"))

        # Adding examples to the table
        table_data = []
        for example in command_data["examples"]:
            table_data.append([example['command'], example['explanation']])

        print(tabulate(table_data, headers=["Example", "Explanation"], tablefmt="grid"))
    except KeyError:
        print(ERROR_MESSAGE)

def scenario_parser(data, query):
    try:
        # Access scenario
        scenario = data["scenario"]
        table_data = [["User Scenario", scenario]]
        print(tabulate(table_data, tablefmt="fancy_grid"))

        # Access commands
        table_data = []
        for command in data["commands"]:
            table_data.append([f"Command: {command['command']}", f"Description: {command['description']}"])

        print(tabulate(table_data, headers=["Parameter", "Description"], tablefmt="grid"))
    except KeyError:
        print(ERROR_MESSAGE)

@app.command()
def main(
    query: str = typer.Argument(None, help="Enter the text"),
    info: bool = typer.Option(False, "--info", "-i", help="Provide basic info and examples of the given command"),
    scenario: bool = typer.Option(False, "--scenario", "-s", help="Suggest commands based on the user scenario"),
):
    if query is None:
        query = typer.prompt("Enter the text")

    if info:
        format_ = """json{
        "mkdir": [{
            "syntax": "mkdir [options] directory_name...",
            "description": "Creates one or more directories (folders). If the directory already exists, an error message will be printed.",
            "options": {
                "-p": "Creates any necessary parent directories.",
                "-v": "Prints the name of each directory created.",
                "-m mode": "Sets the permissions of the new directory to the specified mode.",
                "-Z context": "Sets the SELinux security context of the new directory to the specified value."
            },
            "examples": [
                {
                    "command": "mkdir mydir",
                    "explanation": "Creates a directory named 'mydir'."
                },
                {
                    "command": "mkdir -p mydir/sub1/sub2",
                    "explanation": "Creates a directory named 'mydir' and any necessary parent directories."
                },
                {
                    "command": "mkdir -m 755 mydir",
                    "explanation": "Creates a directory named 'mydir' with permissions set to 755."
                },
                {
                    "command": "mkdir -Z context=user_home_t mydir",
                    "explanation": "Creates a directory named 'mydir' with the specified SELinux security context."
                }
            ]
        }
        ]
        }
        """
        modified_prompt = f"{format_} use the above format to give me explaination to this linux command {query} and make it easier to understand for first linux users and give me smaller description"
        response = model.generate_content([modified_prompt])
        response = response.text
        response = (response.replace("json", "").replace("JSON", "").lstrip("`").rstrip("`"))
        parse_json(response, info_parser, query)
    elif scenario:
        format_ = """
        json{
        "scenario": "I want to change the file write access to the admin only.",
        "commands": [
            {
                "description": "Using symbolic permissions",
                "command": "sudo chmod u=rw,go= /path/to/your/file"
            },
            {
                "description": "Using octal notation",
                "command": "sudo chmod 600 /path/to/your/file"
            },
            {
                "description": "Using symbolic permissions with shorthand",
                "command": "sudo chmod u+w /path/to/your/file && sudo chmod go= /path/to/your/file"
            },
            {
                "description": "Using symbolic permissions with absolute specification",
                "command": "sudo chmod u=rw,g=,o= /path/to/your/file"
            }
        ]
        }
        """
        modified_prompt = f"{format_} use the above format to give me {query}"
        response = model.generate_content([modified_prompt])
        response = response.text
        response = (response.replace("json", "").replace("JSON", "").lstrip("`").rstrip("`"))
        parse_json(response, scenario_parser, query)
    else:
        print("Please select one of the two options: -i for command explainer or -s for scenario-based command suggestion.")

if __name__ == "__main__":
    app()
