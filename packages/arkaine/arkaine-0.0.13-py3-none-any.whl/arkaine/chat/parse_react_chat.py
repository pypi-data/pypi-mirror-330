import json
import re
from typing import Any, List, Tuple

from arkaine.tools.types import ToolCalls


def parse_react_chat(response: str) -> Tuple[str, ToolCalls, str]:
    """
    Parse the LLM response into: - final_response (string),
        - a list of (tool_name, tool_input),
        - the first Thought encountered (multiline if consecutive, stops if we
          see any new 'Thought:', 'Action:', 'Response:', or 'Observation:').

    Rules based on the tests and sample outputs:

    1. We only store the very first "Thought: ..." we find (including its
       subsequent lines until we hit another special marker). If a second
       "Thought:"
        appears, we ignore it.

    2. Multiple lines following the first "Thought:" (and before any other
       marker) are appended to that thought (multiline thought).

    3. Lines starting with "Observation:" are simply ignored as far as final
       output goes, but they do end any action-input collection in progress.

    4. Whenever we see a new "Action:", we finalize whatever action was in
       progress.

    5. "Action Input:" lines are collected until we hit another special marker
       line.

    6. If there is no "Response:", any leftover text is ignored except in the
       case where we have no thought, no tools, and no explicit response, in
       which case the entire input is treated as the final response.

    7. JSON decoding is attempted for each action input. If it fails, we store
       the raw string. We do a minor “escape fix” for the common scenario with
       quotes that LLMs sometimes produce incorrectly (like {“text”: “Hello
       “quoted” friend”}).
    """

    lines = response.splitlines()
    final_response = ""
    tool_calls: List[Tuple[str, Any]] = []

    thought = ""
    found_thought = False  # We'll only store the first Thought
    collecting_thought = False

    action = None
    action_input_lines: List[str] = []

    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()
        idx += 1

        if not line:
            continue  # skip blank lines

        if line.startswith("Thought:"):
            action, tool_calls, action_input_lines = finalize_action(
                action, action_input_lines, tool_calls
            )
            if not found_thought:
                found_thought = True
                # Start gathering lines for the first Thought:
                first_line = line.split("Thought:", 1)[1].lstrip()
                thought = first_line
                collecting_thought = True
            else:
                # Any subsequent 'Thought:' lines are ignored for the thought content
                collecting_thought = False

        elif line.startswith("Observation:"):
            # "Observation:" ends any action input but does not get stored.
            action, tool_calls, action_input_lines = finalize_action(
                action, action_input_lines, tool_calls
            )
            collecting_thought = False

        elif line.startswith("Action:"):
            action, tool_calls, action_input_lines = finalize_action(
                action, action_input_lines, tool_calls
            )
            collecting_thought = False
            action = line.split("Action:", 1)[1].strip()  # e.g. 'calculator'
            action_input_lines = []

        elif line.startswith("Action Input:"):
            collecting_thought = False
            # Grab anything on the same line
            after = line.split("Action Input:", 1)[1].strip()
            if after:
                action_input_lines.append(after)
            # Collect subsequent lines until next marker
            while idx < len(lines):
                peek = lines[idx].strip()
                if any(
                    peek.startswith(marker)
                    for marker in (
                        "Action:",
                        "Thought:",
                        "Observation:",
                        "Response:",
                    )
                ):
                    break
                action_input_lines.append(lines[idx])
                idx += 1

        elif line.startswith("Response:"):
            action, tool_calls, action_input_lines = finalize_action(
                action, action_input_lines, tool_calls
            )
            collecting_thought = False
            final_response = line.split("Response:", 1)[1].strip()
            # The rest of the lines (if any) go into the response
            if idx < len(lines):
                remainder = "\n".join(lines[idx:]).rstrip()
                final_response += ("\n" + remainder).rstrip()
            break  # done parsing

        else:
            # If none of the special markers apply and we're collecting a Thought, keep collecting
            if collecting_thought:
                if thought:
                    thought += "\n" + line
                else:
                    thought = line

    # if we ended the loop with an unfinished action, finalize it
    action, tool_calls, action_input_lines = finalize_action(
        action, action_input_lines, tool_calls
    )

    # If there's no explicit response, no tools, and no thought, treat entire text as final response
    if not final_response and not tool_calls and not thought:
        final_response = response.strip()

    return final_response.rstrip(), tool_calls, thought


def try_json_load(text: str) -> Any:
    """Attempt to parse text as JSON. If it fails because of unescaped quotes,
    try a minimal fix, then return raw text otherwise."""
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        # We'll do a minimal fix for the common case where quotes are not escaped.
        # Example that fails: {"text": "Hello, this is a "quoted" string"}
        # We convert any quote that isn't already escaped inside a string to an escaped version.
        # This is not guaranteed to fix all malformed JSON, but helps with typical quoted-string issues.

        # Only do this fix if the user has a roughly valid JSON structure with unescaped quotes.
        # We'll do it by simple heuristic: if there's a "Expecting ',' delimiter" or "Expecting ':' delimiter"
        # in the error, attempt to escape interior quotes.
        if any(
            msg in str(e)
            for msg in [
                "Expecting ',' delimiter",
                "Expecting ':' delimiter",
            ]
        ):
            # naive approach: replace " x " with \" x \"
            # This regex finds quotes that are not preceded by a backslash
            # and are not the very first quote after a colon. Then we escape them.
            # The pattern can be refined for more complicated cases.
            fixed = re.sub(r'(?<!\\)"(?![,:}\s])', r'\\"', text)
            # Attempt to parse again
            try:
                return json.loads(fixed)
            except json.JSONDecodeError:
                return text
    return text


def finalize_action(
    action: str | None,
    action_input_lines: List[str],
    tool_calls: List[Tuple[str, Any]],
) -> Tuple[None, List[Tuple[str, Any]], List[str]]:
    """Helper to finalize the current action and clear buffers."""
    if action:
        raw_ai = "\n".join(action_input_lines).strip()
        if raw_ai:
            parsed_ai = try_json_load(raw_ai)
            tool_calls.append((action, parsed_ai))
    return None, tool_calls, []
