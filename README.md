## DGPF Flows Example

This repo serves as a minimalistic example for starting flows as part of a DGPF Portal.

Before you start, you need app credentials to run the portal. Create your [app credentials](https://app.globus.org/settings/developers/registration/confidential_client/select-project) inside dgpf_flows_example/`local_settings.py` with the following: 

```
SOCIAL_AUTH_GLOBUS_KEY = "key"
SOCIAL_AUTH_GLOBUS_SECRET = "secret"
```

1. Install requirements -- `pip install -r requirements.txt`
2. Create your flow -- `python create_flow.py`
3. Migrate your Django auth models -- `python manage.py migrate`
4. Start your server -- `python manage.py runserver`

After that, you can navigate through `http://localhost:8000/`, and start the flow you deployed in the step
above, as a user within the Django Portal. Note that only users within the Globus Group set on the flow
may run the flow. Runnable_by may also be modified via the webapp.