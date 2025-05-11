from chara.onebot.events import GroupMessageEvent, MessageEvent
from chara.plugin import Session
from chara.plugin import regex_trigger
from chara.plugin import current_plugin


plugin = current_plugin()

# session的优先级为-1, 在不设置特殊值的情况下Session优先级是高于普通trigger的
session_1 = Session(123, 456) # 创建一个Session，用法同Trigger一致

@session_1.handle()
async def _():
    pass

trigger_add_session = regex_trigger('添加')

@trigger_add_session.handle()
async def _(event: MessageEvent):
    if isinstance(event, GroupMessageEvent):
        session = Session(event.group_id, event.user_id)
    else:
        session = Session(None, event.user_id)
    
    plugin.add_trigger(session) # 动态添加Session


__all__ = [
    'session_1',
    'trigger_add_session',
]