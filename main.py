import ast
import operator
import os
from typing import Any, Callable, Iterable

from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

QUIT_COMMANDS = {"quit", "exit", "q"}
HELP_COMMANDS = {"help", "/help", "?"}
DEFAULT_MODEL = "llama-3.1-8b-instant"


def load_local_env_file(path: str = ".env") -> None:
    env_path = os.path.join(os.getcwd(), path)
    if not os.path.exists(env_path):
        return

    with open(env_path, encoding="utf-8") as env_file:
        for line in env_file:
            raw = line.strip()
            if not raw or raw.startswith("#") or "=" not in raw:
                continue
            key, value = raw.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip(chr(34)).strip(chr(39)))


_ALLOWED_OPERATORS: dict[type[ast.AST], Callable[..., float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


class ExpressionError(ValueError):
    """Raised when a calculator expression cannot be evaluated safely."""


def _safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)

    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        operand = _safe_eval(node.operand)
        return _ALLOWED_OPERATORS[type(node.op)](operand)

    raise ExpressionError("Only numeric arithmetic expressions are supported.")


@tool
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression. Example input: (2 + 3) * 4 / 5"""
    try:
        parsed = ast.parse(expression, mode="eval")
        result = _safe_eval(parsed)
    except ZeroDivisionError:
        return "I cannot divide by zero."
    except (SyntaxError, ExpressionError):
        return (
            "I can only evaluate arithmetic expressions with numbers and operators "
            "(+, -, *, /, **, %, //)."
        )

    return f"The result is {result:g}."


@tool
def say_hello(name: str) -> str:
    """Greet a user by name."""
    clean_name = " ".join(name.split()).strip(",.!?")
    return f"Hello {clean_name or 'there'}! I hope you are well today."


def validate_environment() -> None:
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError(
            "Missing GROQ_API_KEY. Set it in your environment or in a .env file before running."
        )


def get_model_name() -> str:
    return os.getenv("GROQ_MODEL", DEFAULT_MODEL)


def _extract_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
            elif isinstance(item, str):
                parts.append(item)
        return "".join(parts)
    return ""


def stream_agent_response(agent_executor: Any, user_input: str) -> Iterable[str]:
    last_text = None
    for chunk in agent_executor.stream({"messages": [HumanMessage(content=user_input)]}):
        for key in ("agent", "tools"):
            message_group = chunk.get(key, {}).get("messages", [])
            for message in message_group:
                text = _extract_text(getattr(message, "content", "")).strip()
                if text and text != last_text:
                    last_text = text
                    yield text


def print_help() -> None:
    print("Assistant: Try messages like:")
    print("  - 'say hello to Alice'")
    print("  - 'calculate (15 + 3) * 2'")
    print("  - 'what is 22 / 7?'")


def main() -> None:
    load_local_env_file()
    validate_environment()

    model = ChatGroq(model=get_model_name(), temperature=0)
    agent_executor = create_react_agent(model, [calculator, say_hello])

    print("Welcome! I'm your AI assistant. Type 'quit' to exit.")
    print("Need ideas? Type 'help'.")

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAssistant: Goodbye!")
            break

        if not user_input:
            print("Assistant: Please enter a message.")
            continue

        lowered = user_input.lower()
        if lowered in QUIT_COMMANDS:
            print("Assistant: Goodbye!")
            break
        if lowered in HELP_COMMANDS:
            print_help()
            continue

        print("Assistant: ", end="")
        try:
            had_output = False
            for response_text in stream_agent_response(agent_executor, user_input):
                had_output = True
                print(response_text, end="")
            if not had_output:
                print("I couldn't generate a response right now.", end="")
            print()
        except Exception as exc:  # noqa: BLE001
            print(f"Sorry, I hit an error while processing that request: {exc}")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        print(f"Assistant startup error: {exc}")
