# memory.py

conversation_history = []
memory_summary = ""

MAX_HISTORY = 10
SUMMARY_CHUNK = 5

def add_message(role, content):
    global conversation_history
    conversation_history.append({"role": role, "content": content})


def should_summarize():
    return len(conversation_history) > MAX_HISTORY


def summarize_old_messages(call_model_function):
    global memory_summary
    global conversation_history

    old_messages = conversation_history[:SUMMARY_CHUNK]

    summary_prompt = f"""
    Summarize this conversation briefly in 3-5 lines.
    Keep important facts, emotions, and user preferences.

    Conversation:
    {old_messages}
    """

    summary = call_model_function(summary_prompt)

    memory_summary += "\n" + summary

    conversation_history = conversation_history[SUMMARY_CHUNK:]


def get_messages(system_prompt):
    messages = [{"role": "system", "content": system_prompt}]

    if memory_summary:
        messages.append({
            "role": "system",
            "content": "Conversation summary so far: " + memory_summary
        })

    messages.extend(conversation_history)

    return messages
