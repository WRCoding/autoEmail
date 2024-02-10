class AIRegister:
    _registry = {}

    @classmethod
    def register(cls, ai_type, ai_class):
        if ai_type in cls._registry:
            raise ValueError(f"AI type {ai_type} already registered.")
        cls._registry[ai_type] = ai_class

    @classmethod
    def get_ai(cls, ai_type):
        if ai_type not in cls._registry:
            raise ValueError(f"AI type {ai_type} not found.")
        ai_class = cls._registry[ai_type]
        clazz = ai_class()
        print(clazz)
        return clazz


def register_ai(ai_type):
    def decorator(ai_class):
        print(type(ai_class))
        AIRegister.register(ai_type, ai_class)
        return ai_class
    return decorator
