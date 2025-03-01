# cosmic_sdk
python package for cosmic


## Installation

```bash
pip install cosmic_sdk
```

## Example

```python
from cosmic_sdk.secrets import SecretsManager
from cosmic_sdk.connectors import PostHogService

secrets_manager = SecretsManager()

credentials = secrets_manager.get_secrets(org_id="org_123", connector_type="posthog")
posthog_service = PostHogService(credentials)

posthog_service.get_user_logins("2024-01-01")
```


# TODO
- [ ] Move to uv package manager 
- [ ] Support doc per connector 
- [ ] Add github actions deploy to pypi