# Databricks docs RAG Agent integrated with Slack
This is a RAG agent that uses Databricks tools like Vector Search, Model Serving and Databricks Apps to create a Slack Bot that answers Databricks questions based on the official docs. A few of the configurations involve UI interactions in Slack and Databricks, but each step is documented here.
<br><br>
<img src="https://github.com/PSPedro176/databricks_rag_docs/blob/rag_bot/images/architecture?raw=true" width="1000px" style="float:right"/>
### Creating the RAG Agent
1. Define a target catalog and schema to the project, and save the names in the variables `CATALOG` and `SCHEMA` in the script `create_configs`
2. Execute the job `databricks_docs_update`: `create_configs` -> `update_docs` -> `embedding_config` -> `deploy_model`
3. After the execution of all the notebooks, go the catalog, find the deployed model and save the endpoint name. It is going to be a parameter to the Databricks App
### Configuring the Slack API
1. Go to the [Slack API](https://api.slack.com/) page and create a bot
1. In the Bot page, go to **OAuth & Permissions -> Scopes -> Bot Token Scopes**, and enable the following scopes:
  - `app_mentions:read`
  - `channels:join`
  - `channels:read`
  - `chat:write`
2. Go to **Socket Mode** and enable it
3. In **Event Subscriptions**:
  - Enable it
  - Add `app_mention` in "Subscribe to bot events"
4. Save/take note of the following tokens:
  - Signing Secret and App-Level token created in (2), both available in **Basic Information**
  - Bot User OAuth Token, available in **OAuth & Permissions**
### Configuring the Databricks Apps
1. Go to "Compute" and create a new app
2. Add the model serving endpoint as an app resource
3. Add the previously saved tokens and the endpoint name in the file `app.yaml`:
  ```yaml
  command:
  - python
  - bot.py
  env:
      - name: BOT_TOKEN
        value: xoxb-token
      - name: SIGN_SECRET
        value: sign_secret
      - name: APP_TOKEN
        value: xapp-token
      - name: RAG_ENDPOINT_NAME
        value: rag-endpoint-name
  ```
4. Deploy the app