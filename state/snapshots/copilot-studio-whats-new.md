# What's new in Copilot Studio

This article provides resources to learn about new features in Copilot Studio.

## Released versions

For information about the new features, fixes, and improvements released in the past few weeks, see Released versions of Microsoft Copilot Studio.

Note

Releases roll out over several days. New or updated functionality might not appear immediately.

## Notable changes

The following sections list features released in the past months, with links to related information.

### July 2026

- Starting in July 2026, Copilot Studio automatically creates a Microsoft Entra Agent ID for every new agent, and you can no longer opt out at the environment level.

- (Preview) Add a workflow or MCP server as a tool for agents powered by the GitHub Copilot harness to extend your agent with multistep automated processes or external services.

- (Preview) Submit your MCP server for Microsoft certification to give customers and administrators confidence that it meets Microsoft's expectations for reliability, security, compliance, and responsible operation.

- Deploy the same real-time agent across voice and digital messaging channels (digital messaging in preview) for consistent, natural, context-aware conversations. Use the GPT-5-Chat (Preview) model for greater voice customization and deployment flexibility, and monitor real-time agents with Application Insights.

- (Preview) Export environment-level agent telemetry to Azure Application Insights through the Power Platform admin center.

- (Preview) Let users attach files to a conversation and view files your agent creates during a conversation, for agents powered by the GitHub Copilot harness.

### June 2026

- (Production-ready preview) Use the new experience in Copilot Studio to build agents. The GitHub Copilot harness uses an enhanced orchestration runtime for improved response quality and reasoning, available alongside the standard harness.

- Use Microsoft IQ for agents powered by the GitHub Copilot harness to connect your agent to organizational data, giving it access to emails, calendar events, files, Teams messages, and people information.

- Build and reuse skills for agents powered by the GitHub Copilot harness to extend your agent's capabilities with modular, self-contained sets of instructions. Create a skill once, add it to multiple agents, and export it as a Markdown file or package to share with others.

- Turn on memory for agents powered by the GitHub Copilot harness to give your agent persistent context across interactions. It captures user preferences and patterns, stores them per user, and applies them to deliver more relevant and personalized responses over time.

- (General availability) Use the Windows 365 for Agents MCP server to give your agents full operational control of a Windows 365 cloud PC, including desktop interaction, browser automation, and semantic UI inspection.

- Use condition groups to manage multiple conditions in a single Message, Question, or prompt node, reducing branching and making topic flows easier to review and maintain.

- (Preview) Integrate voice agents with Teams Phone Agent to handle specialized call workflows like billing, prescription refills, and order status, with a seamless handoff between Teams Phone Agent and your custom voice agent.

- (Preview) Connect other agents to your agent powered by the GitHub Copilot harness so it can delegate requests to specialized agents, letting you build modular solutions with a single front-door agent routing to the right specialist.

- (Preview) Connect your agent to Foundry IQ for agents powered by the GitHub Copilot harness to ground responses in a knowledge base already built and tuned in Azure AI Foundry.

- (General availability) Select Claude Sonnet 5 or GPT-5.5 Chat as your agent's primary AI model for improved response quality and reasoning.

### May 2026

- (General availability) Computer use is now generally available, letting your agents automate web and desktop apps by controlling browsers and desktop applications on behalf of users.

- Add a prompt node to an agent flow to make a single AI call with dynamic content and model selection, useful for scenarios like translation and structured data extraction.

- Add a Microsoft 365 Copilot node to a workflow to send prompts to Microsoft 365 Copilot or a specific agent, enabling automation scenarios like research and audit drafting.

- Configure consent-based recording on voice-enabled agents to ask callers for consent before recording, with configurable compliance behavior and retention settings.

- Use the agent inventory schema to discover and audit all Copilot Studio agents in your organization from the admin center, API, or Azure Resource Graph.

- (Preview) Review agent readiness and issue status from a consolidated status page that surfaces publishing errors, runtime issues, and configuration blocks with severity levels.

- Use asynchronous responses for agent flows to let long-running processes exceed the two-minute limit and return results to the agent when they complete.

- (Preview) Automatically create Microsoft Entra Agent IDs for each of your agents to scope connector permissions, Conditional Access policies, and DLP governance to individual agents.

- (Preview) Add computer use standalone tools to agents and agent flows for modular, reusable UI automation with built-in governance, model selection, and observability.

- (Preview) Choose Mistral Medium 3.5 as the primary AI model for your agent, now available as an experimental option alongside Anthropic, xAI, and other supported providers.

### April 2026

- Configure hold and resume for voice-enabled agents to pause mid-conversation and resume where you left off, giving users a more natural calling experience.

- (Preview) Build and deploy real-time voice agents for Copilot Studio and Dynamics 365 Contact Center, with support for NLU, multilingual conversations, knowledge integration, security settings, and voice tuning settings like speech sensitivity and silence detection. Configure and test your real-time voice agent directly in Copilot Studio, then publish it to your telephony channel.

- Trigger agent evaluations automatically using the Copilot Studio connector with Power Automate, reducing manual effort in your testing workflow.

- (Preview) Run automated agent evaluations from a REST API using the Power Platform API to integrate evaluation into CI/CD and custom automation pipelines.

- Use the agent usage estimator to forecast Copilot credit consumption across Copilot Studio and Dynamics 365 agents before deploying at scale.

- (Preview) Analyze your agent with custom metrics by defining your own analytics categories and visualizing results alongside built-in analytics.

- (General availability) Connect agents to other agents using the agent-to-agent (A2A) protocol.

- (Preview) Add a display name suffix to identify agents across environments in Teams and Microsoft 365 Copilot using environment variables.

- (Preview) Use GPT-5.5 Reasoning (Deep) as an experimental model for agents requiring deep analytical reasoning.

- Share analytics access with colleagues using the new Analytics Viewer role, without granting broader maker permissions.

### March 2026

- (Preview) Use Work IQ tools to connect Microsoft 365 Copilot and your agents to the Work IQ service. By using this connection, you can access real-time work insights and context from Microsoft 365 files, emails, meetings, chats, and more.

- View and filter detailed lists of user questions and reactions from your agent's conversations. Use this data to identify gaps, create evaluation test sets, and export data for further analysis.

- For users with Bot transcript viewer privileges, downloaded session transcripts from Copilot Studio now include session-level customer satisfaction (CSAT) values.

- For users with Bot transcript viewer privileges, after you filter your list of questions or reactions, you can download the filtered questions or reactions to a .csv file.

- Use the Prompt assistant in Prompt builder to draft prompts faster with GPT model–powered suggestions. This feature reduces the time needed to craft effective prompts.

- Add Bing Custom Search as a knowledge source to ground your agent's responses in a curated, scoped web index by using a Custom Configuration ID.

- Configure post-call action topics for voice-enabled agents to trigger backend actions automatically after a call ends, based on how the conversation concluded.

- Configure reprompt messages in Question nodes with randomization support to improve conversation recovery for retry prompts, entity recognition failures, and voice scenarios.

- Apply accessibility best practices for Adaptive Cards to support screen readers, keyboard navigation, and Teams-specific scenarios. These practices help you build more inclusive agent experiences.

- Agent evaluations are now generally available (GA). You can validate agent performance using customizable test sets to help identify strengths and areas for improvement across diverse scenarios.

- Create multi‑turn conversation tests in Copilot Studio to evaluate how agents perform across realistic dialog flows instead of single‑turn interactions.

- ChatGPT‑5 is now generally available globally (excluding GCC environments) for use in production agents.

- Claude Sonnet 4.5, Claude Sonnet 4.6, and Claude Opus are now generally available globally (excluding GCC environments). Use these models to optimize reasoning depth, quality, latency, and cost for your agents. Availability of some models might require data processing and storage outside of your organization's geographical boundaries. Learn more in Choose an external model as the primary AI model.

- Use an agent node to call a Copilot Studio agent from an agent flow.

### February 2026

- Improved agent responses for ticket‑based Microsoft 365 Graph connectors. Agents more accurately retrieve ServiceNow tickets and Azure DevOps work items and generate clear, actionable summaries, which improves workflow reliability, and time to value.

- Select Claude Sonnet 4.5 (beta) for Computer Use agents. This model improves nuanced decision‑making for complex tasks, increasing reliability, and success rates for advanced uses.

- Enhancements to the prompt builder include:

- Configure content moderation sensitivity per prompt to control how hate/fairness, sexual, violence, and self‑harm content is filtered—supporting regulated and document‑processing scenarios with low or high sensitivity settings for managed models.

- Optimize prompts with new Claude models by choosing Claude Opus 4.6 or Claude Sonnet 4.5, enabling fine‑grained control over reasoning depth, quality, latency, and cost per prompt.

- Edit prompt instructions and settings inline in agent tool details, bringing model selection, inputs, knowledge, and testing into a single, streamlined authoring experience.

### January 2026

- (Preview) New enhancements to agent evaluations:

- Provide real‑time thumbs‑up/down feedback on evaluation results to verify grading performance and drive ongoing improvements to evaluation reliability.

- View your agent's sequence of inputs, decisions, and outputs with activity maps so you can quickly diagnose issues and get clearer insight into how your agent behaves at runtime.

- Use a validated CSV template to create test sets, reducing formatting errors, and helping your team standardize evaluation data more quickly.

- (Preview) Expand computer use capabilities with new model support, built‑in credentials, enhanced audit logging with session replay, and Cloud PC pooling—giving you greater security, scalability, and governance for agent‑driven workflows.

- (General availability) Use the Microsoft Copilot Studio extension for Microsoft Visual Studio Code to build, edit, and manage agents inside Microsoft Visual Studio Code, supporting advanced and highly flexible developer workflows.

### December 2025

- Compare multiple agent versions side by side to validate improvements and quickly spot regressions when evaluating agents with test sets.

### November 2025

- Updates for models used in Copilot Studio:

- On November 24, 2025, GPT-5 Chat rolls out to Copilot Studio in general availability for European and United States regions. You can use generally available models for orchestration in production agents. For more information on choosing orchestration models, see Select a primary AI model for your agent.

- (Preview) Automatically create Microsoft Entra Agent IDs for agents. When turned on, automatically apply identity management to individual agents by assigning a Microsoft Entra Agent ID, helping admins secure and manage agents more effectively.

- Improved knowledge retrieval for SharePoint-grounded agents using tenant graph grounding with semantic search. Updated system architecture and new retrieval methods deliver more precise, context-rich responses, enhancing answer quality.

Note

Some queries might lead to slightly higher latency.

- Improve response accuracy with SharePoint metadata filters. Use metadata like filename, owner, and modified date to refine knowledge retrieval and ensure responses come from the most relevant, up-to-date documents.

- Orchestrate multiple agents to break down complex tasks across specialized agents, improving accuracy and speeding up end‑to‑end automation. Enhance your agents by linking them to other agents—either within your environment or external sources like Microsoft Fabric data agents—for modular, task-specific functionality.

- (Preview) Add tool groups to agents for faster setup. Quickly equip your agents with curated sets of tools from Outlook and SharePoint connectors in one step. This streamlines setup, reduces errors, and ensures consistent, reliable orchestration.

- Copy agents from Microsoft 365 Copilot to Copilot Studio. Easily move agents you created in Microsoft 365 Copilot into Copilot Studio to unlock advanced capabilities like multistep workflows, custom integrations, and broader deployment options.

- (Preview) Add human input to agent workflows with the request information action. Pause an agent flow to collect details from designated reviewers via Outlook, then resume execution using their responses as dynamic parameters. This action ensures workflows can handle missing data or context without relying on hard-coded values.

- Update Power Platform API calls to use the new 'copilotstudio' namespace. The previous namespace will continue to work temporarily, but switching now ensures compatibility with future updates.

- Use component collections with new enhancements. Access collections directly from the sidebar, quickly export or import collections, and take advantage of support for primary agents and new connector types, including child agents and Model Context Protocol (MCP).

### October 2025

- Updates for models used in Copilot Studio:

- Between October 27 and 31, 2025, GPT‑4o will be retired in Copilot Studio for agents using generative orchestration, except for GCC customers who can continue using GPT‑4o. The new default model is GPT‑4.1, which delivers improved performance, reliability, and consistency across experiences. GPT‑4o remains available until November 26, 2025 if you turn on the "Continue using retired models" option.

- Choose from multiple AI models to tailor your agent's performance to your needs.

- (Preview) Test and deploy GPT‑5 models to explore advanced capabilities and enhance your agent's performance.

- Learn about Copilot Agent Kit, a suite of tools developed by the Power Customer Advisory Team (Power CAT) to help test custom agents, validate AI-generated content, analyze conversation key performance indicators, and more.

- (Preview) Group related user questions into themes and drill down into analytics to uncover patterns and gain deeper insights.

- Track time and cost savings for both autonomous and conversational agents to measure ROI and optimize performance.

- Access a unified activity and transcript view, pin sessions, and submit feedback for faster, more effective troubleshooting.

- (Preview) Accelerate flow execution to minimize timeouts and deliver a faster, smoother user experience.

- Use the Model Context Protocol (MCP) server to access dynamic, real-time content—such as files, database records, and API responses—for richer context and improved agent responses.

- (Preview) Evaluate your agents using customizable test sets—whether uploaded, manually created, or AI-generated. Test sets can include test cases using different test methods (graders) measured against defined reference answers, helping teams identify strengths and areas for improvement. This capability supports more reliable, high-quality agent experiences across diverse scenarios.

### September 2025

- (Preview) Automate tasks in desktop applications on Windows using Computer-Using Agents (CUA), which combines vision and reasoning to interact with interfaces—even when APIs aren't available.

- Embed Copilot agents into Android, iOS, and Windows apps using the Client SDK to provide rich, multimodal conversations within native experiences.

- (Preview) Upload Excel, CSV, and PDF files for your agent to analyze using Python code, powered by the code interpreter in chat.
