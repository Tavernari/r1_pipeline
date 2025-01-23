import asyncio
import os
from pipeline import Pipeline

async def validate_pipeline(user_input: str):
    # Initialize the pipeline
    pipeline = Pipeline()
    
    # Check if DEEPSEEK_API_KEY is set
    if os.getenv('DEEPSEEK_API_KEY') is None:
        print("Error: DEEPSEEK_API_KEY environment variable is not set")
        return
    
    try:
        # Call startup to initialize the client
        await pipeline.on_startup()
        
        # Prepare test messages
        messages = []
        
        # Execute the pipeline
        response = pipeline.pipe(
            user_message=user_input,
            model_id="deepseek-chat",
            messages=messages,
            body={}
        )
        
        print("Pipeline Response:")
        print(response)
        
    except Exception as e:
        print(f"Error occurred while running the pipeline: {str(e)}")
    finally:
        # Ensure we properly shut down
        await pipeline.on_shutdown()

def main():
    # Get user input
    user_input = input("Enter your message to test the pipeline: ")
    
    # Run the async validation
    asyncio.run(validate_pipeline(user_input))

if __name__ == "__main__":
    main()