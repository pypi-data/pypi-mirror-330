from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional, Literal, Any, List

"""
In this modeling, the model_validate method from pydantic is dependant on the API REST responses from
the GEAI platform.
It's not expected that the user creates a dictionary to populate the models. If they wish to do so, they
should rely on the GEAI documentation to structure the dictionaries as API responses.
"""


class CustomBaseModel(BaseModel):

    class Config:
        populate_by_name = True


class Error(CustomBaseModel):
    id: int = Field(..., alias="id")
    description: str = Field(..., alias="description")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        return str(self.to_dict())


class AssistantRevisionMetadata(CustomBaseModel):
    """
    {
      "key": "string",
      "type": "string",
      "value": "string"
    }
    """
    key: str = Field(..., alias="key")
    type: str = Field(..., alias="type")
    value: str = Field(..., alias="value")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        return str(self.to_dict())


class AssistantRevision(CustomBaseModel):
    """
    {
      "metadata": [
        ...
      ],
      "modelId": "string",
      "modelName": "string",
      "prompt": "string",
      "providerName": "string",
      "revisionDescription": "string",
      "revisionId": "string",
      "revisionName": "string",
      "timestamp": "timestamp"
    }
    """
    metadata: Optional[list[AssistantRevisionMetadata]] = Field(default_factory=list, alias="metadata")
    model_id: Optional[str] = Field(None, alias="modelId")
    model_name: Optional[str] = Field(None, alias="modelName")
    prompt: Optional[str] = Field(None, alias="prompt")
    provider_name: Optional[str] = Field(None, alias="providerName")
    revision_description: Optional[str] = Field(None, alias="revisionDescription")
    revision_id: Optional[int] = Field(None, alias="revisionId")
    revision_name: str = Field(..., alias="revisionName")
    timestamp: Optional[datetime] = Field(None, alias="timestamp")

    class Config:
        protected_namespaces = ()

    @classmethod
    def model_validate(cls, data):
        if "metadata" in data and isinstance(data["metadata"], list):
            data["metadata"] = [AssistantRevisionMetadata.model_validate(item) for item in data["metadata"]]
        return super().model_validate(data)

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        return str(self.to_dict())


class AssistantIntent(CustomBaseModel):
    """
    DEPRECATED: It's ignored in the modeling of the responses, since it's added complexity
    that doesn't provide any benefit. From assistant, there will be a direct relationship
    to revisions.
    {
          "assistantIntentDefaultRevision": "number",
          "assistantIntentDescription": "string",
          "assistantIntentId": "string",
          "assistantIntentName": "string",
          "revisions": [
            ...
          ]
        }
    """
    default_revision: float
    description: str
    id: str
    name: str
    revisions: Optional[list[AssistantRevision]] = []

    def __str__(self):
        intent = {
            "assistantIntentDefaultRevision": self.default_revision,
            "assistantIntentDescription": self.description,
            "assistantIntentId": self.id,
            "assistantIntentName": self.name
        }
        if any(self.revisions):
            intent["revisions"] = self.revisions

        return str(intent)


class Organization(CustomBaseModel):
    id: Optional[str] = Field(None, alias="organizationId")
    name: Optional[str] = Field(None, alias="organizationName")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        organization = self.to_dict()
        return str(organization)


class SearchProfile(CustomBaseModel):
    """
     {
      "name": "string",
      "description": "string"
    }
    """
    name: str = Field(..., alias="name")
    description: str = Field(..., alias="description")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        search_profile = self.to_dict()
        return str(search_profile)


class ProjectToken(CustomBaseModel):
    """
     {
      "description": "string",
      "id": "string",
      "name": "string",
      "status": "string", /* Active, Blocked */
      "timestamp": "timestamp"
    }
    """
    description: Optional[str] = Field(None, alias="description")
    token_id: str = Field(..., alias="id")
    name: str = Field(..., alias="name")
    status: str = Field(..., alias="status")
    timestamp: datetime = Field(..., alias="timestamp")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        token = self.to_dict()
        return str(token)


class UsageLimit(CustomBaseModel):
    """
    "hardLimit": "number",                // Upper usage limit
    "id": "string",                       // Usage limit ID
    "relatedEntityName": "string",        // Name of the related entity
    "remainingUsage": "number",           // Remaining usage
    "renewalStatus": "string",            // Renewal status (Renewable, NonRenewable)
    "softLimit": "number",                // Lower usage limit
    "status": "integer",                  // Status (1: Active, 2: Expired, 3: Empty, 4: Cancelled)
    "subscriptionType": "string",         // Subscription type (Freemium, Daily, Weekly, Monthly)
    "usageUnit": "string",                // Usage unit (Requests, Cost)
    "usedAmount": "number",               // Amount used (decimal or scientific notation)
    "validFrom": "timestamp",             // Start date of the usage limit
    "validUntil": "timestamp"             // Expiration or renewal date
    """
    hard_limit: Optional[float] = Field(None, alias="hardLimit")
    id: Optional[str] = Field(None, alias="id")
    related_entity_name: Optional[str] = Field(None, alias="relatedEntityName")
    remaining_usage: Optional[float] = Field(None, alias="remainingUsage")
    renewal_status: Optional[Literal["Renewable", "NonRenewable"]] = Field(None, alias="renewalStatus")
    soft_limit: Optional[float] = Field(None, alias="softLimit")
    status: Optional[Literal[1, 2, 3, 4]] = Field(None, alias="status")
    subscription_type: Optional[Literal["Freemium", "Daily", "Weekly", "Monthly"]] = Field(None, alias="subscriptionType")
    usage_unit: Optional[Literal["Requests", "Cost"]] = Field(None, alias="usageUnit")
    used_amount: Optional[float] = Field(None, alias="usedAmount")
    valid_from: Optional[datetime] = Field(None, alias="validFrom")
    valid_until: Optional[datetime] = Field(None, alias="validUntil")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        usage_limit = self.to_dict()
        return str(usage_limit)


class Project(CustomBaseModel):
    """
     {
      "projectActive": "boolean",
      "projectDescription": "string",
      "projectId": "string",
      "projectName": "string",
      "projectStatus": "integer", /* 0:Active, 2:Hidden */
    }
    """
    organization: Optional[Organization] = None
    active: Optional[bool] = Field(None, alias="projectActive")
    description: Optional[str] = Field(None, alias="projectDescription")
    id: Optional[str] = Field(None, alias="projectId")
    name: Optional[str] = Field(None, alias="projectName")
    email: Optional[str] = None
    status: Optional[int] = Field(None, alias="projectStatus")
    tokens: Optional[list[ProjectToken]] = []
    usage_limit: Optional[UsageLimit] = None

    @classmethod
    def model_validate(cls, data: dict):
        organization_data = {
            "organizationId": data.get("organizationId"),
            "organizationName": data.get("organizationName"),
        }
        organization = Organization.model_validate(organization_data) if any(value is not None for value in organization_data.values()) else None
        return cls(organization=organization, **data)

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        return str(self.to_dict())


class RequestItem(CustomBaseModel):
    """
    {
      "assistant": "string",
      "intent": "string",
      "timestamp": "string",
      "prompt": "string",
      "output": "string",
      "inputText": "string",
      "status": "string"
    }
    """
    assistant: str = Field(..., alias="assistant")
    intent: Optional[str] = Field(None, alias="intent")
    timestamp: str = Field(..., alias="timestamp")
    prompt: Optional[str] = Field(None, alias="prompt")
    output: Optional[str] = Field(None, alias="output")
    input_text: Optional[str] = Field(None, alias="inputText")
    status: str = Field(..., alias="status")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        return str(self.to_dict())


class GuardrailSettings(CustomBaseModel):
    llm_output: Optional[bool] = Field(False, alias="llmOutputGuardrail")
    input_moderation: Optional[bool] = Field(False, alias="inputModerationGuardrail")
    prompt_injection: Optional[bool] = Field(False, alias="promptInjectionGuardrail")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        settings = self.to_dict()
        return str(settings)


class LlmSettings(CustomBaseModel):
    """
    "llmSettings": {
        "providerName": "string",
        "modelName": "string",
        "temperature": "decimal",
        "maxTokens": "integer",
        "uploadFiles": "boolean",
        "llmOutputGuardrail": "boolean",
        "inputModerationGuardrail": "boolean",
        "promptInjectionGuardrail": "boolean"
      }
    """
    provider_name: Optional[str] = Field(None, alias="providerName")
    model_name: Optional[str] = Field(None, alias="modelName")
    temperature: Optional[float] = Field(None, alias="temperature")
    max_tokens: Optional[int] = Field(None, alias="maxTokens")
    frequency_penalty: Optional[float] = Field(None, alias="frequencyPenalty")
    presence_penalty: Optional[float] = Field(None, alias="presencePenalty")
    upload_files: Optional[bool] = Field(None, alias="uploadFiles")
    guardrail_settings: Optional[GuardrailSettings] = Field(None, alias="guardrail_settings")
    n: Optional[int] = None
    stream: Optional[bool] = Field(None, alias="stream")
    top_p: Optional[float] = Field(None, alias="topP")
    type: Optional[str] = Field(None, alias="type")
    cache: Optional[bool] = Field(None, alias="cache")
    verbose: Optional[bool] = Field(None, alias="verbose")

    class Config:
        protected_namespaces = ()

    @classmethod
    def model_validate(cls, data: dict):
        guardrail_data = {
            "llmOutputGuardrail": data.get("llmOutputGuardrail"),
            "inputModerationGuardrail": data.get("inputModerationGuardrail"),
            "promptInjectionGuardrail": data.get("promptInjectionGuardrail")
        }
        guardrail_settings = GuardrailSettings.model_validate(guardrail_data) \
            if any(value is not None for value in guardrail_data.values()) else None
        return cls(guardrail_settings=guardrail_settings, **data)

    def to_dict(self):
        llm_data = self.model_dump(by_alias=True, exclude_none=True)
        del llm_data["guardrail_settings"]
        if self.guardrail_settings:
            llm_data.update({
                "llmOutputGuardrail": self.guardrail_settings.llm_output,
                "inputModerationGuardrail": self.guardrail_settings.input_moderation,
                "promptInjectionGuardrail": self.guardrail_settings.prompt_injection
            })
        return llm_data

    def __str__(self):
        llm_setting = self.to_dict()
        return str(llm_setting)


class WelcomeDataFeature(CustomBaseModel):
    """
    {
        "title": "string",
        "description": "string"
    }
    """
    title: str = Field(..., alias="title")
    description: str = Field(..., alias="description")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        feature = self.to_dict()
        return str(feature)


class WelcomeDataExamplePrompt(CustomBaseModel):
    """
    {
        "title": "string",
        "description": "string",
        "promptText": "string"
    }
    """
    title: str = Field(..., alias="title")
    description: str = Field(..., alias="description")
    prompt_text: str = Field(..., alias="promptText")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        example_prompt = self.to_dict()
        return str(example_prompt)


class WelcomeData(CustomBaseModel):
    """
    "title": "string",
    "description": "string",
    "features": [
        ],
        "examplesPrompt": [
        ]
      }
    """
    title: Optional[str] = Field(None, alias="title")
    description: Optional[str] = Field(None, alias="description")
    features: Optional[list[WelcomeDataFeature]] = Field([], alias="features")
    examples_prompt: Optional[list[WelcomeDataExamplePrompt]] = Field([], alias="examplesPrompt")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        welcome_data = self.to_dict()
        return str(welcome_data)


class ChatMessage(CustomBaseModel):
    role: str = Field(..., alias="role")
    content: str = Field(..., alias="content")
    function_call: Optional[Any] = Field(None, alias="function_call")
    refusal: Optional[Any] = Field(None, alias="refusal")
    tool_calls: Optional[Any] = Field(None, alias="tool_calls")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        message = self.to_dict()
        return str(message)


class ChatMessageList(CustomBaseModel):
    messages: list[ChatMessage]

    def to_list(self):
        messages = list()
        for message in self.messages:
            messages.append(message.to_dict())

        return messages


class ChatVariable(CustomBaseModel):
    key: str = Field(..., alias="key")
    value: str = Field(..., alias="value")

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        variable = self.to_dict()
        return str(variable)


class ChatVariableList(CustomBaseModel):
    variables: list[ChatVariable]

    def to_list(self):
        variables = list()
        for variable in self.variables:
            variables.append(variable.to_dict())

        return variables


class Assistant(CustomBaseModel):
    id: Optional[str] = Field(None, alias="assistantId")
    name: Optional[str] = Field(None, alias="assistantName")
    description: Optional[str] = Field(None, alias="assistantDescription")
    status: Optional[Literal[1, 2]] = Field(1, alias="assistantStatus")
    priority: Optional[int] = Field(0, alias="assistantPriority")
    type: Optional[str] = Field(None, alias="type")
    prompt: Optional[str] = Field(None, alias="prompt")
    default_revision: Optional[float] = Field(None, alias="assistantIntentDefaultRevision")
    intent_description: Optional[str] = Field(None, alias="assistantIntentDescription")
    intent_id: Optional[str] = Field(None, alias="assistantIntentId")
    intent_name: Optional[str] = Field(None, alias="assistantIntentName")
    revisions: Optional[List["AssistantRevision"]] = Field([], alias="revisions")
    project: Optional["Project"] = Field(None, alias="project")
    welcome_data: Optional["WelcomeData"] = Field(None, alias="welcomeData")
    llm_settings: Optional["LlmSettings"] = Field(None, alias="llmSettings")

    @classmethod
    def model_validate(cls, data):
        revisions = [AssistantRevision.model_validate(revision_data) for revision_data in data.get('revisions', [])]

        welcome_data = WelcomeData(
            features=data.get('welcomeData', {}).get('features', []),
            examples_prompt=data.get('welcomeData', {}).get('examplesPrompt', [])
        ) if 'welcomeData' in data else None

        llm_settings = LlmSettings(
            temperature=data.get('llmSettings', {}).get('temperature', 0.7),
            max_tokens=data.get('llmSettings', {}).get('maxTokens', 1000)
        ) if 'llmSettings' in data else None

        return cls(
            id=data.get('assistantId'),
            name=data.get('assistantName'),
            description=data.get('assistantDescription'),
            status=data.get('assistantStatus', 1),
            priority=data.get('assistantPriority', 0),
            type=data.get('type'),
            prompt=data.get('prompt'),
            default_revision=data.get('assistantIntentDefaultRevision'),
            intent_description=data.get('assistantIntentDescription'),
            intent_id=data.get('assistantIntentId'),
            intent_name=data.get('assistantIntentName'),
            revisions=revisions,
            project=data.get('project'),
            welcome_data=welcome_data,
            llm_settings=llm_settings
        )

    def to_dict(self):
        return self.model_dump(by_alias=True, exclude_none=True)

    def __str__(self):
        assistant = self.to_dict()
        return str(assistant)


class TextAssistant(Assistant):
    type: Literal["text"] = "text"


class ChatAssistant(Assistant):
    type: Literal["chat"] = "chat"


class DataAnalystAssistant(Assistant):
    pass


class ChatWithDataAssistant(Assistant):
    pass
