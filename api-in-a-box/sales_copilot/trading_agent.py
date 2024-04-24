from AgentSettings import AgentSettings
from AssistantAgent import AssistantAgent
from openai import AzureOpenAI
import yfinance as yf
import requests
import html

email_URI = None


def send_logic_apps_email(to: str, content: str) -> None:
    """This function sends an email using an Http endpoint implemented with Logic Apps"""
    # In this demo email was implemented using a Logic App with an HTTP trigger and M365 email action
    # Here are instructions on how to create an email endpoint using Logic Apps
    #   https://learn.microsoft.com/en-us/azure/app-service/tutorial-send-email?tabs=python
    try:
        json_payload = {"to": to, "content": html.unescape(content)}
        headers = {"Content-Type": "application/json"}
        response = requests.post(email_URI, json=json_payload, headers=headers)
        if response.status_code == 202:
            print("Email sent to: " + json_payload["to"])
    except:
        print("Failed to send email via Logic Apps")


def get_stock_price(symbol: str) -> float:
    """This function gets the latest stock price based on a ticker symbol"""
    stock = yf.Ticker(symbol)
    return stock.history(period="1d")["Close"].iloc[-1]


def call_functions(client, thread, run):
    """This function is delegate function that is called when the Assistant needs to make function calls"""
    print("Function Calling")
    
    # Implement the function calling logic here

    print("Submitting outputs back to the Assistant...")
    client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=tool_outputs
    )


tools_list = [
    {"type": "code_interpreter"},
    {
        # Define the function specification for the get_stock_price function
    },   

DATA_FOLDER = None


def get_agent(settings=None, client=None):
    """This function creates a trading Assistants API agent"""

    if settings is None:
        settings = AgentSettings()

    if client is None:
        client = AzureOpenAI(
            api_key=settings.api_key,
            api_version=settings.api_version,
            azure_endpoint=settings.api_endpoint)

    email_URI = settings.email_URI

    agent = AssistantAgent(settings,
                           client,
                           "Trading Agent", "You are an agent that can help get the latest stock prices and perform investment related calculations.",
                           DATA_FOLDER, tools_list, fn_calling_delegate=call_functions)

    return agent
