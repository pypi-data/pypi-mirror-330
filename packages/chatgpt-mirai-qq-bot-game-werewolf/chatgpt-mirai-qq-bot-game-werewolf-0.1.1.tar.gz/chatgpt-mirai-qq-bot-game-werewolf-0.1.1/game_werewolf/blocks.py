from typing import Any, Dict, List, Optional, Annotated
from kirara_ai.workflow.core.block import Block, Input, Output, ParamMeta
from kirara_ai.im.message import IMMessage, TextMessage, VoiceMessage
from kirara_ai.im.sender import ChatSender
from .game_werewolf import GameWerewolf
import asyncio
from kirara_ai.logger import get_logger
from kirara_ai.ioc.container import DependencyContainer
from kirara_ai.llm.llm_manager import LLMManager
from kirara_ai.llm.llm_registry import LLMAbility
import threading  # 新增导入

logger = get_logger("GameWerewolf")

def model_name_options_provider(container: DependencyContainer, block: Block) -> List[str]:
    llm_manager: LLMManager = container.resolve(LLMManager)
    return llm_manager.get_supported_models(LLMAbility.TextChat)

class GameWerewolfBlock(Block):
    """音乐搜索Block"""
    name = "game_werewolf"

    inputs = {
        "speech": Input(name="speech", label="发言", data_type=str, description="发言"),
        "sender": Input("sender", "聊天对象", ChatSender, "聊天对象")
    }


    outputs = {
        "message": Output(name="message", label="IM消息", data_type=IMMessage, description="IM消息"),
    }
    container: DependencyContainer
    game_instances: Dict[str, GameWerewolf]  # 新增字典来存储实例

    def __init__(self, werewolf_count: Annotated[Optional[int],ParamMeta(label="狼人数量", description="狼人数量"),] = 1, willager_count: Annotated[Optional[int],ParamMeta(label="平民数量", description="平民数量"),] = 1,
      model_name: Annotated[
          Optional[str],
          ParamMeta(label="模型 ID", description="要使用的模型 ID", options_provider=model_name_options_provider),
      ] = None,):
        super().__init__()
        self.game_instances = {}  # 初始化字典
        self.werewolf_count = werewolf_count
        self.willager_count = willager_count
        self.model_name = model_name
        self.logger = logger

    def execute(self, **kwargs) -> Dict[str, Any]:
        speech = kwargs.get("speech", "").lstrip().strip()
        sender = kwargs.get("sender")
        group_id = sender.group_id if sender.group_id else sender.user_id  # 获取 group_id 或 user_id
        llm_manager = self.container.resolve(LLMManager)
        model_id = self.model_name
        if not model_id:
            model_id = llm_manager.get_llm_id_by_ability(LLMAbility.TextChat)
            if not model_id:
                raise ValueError("No available LLM models found")
            else:
                self.logger.info(
                    f"Model id unspecified, using default model: {model_id}"
                )
        else:
            self.logger.debug(f"Using specified model: {model_id}")

        llm = llm_manager.get_llm(model_id)
        # 获取或创建 GameWerewolf 实例
        if group_id not in self.game_instances:
            self.game_instances[group_id] = GameWerewolf(self.werewolf_count,self.willager_count, llm,model_id)  # 创建新实例
            self.game_instances[group_id].lock = threading.Lock()  # 为每个实例添加锁

        # 使用现有实例
        game = self.game_instances[group_id]

        message_elements = []
        try:
            if not game.lock.acquire(blocking=False):  # 尝试获取锁，不阻塞
                result = "游戏正在进行中"  # 如果锁被占用，返回相应消息
            else:
                try:
                    result = game.play(speech, llm, self.model_name)
                finally:
                    game.lock.release()  # 确保释放锁
            message_elements.append(TextMessage(result))
            return {"message": IMMessage(sender=ChatSender.get_bot_sender(), message_elements=message_elements)}
        except Exception as e:
            self.logger.error(str(e))
            message_elements.append(TextMessage(str(e)))
            return {"message": IMMessage(sender=ChatSender.get_bot_sender(), message_elements=message_elements)}

