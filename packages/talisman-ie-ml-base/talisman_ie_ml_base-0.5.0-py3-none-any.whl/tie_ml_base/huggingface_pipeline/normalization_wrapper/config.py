from abc import ABCMeta, abstractmethod
from typing import Annotated

from pydantic import ConfigDict, Field, PrivateAttr, WithJsonSchema

from tp_interfaces.abstract import ImmutableBaseModel


class AbstractLanguageStrategy(ImmutableBaseModel, metaclass=ABCMeta):
    @abstractmethod
    def get_lang(self, lang: str, supported_langs: tuple[str, ...]) -> str | None:
        raise NotImplementedError


class BaseLanguageStrategy(AbstractLanguageStrategy):
    """Use node language"""
    model_config = ConfigDict(title="Без настроек", json_schema_extra={'description': 'Используется язык ноды'})

    def get_lang(self, lang: str, supported_langs: tuple[str, ...]) -> str | None:
        return lang


class ForceOneLang(AbstractLanguageStrategy):
    """
    Force language 'lang'
    if 'for_all=true' than ignore node language else use force lang only for unsupported languages
    """
    lang: str = Field(title="Язык")
    for_all: bool = Field(False, title="Для всех значений")
    model_config = ConfigDict(title="Задать язык", json_schema_extra={'description': 'Принудительно задаёт язык'})

    def get_lang(self, lang: str, supported_langs: tuple[str, ...]) -> str | None:
        if self.for_all:
            return self.lang

        return lang if lang in supported_langs else self.lang


class LangMappingStrategy(AbstractLanguageStrategy):
    """
    map supported language(including unknown) to list of unsupported language
    """
    lang_mapping: dict[str, tuple[str, ...]]
    _lang_mapping: dict[str, str] = PrivateAttr()  # mapping unsupported language to supported
    model_config = ConfigDict(extra='allow', title="Отображение языков", json_schema_extra={
        'description': 'Задаёт отображение поддерживаемого языка в список неподдерживаемых'
    })

    def model_post_init(self, context):
        real_mapping = {value: key for key, values in self.lang_mapping.items() for value in values}
        self._lang_mapping = real_mapping

    def get_lang(self, lang: str, supported_langs: tuple[str, ...]) -> str:
        return self._lang_mapping.get(lang, lang)

    def __hash__(self):
        return hash(tuple(self.lang_mapping.items()))


_TypeStr = Annotated[str, WithJsonSchema({"type": "string", "title": "Тип предметной области"})]


class StringNormalizerConfig(ImmutableBaseModel):
    possible_types: tuple[_TypeStr, ...] = Field(
        tuple(),
        title="Используемые типы характеристик и значений характеристик из предметной области"
    )
    lang_strategy: BaseLanguageStrategy | ForceOneLang | LangMappingStrategy = Field(BaseLanguageStrategy(), title="Стратегия обработки")
    model_config = ConfigDict(title="Настройка ml-обработчика строк")
