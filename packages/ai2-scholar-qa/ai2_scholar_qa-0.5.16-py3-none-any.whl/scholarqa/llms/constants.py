from collections import namedtuple

GPT_4_TURBO = "openai/gpt-4-turbo-2024-04-09"
GPT_4o = "openai/gpt-4o"
GPT_4o_MINI = "openai/gpt-4o-mini"
CLAUDE_3_OPUS = "anthropic/claude-3-opus-20240229"
CLAUDE_35_SONNET = "anthropic/claude-3-5-sonnet-20241022"
LLAMA_405_TOGETHER_AI = "together_ai/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"

CompletionResult = namedtuple("CompletionCost",
                              ["content", "model", "cost", "input_tokens", "output_tokens", "total_tokens"])

CostReportingArgs = namedtuple("CostReportingArgs", ["task_id", "user_id", "msg_id", "description", "model"])

CostAwareLLMResult = namedtuple("CostAwareLLMResult", ["result", "tot_cost", "models"])
