"""
Make sure you are part of the Globus Flows Users group so that you can deploy this flow,
or delete any prior flows before running this example.

Make sure also to install Gladier (pip install gladier)
"""
from gladier import GladierBaseClient
from pprint import pprint


class HelloWorldClient(GladierBaseClient):
    # Setting a group will give the group admin access to the flow.
    globus_group = "e4f05c93-cd9d-11ec-94f6-51db4d10f5bd"
    flow_definition = {
        "StartAt": "Hello",
        "States": {
            "Hello": {
                "ActionUrl": "https://actions.globus.org/hello_world",
                "Type": "Action",
                "Parameters": {
                    "echo_string.$": "$.input.echo_string",
                    "sleep_time.$": "$.input.sleep_time",
                },
                "End": True,
            }
        },
    }


if __name__ == "__main__":
    # Instantiate the client
    hello_world_client = HelloWorldClient()
    hello_world_client.sync_flow()
    fid = hello_world_client.get_flow_id()
    url = f"https://app.globus.org/flows/{fid}"
    print(f"Set this flow in your settings.py under FLOW_ID: {fid}")
    print(f"You can view the flow from the Globus Webapp here: {url}")

    # # Run the flow and track progress, if you want to test!
    # flow_input = {
    #     "input": {
    #         "echo_string": "hello_world",
    #         "sleep_time": 1
    #     }
    # }
    # flow = hello_world_client.run_flow(flow_input=flow_input, label="Schema Example")
    # run_id = flow["run_id"]
    # hello_world_client.progress(run_id)
    # pprint(hello_world_client.get_status(run_id))
