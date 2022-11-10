import functions_framework

@functions_framework.http
def hello(request):
    return "Hello world!"

@functions_framework.cloud_event
def hello_cloud_event(cloud_event):
   print(f"Received event with ID: {cloud_event['id']} and data {cloud_event.data}")