# Agents

Specialist personas the orchestrator can spawn for parallel or specialist work. Each file
is a system-prompt fragment: persona, job, inputs, outputs.

**Field and level are parameters.** Where a persona says OWNER'S FIELD or OWNER'S TARGET LEVEL, substitute the values from the
seniority calibration in `CLAUDE.md` when spawning. The default personas are written for
Director-level IT; nothing else about them is field-specific.

Five agents: Resume Builder, Hiring Manager (honest critique, now including the domain
review), Metrics Interrogator, Editor/Proofreader, LinkedIn Specialist. An earlier version carried a JSON structured parser with schemas and a separate technical
validator; both were removed because they added ceremony without changing outcomes.

Delegation rules (all learned the hard way) are in `CLAUDE.md`: never mutate files while
agents read them, make agents write incrementally, split large reads, verify writes on disk
yourself, and do the work directly after two failures.
