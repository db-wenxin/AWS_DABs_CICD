from databricks.sdk import WorkspaceClient

client = WorkspaceClient()
current_principal = client.current_user.me()
print("Hello, " + str(current_principal.user_name) + "!")