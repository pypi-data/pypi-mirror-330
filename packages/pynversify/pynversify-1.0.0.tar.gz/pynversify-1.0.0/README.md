# Inversify for Python

A dependency injection container inspired by Inversify for Python.

This library supports hierarchical containers, various binding types (toSelf, to, constant, dynamic),
and scopes (singleton and transient).

## Examples

```py
from inversify import Container, injectable, inject_params

class Token:
    def __init__(self, name):
        self.name = name
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return isinstance(other, Token) and self.name == other.name

# Tokens for bindings
LOGGER_TOKEN = Token("LOGGER")
USER_SERVICE_TOKEN = Token("USER_SERVICE")

@injectable
class Logger:
    def __init__(self):
        self.name = "Parent Logger"
    def log(self, message: str):
        print(f"[{self.name}]: {message}")

@injectable
class CustomLogger:
    def __init__(self):
        self.name = "Child Logger"
    def log(self, message: str):
        print(f"[{self.name}]: {message}")

@injectable
class UserService:
    @inject_params({'logger': LOGGER_TOKEN})
    def __init__(self, logger):
        self.logger = logger
    def process(self):
        self.logger.log("Processing in UserService")

# Create parent container and bind tokens
parent_container = Container()
parent_container.bind(LOGGER_TOKEN).to(Logger).inSingletonScope()
parent_container.bind(USER_SERVICE_TOKEN).to(UserService).inTransientScope()

# Create child container and override the LOGGER_TOKEN binding
child_container = parent_container.create_child()
child_container.bind(LOGGER_TOKEN).to(CustomLogger).inSingletonScope()

# Get services from parent and child containers
parent_service = parent_container.get(USER_SERVICE_TOKEN)
child_service = child_container.get(USER_SERVICE_TOKEN)

parent_service.process()  # Uses Parent Logger
child_service.process()   # Uses Child Logger
```
