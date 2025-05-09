# DABs CI/CD Pipeline Example with GitHub Actions

This example demonstrates how to set up a CI/CD pipeline for deploying Databricks resources such as jobs and pipelines using **[Databricks Asset Bundles (DABs)](https://docs.databricks.com/en/dev-tools/bundles/index.html)** with GitHub repository and GitHub Actions.

## Solution Introduction

This solution uses GitHub Actions workflows to implement a CI/CD pipeline for Databricks Asset Bundles. The CI/CD pipeline retrieves the Databricks PAT tokens from GitHub Secrets to authenticate to the target workspaces. It then deploys sample Databricks jobs and pipelines using the Databricks bundle template and Python sample code from this repository.

The Python notebooks and pipelines used in this sample solution are **basic examples** that can be directly obtained using the databricks bundle init command. This solution aims to demonstrate how to deploy and integrate Databricks Asset Bundles within a GitHub Actions CI/CD pipeline. For more complex ML solutions, please refer to other Databricks ML references, such as the Databricks MLOps stack.

## Prerequisites

1. All Databricks workspaces (development workspace, QA workspace, and Prod workspace) and PAT tokens used in this solution are created separately.
2. The GitHub repository must be configured with appropriate secrets for Databricks workspace URLs and PAT tokens.
3. The workspaces used in this demo must have access to the public internet to run `pip install` for downloading public resources, such as [nutter](https://github.com/microsoft/nutter).
4. For the introduction to Databricks Asset Bundles and Databricks CLI, please refer to:
    - [Databricks Asset Bundles Documentation](https://docs.databricks.com/en/dev-tools/bundles/index.html)
    - [Databricks CLI Installation Guide](https://docs.databricks.com/en/dev-tools/cli/install.html)

## Workspace Authentication

Databricks [personal access tokens (PATs)](https://docs.databricks.com/en/dev-tools/auth/pat.html) are used to authenticate the GitHub Actions workflow to Databricks workspaces. The PAT tokens are stored as GitHub Secrets.

For both QA and production environments, you'll need to create the following GitHub Secrets:
- `DB_QA_HOST`: The URL of your QA Databricks workspace
- `DB_QA_TOKEN`: The Databricks Personal Access Token for the QA workspace
- `DB_PROD_HOST`: The URL of your production Databricks workspace
- `DB_PROD_TOKEN`: The Databricks Personal Access Token for the production workspace

We recommend creating Databricks PATs with an expiration date. Using access tokens set to never expire is highly not recommended, because this significantly increases the risk of token misuse or compromise.

## High-level Architecture Diagram

```
┌─────────────────┐     ┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│  GitHub         │     │ GitHub Actions │     │  GitHub        │     │  GitHub        │
│  Repository     │────▶│ Workflow       │────▶│  Environment   │────▶│  Environment   │
│  (Code Source)  │     │ (CI/CD)        │     │  (QA)          │     │  (Production)  │
└─────────────────┘     └────────────────┘     └────────────────┘     └────────────────┘
                                                       │                      │
                                                       ▼                      ▼
┌────────────────┐                             ┌────────────────┐     ┌────────────────┐
|  (optional)    |                             │  Databricks    │     │  Databricks    │
│  dev workspace │                             │  QA Workspace  │     │  Prod Workspace│
└────────────────┘                             └────────────────┘     └────────────────┘
```

## High-level Workflow

1. Users can use DABs `databricks bundle` commands to deploy the code from their local development environment to a development Databricks workspace, and use this workspace to develop the notebook code and the DABs YAML template code.
     - ( *Optional* ) Users can also directly associate the development workspace with the GitHub repository using the [Databricks Git integration](https://docs.databricks.com/en/repos/index.html) to push code or create pull requests.
2. After development and debugging, users can push the local DABs folder/code to the GitHub repository, and then merge the code into the target branch (e.g., "main") via a Pull Request.
3. Once the PR is merged into the target branch, it triggers the GitHub Actions workflow.
4. In the QA stage of the GitHub Actions workflow, the pipeline retrieves the QA workspace PAT token from GitHub Secrets for authentication and deploys the resources defined in the DABs template to the QA workspace. In this sample solution, the QA stage also runs nutter tests to perform a sample test on one of the notebook functions.
5. If the QA stage completes successfully, it moves to the Production stage. The Production stage is configured as a separate environment in GitHub Actions with required reviewers, which acts as a manual approval gate.
6. Upon approval, the Production stage retrieves the Prod workspace PAT token and deploys the resources defined in the DABs template to the Prod workspace, such as jobs or DLT pipelines.

## Setup Instructions

1. **Fork or Clone this Repository**:
   - Create your own copy of this repository by forking or cloning it.

2. **Configure GitHub Secrets**:
   - Go to your repository Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `DB_QA_HOST`: The URL of your QA Databricks workspace (e.g., `https://your-qa-workspace.cloud.databricks.com`)
     - `DB_QA_TOKEN`: The Databricks Personal Access Token for the QA workspace
     - `DB_PROD_HOST`: The URL of your production Databricks workspace
     - `DB_PROD_TOKEN`: The Databricks Personal Access Token for the production workspace

3. **Configure GitHub Environments**:
   - Go to your repository Settings → Environments
   - Create two environments:
     - `qa`: No protection rules needed (or add as desired)
     - `production`: Add protection rules such as "Required reviewers" to enforce manual approval

4. **Update the Databricks Configuration**:
   - Modify the `databricks.yml` file to match your workspace configurations and desired resources.
   - Update the resources YAML files in the `resources/` directory as needed.

5. **Commit and Push to the Main Branch**:
   - Once your changes are ready, commit and push them to the main branch.
   - This will trigger the GitHub Actions workflow.

6. **Monitor the Workflow**:
   - Go to the "Actions" tab in your GitHub repository to monitor the workflow execution.
   - You can see the logs for each step of the process.
   - You'll see each workflow step and its status (success/failure) including installation, deployment, and test execution.

7. **Approve Production Deployment**:
   - Once the QA stage completes successfully, you'll need to approve the production deployment.
   - Go to the running workflow and you'll see a "Review deployments" button in the production job.
   - Click the button to review details and approve the deployment to the production environment.

8. **Verify Deployed Resources**:
   - After the workflow completes, verify the deployed resources in your Databricks workspaces.
   - Check both QA and Production environments to ensure all resources were deployed correctly.

## Unit Testing

This repository includes unit testing capabilities both locally and in Databricks workspaces.

### Local Unit Testing

A GitHub Actions workflow is defined in `.github/workflows/unit-tests.yml` that runs unit tests locally in the GitHub Actions environment:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run the tests
python -m pytest tests/ -v
```

### Databricks Workspace Unit Testing

This solution also provides the ability to run unit tests directly in Databricks workspaces, which has several advantages:
- Tests run in the same environment where your code will be deployed
- Access to Databricks-specific features and APIs
- Test results stored in DBFS for persistence and review

#### Running Unit Tests in Databricks

There are two ways to run unit tests in Databricks:

1. **Through GitHub Actions Workflow**:
   - Go to the "Actions" tab in your GitHub repository
   - Select the "Databricks Workspace Unit Tests" workflow
   - Click "Run workflow"
   - Choose the target environment (qa or prod)
   - Click "Run workflow" to execute the tests in the selected Databricks workspace

2. **Directly in Databricks Workspace**:
   - Deploy the DABs bundle to your Databricks workspace:
     ```bash
     databricks bundle deploy -t qa
     ```
   - Trigger the unit test job from the Databricks Jobs UI or using the CLI:
     ```bash
     databricks bundle run -t qa unittest-job
     ```

#### Test Results

Unit test results are stored in both locations:
- Test outputs are shown in the Databricks job run logs
- HTML test reports are saved to `/dbfs/databricks/unittest-results/` for detailed review
- JSON results summary is stored in the same location for programmatic access

#### Customizing Tests

To add or modify tests:

1. Edit the `src/unittest_notebook.py` file to add new test cases
2. For more extensive test suites, create separate test modules and import them in the test notebook
3. Update the `resources/unittest_job.yml` configuration if you need to change job settings

## Clean Up

1. Delete the resources created in the Databricks workspace, either through the console or using the Databricks CLI.
2. If you no longer need the GitHub repository, you can archive or delete it.

## Reference

1. [What are Databricks Asset Bundles?](https://docs.databricks.com/en/dev-tools/bundles/index.html)
2. [Databricks Asset Bundles for MLOps Stacks](https://docs.databricks.com/en/dev-tools/bundles/mlops-stacks.html)
3. [GitHub Actions Documentation](https://docs.github.com/en/actions)
4. [GitHub Environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
5. [Databricks CLI Installation Guide](https://docs.databricks.com/en/dev-tools/cli/install.html)
6. [Pytest Documentation](https://docs.pytest.org/)
7. [Running Python Tests in Databricks](https://docs.databricks.com/en/delta-live-tables/testing.html)