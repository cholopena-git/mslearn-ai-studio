import os
import asyncio
from dotenv import load_dotenv

# import namespaces for async
from openai import AsyncAzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

async def main(): 

    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings 
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")
        
        # Azure OpenAI requires an API version
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-08-07")

        # Initialize an async OpenAI client
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://ai.azure.com/.default"
        )
        
        openai_client = OpenAI(
            base_url=azure_openai_endpoint,
            api_key=token_provider
        )   
        
        openai_client = AsyncAzureOpenAI(
            azure_endpoint=azure_openai_endpoint,
            azure_ad_token_provider=token_provider,
            api_version=api_version
        )

        # Track responses
        last_response_id = None

        # Loop until the user wants to quit
        while True:
            input_text = input('\nEnter a prompt (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text.strip()) == 0:
                print("Please enter a prompt.")
                continue

            # Await an asynchronous response
            completion = await openai_client.chat.completions.create(
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
            
            print(completion.choices[0].message.content)

    except Exception as ex:
        print(f"An error occurred: {ex}")

    finally:
        # Close the async client session safely
        if 'openai_client' in locals():
            await openai_client.close()

if __name__ == '__main__': 
    asyncio.run(main())