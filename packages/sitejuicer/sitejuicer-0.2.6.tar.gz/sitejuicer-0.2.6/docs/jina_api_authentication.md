# Jina Reader API Authentication

This document outlines the authentication process for the Jina Reader API when using SiteJuicer.

## API Key Format

The Jina Reader API uses bearer token authentication. API keys have the following format:

```
jina_XXXXXXXXXXXXXXXXXXXXXXXX_XXXXXXXXXXXXXXXX
```

For example: `jina_2caa021406de46c7837bc05cce50e14d_qcv8AqU_xS_fCtKz3nJ2qS5IcDk`

The key always starts with the prefix `jina_` followed by two segments of alphanumeric characters separated by an underscore.

## Setting Up Your API Key

There are several ways to set up your Jina Reader API key:

### 1. Environment Variable

Set the `JINA_API_KEY` environment variable:

**Linux/macOS:**
```bash
export JINA_API_KEY=jina_XXXXXXXXXXXXXXXXXXXXXXXX_XXXXXXXXXXXXXXXX
```

**Windows:**
```cmd
set JINA_API_KEY=jina_XXXXXXXXXXXXXXXXXXXXXXXX_XXXXXXXXXXXXXXXX
```

### 2. Configuration File

Update the configuration file located at `~/.sitejuicer/config.ini`:

```ini
[api]
jina_api_key = jina_XXXXXXXXXXXXXXXXXXXXXXXX_XXXXXXXXXXXXXXXX
```

### 3. Programmatically

When using SiteJuicer in your Python code, you can pass the API key directly:

```python
from core import fetch_content

options = {
    "api_key": "jina_XXXXXXXXXXXXXXXXXXXXXXXX_XXXXXXXXXXXXXXXX",
    "main_content_only": True,
    "content_format": "markdown"
}

result = fetch_content("https://example.com", options)
```

## Implementation Details

The `fetch_content` function in `core.py` has been updated to support the new API key format. The key changes include:

1. Bearer token authentication in the request headers
2. Validation of the API key format (checking for the `jina_` prefix)
3. Warning messages for incorrect API key formats

Here's how the authentication is implemented:

```python
# Check if the API key has the correct format (starts with jina_)
if api_key.startswith('jina_'):
    headers["Authorization"] = f"Bearer {api_key}"
else:
    print(f"Warning: API key does not have the expected format (should start with 'jina_'). Authentication may fail.", file=sys.stderr)
    # Still try to use it as a Bearer token
    headers["Authorization"] = f"Bearer {api_key}"
```

## Verifying Authentication

You can verify that your API key is working correctly by running the validation script:

```bash
export JINA_API_KEY=jina_XXXXXXXXXXXXXXXXXXXXXXXX_XXXXXXXXXXXXXXXX
python test_api_changes.py
```

If successful, you should see output similar to:

```
Testing fetch_content with URL: https://example.com
Using API key: jina_XXXX...XXXX

Fetch Content Result Summary:
Title: Example Domain
URL: https://example.com
Content length: 310

Content preview:
[Content preview will be shown here]

All tests passed!
```

## Troubleshooting

If you encounter authentication issues, check the following:

1. **Verify API Key Format**: Ensure your API key starts with `jina_` and follows the correct format.

2. **Check Environment Variable**: Confirm that the `JINA_API_KEY` environment variable is set correctly:
   ```bash
   echo $JINA_API_KEY
   ```

3. **Inspect Configuration File**: Verify the contents of your configuration file:
   ```bash
   cat ~/.sitejuicer/config.ini
   ```

4. **API Response**: When authentication fails, the API typically returns a JSON error message:
   ```json
   {
     "error": "Invalid API key"
   }
   ```

5. **Debug Mode**: Run your script with debug output to see the full request and response:
   ```bash
   DEBUG=1 python your_script.py
   ```

## Migrating from Old API Key Format

If you're migrating from an older version of SiteJuicer that used a different API key format, you'll need to:

1. Obtain a new API key in the format `jina_XXXXXXXXXXXXXXXXXXXXXXXX_XXXXXXXXXXXXXXXX`
2. Update your environment variables, configuration files, or code to use the new key
3. Run the validation script to verify the new key works correctly

For any issues or questions about API authentication, please contact support or open an issue on the project repository. 