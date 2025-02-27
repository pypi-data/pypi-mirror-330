# lifter-hub

# Build
```
pip install -r requirements.txt
```

```
python setup.py sdist bdist_wheel
```

# install from filesystem
```
pip install lifter-hub
```

# install from github
```
pip install lifter-hub

```

# Usage

```
from lifter import hub

# Initialize database (Choose "sqlite" or "postgres")
prompt_hub = hub.init(db_type="sqlite")  # or "postgres"

# Create a prompt
prompt_hub.create(
        prompt_type,
        description,
        system_message,
        human_message,
        structured_output,
        output_format
    )

# Retrieve a prompt
prompt = prompt_hub.pull(prompt_type)
print("Fetched prompt:", prompt)

# Update a prompt
prompt_hub.update(
        prompt_type,
        new_description,
        new_system_message,
        new_human_message,
        new_structured_output,
        new_output_format
    )
# Delete a prompt
prompt_hub.delete(prompt_type)
```