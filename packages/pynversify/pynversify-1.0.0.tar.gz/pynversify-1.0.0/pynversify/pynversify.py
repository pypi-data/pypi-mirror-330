import inspect

def inject_params(metadata: dict):
    """Decorator to attach metadata mapping parameter names to tokens."""
    def decorator(func):
        setattr(func, '__inject_metadata__', metadata)
        return func
    return decorator

class Binding:
    def __init__(self, implementation, binding_type='class', singleton=False):
        self.implementation = implementation
        self.binding_type = binding_type  # 'class', 'constant', or 'dynamic'
        self.singleton = singleton
        self.instance = None

class BindingBuilder:
    def __init__(self, container, key):
        self.container = container
        self.key = key
        self._binding = None

    def toSelf(self):
        self._binding = Binding(self.key, binding_type='class', singleton=False)
        self.container._bindings[self.key] = self._binding
        return self

    def to(self, implementation):
        self._binding = Binding(implementation, binding_type='class', singleton=False)
        self.container._bindings[self.key] = self._binding
        return self

    def toConstantValue(self, value):
        self._binding = Binding(value, binding_type='constant', singleton=True)
        self.container._bindings[self.key] = self._binding
        return self

    def toDynamicValue(self, func):
        self._binding = Binding(func, binding_type='dynamic', singleton=False)
        self.container._bindings[self.key] = self._binding
        return self

    def inSingletonScope(self):
        if self._binding is None:
            raise ValueError("No binding defined prior to inSingletonScope().")
        self._binding.singleton = True
        return self

    def inTransientScope(self):
        if self._binding is None:
            raise ValueError("No binding defined prior to inTransientScope().")
        self._binding.singleton = False
        return self

class Container:
    def __init__(self, parent=None):
        self._bindings = {}
        self.parent = parent
        self.children = []

    def bind(self, key):
        return BindingBuilder(self, key)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def create_child(self):
        child = Container(parent=self)
        self.children.append(child)
        return child

    def get(self, key):
        if key in self._bindings:
            binding = self._bindings[key]
            if binding.singleton and binding.instance is not None:
                return binding.instance
            if binding.binding_type == 'constant':
                instance = binding.implementation
            elif binding.binding_type == 'dynamic':
                instance = binding.implementation()
            elif binding.binding_type == 'class':
                instance = self._resolve(binding.implementation)
            else:
                raise ValueError("Unknown binding type.")
            if binding.singleton:
                binding.instance = instance
            return instance
        if self.parent is not None:
            return self.parent.get(key)
        raise ValueError(f"No binding found for {key}")

    def _resolve(self, implementation):
        if not inspect.isclass(implementation):
            return implementation
        constructor = implementation.__init__
        sig = inspect.signature(constructor)
        kwargs = {}
        metadata = getattr(constructor, '__inject_metadata__', {})
        for name, param in list(sig.parameters.items())[1:]:
            token = metadata.get(name, None)
            if token is None:
                if param.annotation != inspect.Parameter.empty:
                    token = param.annotation
                else:
                    raise ValueError(f"Dependency '{name}' in {implementation.__name__} must have a token.")
            kwargs[name] = self.get(token)
        return implementation(**kwargs)

def injectable(cls):
    return cls
