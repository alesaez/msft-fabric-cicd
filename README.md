# Fabric CICD - Option 2 - Git-based deployment using Fabric Item API and GitHub Actions 

This repository uses the [Fabric Item APIs](https://learn.microsoft.com/en-us/rest/api/fabric/core/items/update-item) to publish and unpublish Fabric Items to a given workspace ID.

This script and GitHub Action uses a local copy of a Microsoft Fabric team Python named `fabric_cicd`. You can also use this locally and extend to other item types. Currently this repo only supports Environments, Data Pipelines and Notebooks.

> Original GitHub repo is here: [microsoft/fabric-cicd](https://github.com/microsoft/fabric-cicd)

The source code of the package located in this directory: `https://github.com/microsoft/fabric-cicd/tree/main/src/fabric_cicd` is copied in this repo here `/fabric_cicd` to be imported by `main.py` script.

The `main.py` script is launched by the GitHub Action.

## Workspace Items Directory

The workspace items are located in the `workspace` directory. This directory contains the following structure:

```
workspace
    ├───Hello World.Notebook
    ├───Run Hello World.DataPipeline
```

## Running the Script Locally

If necessary, you can run the script locally by executing `main.py`:

```bash
python main.py
```

Certain Fabric items doesn't support Service Principal or Managed Identity Authentication, for example, Data Pipelines can't use Service Principal, so you can run main.py locally and use your user credentials. 

## GitHub Actions Workflow

To automate the deployment of the Python code, you can use the GitHub Actions workflow in this repo. Make sure to add `AZURE_TENANT_ID` and  `AZURE_CLIENT_ID` as a variable and `AZURE_CLIENT_SECRET` as a [secret](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) in your GitHub repository settings.

This workflow has a required parameter `workspaceId` to input the specific workspace you want target/publish your Fabric Items at runtime. 
