# PRD Section Templates

Reference templates for Phase 1 outline planning. Each template defines sections, their purpose, and which source types typically feed them.

---

## Template 1: Technical PRD (Engineering Specs)

Use when the PRD targets an engineering audience building infrastructure, services, or internal tools.

| # | Section | What Belongs Here | Typical Source Mapping |
|---|---------|-------------------|----------------------|
| 1 | **Problem Statement** | Clear definition of the technical problem being solved, including scope and constraints | User briefs, support tickets, incident reports, stakeholder interviews |
| 2 | **Background / Research** | Prior art, existing solutions evaluated, technical landscape | Research papers, competitor analysis, internal docs, architecture decision records |
| 3 | **Solution Architecture** | High-level system design, component diagram, data flow, technology choices | Architecture docs, design discussions, whiteboard sessions, existing system diagrams |
| 4 | **Implementation Plan** | Step-by-step build plan, module breakdown, dependency ordering | Engineering estimates, sprint plans, team capacity docs |
| 5 | **API / Interface Design** | Endpoint definitions, request/response schemas, contract specs, SDK surface | OpenAPI specs, existing API docs, integration partner requirements |
| 6 | **Data Model** | Entity-relationship diagrams, schema definitions, storage strategy, migration paths | Database schemas, data dictionaries, analytics requirements |
| 7 | **Testing Strategy** | Unit, integration, load, and chaos testing plans with coverage targets | QA runbooks, existing test suites, reliability SLAs |
| 8 | **Migration / Rollout** | Phased deployment plan, feature flags, rollback procedures, backward compatibility | Deployment playbooks, infrastructure docs, change management policies |
| 9 | **Cost Analysis** | Infrastructure costs, licensing, headcount, ongoing operational expense | Cloud pricing calculators, vendor quotes, historical spend data |
| 10 | **Success Criteria** | Measurable outcomes that define "done" - latency targets, throughput, error rates | SLAs, performance baselines, business KPIs |
| 11 | **Risks** | Technical risks, dependency risks, security concerns, mitigation strategies | Threat models, risk registers, incident postmortems |
| 12 | **Open Questions** | Unresolved decisions, items needing stakeholder input, known unknowns | Meeting notes, review comments, unresolved threads |

---

## Template 2: Product PRD (Feature Specs)

Use when the PRD targets a cross-functional audience (product, design, engineering, marketing) for a user-facing feature.

| # | Section | What Belongs Here | Typical Source Mapping |
|---|---------|-------------------|----------------------|
| 1 | **Executive Summary** | One-paragraph overview of what is being built and why it matters | Product strategy docs, OKRs, leadership directives |
| 2 | **Problem / Opportunity** | User pain points, market gap, business case with supporting data | User research, analytics dashboards, customer feedback, competitive intel |
| 3 | **User Stories** | Persona-driven scenarios in "As a [role], I want [goal] so that [benefit]" format | User interviews, support tickets, persona documents, journey maps |
| 4 | **Functional Requirements** | Specific behaviors the system must exhibit, organized by feature area | User stories (derived), stakeholder requirements, regulatory docs |
| 5 | **Non-Functional Requirements** | Performance, accessibility, security, scalability, and compliance constraints | SLAs, compliance frameworks, platform guidelines, audit reports |
| 6 | **Design / UX** | Wireframes, interaction flows, visual design references, accessibility standards | Design mockups, style guides, usability test results, brand guidelines |
| 7 | **Technical Approach** | High-level architecture, key technology decisions, integration points | Engineering input, architecture docs, platform constraints |
| 8 | **Launch Plan** | Go-to-market phases, beta/GA timeline, communication plan, support readiness | Marketing briefs, release calendars, training plans |
| 9 | **Metrics / KPIs** | How success will be measured post-launch - adoption, retention, revenue impact | Analytics frameworks, OKRs, baseline measurements |
| 10 | **Dependencies** | Cross-team dependencies, third-party services, external approvals needed | Project plans, vendor contracts, legal review queues |
| 11 | **Timeline** | Milestone-based schedule with key dates, checkpoints, and delivery phases | Sprint plans, resource calendars, dependency maps |

---

## Template 3: Research-to-Engineering PRD (Paper-to-Implementation)

Use when translating academic research, whitepapers, or experimental findings into a concrete engineering plan.

| # | Section | What Belongs Here | Typical Source Mapping |
|---|---------|-------------------|----------------------|
| 1 | **Paper Summary** | Concise summary of the source paper(s) - authors, publication, core thesis, methodology | Academic papers, preprints, technical blog posts |
| 2 | **Key Findings** | Main results, statistical significance, novel contributions, reported performance | Paper results sections, supplementary materials, replication studies |
| 3 | **Relevance to Our System** | Why these findings matter for our product/platform, strategic alignment | Product roadmap, technical strategy docs, user research |
| 4 | **Proposed Architecture** | System design that operationalizes the research - where the new component fits | Existing architecture docs, infrastructure diagrams, platform constraints |
| 5 | **Algorithm Adaptation** | How the paper's algorithm/method is modified for production - simplifications, approximations, tradeoffs | Paper pseudocode, reference implementations, our codebase conventions |
| 6 | **Integration Points** | Where the new capability connects to existing systems - APIs, data pipelines, UX surfaces | System diagrams, API docs, data flow documentation |
| 7 | **Benchmarks / Expected Results** | Reproduction targets, performance expectations, comparison baselines | Paper benchmarks, our current system metrics, industry standards |
| 8 | **Implementation Phases** | Progressive build plan - from proof-of-concept through production hardening | Engineering capacity, risk assessment, dependency analysis |
| 9 | **Cost Model** | Compute costs, data requirements, training/inference budgets, ongoing maintenance | Cloud pricing, GPU estimates, data pipeline costs, paper resource reports |
| 10 | **Success Criteria** | Quantitative thresholds that validate the implementation matches or improves on the research | Paper-reported metrics, business KPIs, A/B test design |
| 11 | **Limitations / Open Questions** | Known constraints of the research, gaps between paper conditions and production reality, areas needing experimentation | Paper limitations sections, reviewer comments, domain expert input |

---

## Template Selection Guide

| Signal in Sources | Recommended Template |
|-------------------|---------------------|
| Heavy API specs, schemas, infrastructure diagrams | Technical PRD |
| User research, mockups, business cases, OKRs | Product PRD |
| Academic papers, benchmark tables, algorithm pseudocode | Research-to-Engineering PRD |
| Mix of the above | Start with the dominant type, pull sections from others as needed |

When sources span multiple categories, the skill should compose a hybrid outline by selecting the best-fit sections from each template rather than forcing a single template.
