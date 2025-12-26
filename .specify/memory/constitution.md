<!--
================================================================================
SYNC IMPACT REPORT
================================================================================
Version Change: [New Constitution] → 1.0.0
Modified Principles: N/A (Initial creation)
Added Sections:
  - Core Principles (7 principles)
  - Technology Stack & Architecture
  - Phase Governance Model
  - Development Workflow
  - Quality Standards
  - Governance
Removed Sections: N/A
Templates Requiring Updates:
  ✅ spec-template.md - Reviewed, aligned with constitution requirements
  ✅ plan-template.md - Reviewed, Constitution Check section aligns
  ✅ tasks-template.md - Reviewed, phase structure and test requirements align
Follow-up TODOs: None
================================================================================
-->

# Evolution of Todo Project Constitution

## Core Principles

### I. Spec-Driven Development (MANDATORY)

**Rule**: No agent may write code without approved specifications and tasks.

All development MUST follow this strict sequence:
1. **Constitution** → Project principles established (this document)
2. **Specification** → Requirements documented in `specs/<feature>/spec.md`
3. **Plan** → Architecture documented in `specs/<feature>/plan.md`
4. **Tasks** → Implementation steps documented in `specs/<feature>/tasks.md`
5. **Implementation** → Code written following approved tasks

**Rationale**: Spec-Driven Development ensures all stakeholders understand requirements before implementation begins, prevents scope creep, enables parallel work across phases, and maintains architectural integrity.

**Enforcement**:
- All PRs MUST reference approved spec, plan, and task documents
- Code review MUST verify alignment with specifications
- Agents MUST refuse implementation requests without approved specs
- Any deviation requires spec amendment, not code-level workarounds

### II. Agent Autonomy Boundaries

**Rule**: Agents implement approved specifications; humans define requirements.

Agents MUST:
- Execute tasks precisely as specified in approved task documents
- Request clarification when specifications are ambiguous
- Report blockers and propose spec amendments when necessary
- Follow the established architecture without deviation

Agents MUST NOT:
- Write code without approved specifications
- Invent features or requirements
- Make architectural decisions not covered in the plan
- Deviate from approved specifications for "improvements"
- Manually refactor code outside of planned tasks

**Rationale**: Clear boundaries prevent scope creep, ensure human oversight of business decisions, and maintain predictable system behavior. Agents are execution tools, not product managers.

**Exception Handling**: When agents encounter ambiguity or blockers:
1. Stop implementation immediately
2. Document the specific issue
3. Propose spec amendment with options
4. Wait for human approval before proceeding

### III. Refinement at Spec Level

**Rule**: All changes occur through specification updates, never through code modifications.

When improvements or changes are identified:
1. Halt implementation
2. Update the specification document
3. Revise the plan if architectural changes needed
4. Update task list to reflect new requirements
5. Resume implementation with approved changes

**Rationale**: Code-level refinement creates drift between specifications and implementation. Maintaining specs as single source of truth ensures documentation accuracy, enables impact analysis, and preserves system integrity.

**Prohibited Patterns**:
- "Quick fixes" that bypass specification
- Refactoring unrelated to current tasks
- Feature additions discovered during implementation
- Architecture changes without plan updates

### IV. Phase Boundary Enforcement

**Rule**: Each phase is strictly scoped by its specification; no feature leakage.

Phase boundaries MUST be maintained:
- Phase I features MUST NOT include Phase II+ capabilities
- Implementation MUST deliver exactly what the phase spec defines
- Future-phase mentions in current-phase code are FORBIDDEN
- Architecture MAY evolve only through updated specs

**Rationale**: Phase discipline ensures:
- Each phase delivers working, deployable software
- Dependencies are clear and manageable
- Teams can plan and estimate accurately
- System complexity grows incrementally, not all at once

**Verification**: Each phase completion requires:
- Functional review against phase specification
- Architecture review to confirm no future-phase leakage
- Documentation review to ensure specs match implementation
- Approval before next phase begins

### V. Test-First Development (NON-NEGOTIABLE)

**Rule**: Tests written → User approved → Tests fail → Implementation begins.

Red-Green-Refactor cycle strictly enforced:
1. **Red**: Write tests based on acceptance criteria; verify they FAIL
2. **Green**: Implement minimum code to make tests pass
3. **Refactor**: Clean up while keeping tests green

**Rationale**: Test-first development catches misunderstandings early, documents expected behavior, prevents regression, and ensures specifications are testable.

**Test Categories**:
- **Contract Tests**: API endpoints match specified contracts
- **Integration Tests**: User stories work end-to-end
- **Unit Tests**: Individual components behave correctly

**Enforcement**:
- Task lists MUST include test tasks before implementation tasks
- PRs MUST show failing tests in initial commits
- CI/CD MUST enforce test coverage requirements
- Agents MUST refuse to implement without failing tests

### VI. Clean Architecture & Separation of Concerns

**Rule**: Maintain clear boundaries between layers; dependencies point inward.

Architecture layers (from outer to inner):
1. **Interface Layer**: API endpoints, CLI commands, UI components
2. **Application Layer**: Use cases, business workflows
3. **Domain Layer**: Business logic, entities, rules
4. **Infrastructure Layer**: Database, external services, frameworks

**Principles**:
- Domain layer has NO dependencies on outer layers
- Business logic isolated from infrastructure details
- Each layer communicates through defined interfaces
- Dependencies are explicit and injected, not hardcoded

**Rationale**: Clean architecture enables:
- Independent testing of business logic
- Framework/database swapping without business logic changes
- Parallel development across layers
- Long-term maintainability

**Verification**: Architecture reviews MUST confirm:
- No circular dependencies
- Domain layer purity (no infrastructure imports)
- Clear interface definitions
- Proper dependency injection

### VII. Cloud-Native & Stateless Design

**Rule**: Services MUST be stateless, horizontally scalable, and failure-resilient.

Design requirements:
- **Statelessness**: No in-memory state tied to specific instances
- **Idempotency**: Operations safe to retry (especially Phase III+)
- **Graceful Degradation**: Service failures don't cascade
- **Observability**: All operations traced and logged
- **Configuration**: Environment-driven, not hardcoded

**Rationale**: Cloud-native design enables:
- Horizontal scaling under load
- Zero-downtime deployments
- Cost optimization through auto-scaling
- Multi-region deployment (Phase IV+)

**Phase-Specific Requirements**:
- Phase I-II: Stateless design patterns established
- Phase III: Distributed operations with idempotency
- Phase IV: Event-driven architecture, eventual consistency
- Phase V: Multi-region, CRDT-based synchronization

## Technology Stack & Architecture

### Mandated Technologies

**Backend** (All Phases):
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon DB (PostgreSQL-compatible)
- **Testing**: pytest with coverage

**Frontend** (Phase II+):
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript 5+
- **State Management**: React Context / Zustand (as needed)
- **Testing**: Jest + React Testing Library

**Agent & Intelligence** (Phase III+):
- **Agent Framework**: OpenAI Agents SDK
- **Protocol**: Model Context Protocol (MCP)
- **Communication**: MCP servers for tool integration

**Infrastructure** (Phase III+):
- **Containerization**: Docker
- **Orchestration**: Kubernetes (Phase IV+)
- **Messaging**: Apache Kafka (Phase IV+)
- **Service Mesh**: Dapr (Phase IV+)

### Architecture Evolution by Phase

**Phase I: In-Memory Backend**
- Simple FastAPI service
- In-memory data structures
- Core CRUD operations
- Basic API contracts established

**Phase II: Persistent Backend + Frontend**
- Neon DB integration
- SQLModel entities
- Next.js web interface
- Authentication/authorization basics

**Phase III: Agent Integration**
- OpenAI Agents SDK integration
- MCP servers for tool access
- Agent-driven task decomposition
- Stateless agent operations

**Phase IV: Distributed System**
- Kubernetes deployment
- Kafka event streaming
- Dapr sidecar pattern
- Horizontal scaling
- Multi-service architecture

**Phase V: Advanced Intelligence**
- Multi-agent collaboration
- Persistent agent memory
- Context-aware task management
- Advanced intelligence features

### Technology Constraints

**Prohibited**:
- Direct database access from presentation layer
- Synchronous blocking calls in distributed phases (IV+)
- Hardcoded configuration or secrets
- Framework-specific logic in domain layer
- Technologies not listed in mandated stack

**Discouraged Without Justification**:
- Additional frameworks or libraries
- Custom implementations of standard patterns
- Reinventing existing SDK capabilities
- Complex state management (keep simple until needed)

## Phase Governance Model

### Phase Scope Enforcement

**Each Phase MUST**:
1. Have a complete specification before implementation
2. Deliver all specified features (no partial delivery)
3. Pass all acceptance criteria tests
4. Complete architecture review
5. Receive formal approval before next phase

**Phase Transition Rules**:
- No Phase N+1 work begins until Phase N approved
- Phase N code MUST NOT anticipate Phase N+1 features
- Architecture may evolve, but only through updated specs
- Each phase delivers deployable, working software

### Phase Dependencies

**Linear Progression**:
- Phase I (In-Memory) → Foundation for all
- Phase II (Persistent) → Depends on Phase I contracts
- Phase III (Agents) → Depends on Phase II data model
- Phase IV (Distributed) → Depends on Phase III stateless patterns
- Phase V (Advanced) → Depends on Phase IV infrastructure

**Backward Compatibility**:
- Phase N MUST NOT break Phase N-1 functionality
- API contracts established in Phase I remain stable
- Database migrations MUST be non-breaking
- Frontend features gracefully degrade if backend unavailable

### Cross-Phase Contamination Prevention

**Prohibited**:
- Phase II code referencing Phase III agent concepts
- Phase I including database schema for Phase II
- Comments like "TODO: Phase IV will need this"
- Unused interfaces "for future phases"
- Over-engineering for future requirements

**Verification**:
- Code reviews MUST check for future-phase references
- Architecture reviews validate phase boundary integrity
- Specifications explicitly state "Out of Scope" items
- Test coverage confirms only in-scope functionality

## Development Workflow

### Execution Sequence (Strict)

1. **Constitution Review**: Verify principles still hold
2. **Specification**: Document requirements in `specs/<phase>/spec.md`
3. **Planning**: Create architecture plan in `specs/<phase>/plan.md`
4. **Task Breakdown**: Generate task list in `specs/<phase>/tasks.md`
5. **Test Creation**: Write failing tests per acceptance criteria
6. **Implementation**: Write minimum code to pass tests
7. **Refactoring**: Clean up while maintaining green tests
8. **Review**: Verify alignment with spec, plan, tasks
9. **Approval**: Phase completion sign-off

### Prompt History Records (PHR)

**Mandatory Recording**: Every user interaction MUST generate a PHR.

PHR Creation:
- After completing any implementation work
- After planning or architecture discussions
- After debugging sessions
- After spec/task/plan creation
- For all multi-step workflows

PHR Routing:
- Constitution changes → `history/prompts/constitution/`
- Phase-specific work → `history/prompts/<phase-name>/`
- General work → `history/prompts/general/`

### Architecture Decision Records (ADR)

**Trigger for ADR Suggestion**: When a decision meets ALL criteria:
1. **Impact**: Long-term architectural consequences
2. **Alternatives**: Multiple viable options considered
3. **Scope**: Cross-cutting, influences system design

**ADR Process**:
1. Agent detects significant decision during planning
2. Agent suggests: "📋 Architectural decision detected: [brief]. Document? Run `/sp.adr [title]`"
3. Wait for user approval
4. User runs command to create ADR
5. ADR linked in relevant specifications

**Never Auto-Create**: Agents MUST NOT create ADRs autonomously.

### Commit & PR Standards

**Commit Requirements**:
- Reference spec, plan, or task ID
- Single logical change per commit
- Tests included in same commit as implementation
- Commit message format: `type(scope): description [ref]`

**PR Requirements**:
- Link to specification document
- List completed tasks with checkboxes
- Architecture diagram if changes structure
- Test coverage report
- Reviewer checklist completed

**PR Review Checklist**:
- [ ] Specification exists and approved
- [ ] Implementation matches spec exactly
- [ ] No future-phase features included
- [ ] Tests written first and pass
- [ ] Clean architecture maintained
- [ ] No hardcoded secrets or config
- [ ] Documentation updated

## Quality Standards

### Code Quality

**Required**:
- Type hints in all Python code (mypy strict mode)
- Comprehensive docstrings (Google style)
- Linting passes (ruff for Python, ESLint for TypeScript)
- Formatting consistent (black for Python, Prettier for TypeScript)
- No commented-out code in main branch

**Complexity Limits**:
- Functions: Max 50 lines (excluding docstrings)
- Cyclomatic complexity: Max 10
- Classes: Single Responsibility Principle
- Modules: High cohesion, low coupling

### Testing Standards

**Coverage Requirements**:
- Overall: 80% minimum
- Critical paths: 100% (auth, payments, data integrity)
- New code: 90% minimum

**Test Quality**:
- Tests MUST be independent (no shared state)
- Tests MUST be deterministic (no randomness, no time dependencies)
- Tests MUST be fast (unit tests <1s, integration <10s)
- Tests MUST have clear arrange-act-assert structure

### Performance Standards

**Phase-Specific SLOs**:
- Phase I: API responses <100ms (95th percentile)
- Phase II: Page load <2s, API <200ms
- Phase III: Agent operations <5s, API <200ms
- Phase IV: Distributed operations <500ms (95th percentile)
- Phase V: Intelligence operations <10s

**Resource Constraints**:
- Container memory: <512MB (Phase I-II), <1GB (Phase III-V)
- Database connections: <10 per service instance
- API rate limits: 1000 req/min per user (Phase II+)

### Security Standards

**Authentication/Authorization** (Phase II+):
- JWT tokens with short expiry (15 min access, 7 day refresh)
- RBAC for all protected endpoints
- No sensitive data in JWT payload

**Data Protection**:
- Secrets MUST be in environment variables, never hardcoded
- Database passwords rotated quarterly
- API keys scoped to minimum required permissions
- PII encrypted at rest and in transit

**Dependency Management**:
- Automated vulnerability scanning (Dependabot)
- Critical vulnerabilities patched within 7 days
- Regular dependency updates (monthly)

## Governance

### Constitutional Authority

This constitution is the supreme governing document for the Evolution of Todo project across all five phases.

**Hierarchy**:
1. **Constitution** (this document) - Non-negotiable principles
2. **Phase Specifications** - Phase-specific requirements
3. **Plans** - Implementation architecture
4. **Tasks** - Execution instructions
5. **Code** - Implementation artifacts

**Conflict Resolution**: Constitution overrides all other documents.

### Amendment Process

**Minor Amendments** (clarifications, non-breaking changes):
1. Propose change with rationale
2. Review by project stakeholders
3. Update constitution with version bump (patch)
4. Update dependent templates
5. Create PHR documenting change

**Major Amendments** (breaking changes, principle modifications):
1. Propose change with full impact analysis
2. Review by all stakeholders
3. Vote/approval required
4. Update constitution with version bump (major/minor)
5. Migrate existing artifacts to new standard
6. Create ADR documenting decision
7. Create PHR documenting change

### Compliance & Review

**PR Review**:
- All PRs MUST verify constitutional compliance
- Reviewers MUST check phase boundary integrity
- Complexity MUST be justified if constitution limits exceeded
- Architecture MUST align with mandated patterns

**Periodic Reviews**:
- Constitution review at end of each phase
- Technology stack review before Phase III, IV, V
- Architecture pattern review if issues identified
- Governance process review if violations detected

**Violation Handling**:
1. Identify violation (review, audit, automated check)
2. Assess impact (isolated or systemic)
3. Create remediation plan
4. Implement fix following spec-driven process
5. Update processes to prevent recurrence

### Runtime Development Guidance

For day-to-day development rules and agent-specific instructions, consult:
- `CLAUDE.md` (or equivalent agent guidance file at project root)
- `.specify/templates/commands/*.md` for command-specific workflows
- Phase-specific `specs/<phase>/quickstart.md` for getting started

**Version**: 1.0.0 | **Ratified**: 2025-12-26 | **Last Amended**: 2025-12-26
