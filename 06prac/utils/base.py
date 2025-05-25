from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any

T = TypeVar("T")


class BaseTool(ABC, Generic[T]):
    @abstractmethod
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """도구 초기화"""
        pass

    @abstractmethod
    def _create_tool(self) -> T:
        """도구 객체 생성"""
        pass

    @classmethod
    def create(cls, *args: Any, **kwargs: Any) -> T:
        """도구객체 생성 팩토리 메서드"""
        instance = cls(*args, **kwargs)
        tool = instance._create_tool()
        return tool

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """도구실행"""
        pass
