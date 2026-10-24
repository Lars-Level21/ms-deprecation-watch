# Select a primary AI model for your agent

Note

This article describes features used in agents or agent flows powered by the standard harness.

In Microsoft Copilot Studio, the primary AI model you select for your agent powers generative orchestration. Choose a model based on how much your agent needs in response speed, output quality, reasoning, and cost.

Primary model selection is separate from the settings for deep reasoning (preview), generative responses (preview), and prompt builder models.

Important

- Experimental models are available for exploration and testing but aren't recommended for production use. Review Limitations of experimental and preview models before choosing an experimental or preview model for your agent.

- Data processed within an experimental model might be processed and stored outside of your organization's geographical boundaries.

- This article contains Copilot Studio documentation on model selection, which includes experimental model previews, and is subject to change.

## Model availability by region

Copilot Studio models vary by intended use, release status, and region. You can see each model's tags when you change your agent's AI model.

The following tables show selected models' regional availability. GA means generally available, and cross-geo indicates that data might be processed outside your region.

### Standard harness availability

| Model | Tag/Category | Asia | Australia | Brazil | Canada | Europe (Except UK) | India | Japan | Korea | Saudi Arabia | Singapore | South Africa | United Kingdom | United States |

| GPT Chat Latest | General | Default (cross-geo) | Default | Default (cross-geo) | Default (cross-geo) | Default | Default (cross-geo) | Default (cross-geo) | Default (cross-geo) | Default (cross-geo) | Default (cross-geo) | Default (cross-geo) | Default | Default |

| GPT-4.1 | General | GA (cross-geo) | GA | GA (cross-geo) | GA (cross-geo) | GA | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA | GA |

| GPT-5 Chat | General | GA (cross-geo) | GA | GA (cross-geo) | GA (cross-geo) | GA | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA | GA |

| GPT-5 Reasoning | Deep | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview |

| GPT-5 Auto | Auto | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview |

| GPT-5.3 Chat | General | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview (cross-geo) | Preview |

| GPT-5.5 Chat | General | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA |

| Claude Sonnet 4.6 | General | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA |

| Claude Opus 4.6 | Deep | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA |

| Claude Opus 4.7 | Deep | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA |

| Claude Opus 4.8 | Deep | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA (cross-geo) | GA |

| Grok 4.2 | Deep | - | - | - | - | - | - | - | - | - | - | - | - | Experimental (early access environment) |

Important

GPT Chat Latest is the supported chat model for the Copilot Studio standard harness. It keeps agents on the latest supported GPT chat model as snapshots within the current major model version are updated. Moving to a new major model version is a separate change, and you receive at least 30 days' notice.

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

| Auto | Optimized for coverage across mixed workloads; routes queries dynamically. | Helpdesk and employee agents with mixed intents, blending knowledge and actions, and tier-0 customer support with unpredictable complexity | Variable | Variable | Adaptive per turn |

| General | Optimized for speed and cost on everyday chat and light grounding. | Drafting, rewriting, summarizing, and translation, FAQ-style grounded answers, and simple action automation | Lowest | Lowest | Shallow-to-moderate |

### Model release types

Model tags identify release types, defaults, and availability requirements. Use generally available models for production and experimental or preview models for exploration and testing.

- Experimental: Used for experimentation, and not intended for production use. Subject to preview terms, and can have limitations on availability and quality. See Limitations of experimental and preview models.

- Preview: Might eventually become a generally available model, but isn't intended for production use. Subject to preview terms, and can have limitations on availability and quality. See Limitations of experimental and preview models.

- Generally available (GA): Models without a release tag are generally available and intended for production use. Availability can vary by region.

- Default: The default model for all agents, and usually the best performing generally available model. The default model is periodically upgraded as new, more capable models become generally available. Agents also use the default model as a fallback if a selected model is turned off or unavailable.

- Retired: Models that are no longer supported. Some models offer an extension of up to 30 days after retirement. Check retirement dates and extension availability, and learn how to continue using a retired AI model.

- Cross-geo: Might require data processing and storage outside of your organization's geographical boundaries. Your admin can turn data movement across regions on or off.

- Early access environment: An early release cycle environment. These environments receive new updates and features first. Learn more in Early release cycle environments.

### External models

You can also add external AI models from Anthropic, xAI, or Mistral to your agent. Learn more in Choose an external model as the primary AI model.

## Model retirement dates and extension availability

| Retiring model | Harness | Planned replacement | Retirement date | Extension available (up to 30 days) |

| GPT-5.3 Chat | Standard | GPT Chat Latest | October 15, 2026 | Yes ( Continue using a retired AI model ) |

| GPT-5.4 Reasoning | Standard | GPT Chat Latest | October 15, 2026 | Yes ( Continue using a retired AI model ) |

| GPT-5.5 Chat | Standard | GPT Chat Latest | October 31, 2026 | No |

| GPT-4.1 | Standard | GPT Chat Latest | November 12, 2026 | Yes ( Continue using a retired AI model ) |

| GPT-4.1 Mini | Standard | GPT Chat Latest | November 12, 2026 | Yes ( Continue using a retired AI model ) |

| GPT-5 Chat | Standard | GPT Chat Latest | November 12, 2026 | Yes ( Continue using a retired AI model ) |

| GPT-5 Auto | Standard | GPT Chat Latest | November 12, 2026 | Yes ( Continue using a retired AI model ) |

| GPT-5 Reasoning | Standard | GPT Chat Latest | November 12, 2026 | Yes ( Continue using a retired AI model ) |

Note

For Federal Risk and Authorization Management Program (FedRAMP) tenants and for environments outside the United States where cross-geo data movement is restricted, GPT-4.1 and GPT-5 will remain supported and won't retire as part of this migration. Learn more about availability and eligibility in Move data across regions for Copilots, AI agents, and generative AI features.

## Limitations of experimental and preview models

You can explore and test experimental and preview models, but don't use them for production:

- They might show variability in performance, response quality, latency, or message consumption, and might time out or be unavailable.

- Usage of published agents with an experimental or preview model is billed at the Copilot Studio billing rates.

Experimental and preview models are subject to preview terms. Use these models to evaluate capabilities before an official release and share feedback in the Copilot Studio community.

## Change your agent's AI model

Your agent starts with a default model optimized for most scenarios. To change your agent's model:

- Go to your agent's Overview page.

- In the Model section, select your agent's primary model. You can switch between experimental and production models at any time.

## Admin controls for AI model selection

Administrators control access to preview and experimental AI models with these environment settings:

- Preview and experimental AI models: Turn on this setting to let makers use preview and experimental models in the environment.

- Move data across regions: Turn on this setting to make experimental models available. Data processed within a preview or experimental model might be processed and stored outside your organization's geographical boundaries. The tenant administrator manages this setting in the Power Platform admin center.

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
