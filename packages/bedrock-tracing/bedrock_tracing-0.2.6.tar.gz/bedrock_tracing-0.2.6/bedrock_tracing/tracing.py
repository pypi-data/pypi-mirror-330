import json
import logging
from functools import wraps
from opentelemetry import trace

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

def process_trace_data(event, span):
    """Extracts and processes trace data from Bedrock response event."""
    trace_data = event.get("trace", {})
    orchestration_trace = trace_data.get("trace", {}).get("orchestrationTrace", {})

    invocation_type = (
        orchestration_trace.get("observation", {}).get("type")
        or orchestration_trace.get("modelInvocationInput", {}).get("type")
        or (
            f"GUARDRAIL_ACTION:{trace_data.get('trace', {}).get('guardrailTrace', {}).get('action')}"
            if trace_data.get("trace", {}).get("guardrailTrace", {}).get("action")
            else None
        )
        or ("LLM_RESPONSE" if orchestration_trace.get("modelInvocationOutput", {}).get("rawResponse", {}).get("content") else None)
        or "bedrock-agent-execution"
    )

    with tracer.start_as_current_span(invocation_type) as trace_span:
        def parse_dict(prefix, data):
            if isinstance(data, dict):
                for k, v in data.items():
                    parse_dict(f"{prefix}.{k}" if prefix else k, v)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    parse_dict(f"{prefix}[{i}]", item)
            else:
                trace_span.set_attribute(prefix, str(data))

        parse_dict("trace", trace_data)
        logger.debug("Processed Trace Data: %s", json.dumps(trace_data, indent=2))

def trace_decorator(func):
    """Decorator to handle tracing for Bedrock agent responses."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with tracer.start_as_current_span("bedrock-agent-execution") as span:
            span.set_attribute("session.id", kwargs.get("session_id", "unknown"))
            agent_id = kwargs.get("agent_id")
            agent_alias_id = kwargs.get("agent_alias_id")

            if agent_id:
                span.set_attribute("agent.id", agent_id)
            if agent_alias_id:
                span.set_attribute("agent.alias_id", agent_alias_id)

            for event in func(*args, **kwargs):
                if isinstance(event, dict):
                    if "chunk" in event:
                        agent_answer = event["chunk"]["bytes"].decode('utf-8').replace("\n", " ")
                        span.set_attribute("agent.answer", agent_answer)
                        yield f"{agent_answer}"
                    elif "trace" in event:
                        process_trace_data(event, span)
                    elif "preGuardrailTrace" in event:
                        logger.debug(json.dumps(event["preGuardrailTrace"], indent=2))
                    else:
                        raise Exception("Unexpected event format", event)
                else:
                    yield event
    return wrapper