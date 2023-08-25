import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django import forms

import globus_sdk
from globus_portal_framework.gclients import load_globus_access_token


log = logging.getLogger(__name__)


class HelloFlowForm(forms.Form):
    """
    This is a Django form to control and validate user input fields.

    https://docs.djangoproject.com/en/4.2/topics/forms/

    Typically this would go into its own forms.py class, but it's added here for simplicity.
    """

    echo_string = forms.CharField(
        label="Echo String",
        initial="Hello World!",
        max_length=256,
        help_text="Something to echo inside the flow",
    )
    sleep_time = forms.IntegerField(help_text="How long to pause flow execution")
    label = forms.CharField(
        initial="An example run started via DGPF",
        max_length=256,
        help_text="A nice label to add context to this flow",
    )
    tags = forms.CharField(
        label="Tags",
        max_length=256,
        help_text="Tags help categorize many runs over time. You can use a comma separated list here.",
    )

    def clean_sleep_time(self):
        """Extra validation and a bit of fun"""
        if self.cleaned_data["sleep_time"] == 3:
            raise forms.ValidationError(
                "Value may not be '3'. This number is cursed and may not be used."
            )
        return self.cleaned_data["sleep_time"]


def index(request):
    """
    The simplest Django view, used to greet the user.
    """
    log.info(
        f"User hit main index page. Authenticated? {request.user.is_authenticated}"
    )
    return render(request, "index.html", {})


@login_required
def hello_flow(request):
    """
    This view is the heart of this project. It behaves a few different ways.
    First, it renders the form above in normal GET requests, and allows the user to
    populate it with values.

    When a user POSTs a valid form, it loads a _user_ access token and starts the flow
    as the user with the values they provide. The JSON response is given directly to
    the template, and used to build a link to the webapp to track progress.
    """
    context = {}
    if request.method == "POST":
        form = HelloFlowForm(request.POST)
        if form.is_valid():
            log.debug(f"Loading flow token for user {request.user.username}")
            token = load_globus_access_token(request.user, settings.FLOW_ID)
            authorizer = globus_sdk.AccessTokenAuthorizer(token)
            sfc = globus_sdk.SpecificFlowClient(settings.FLOW_ID, authorizer=authorizer)
            run = sfc.run_flow(
                body={
                    "input": {
                        "echo_string": form.cleaned_data["echo_string"],
                        "sleep_time": form.cleaned_data["sleep_time"],
                    },
                },
                label=form.cleaned_data["label"],
                tags=form.cleaned_data["tags"].split(","),
            )
            log.info(
                f"Flow started with run {run.data['run_id']} for user {request.user.username}"
            )
            return render(request, "hello-flow-started.html", run.data)
        log.debug(
            f"User {request.user.username} failed to start flow due to {len(form.errors)} form errors."
        )
    else:
        log.debug(f"Loading new form for user {request.user.username}")
        form = HelloFlowForm()
    context["form"] = form
    return render(request, "hello-flow.html", context)
