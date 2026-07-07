import os
import asyncio
from dotenv import load_dotenv

# Import standard AsyncOpenAI for Serverless deployments
from openai import AsyncOpenAI
from azure.identity import DefaultAzureCredential

async def main(): 

    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Force reload the .env file
        load_dotenv(override=True)
        
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")
        
        print(f"\nDEBUG - Endpoint being used: {endpoint}")
        print(f"DEBUG - Model being used: {model_deployment}\n")

        # For Serverless endpoints, we generate a token directly
        credential = DefaultAzureCredential()
        token = credential.get_token("https://cognitiveservices.azure.com/.default").token
        
        # Initialize the STANDARD async OpenAI client, pointing to your Azure endpoint
        openai_client = AsyncOpenAI(
            base_url=endpoint,
            api_key=token
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