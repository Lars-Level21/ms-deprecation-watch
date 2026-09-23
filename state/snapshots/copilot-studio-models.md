# Select a primary AI model for your agent

Note

This article describes features used in agents or agent flows powered by the standard harness.

AI capabilities evolve rapidly, and each generative model brings distinct strengths, whether it's faster responses, higher-quality outputs, or improved cost efficiency. By using Copilot Studio, you can choose the best model for your agent's orchestration by using a simple dropdown menu.

Want to try out cutting-edge models before they're production-ready? Access the latest experimental models to evaluate them early. However, they might have limited testing, availability, and functionality.

This article describes how to select an AI model for your agent's generative orchestration. Separate settings exist for changing models for deep reasoning (preview), generative responses (preview), and the prompt builder.

Important

- Experimental models are available for exploration and testing but aren't recommended for production use. Review Limitations of experimental and preview models before choosing an experimental or preview model for your agent.

- Data processed within an experimental model might be processed and stored outside of your organization's geographical boundaries.

- This article contains Copilot Studio documentation on model selection, which includes experimental model previews, and is subject to change.

## Model availability by region

Copilot Studio offers different types of models. These model types are based on their intended use and availability.

You can see each model's tags in the list of models in Copilot Studio.

The following tables show the availability status of selected models across regions and special scopes.

### Standard harness availability

| Model | Tag/Category | Asia | Australia | Brazil | Canada | Europe (Except UK) | India | Japan | Korea | Saudi Arabia | Singapore | South Africa | United Kingdom | United States |

| GPT-4o | General | Retired | Retired | Retired | Retired | Retired | Retired | Retired | Retired | Retired | Retired | Retired | Retired | Retired |

| GPT-4.1 | General | GA (cross-geo) | GA | GA (cross-geo) | GA (cross-geo) | GA | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA | GA |

| GPT-5 Chat | General | GA (cross-geo) | GA | GA (cross-geo) | GA (cross-geo) | GA | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA | GA |

| GPT-5 Reasoning | Deep | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview |

| GPT-5 Auto | Auto | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview |

| GPT-5.3 Chat | General | - | - | - | - | - | - | - | - | - | - | - | - | Experimental (early access environment) |

| GPT-5.4 Reasoning | Deep | - | - | - | - | - | - | - | - | - | - | - | - | Experimental (early access environment) |

| GPT-5.5 Chat | General | Default | Default | Default | Default | Default | Default | Default | Default | Default | Default | Default | Default | Default |

| GPT-5.5 Reasoning | Deep | - | - | - | - | - | - | - | - | - | - | - | - | Experimental (early access environment) |

| Claude Sonnet 4.5 | General | Retired | Retired | Retired | Retired | Retired | Retired | Retired | Retired | Retired | Retired | Retired | Retired | Retired |

| Claude Sonnet 4.6 | General | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA |

| Claude Opus 4.6 | Deep | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA |

| Claude Opus 4.7 | Deep | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA |

| Grok 4.1 Fast (Non-reasoning) (see important note below) | General | - | - | - | - | - | - | - | - | - | - | - | - | Experimental (early access environment) |

| Mistral Medium 3.5 | General | Experimental (cross-geo) | Experimental (cross-geo) | Experimental (cross-geo) | Experimental (cross-geo) | Experimental | Experimental (cross-geo) | Experimental (cross-geo) | Experimental (cross-geo) | Experimental (cross-geo) | Experimental (cross-geo) | Experimental (cross-geo) | Experimental (cross-geo) | Experimental (cross-geo) |

Note

Models marked as cross-geo might process data outside of your region.

Important

Microsoft's safety and responsible AI evaluations found Grok-4.1 Fast (Non-Reasoning) to be less aligned than other models evaluated resulting in (i) higher risks that the model will produce potentially harmful content and (ii) lower scores on safety and jailbreak benchmarks. Grok-4.1 Fast (Non-Reasoning) may be capable of producing explicit content, and may do so with a higher propensity than other models. Customers must comply with both the Microsoft Enterprise AI Services Code of Conduct and xAI's Enterprise Terms of Service, including its Acceptable Use Policy. Additionally, there may be categories of harm this model can produce that are not covered by Microsoft's content safety systems. Accordingly, as with all Experimental models, Grok-4.1 Fast (Non-Reasoning) is not recommended for production use and customers should review Limitations of experimental and preview models and conduct their own evaluations before choosing Grok-4.1 Fast (Non-Reasoning).

### US Government availability

| Model | Government Community Cloud (GCC) | Government Community Cloud - High (GCC High) | Department of Defense (DoD) |

| GPT-4o | Default | Default | Default |

### Model use categories

Models are optimized for different purposes. Your agent can perform better when you choose a model with the strengths that fit your agent's purpose. For example, an agent that makes complex decisions can benefit from a deep model, while an agent expected to talk about a wide range of topics could use a general model.

The following table describes the model use tags, their strengths, and considerations to keep in mind if you use the model.

| Tag | Description | Strengths | Latency | Cost | Reasoning depth |

| Deep | Optimized for deliberate, multistep reasoning and tool-supported workflows. | Complex analytics, multistep reasoning, policy and contract analysis, troubleshooting with multi-system steps, and synthesis of long documents with citations | Highest | Highest | Multistep, tool-rich |

| Auto | Optimized for coverage across mixed workloads; routes queries dynamically. | Helpdesk and employee agents with mixed intents, blending knowledge and actions, and tier‑0 customer support with unpredictable complexity | Variable | Variable | Adaptive per turn |

| General | Optimized for speed and cost on everyday chat and light grounding. | Drafting, rewriting, summarizing, and translation, FAQ-style grounded answers, and simple action automation | Lowest | Lowest | Shallow-to-moderate |

### Model release types

Each model listed in Copilot Studio has a tag that identifies its release type. You can try new, cutting-edge experimental and preview models, or choose a reliable, thoroughly tested generally available model.

- Experimental: Used for experimentation, and not intended for production use. Subject to preview terms, and can have limitations on availability and quality. See Limitations of experimental and preview models.

- Preview: Might eventually become a generally available model, but currently not intended for production use. Subject to preview terms, and can have limitations on availability and quality. See Limitations of experimental and preview models.

- Generally available (GA): Models without a release tag are generally available. You can use this model for scaled and production use. In most cases, generally available models have no limitations on availability and quality, but some might still have some limitations, like regional availability.

- Default: The default model for all agents, and usually the best performing generally available model. The default model is periodically upgraded as new, more capable models become generally available. Agents also use the default model as a fallback if a selected model is turned off or unavailable.

- Retired: When a new model becomes the default model, the old default model is retired. You can still use the retired model for up to one month after retirement. Learn more in Continue using a retired AI model.

- Cross-geo: Might require data processing and storage outside of your organization's geographical boundaries. Your admin can turn data movement across regions on or off.

- Early access environment: An early release cycle environment. These environments receive new updates and features first. Learn more in Early release cycle environments.

### External models

You can also add external AI models from Anthropic, xAI, or Mistral to your agent. Learn more in Choose an external model as the primary AI model.

## Limitations of experimental and preview models

You can explore and test experimental and preview models, but don't use them for production:

- They might show variability in performance, response quality, latency, or message consumption, and might time out or be unavailable.

- If you publish an agent with an experimental or preview model, and users use the agent, that use is billed at the established rates.

Feel free to experiment with these models. However, be cautious about deploying them in production environments.

Experimental and preview models are subject to preview terms. Microsoft makes these models available before an official release so that you can get early access and provide feedback. If you're building a production-ready agent, see Copilot Studio overview.

## Change your agent's AI model

Your agent starts with a default model optimized for most scenarios. To change your agent's model:

- Go to your agent's Overview page.

- In the Model section, select your agent's primary model. You can switch between experimental and production models at any time.

## Admin controls for AI model selection

Administrators can allow or block makers from adding preview and experimental AI models to agents by using the following settings:

- Administrators can choose to allow or block preview and experimental models in an environment. To use these models, the Preview and experimental AI models setting must be turned on for your environment.

- Data processed within a preview or experimental model might be processed and stored outside of your organization's geographical boundaries. To make experimental models available, your environment must have the Move data across regions setting turned on. The tenant administrator manages this environment-level setting in the Power Platform admin center.

### Admin controls and requirements for external models

Admins control whether makers can add external models to agents. To grant access to external models, admins must complete the following actions:

- Turn on external models in Power Platform admin center for the environment or the environment group.

- Allow access to each external model provider in the Microsoft 365 admin center. Learn more in the Microsoft 365 admin center documentation:

- Connect to Anthropic LLM

- Connect to Mistral

- Connect to xAI

Preview models and external models are two different sets that can overlap but aren't the same, and their settings are separate. For example:

- Admins can block external models but allow preview or experimental models. In this case, makers can't use external models but can use preview, experimental, and generally available internal models.

- Admins can block preview or experimental models but allow external models. In this case, makers can't use any preview or experimental models, but can use any generally available external and internal models.
