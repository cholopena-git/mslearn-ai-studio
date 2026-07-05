import os
from dotenv import load_dotenv

# Import namespaces
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def main(): 
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings 
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")
        
        # Azure OpenAI requires an API version
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-08-07") 

        # Initialize the Token Provider
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        )
    
        # Initialize the Azure OpenAI client
        openai_client = AzureOpenAI(
            azure_endpoint=azure_openai_endpoint,
            azure_ad_token_provider=token_provider,
            api_version=api_version
        )

        # Loop until the user wants to quit
        while True:
            input_text = input('\nEnter a prompt (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text.strip()) == 0:
                print("Please enter a prompt.")
                continue

            # Get a response
            completion = openai_client.chat.completions.create(
                model=model_deployment,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant that answers questions and provides information."
                    },
                    {
                        "role": "user",
                        "content": input_text
                    }
                ]
            )
            
            # This print statement is now properly indented inside the while loop!
            print(completion.choices[0].message.content)

    except Exception as ex:
        print(f"An error occurred: {ex}")

if __name__ == '__main__': 
    main()