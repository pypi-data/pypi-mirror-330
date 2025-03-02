# Automations

Types:

```python
from ittybit.types import AutomationCreateResponse, AutomationDeleteResponse
```

Methods:

- <code title="post /automations">client.automations.<a href="./src/ittybit/resources/automations.py">create</a>() -> <a href="./src/ittybit/types/automation_create_response.py">AutomationCreateResponse</a></code>
- <code title="delete /automations/:id">client.automations.<a href="./src/ittybit/resources/automations.py">delete</a>() -> <a href="./src/ittybit/types/automation_delete_response.py">AutomationDeleteResponse</a></code>

# Files

Types:

```python
from ittybit.types import FileCreateResponse, FileListResponse, FileUploadResponse
```

Methods:

- <code title="post /files">client.files.<a href="./src/ittybit/resources/files.py">create</a>(\*\*<a href="src/ittybit/types/file_create_params.py">params</a>) -> <a href="./src/ittybit/types/file_create_response.py">FileCreateResponse</a></code>
- <code title="get /files/{id}">client.files.<a href="./src/ittybit/resources/files.py">retrieve</a>(id) -> None</code>
- <code title="put /files/{id}">client.files.<a href="./src/ittybit/resources/files.py">update</a>(id, \*\*<a href="src/ittybit/types/file_update_params.py">params</a>) -> None</code>
- <code title="get /files">client.files.<a href="./src/ittybit/resources/files.py">list</a>(\*\*<a href="src/ittybit/types/file_list_params.py">params</a>) -> <a href="./src/ittybit/types/file_list_response.py">FileListResponse</a></code>
- <code title="delete /files/{id}">client.files.<a href="./src/ittybit/resources/files.py">delete</a>(id) -> None</code>
- <code title="put /files/upload">client.files.<a href="./src/ittybit/resources/files.py">upload</a>(\*\*<a href="src/ittybit/types/file_upload_params.py">params</a>) -> <a href="./src/ittybit/types/file_upload_response.py">FileUploadResponse</a></code>

# Logs

Types:

```python
from ittybit.types import LogRetrieveResponse, LogListResponse
```

Methods:

- <code title="get /logs/:id">client.logs.<a href="./src/ittybit/resources/logs.py">retrieve</a>() -> <a href="./src/ittybit/types/log_retrieve_response.py">LogRetrieveResponse</a></code>
- <code title="get /logs">client.logs.<a href="./src/ittybit/resources/logs.py">list</a>() -> <a href="./src/ittybit/types/log_list_response.py">LogListResponse</a></code>

# Events

Types:

```python
from ittybit.types import EventRetrieveResponse, EventListResponse
```

Methods:

- <code title="get /events/:id">client.events.<a href="./src/ittybit/resources/events.py">retrieve</a>() -> <a href="./src/ittybit/types/event_retrieve_response.py">EventRetrieveResponse</a></code>
- <code title="get /events">client.events.<a href="./src/ittybit/resources/events.py">list</a>() -> <a href="./src/ittybit/types/event_list_response.py">EventListResponse</a></code>

# Media

Types:

```python
from ittybit.types import MediaCreateResponse, MediaDeleteResponse, MediaIntelligenceResponse
```

Methods:

- <code title="post /media">client.media.<a href="./src/ittybit/resources/media.py">create</a>() -> <a href="./src/ittybit/types/media_create_response.py">MediaCreateResponse</a></code>
- <code title="delete /media/:id">client.media.<a href="./src/ittybit/resources/media.py">delete</a>() -> <a href="./src/ittybit/types/media_delete_response.py">MediaDeleteResponse</a></code>
- <code title="get /media/:id/intelligence">client.media.<a href="./src/ittybit/resources/media.py">intelligence</a>() -> <a href="./src/ittybit/types/media_intelligence_response.py">MediaIntelligenceResponse</a></code>

# Projects

Types:

```python
from ittybit.types import ProjectListResponse
```

Methods:

- <code title="post /projects/{id}">client.projects.<a href="./src/ittybit/resources/projects.py">create</a>(id, \*\*<a href="src/ittybit/types/project_create_params.py">params</a>) -> None</code>
- <code title="get /projects/{id}">client.projects.<a href="./src/ittybit/resources/projects.py">retrieve</a>(id) -> None</code>
- <code title="get /projects">client.projects.<a href="./src/ittybit/resources/projects.py">list</a>() -> <a href="./src/ittybit/types/project_list_response.py">ProjectListResponse</a></code>
- <code title="delete /projects/{id}">client.projects.<a href="./src/ittybit/resources/projects.py">delete</a>(id) -> None</code>

# Tasks

Types:

```python
from ittybit.types import TaskCreateResponse, TaskRetrieveResponse, TaskConfigResponse
```

Methods:

- <code title="post /tasks">client.tasks.<a href="./src/ittybit/resources/tasks.py">create</a>(\*\*<a href="src/ittybit/types/task_create_params.py">params</a>) -> <a href="./src/ittybit/types/task_create_response.py">TaskCreateResponse</a></code>
- <code title="get /tasks/:id">client.tasks.<a href="./src/ittybit/resources/tasks.py">retrieve</a>() -> <a href="./src/ittybit/types/task_retrieve_response.py">TaskRetrieveResponse</a></code>
- <code title="get /tasks/config">client.tasks.<a href="./src/ittybit/resources/tasks.py">config</a>() -> <a href="./src/ittybit/types/task_config_response.py">TaskConfigResponse</a></code>

# Webhooks

Types:

```python
from ittybit.types import WebhookCreateResponse, WebhookUpdateResponse
```

Methods:

- <code title="post /webhooks">client.webhooks.<a href="./src/ittybit/resources/webhooks.py">create</a>() -> <a href="./src/ittybit/types/webhook_create_response.py">WebhookCreateResponse</a></code>
- <code title="patch /webhooks/:id">client.webhooks.<a href="./src/ittybit/resources/webhooks.py">update</a>() -> <a href="./src/ittybit/types/webhook_update_response.py">WebhookUpdateResponse</a></code>
