# Completions

Types:

```python
from scale_gp_beta.types import Completion
```

Methods:

- <code title="post /v5/completions">client.completions.<a href="./src/scale_gp_beta/resources/completions.py">create</a>(\*\*<a href="src/scale_gp_beta/types/completion_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/completion.py">Completion</a></code>

# Chat

## Completions

Types:

```python
from scale_gp_beta.types.chat import ChatCompletion, ChatCompletionChunk, CompletionCreateResponse
```

Methods:

- <code title="post /v5/chat/completions">client.chat.completions.<a href="./src/scale_gp_beta/resources/chat/completions.py">create</a>(\*\*<a href="src/scale_gp_beta/types/chat/completion_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/chat/completion_create_response.py">CompletionCreateResponse</a></code>

# Inference

Types:

```python
from scale_gp_beta.types import InferenceResponse, InferenceResponseChunk, InferenceCreateResponse
```

Methods:

- <code title="post /v5/inference">client.inference.<a href="./src/scale_gp_beta/resources/inference.py">create</a>(\*\*<a href="src/scale_gp_beta/types/inference_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/inference_create_response.py">InferenceCreateResponse</a></code>

# Questions

Types:

```python
from scale_gp_beta.types import Question, QuestionList
```

Methods:

- <code title="post /v5/questions">client.questions.<a href="./src/scale_gp_beta/resources/questions.py">create</a>(\*\*<a href="src/scale_gp_beta/types/question_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/question.py">Question</a></code>
- <code title="get /v5/questions/{question_id}">client.questions.<a href="./src/scale_gp_beta/resources/questions.py">retrieve</a>(question_id) -> <a href="./src/scale_gp_beta/types/question.py">Question</a></code>
- <code title="get /v5/questions">client.questions.<a href="./src/scale_gp_beta/resources/questions.py">list</a>(\*\*<a href="src/scale_gp_beta/types/question_list_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/question.py">SyncCursorPage[Question]</a></code>

# QuestionSets

Types:

```python
from scale_gp_beta.types import QuestionSet, QuestionSetList, QuestionSetDeleteResponse
```

Methods:

- <code title="post /v5/question-sets">client.question_sets.<a href="./src/scale_gp_beta/resources/question_sets.py">create</a>(\*\*<a href="src/scale_gp_beta/types/question_set_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/question_set.py">QuestionSet</a></code>
- <code title="get /v5/question-sets/{question_set_id}">client.question_sets.<a href="./src/scale_gp_beta/resources/question_sets.py">retrieve</a>(question_set_id, \*\*<a href="src/scale_gp_beta/types/question_set_retrieve_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/question_set.py">QuestionSet</a></code>
- <code title="patch /v5/question-sets/{question_set_id}">client.question_sets.<a href="./src/scale_gp_beta/resources/question_sets.py">update</a>(question_set_id, \*\*<a href="src/scale_gp_beta/types/question_set_update_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/question_set.py">QuestionSet</a></code>
- <code title="get /v5/question-sets">client.question_sets.<a href="./src/scale_gp_beta/resources/question_sets.py">list</a>(\*\*<a href="src/scale_gp_beta/types/question_set_list_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/question_set.py">SyncCursorPage[QuestionSet]</a></code>
- <code title="delete /v5/question-sets/{question_set_id}">client.question_sets.<a href="./src/scale_gp_beta/resources/question_sets.py">delete</a>(question_set_id) -> <a href="./src/scale_gp_beta/types/question_set_delete_response.py">QuestionSetDeleteResponse</a></code>

# Files

Types:

```python
from scale_gp_beta.types import File, FileList, FileDeleteResponse
```

Methods:

- <code title="post /v5/files">client.files.<a href="./src/scale_gp_beta/resources/files/files.py">create</a>(\*\*<a href="src/scale_gp_beta/types/file_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/file.py">File</a></code>
- <code title="get /v5/files/{file_id}">client.files.<a href="./src/scale_gp_beta/resources/files/files.py">retrieve</a>(file_id) -> <a href="./src/scale_gp_beta/types/file.py">File</a></code>
- <code title="patch /v5/files/{file_id}">client.files.<a href="./src/scale_gp_beta/resources/files/files.py">update</a>(file_id, \*\*<a href="src/scale_gp_beta/types/file_update_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/file.py">File</a></code>
- <code title="get /v5/files">client.files.<a href="./src/scale_gp_beta/resources/files/files.py">list</a>(\*\*<a href="src/scale_gp_beta/types/file_list_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/file.py">SyncCursorPage[File]</a></code>
- <code title="delete /v5/files/{file_id}">client.files.<a href="./src/scale_gp_beta/resources/files/files.py">delete</a>(file_id) -> <a href="./src/scale_gp_beta/types/file_delete_response.py">FileDeleteResponse</a></code>

## Content

Types:

```python
from scale_gp_beta.types.files import ContentRetrieveResponse
```

Methods:

- <code title="get /v5/files/{file_id}/content">client.files.content.<a href="./src/scale_gp_beta/resources/files/content.py">retrieve</a>(file_id) -> <a href="./src/scale_gp_beta/types/files/content_retrieve_response.py">object</a></code>

# Models

Types:

```python
from scale_gp_beta.types import InferenceModel, InferenceModelList, ModelDeleteResponse
```

Methods:

- <code title="post /v5/models">client.models.<a href="./src/scale_gp_beta/resources/models.py">create</a>(\*\*<a href="src/scale_gp_beta/types/model_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/inference_model.py">InferenceModel</a></code>
- <code title="get /v5/models/{model_id}">client.models.<a href="./src/scale_gp_beta/resources/models.py">retrieve</a>(model_id) -> <a href="./src/scale_gp_beta/types/inference_model.py">InferenceModel</a></code>
- <code title="patch /v5/models/{model_id}">client.models.<a href="./src/scale_gp_beta/resources/models.py">update</a>(model_id, \*\*<a href="src/scale_gp_beta/types/model_update_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/inference_model.py">InferenceModel</a></code>
- <code title="get /v5/models">client.models.<a href="./src/scale_gp_beta/resources/models.py">list</a>(\*\*<a href="src/scale_gp_beta/types/model_list_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/inference_model.py">SyncCursorPage[InferenceModel]</a></code>
- <code title="delete /v5/models/{model_id}">client.models.<a href="./src/scale_gp_beta/resources/models.py">delete</a>(model_id) -> <a href="./src/scale_gp_beta/types/model_delete_response.py">ModelDeleteResponse</a></code>
