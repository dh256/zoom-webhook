# webhook
A Flask application (running in Azure Web App) that provides a Webhook to process Zoom events.

## Requirements:
- VS Code with Python development environment
- Azure Tools Extension Pack (VSCode)
- Zoom account (with admin access to Zoom Portal)
- Azure account with subscription

Note: All instructions below are for macOS. Please make necessary changes for your specific environment (Windows, Linux)

## References:
- Zoom Webhooks: https://developers.zoom.us/docs/api/rest/webhook-reference/ 
- Publishing a Python Flask app to Azure: https://learn.microsoft.com/en-us/azure/app-service/quickstart-python?toc=%2Fazure%2Fdeveloper%2Fpython%2Ftoc.json&bc=%2Fazure%2Fdeveloper%2Fpython%2Fbreadcrumb%2Ftoc.json&tabs=flask%2Cwindows%2Cvscode-aztools%2Cvscode-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli 

## VSCode
1. Install the Azure Tools extension pack
2. Sign into Azure using an account with an Azure Subscription

## Python
1. Create a Python Virtual environment (python -m venv .)
2. Activate virtual environment (. bin/activate) 
3. Install flask (pip install flask)
4. Create app.py and add Flask code needed to accept a Zoom webhook event
5. Test locally (using Postman to submit test events to webhook) and make sure working (as far as possible)
6. Publish app to Azure and again use Postman to submit test events to Azure hosted webhook

Create Azure App Service Web App:
- In VSCode Azure Tools, right click on Azure Subscripton and select Create Resource
- Resource type: Create App Service Web App
- Provide a (globally unique) name e.g.: _zoomwebhook_

Note: Azure endpoint is _https://zoomwebhook.azurewebsites.net_

- Select Runtime: Python 3.12
- Select Pricing Tier: Basic (this is free)
- Your new resource is now created (takes a few minutes)
- Can view and manage under _App Services_ (in Resources view)
- Check app is up and running by visiting: https://zoomwebhook.azurewebsites.net - you will get a _Hello_ message in your browser.
- To Deploy app:
- Right click on zoomwebhook service and select _Deploy to Web App_


## Zoom
1. In Zoom configure Webhooks to point at your Azure hosted webhook
2. Get the shared secret and make sure this is available to Flask app in Azure (may need to update app in Azure). You can do this by adding SECRET_TOKEN to Application Settings in your web app.
3. Use Zoom client to perform some Zoom actions (e.g. joining a call) and make sure that associated webhook event is sent to the Azure hosted Webhook (check the Azure Web App Log Stream)



