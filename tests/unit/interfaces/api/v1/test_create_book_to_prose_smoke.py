from __future__ import annotations

from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient

from domain.ai.services.llm_service import GenerationConfig, GenerationResult
from domain.ai.value_objects.prompt import Prompt
from domain.ai.value_objects.token_usage import TokenUsage
from infrastructure.persistence.database.connection import DatabaseConnection
from infrastructure.persistence.database.sqlite_ai_invocation_repository import SqliteVariableHubRepository
from interfaces.api.v1.core import chapters as chapters_routes
from interfaces.api.v1.core import novels as novels_routes
from interfaces.api.v1.engine import ai_invocation_routes
from interfaces.api.v1.world import bible as bible_routes


def _reset_prompt_singletons() -> None:
    import infrastructure.ai.prompt_manager as prompt_manager_module
    import infrastructure.ai.prompt_registry as prompt_registry_module

    prompt_manager_module._manager_instance = None
    prompt_registry_module._registry_instance = None


class _SmokeLLM:
    async def generate(self, prompt: Prompt, config: GenerationConfig) -> GenerationResult:
        return GenerationResult(
            content="烟测正文",
            token_usage=TokenUsage(input_tokens=1, output_tokens=1),
        )

    async def stream_generate(self, prompt: Prompt, config: GenerationConfig):
        yield "烟测"
        yield "正文"


def test_create_book_setup_worldbuilding_and_prose_prompt_flow(tmp_path, monkeypatch):
    db = DatabaseConnection(str(tmp_path / "plotpilot-create-book-smoke.db"))
    llm = _SmokeLLM()

    monkeypatch.setattr("infrastructure.persistence.database.connection.get_database", lambda db_path=None: db)
    monkeypatch.setattr("interfaces.api.dependencies.get_database", lambda db_path=None: db)
    monkeypatch.setattr("interfaces.api.dependencies.get_llm_service", lambda: llm)
    monkeypatch.setattr(ai_invocation_routes, "get_database", lambda db_path=None: db)
    monkeypatch.setattr(ai_invocation_routes, "get_llm_service", lambda: llm)
    _reset_prompt_singletons()

    app = FastAPI()
    app.include_router(novels_routes.router)
    app.include_router(chapters_routes.router, prefix="/novels")
    app.include_router(bible_routes.router)
    app.include_router(ai_invocation_routes.router)
    app.dependency_overrides[bible_routes.get_auto_bible_generator] = lambda: SimpleNamespace(llm_service=llm)
    app.dependency_overrides[bible_routes.get_auto_knowledge_generator] = lambda: SimpleNamespace()
    client = TestClient(app)

    novel_id = "novel-create-book-smoke"
    created = client.post(
        "/novels/",
        json={
            "novel_id": novel_id,
            "title": "端到端烟测",
            "author": "作者",
            "target_chapters": 0,
            "length_tier": "short",
            "premise": "一个债务缠身的青年在海边小城寻找失踪姐姐。",
            "genre": "都市/悬疑",
            "world_preset": "近未来海滨城市",
            "story_structure": "开篇从现实压力切入，逐步转入规则真相。",
            "pacing_control": "前三章必须兑现一次线索反转。",
            "writing_style": "克制写实，动作与对话都服务压迫感。",
            "special_requirements": "不得改写成修仙、王朝或血脉宿命。",
        },
    )
    assert created.status_code == 201, created.text
    novel_payload = created.json()
    assert novel_payload["id"] == novel_id
    assert novel_payload["locked_story_structure"] == "开篇从现实压力切入，逐步转入规则真相。"
    assert novel_payload["target_chapters"] > 0
    assert novel_payload["target_words_per_chapter"] > 0

    variable_repo = SqliteVariableHubRepository(db)
    context_key = f"novel_id:{novel_id}"
    assert variable_repo.get_value("novel.premise", context_key).value == "一个债务缠身的青年在海边小城寻找失踪姐姐。"
    assert variable_repo.get_value("novel.story_structure", context_key).value == "开篇从现实压力切入，逐步转入规则真相。"
    assert variable_repo.get_value("novel.special_requirements", context_key).value == "不得改写成修仙、王朝或血脉宿命。"
    db.close()

    bible_invocation = client.post(f"/bible/novels/{novel_id}/generate?stage=worldbuilding")
    assert bible_invocation.status_code == 202, bible_invocation.text
    bible_session = bible_invocation.json()["session"]
    bible_prompt = bible_session["prompt_snapshot"]["prompt"]["user"]
    assert "一个债务缠身的青年" in bible_prompt
    assert "开篇从现实压力切入" in bible_prompt
    assert "不得改写成修仙" in bible_prompt
    db.close_all(skip_checkpoint=True)
    _reset_prompt_singletons()

    ensured = client.post(f"/novels/{novel_id}/chapters/1/ensure", json={"title": "债务雨夜"})
    assert ensured.status_code == 200, ensured.text
    db.close_all(skip_checkpoint=True)
    _reset_prompt_singletons()

    prose_invocation = client.post(
        "/ai-invocations",
        json={
            "operation": "chapter.generate.prose",
            "node_key": "chapter-prose-generation",
            "policy": "FULL_INTERACTIVE",
            "context": {"novel_id": novel_id, "chapter_number": 1},
            "variables": {
                "novel_title": "端到端烟测",
                "target_words": novel_payload["target_words_per_chapter"],
                "chapter_number": 1,
                "chapter_title": "债务雨夜",
                "chapter_outline": "第一章：债务雨夜\n\n主角收到姐姐留下的债务单，并发现海边仓库的异常灯光。",
                "user_requirements": "强化现实压迫，不要引入超自然设定。",
            },
        },
    )
    assert prose_invocation.status_code == 200, prose_invocation.text
    prose_session = prose_invocation.json()["session"]
    prose_prompt = prose_session["prompt_snapshot"]["prompt"]["user"]
    assert "端到端烟测" in prose_prompt
    assert "债务雨夜" in prose_prompt
    assert "强化现实压迫" in prose_prompt
    assert "一个债务缠身的青年" in prose_prompt
    assert "开篇从现实压力切入" in prose_prompt
    assert "不得改写成修仙" in prose_prompt

    db.close_all(skip_checkpoint=True)
    _reset_prompt_singletons()
