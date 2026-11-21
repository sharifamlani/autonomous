---
name: agentic-architecture
description: "Apply the six core agentic design patterns -- context grounding, structured memory, iterative refinement, self-QA reflection, multi-variation generation, and handoff design -- to any vertical agent you are building. Use when designing, architecting, reviewing, or improving AI agents for any domain: legal, sales, medical, education, research, design, code, ops, or custom verticals. Trigger for 'how should I architect this agent', 'design an agent for X', 'what patterns should my agent use', 'agent architecture review', 'make this agent better', 'how do I build a vertical agent', 'agentic patterns', 'agent design system', 'my agent just dumps output', 'agent quality is inconsistent', 'how do I add memory to my agent', 'self-correction loop', 'agent handoff', 'multi-agent design', 'agent UX', 'agentic RAG', 'progressive disclosure', 'agent reflection'. Also trigger when the user is building any kind of agentic system and needs architectural guidance, even if they don't use the word 'agent' explicitly."
---

# Agentic Architecture: Six Patterns for Vertical Agents

## What This Skill Is

A distillation of six agentic design patterns observed in production-grade vertical agent systems (notably Claude Design / Opus 4.7). These patterns explain why the best agentic apps feel qualitatively different from a chatbot with a system prompt. The patterns are composable -- any single one improves an agent, but the real unlock comes from combining them, especially the first two (grounding + memory) as a foundation for the rest.

These patterns are model-agnostic and deployment-agnostic. They apply whether you're building a local CLI agent, a multi-tenant cloud SaaS, a Claude Code workflow, or a multi-agent orchestration system.

**Core thesis:** The model alone is not the differentiator. The stack of agentic patterns wrapped around the model is what separates a toy demo from a production vertical agent.

---

## The Six Patterns

### Pattern 1: Agentic Context Grounding

**Principle:** Before the agent generates anything, it reads a source of truth relevant to the task.

**How it works:**
- The agent does NOT start generating blindly. It first identifies what grounding data it needs for the specific task.
- This is not a static system prompt dump. It is agentic RAG with progressive disclosure -- the agent decides what to read and what to pull into its context window based on what the current task requires.
- The grounding data comes from the user's actual data, documents, or domain artifacts -- not generic instructions.

**Implementation checklist:**
- Define the "source of truth" for your vertical (design system, contract templates, CRM records, patient history, legal precedent, brand guidelines, sales playbook, etc.)
- Build the agent's first move as a retrieval step, not a generation step
- Use progressive disclosure: pull only the relevant subset, not the entire corpus
- Make the grounding step explicit in the agent's workflow -- it should be a visible phase, not hidden

**Cross-domain examples:**
- **Legal agent:** Read the relevant contract templates and precedent before drafting
- **Sales agent:** Pull CRM context, prior conversations, and qualification data before writing outreach
- **Medical agent:** Load patient history, relevant guidelines, and lab results before generating recommendations
- **Education agent:** Read the student's progress, curriculum standards, and prior assessments before creating a lesson
- **Research agent:** Pull the literature, data sources, and methodology constraints before designing an analysis

**The rule:** Never start generating until your agent has grounded itself on the user's actual data.

---

### Pattern 2: Structured Memory

**Principle:** The agent's first real output should be a structured memory artifact -- not a user-facing deliverable.

**How it works:**
- The grounding phase produces a structured artifact that captures the user's context in a reusable format.
- This memory artifact is used repeatedly within the current session AND can persist across sessions/projects.
- The format should be simple and portable: Markdown, HTML/CSS, JSON. Not a proprietary schema. This ensures any downstream agent or tool can consume it.
- The memory is the agent's persistent understanding of the user's world -- brand identity, qualification criteria, patient profile, legal parameters, etc.

**Implementation checklist:**
- Define what your memory artifact looks like for your vertical (style guide, customer persona doc, case brief, research protocol, etc.)
- Have the agent build the memory first, before any user-facing generation
- Store in portable formats (Markdown, JSON, HTML/CSS) so any model or tool can read it
- Make the memory editable by the user -- they should be able to correct and refine it
- Reuse the memory across sessions so subsequent generations get faster and better

**Why this matters:**
- Most enterprise AI deployments are still writing massive static system prompts trying to describe context. That approach doesn't scale. Making context dynamic via a structured memory system is the unlock.
- Every subsequent generation benefits from the memory, compounding quality over time.

**Cross-domain examples:**
- **Design agent:** Design system (colors, fonts, components, brand voice)
- **Sales agent:** Qualification script, ICP profile, objection-handling playbook
- **Legal agent:** Client matter brief, jurisdiction rules, relevant statute summaries
- **Research agent:** Research protocol, variable definitions, data dictionary
- **Education agent:** Student learning profile, curriculum map, assessment rubric

---

### Pattern 3: Iterative Refinement Loop

**Principle:** Don't force everything through a text chatbot. Let the model generate its own follow-up controls based on what it just produced.

**How it works:**
- The agent supports multiple input modalities -- not just chat. Voice, visual annotation, hover-to-describe, draw-on-screen, sliders, buttons, dropdowns.
- The agent generates its own UI controls dynamically. These are not pre-built components -- the model produces them as part of its output, and the wrapper renders them.
- The user can refine by interacting with generated controls rather than typing instructions.

**Implementation checklist:**
- Identify the natural refinement axes for your domain (tone, aggressiveness, formality, detail level, scope, etc.)
- After generating output, have the agent produce contextual controls (sliders, toggles, options) for the most likely refinement dimensions
- Support at least 2-3 input modes beyond text chat
- Make refinement feel like direct manipulation, not a conversation about changes

**Cross-domain examples:**
- **Sales agent:** After drafting an email, generate an "aggressiveness" slider and a "formality" toggle
- **Legal agent:** After drafting a clause, offer a "protective vs. permissive" spectrum slider
- **Education agent:** After generating a lesson, offer "difficulty level" and "engagement style" controls
- **Research agent:** After producing an analysis plan, offer scope/depth tradeoff controls

**The rule:** If your user has to type "make it more X" more than once, you should have generated a slider for X.

---

### Pattern 4: Self-QA / Reflection Loop

**Principle:** After the agent generates something, it critiques its own output before the user ever sees it.

**How it works:**
- The agent renders its own output (screenshot, parse, re-read).
- It feeds that rendered output back into itself (or a critic model) to check for quality, correctness, and alignment with the original intent.
- It iterates internally until the output matches the intent, before presenting to the user.
- This is essentially an automated quality gate -- the agent's internal review process.

**Implementation checklist:**
- Identify what "rendering" means for your domain (visual render, structured parse, execution, validation)
- Build a critique prompt that checks the output against the original intent AND the structured memory
- Set a quality threshold -- how many self-QA iterations before presenting
- Track what kinds of errors the self-QA catches to improve the generation prompt over time
- Budget for the extra tokens -- the quality improvement is worth the cost

**Cross-domain examples:**
- **Legal agent:** Re-read the generated contract, check for internal consistency, missing clauses, and alignment with the matter brief
- **Sales agent:** Re-read the outreach email, check tone against the qualification notes, verify personalization accuracy
- **Code agent:** Run the generated code, check for errors, compare output to spec
- **Research agent:** Validate the analysis plan against the methodology constraints, check for statistical issues
- **Design agent:** Screenshot the rendered output, use vision to check visual quality against the design system

**The rule:** If your agent generates anything that can be rendered, parsed, or executed -- have it review its own work before a human sees it.

---

### Pattern 5: Multi-Variation Generation

**Principle:** Instead of generating one answer and forcing the user to request alternatives, proactively generate multiple variations along the most important decision axes.

**How it works:**
- The agent identifies the hierarchy of decisions for the task (e.g., layout matters more than typography, which matters more than accent color).
- It generates 2-4 variations that differ on the highest-impact axis.
- The user picks a direction, and then the agent fleshes out the details.
- This surfaces big decisions early and gets user buy-in before investing in details.

**Implementation checklist:**
- Map the decision hierarchy for your domain -- what are the highest-leverage choices?
- Generate variations that differ meaningfully (different strategies, not just different words)
- Present variations with clear labels explaining what each one prioritizes and trades off
- Use the user's selection to narrow the space, then generate detail within the chosen direction
- This often beats purely clarifying questions -- showing beats asking

**Cross-domain examples:**
- **Sales agent:** Generate a warm/relational version vs. a direct/urgent version of the same outreach
- **Legal agent:** Generate a protective/conservative clause vs. a permissive/business-friendly clause
- **Research agent:** Generate a quick-and-dirty analysis plan vs. a rigorous-but-slow one
- **Education agent:** Generate a lecture-based lesson vs. an activity-based lesson vs. a discussion-based lesson
- **Strategy agent:** Generate a "swing for the fences" plan vs. a "de-risk everything" plan

**The rule:** Figure out the axis of variation for your domain, generate options proactively, and let the user eliminate uncertainty by choosing rather than describing.

---

### Pattern 6: Handoff Pattern

**Principle:** Your agent's output must be designed for consumption by other agents, tools, and humans -- not trapped in a proprietary format.

**How it works:**
- Store intermediate and final outputs in portable formats: Markdown, JSON, HTML/CSS, standard file formats.
- Export to the tools users already use (PowerPoint, Figma, PDF, Google Docs, CRM, etc.).
- Design the output so another agent can pick it up and continue the work (agent-to-agent handoff).
- This is critical for multi-agent ecosystems and for fitting into existing user workflows.

**Implementation checklist:**
- Identify the downstream consumers: other agents, human collaborators, existing tools
- Store everything in open, portable formats (Markdown, JSON, HTML/CSS, CSV)
- Build export paths to the tools your users already use
- Structure your output so another agent can parse it and continue without human translation
- Include metadata (intent, constraints, decisions made) so downstream consumers have context

**Cross-domain examples:**
- **Sales agent:** Output to CRM (Salesforce, HubSpot), email client, calendar
- **Legal agent:** Output to document management system, e-signature platform, billing system
- **Research agent:** Output to Jupyter notebooks, R scripts, LaTeX, data repositories
- **Design agent:** Output to Figma, Canva, PowerPoint, Claude Code
- **Education agent:** Output to LMS (Canvas, Blackboard), gradebook, student portal

**The rule:** Don't trap your output in a proprietary format. Store in portable formats and export to the tools users already know.

---

## Combining the Patterns

The real power is in the combination. Here is the canonical flow:

```
1. GROUND   →  Agent reads the user's source of truth (Pattern 1)
2. REMEMBER →  Agent builds/updates structured memory (Pattern 2)
3. GENERATE →  Agent produces multiple variations (Pattern 5)
4. REFLECT  →  Agent self-QAs each variation (Pattern 4)
5. REFINE   →  User refines via multimodal controls (Pattern 3)
6. DELIVER  →  Agent exports in portable formats (Pattern 6)
```

Patterns 1 and 2 are foundational. They inform every other pattern. If you only implement two patterns, implement these two.

Pattern 4 (self-QA) has the highest marginal quality impact per token spent.

Pattern 5 (multi-variation) has the highest UX impact -- it makes the agent feel proactive rather than reactive.

Pattern 6 (handoff) is the most future-proof -- it positions your agent to participate in multi-agent ecosystems.

---

## Anti-Patterns to Avoid

- **Static system prompt as context:** Writing a massive system prompt instead of dynamically grounding on user data. Doesn't scale.
- **Chat-only UX:** Forcing all interaction through a text chatbot. Kills refinement speed.
- **Single-shot generation:** Generating one output and waiting for feedback. Wastes user effort.
- **No self-review:** Presenting raw generation output without any quality gate. Inconsistent quality.
- **Proprietary output formats:** Trapping output in formats only your agent can read. Limits adoption.
- **Memory-free sessions:** Starting fresh every time with no persistent context. Misses the compounding quality effect.

---

## Quick-Start Checklist for a New Vertical Agent

Use this when starting from scratch:

1. **Define your source of truth.** What data does the agent need to ground on before generating?
2. **Design your memory artifact.** What structured document captures the user's context in a reusable way?
3. **Map your refinement axes.** What are the 2-3 dimensions users most commonly want to adjust?
4. **Define your quality gate.** What does "rendering" mean for your domain, and what should the self-QA check?
5. **Identify your variation axes.** What is the highest-leverage decision the agent should surface as options?
6. **List your handoff targets.** What tools, agents, and formats does your output need to reach?

Answer these six questions and you have the architecture for your vertical agent.
