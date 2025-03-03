# otaro

- Problem with current prototype is that it is too different from the usual workflow of developers
    - Likewise with DSPy
- Defining LLMs programmatically has potential though
- How do we use LLMs now?
    - API, prompt, pre and post processing
- What if we define it as a JSON or YAML?
    - Then load it via a library
    - Optimizing returns a JSON
        - Contains scores
    - JSON defines the API as well
- BAML
    - Or a schema grammar that optimizes for minimal tokens and maximum noise resistance
    - Does schema declaration need nesting?
        - Rules?
        - **If we are talking about how the LLM responds, rules are not required**
        - If we know the schema, we can parse an output for more efficiently and in a more noise-resistant manner, kinda like constrained generation, but constrained parsing
            - i.e. we want to parse the most likely output from a noisy input
            - If we can place restrictions on the schema (e.g. no reused keys, or all keys must start with _), it becomes even easier to parse
    - Support imports? e.g. commonly used rules
        - Can use imports to improve base config without overwriting
- **Config automatically gets better when you run it**
    - Automatically updates prompt and adds error correction
    - Use lock=True to prevent it from changing
    - Add versioning within config file
        - i.e. use latest prompt by default but retain last 5 prompts
    - Stores examples whenever it is run
        - Tries to rectify any error and add error correction
        - Developer can check records later and fix examples, which will then be used to improve the prompt

## To-do

- Basic YAML config
    - Inputs
        - bool
        - int
        - float
        - str
        - enum
        - list
        - object
    - Outputs
    - Rules
    - Imports
- Basic optimization
    - Optimize desc
NAP
- Basic parsing
- Config - Demos
- Basic API
- Config - Basic rules
---
- Basic tests
    - Tests for different input/output types of varying complexities
- Support sync and async
- Examples
- Documentation
- Use yaml template for tasks (e.g. prompt generator and error summary)
---
- Optimization - error correction
    Options:
    - Add to system prompt (e.g. DSPy)
        - Kind of works - tested by appending user message with error summary
        - But sometimes fails with repeated (different) errors because the summarizer does not know about the history and suggests a fix that reverts a previous suggestion
        - Sometimes fails because the error summary lacks detail versus seeing the actual error response
        - Results on 10 runs:
            - Pass after 1 correction
            - False pass after 1 correction (returned [[quote, quote]] instead of [[quote], [quote]])
            - False pass after 2 corrections
            - Pass after 1 correction
            - Pass after 1 correction
            - Failed
            - Pass after 1 correction
            - Failed
            - Pass after 1 correction
            - Failed
        - Slower at time of error since correction requires a summarizer call
            - But will be cheaper thereafter since we are using fewer tokens
    - Add to system prompt v2
        - More similar to DSPy in that we update the prompt instead of appending a user message and we do not use a summarizer
        - But we add more information i.e. the part of the erroneous response that caused the error
        - Results on 10 runs:
            - Pass after 1 correction
            - False pass after 1 correction
            - Pass after 1 correction
            - Pass after 1 correction
            - False pass after 1 correction
            - Failed
            - False pass after 2 corrections
            - Pass after 1 correction
            - Pass after 1 correction
            - Pass after 1 correction
        - v3 with corrected outputs, results on 10 runs:
            - Pass after 1 correction
            - False pass after 1 correction
            - False pass after 1 correction
            - Pass after 1 correction
            - Pass after 1 correction
            - False pass after 1 correction
            - Pass after 1 correction
            - Pass after 1 correction
            - Pass after 1 correction
            - False pass after 1 correction
    - Add as a demo (will require 4 additional outputs per error: (1) first request, (2) first error response, (3) second request with correction, (4) correct response)
        - This works i.e. corrects the issue for nested array example
        - Results on 10 runs:
            - Pass after 1 correction
            - Pass after 1 correction
            - Pass after 1 correction
            - Pass after 1 correction
            - False pass after 1 correction (returned [[quote, quote]] instead of [[quote], [quote]])
            - Pass after 1 correction
            - Pass after 1 correction
            - Pass after 2 corrections
            - Pass after 1 correction
            - False pass after 1 correction
        - Faster at time of error since correction happens after one more LLM call
            - But will be more costly thereafter since we are using more tokens compared to an error summary
    - Localized correction then add error + correction in system prompt, without corresponding output
        - Results on 10 runs (with subsequent task):
            - False pass after 1 correction
            - Pass after 1 correction
            - Pass after 1 correction
            - Pass after 1 correction
            - Pass after 1 correction
            - Pass after 1 correction
            - Pass after 1 correction
            - Pass after 1 correction
            - False pass after 1 correction
            - Pass after 1 correction
        - Issue is that this leads to the LLM reusing the correction where possible
---
- Documentation
- Change "type" to accept Python class
    - Update Field type attribute to take Python class
    - Update from_config to support 3 modes:
        - String-only
        - Dict of one attribute
        - Dict of Field attributes
---
- Problem: Custom classes cannot be exported to yaml correctly
    - Deconstruct and export
- Change rules to accept function as well as string
    - Should also accept
        - lambda sample: contains(sample.haiku, "green")
        - lambda sample: len(sample.quotes) == 3
    - In config
        - contains(haiku, "green")
        - len(quotes) == 3
- Problem: Lambdas or custom functions cannot be exported to yaml correctly

- How to handle API key?
- Clean code
- Feature highlights
---
- Add tests
- Optimized parsing
- Infer types from YAML for autocomplete and hinting
- Examples logging
- Optimization - demos

## Notes

- Demos ideally need `reasoning` attribute as well
- Need to optimize loading time of config file
- Need to optimize "optimization" - we are running more calls than necessary
- Error correction method has an issue where LLM reuses correction in its responses

## Tests

```
$ uv run coverage run --source ./otaro -m pytest
$ uv run coverage report -m
```

## Features

- YAML config
- Prompt optimization
- Localized correction
- Deployment
- Smarter parsing
