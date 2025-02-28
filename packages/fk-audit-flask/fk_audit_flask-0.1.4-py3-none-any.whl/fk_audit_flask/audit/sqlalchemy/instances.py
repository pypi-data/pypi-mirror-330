

from sqlalchemy import inspect
from sqlalchemy import event
from blinker import Signal
from sqlalchemy.orm import Session

from fk_audit_flask.utils.json import (serializar_dict)
from fk_audit_flask.audit.kwargs import (create_kwargs)


class SQLAlchemySignal:
    def __init__(self, include_flush_event: bool = False):
        self.signal = Signal('Send args')
        self.include_flush_event = include_flush_event

    def keep_logs_models(self, cls):

        @event.listens_for(cls, 'after_insert')
        def after_insert(mapper, connection, target):
            register_audit(cls, target, 'create')

        @event.listens_for(cls, 'before_update')
        def before_update(mapper, connection, target):
            state = inspect(target)
            changes = {}
            object_before_changed = {}

            for attr in state.attrs:
                hist = attr.load_history()
                hist_attr = hist.deleted or hist.unchanged
                if len(hist_attr) > 0:
                    object_before_changed[attr.key] = hist_attr[0]
                else:
                    object_before_changed[attr.key] = None
                if not hist.has_changes():
                    continue
                changes[attr.key] = hist.added
            if len(changes) > 0:
                register_audit(cls, target, 'update', changes, object_before_changed)

        @event.listens_for(cls, 'after_delete')
        def after_delete(mapper, connection, target):
            register_audit(cls, target, 'delete')

        def register_audit(cls, target, event_type, changes=None, object_before_changed=None):
            session_on_target = Session.object_session(target)

            def audit_callback_with_flush(*args, **kwargs):
                session_from_target = Session.object_session(target)
                if session_from_target is not None and session_from_target.is_active:
                    __audit((cls, target), event_type, changes, object_before_changed)
                else:
                    print("No se pudo enviar la señal, la sesión no está activa")

            def audit_callback(session):
                session_from_target = Session.object_session(target)
                if session_from_target is not None and session_from_target.is_active:
                    __audit((cls, target), event_type, changes, object_before_changed)
                else:
                    print("No se pudo enviar la señal, la sesión no está activa")

            if self.include_flush_event:
                event.listen(session_on_target, 'after_flush', audit_callback_with_flush)
            else:
                event.listen(session_on_target, 'before_commit', audit_callback)

        def __audit(cls_target, method, changes: dict, object_before_changed=None):
            if changes is not None:
                changes = {key: value[0] for key, value in changes.items()}

            cls, target = cls_target
            target_dictionary = target.__dict__
            columns = dict(map(lambda x: (x.name, None), inspect(cls).columns))
            object_repr = {column: target_dictionary[column] for column in columns if column in target_dictionary}

            args = {
                'object_pk': getattr(target, cls.__mapper__.primary_key[0].name),
                'content_type': cls.__tablename__,
                'object_repr': serializar_dict(object_repr),
                'action': method,
                'changes': serializar_dict(changes),
                'object_before_changed': serializar_dict(object_before_changed)
            }

            try:
                self.signal.send(None, **create_kwargs(args))
                print("Señal enviada satisfactoriamente")
            except Exception as e:
                print(f"Error al enviar la señal: {e}")
