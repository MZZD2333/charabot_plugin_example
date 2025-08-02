from chara.onebot.events import GroupMessageEvent, MessageEvent
from chara.plugin import Handler, Session
from chara.plugin import regex_trigger
from chara.plugin import get_current_plugin


plugin = get_current_plugin()

# 可以直接创建一个Session
# Session的优先级为-1, 在不设置特殊值的情况下Session优先级是高于普通trigger的
session_1 = Session(gid=123, uid=456) # 创建一个Session，用法同Trigger一致

@session_1.handle()
async def _() -> None:
    pass

# 也可以动态创建
trigger_add_session = regex_trigger('添加')

@trigger_add_session.handle()
async def _(event: MessageEvent) -> None:
    if isinstance(event, GroupMessageEvent):
        session = Session(gid=event.group_id, uid=event.user_id)
    else:
        session = Session(uid=event.user_id)
    
    session.handle(handler_A)
    
    plugin.add_trigger(session)


async def handler_A(event: MessageEvent, session: Session, handler: Handler) -> None:
    await handler.send('由A发出')
    session.exchange_handler(handler_B)
    
    
async def handler_B(event: MessageEvent, session: Session, handler: Handler) -> None:
    await handler.send('由B发出')
    session.exchange_handler(handler_A)

__all__ = [
    'session_1',
    'trigger_add_session',
]