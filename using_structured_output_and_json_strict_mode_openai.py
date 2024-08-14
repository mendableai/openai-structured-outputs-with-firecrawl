# pip install firecrawl openai
# set FIRECRAWL_API_KEY and OPENAI_API_KEY environment variables


from firecrawl import FirecrawlApp
from openai import OpenAI
import os

# Initialize the FirecrawlApp with your API key
firecrawl_app = FirecrawlApp(api_key=os.environ['FIRECRAWL_API_KEY'])

# Scrape data from mendable.ai
url = 'https://mendable.ai'
scraped_data = firecrawl_app.scrape_url(url)

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY']
)

# Define the OpenAI API request
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant that extracts structured data from web pages."
    },
    {
        "role": "user",
        "content": f"Extract the headline and description from the following HTML content: {scraped_data['content']}"
    }
]

response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "extracted_data",
        "schema": {
            "type": "object",
            "properties": {
                "headline": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                }
            },
            "required": ["headline", "description"],
            "additionalProperties": False
        }
    }
}

# Call the OpenAI API to extract structured data
chat_completion = client.chat.completions.create(
    model="gpt-4o-mini-2024-07-18",
    messages=messages,
    response_format=response_format
)

# Extracted data
# Access the content of the first choice in the response
extracted_data = chat_completion.choices[0].message.content

# Print the extracted data
print(extracted_data)