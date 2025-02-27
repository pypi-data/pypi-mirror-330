# Bedrock Syntaxer

A utility to force AWS Bedrock to apply the given syntax to its response.

## Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

### Function: `bedrock_syntaxer`

A utility to force Bedrock to apply the given syntax to its response.

#### Parameters:

- `model_id` (str): The model ID of the Bedrock model.
- `messages` (list): The messages to send to Bedrock.
- `syntax` (str): The syntax to apply to the response.
- `inference_config` (dict, optional): The inference configuration to use.
- `region_name` (str, optional): The region name of the Bedrock model.

#### Returns:

- `str`: The response from Bedrock with the syntax applied.

### Example

```python
from bedrock_syntaxer import bedrock_syntaxer
import json

ACCOUNT_ID = "961341532715"
REGION = "us-east-1"
MODEL_NAME = "claude-3-5-sonnet-20241022-v2:0"
MODEL_ID = f"arn:aws:bedrock:{REGION}:{ACCOUNT_ID}:inference-profile/us.anthropic.{MODEL_NAME}"

prompt = (
    "Write the definition of 3 Filipino word in JSON format. "
    "The words are 'kamusta', 'salamat', and 'paalam'."
    "Use the keys 'word' and 'definition'."
)
messages = [{"role": "user", "content": [{"text": prompt}]}]

response = bedrock_syntaxer(
    model_id=MODEL_ID,
    messages=messages,
    syntax="json",
    region_name=REGION,
)

print(response)

# The response is a JSON string.
response_json = json.loads(response)
```

## Testing

To run the tests, use:

```bash
pytest
```
