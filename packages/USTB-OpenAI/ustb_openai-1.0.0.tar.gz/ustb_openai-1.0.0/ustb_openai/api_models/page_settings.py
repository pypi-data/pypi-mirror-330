from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, field_validator

from .._models import ResponseModel


class BaseText(BaseModel):
    font_colour: str
    font_weight: str
    font_size: str
    align: Optional[str] = None


class CommonText(BaseText):
    value: List[str]


class EditableText(BaseText):
    edit_text_content: str
    value: List[str]


class LinkText(BaseText):
    text_link: Optional[str] = None
    value: List[Union[str, dict]]


class BgConfig(BaseModel):
    card_colour: str


class ModelConfig(BaseModel):
    label: str
    value: str


class IconConfig(BaseModel):
    switch_button_icon: str
    go_front: Optional[bool] = Field(default=None, alias="go_front")
    go_back: Optional[bool] = Field(default=None, alias="go_back")
    sort: Optional[int] = Field(default=None, alias="sort")

    @field_validator("go_front", "go_back", mode="before")
    @classmethod
    def convert_bool(cls, v: Any):
        return v == 1 or v == "1" if v is not None else None


class SwitchConfig(BaseModel):
    is_open: bool

    @field_validator("is_open", mode="before")
    @classmethod
    def convert_bool(cls, v: Any):
        return v and v != 0 and v != "0"


class WelcomeSection(BaseModel):
    welcome_content: EditableText
    welcome_bgcolor: BgConfig
    welcome_head_pic: str = Field(alias="welecome_head_pic")

    @field_validator("welcome_head_pic", mode="before")
    @classmethod
    def unwrap_field(cls, v: Any):
        return v["switch_avatar"]


class AskSection(BaseModel):
    ask_content: CommonText
    ask_bgcolor: BgConfig


class AnswerSection(BaseModel):
    answer_content: CommonText
    answer_bgcolor: BgConfig


class InputBoxSection(BaseModel):
    input_text: EditableText
    send_icon: IconConfig
    input_bgcolor: BgConfig


class SuggestProblemSection(BaseModel):
    suggest_switch: SwitchConfig
    suggest_head: EditableText
    suggest_content: LinkText


class FileSourceSection(BaseModel):
    source_switch: SwitchConfig
    source_head: EditableText
    source_content: CommonText


class ProbeQuestionSection(BaseModel):
    probe_switch: SwitchConfig
    probe_head: EditableText
    probe_content: LinkText


class SimilarQuestionSection(BaseModel):
    similar_switch: SwitchConfig
    similar_head: EditableText
    similar_content: CommonText


class CopyButtonSection(BaseModel):
    copy_switch: SwitchConfig
    copy_icon: IconConfig


class AnswerButtonSection(BaseModel):
    answer_switch: SwitchConfig
    answer_icon: IconConfig


class FeedbackButtonSection(BaseModel):
    feedback_switch: SwitchConfig
    feedback_icon: IconConfig


class UploadFilesSection(BaseModel):
    upload_switch: SwitchConfig
    upload_file_word: CommonText
    upload_file_icon: IconConfig


class VoiceInputSection(BaseModel):
    voice_switch: SwitchConfig
    voice_icon: IconConfig


class VisitSourceSection(BaseModel):
    visit_switch: SwitchConfig
    visit_head: EditableText
    visit_content: CommonText


class SuggestFunctionSection(BaseModel):
    function_switch: SwitchConfig
    function_head: EditableText
    function_content: LinkText


class ModelSelectSection(BaseModel):
    model_switch: SwitchConfig
    model_content: List[ModelConfig]

    @field_validator("model_content", mode="before")
    @classmethod
    def unwrap_field(cls, v: Any):
        return v["value"]


class DeepThinkingSelectSection(BaseModel):
    deepThinking_switch: SwitchConfig


class NetworkingSelectSection(BaseModel):
    networking_switch: SwitchConfig


class PageSettingItem(BaseModel):
    welcome: WelcomeSection
    ask: AskSection
    answer: AnswerSection
    input_box: InputBoxSection
    suggest_problem: SuggestProblemSection
    file_source: FileSourceSection
    probe_question: ProbeQuestionSection
    similar_question: SimilarQuestionSection
    copy_button: CopyButtonSection
    answer_button: AnswerButtonSection
    feedback_button: FeedbackButtonSection
    upload_files: UploadFilesSection
    voice_input: VoiceInputSection
    visit_source: VisitSourceSection
    suggest_function: SuggestFunctionSection
    model_select: ModelSelectSection
    deepThinking_select: DeepThinkingSelectSection
    networking_select: NetworkingSelectSection


class PageSetting(ResponseModel[PageSettingItem]):
    """`GET /site/voom/page-setting`
    - `compose_id` (number)
    - `type` (string)
    """
