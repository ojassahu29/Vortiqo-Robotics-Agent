# Vortiqo Robotics Agent

> An agentic vision-language-action robotics system that enables robots to understand high-level natural-language goals, perceive their environment, autonomously plan and execute tasks, and verify whether the requested goal has been achieved.

## Overview

Vortiqo is an experimental robotics AI project focused on building an **agentic robotic system** capable of translating high-level human instructions into physical robot actions.

Instead of requiring a human to explicitly define every manipulation step, the system is designed around a **goal-driven approach**:

```text
Human provides the goal
        ↓
AI understands the instruction
        ↓
AI perceives the environment
        ↓
AI reasons about the task
        ↓
AI generates a plan
        ↓
Robot executes actions
        ↓
AI observes the new state
        ↓
AI evaluates goal completion
        ↓
      ┌───────┴───────┐
      NO              YES
      ↓                ↓
   Replan            Finish
```

For example, given:

> "Clean the table."

the robot should not rely on a predefined sequence of movements. Instead, the agent should determine what objects are present, identify which objects are relevant to the goal, determine appropriate actions and destinations, execute those actions, and inspect the environment again to determine whether the table is now clean.

This perception → reasoning → action → verification loop is the central concept of Vortiqo.

---

## Project Goals

The primary goals of the project are to develop a robotic agent capable of:

- Understanding natural-language instructions
- Extracting high-level task goals
- Connecting language to objects and locations in the physical environment
- Perceiving and understanding the surrounding scene
- Maintaining a representation of the current world state
- Decomposing high-level goals into actionable subtasks
- Generating task plans dynamically
- Generating robot actions using Vision-Language-Action models
- Executing actions through a robotics software stack
- Observing the environment after actions
- Detecting whether the goal has been achieved
- Replanning when the current plan is insufficient
- Reporting task completion, failure, or uncertainty to the human

---

## Core Architecture

The intended architecture consists of several interacting layers:

```text
                         HUMAN
                           │
                           │ Natural-language goal
                           ▼
                ┌─────────────────────┐
                │ LANGUAGE / GOAL     │
                │ UNDERSTANDING       │
                │                     │
                │ Goal Parser         │
                │ + VLM capabilities  │
                └──────────┬──────────┘
                           │
                           ▼
                    Goal Understanding
                           │
                           ▼
                     Task Reasoning
                           │
                           ▼
                    Task Decomposition
                           │
                           ▼
                ┌─────────────────────┐
                │     PERCEPTION      │
                │                     │
                │ Camera + SAM3       │
                │        +            │
                │      SmolVLM2       │
                └──────────┬──────────┘
                           │
                           ▼
                     Evidence Fusion
                           │
                           ▼
                       WORLD STATE
                           │
                           ▼
                     Task Planning
                           │
                           ▼
                ┌─────────────────────┐
                │         VLA         │
                │       SmolVLA       │
                └──────────┬──────────┘
                           │
                           ▼
                      Robot Actions
                           │
                           ▼
                         ROBOT
                           │
                           ▼
                       New State
                           │
                           ▼
                      Verification
                           │
                   ┌───────┴───────┐
                   │               │
                  NO              YES
                   │               │
                   ▼               ▼
                Replan           Finish
```

The exact division of responsibility between the language model, perception models, reasoning/planning layer, and VLA policy will continue to be refined through implementation and evaluation.

A current architectural principle is that **SAM3 provides grounded visual evidence**, while **SmolVLM2 provides semantic interpretation**. SmolVLM2 outputs are treated as semantic evidence or hypotheses rather than unquestioned ground truth.

---

## Technology Stack

The project is being developed around the Hugging Face robotics ecosystem and related vision-language models.

### LeRobot

[LeRobot](https://github.com/huggingface/lerobot) provides the primary robotics software foundation for the project.

It is being explored for:

- Robot interfaces
- Robot policies
- Vision-Language-Action models
- Robot datasets
- Imitation learning
- Training and evaluation
- Hardware integration

Current development environment:

- Python 3.12.10
- PyTorch 2.10.0 + CUDA 12.8 build
- LeRobot 0.6.1
- NVIDIA RTX 4060 Laptop GPU

### SmolVLM2

SmolVLM2 is being evaluated as a compact **Vision-Language Model** for semantic visual understanding.

Current model under evaluation:

```text
HuggingFaceTB/SmolVLM2-500M-Video-Instruct
```

The model is currently being explored for:

- Visual scene interpretation
- Object and attribute recognition
- Connecting language to visual information
- Semantic scene descriptions
- Object relationships
- Language grounding
- Supporting task reasoning

#### Current SmolVLM2 evaluation findings

Initial inference testing has been performed on a controlled synthetic scene containing:

- A red rectangular shape in the upper-left region
- A blue circle in the upper-right region
- A green rectangular shape in the lower region

The model successfully identified the visible shapes when given constrained prompts and produced structured JSON containing color, shape, and approximate position.

However, an open-ended prompt caused substantial semantic hallucination. The model interpreted the arrangement as a **flag** and generated additional contextual claims about national identity and pride that were not visually present.

A subsequent targeted negative query asking whether a flag was actually visible produced:

```text
No.
```

This indicates that the model's behavior is strongly dependent on prompting and that its open-ended generation can introduce semantic priors that are not grounded in the image.

The current working conclusion is therefore:

> **SmolVLM2 is promising as a constrained semantic perception component, but unrestricted scene description should not be treated as authoritative ground truth.**

The project will continue evaluating SmolVLM2 rather than discarding it based on the initial hallucination.

Planned evaluation areas include:

- Open-ended versus constrained visual descriptions
- Object counting
- Object attributes
- Negative evidence
- Spatial relationships
- Natural-scene understanding
- Task-relevant scene interpretation
- Structured output reliability
- Semantic interpretation of SAM3-generated object regions

### SmolVLA

SmolVLA is the primary **Vision-Language-Action** model being explored for robot action generation.

Conceptually:

```text
Visual observations
        +
Natural-language instruction
        +
Robot state
        ↓
     SmolVLA
        ↓
   Robot actions
```

SmolVLA is part of the LeRobot ecosystem and is intended to bridge visual/language information with robot manipulation actions.

SmolVLA has **not yet been integrated into the active Vortiqo execution pipeline**. Its role will be evaluated after the perception, world-state, reasoning, and planning interfaces are sufficiently established.

### SAM3

[Meta's SAM3](https://github.com/facebookresearch/sam3) is being used as a visual perception and segmentation component.

Current responsibilities include:

- Object segmentation
- Region identification
- Object localization
- Bounding-box extraction
- Mask generation
- Confidence estimation
- Visual scene information extraction

SAM3 is primarily treated as a **grounded perception component**, rather than the task-planning or action-generation component.

Current SAM3 testing has successfully detected multiple objects from a controlled synthetic scene and produced structured observations containing:

- Label
- Confidence
- Bounding box
- Center position
- Segmentation mask
- Mask area

The SAM3 model checkpoint is stored through the Hugging Face cache on the project's Z: drive. The official SAM3 source repository is kept separately under `external/sam3`.

---

## Important Architectural Principle

Vortiqo is intended to be **goal-driven rather than rule-driven**.

A traditional hard-coded manipulation system might use logic such as:

```python
if object == "bottle":
    move_to("blue_bin")
elif object == "cup":
    move_to("red_bin")
```

Vortiqo instead aims for:

```text
High-level goal
      ↓
Understand goal
      ↓
Observe environment
      ↓
Determine relevant objects
      ↓
Determine required subtasks
      ↓
Generate plan
      ↓
Execute
      ↓
Verify
      ↓
Replan if necessary
```

The intermediate procedure should be derived by the agent rather than completely hard-coded.

---

## Perception → Reasoning → Action Loop

The agent is designed around an iterative loop:

```text
PERCEIVE
   ↓
UNDERSTAND
   ↓
PLAN
   ↓
ACT
   ↓
OBSERVE
   ↓
EVALUATE
   ↓
GOAL ACHIEVED?
   │
   ├── YES → REPORT COMPLETION
   │
   └── NO  → REPLAN
                ↓
               ACT
```

This allows the agent to respond to changes in the environment.

For example, an object that was hidden during the initial observation may become visible after another object is moved. The agent should update its world state and determine whether another action is required.

---

## Perception and Evidence Fusion

The current perception architecture separates **grounded geometric evidence** from **semantic interpretation**.

```text
                         CAMERA
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
               SAM3                SmolVLM2
                 │                     │
        masks / boxes /          semantic evidence
        geometry / confidence    attributes / labels
                 │                     │
                 └──────────┬──────────┘
                            ▼
                     Evidence Fusion
                            │
                            ▼
                       WORLD STATE
```

The purpose of this separation is to avoid allowing a generative VLM to silently replace grounded observations.

For example:

```text
SAM3:
    region_01
    bbox = [...]
    mask = [...]
    detection_confidence = 0.91

SmolVLM2:
    semantic_label = "cup"
    semantic interpretation = ...
```

The system should retain the distinction between:

- What is geometrically observed
- What is semantically inferred
- How confident each source is
- Which model produced each observation

This evidence-fusion layer is still under development.

---

## World State

The agent requires a representation of the environment that can be used for planning.

A conceptual world state may contain:

```text
Object
 ├── Identity
 ├── Location
 ├── Properties
 ├── Relationships
 ├── Task relevance
 └── Observation / confidence metadata
```

Current implementation includes explicit `WorldObject` and `WorldState` structures.

A `WorldObject` currently stores:

- Label
- Confidence
- Bounding box
- Center
- Segmentation mask
- Mask area
- Optional semantic location

The current implementation intentionally keeps the world-state representation independent from the SAM3 `Scene` object. A dedicated adapter converts perception output into world-state objects.

Semantic information from SmolVLM2 has **not yet been directly merged into the authoritative world state**. This will be introduced through an evidence-fusion/normalization layer after further evaluation.

Example conceptual state:

```text
Object:
    Identity: red cup
    Location: Table
    Properties: [...]
    Relationships: [...]
    Relevant to current goal: Yes
    Detection confidence: [...]
    Semantic confidence: [...]
```

The world state is intended to provide the bridge between perception and task planning.

---

## Language Grounding

A major objective is to ground natural language into the physical environment.

For example:

```text
"Move the red cup to the kitchen."
```

must be connected to:

```text
"red cup"
     ↓
Actual visual object
```

and:

```text
"kitchen"
     ↓
Physical / semantic destination
```

Similarly:

```text
"Clean the table."
```

must be translated from an abstract goal into a set of meaningful physical actions.

### Current language implementation

The current baseline language layer contains a structured `Goal` representation:

```text
Goal
 ├── action
 └── target
```

A temporary rule-based goal parser currently supports basic variations of cleaning/table instructions, including:

- "Clean the table."
- "Can you get the table cleaned up?"
- "I want the table tidy."
- "Please clear everything from the table."

This parser is a **temporary baseline**, not the intended final language-understanding system.

---

## Task Context

The goal and current world state are combined into a `TaskContext` before reasoning.

Conceptually:

```text
Goal
  +
World State
  ↓
Task Context
  ↓
Reasoning / Planning
```

This establishes a stable interface between language understanding, perception, and the planning layer.

---

## Task Reasoning and Planning

The planning layer uses a structured task representation.

A `PlanStep` currently contains:

```text
PlanStep
 ├── action
 ├── target
 ├── destination
 └── parameters
```

A `TaskPlan` contains an ordered list of `PlanStep` objects.

The project currently contains:

- A `TaskReasoner` abstract interface
- A temporary `BaselineReasoner`
- An `AIReasoner` abstraction
- A `ReasoningInput` representation
- A `MockAIReasoner` used to validate the reasoning/planning interfaces

The baseline and mock implementations exist to validate architecture and data flow. They are **not the final autonomous reasoning system**.

The intended future flow is:

```text
Goal
  +
World State
  ↓
Reasoning Input
  ↓
AI Task Reasoner
  ↓
Task Plan
  ↓
Action Generation
```

The final reasoning model and planning strategy remain under evaluation.

---

## Current Repository Structure

The repository is organized to keep the major components of the agent separate:

```text
Epson-VT6L-Vision-Guided-System/   # separate WILP project
```

Vortiqo uses:

```text
Robotics-AI-Agent/
│
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── requirements.txt
├── pyproject.toml
│
├── configs/
│
├── src/
│   └── vortiqo/
│       ├── agent/
│       ├── perception/
│       ├── language/
│       ├── planning/
│       ├── policy/
│       ├── robotics/
│       ├── execution/
│       ├── verification/
│       └── interfaces/
│
├── models/
├── scripts/
├── experiments/
├── tests/
├── data/
├── logs/
├── docs/
└── notebooks/
```

### `src/vortiqo/`

Contains the reusable implementation of the Vortiqo agent.

### `agent/`

High-level agent orchestration, goal management, world-state management, and task coordination.

### `perception/`

Camera processing, SAM3 integration, segmentation, object localization, scene understanding, and visual grounding. SmolVLM2 semantic perception is also being evaluated here.

### `language/`

Natural-language processing, goal extraction, and language grounding. VLM capabilities may contribute to language/vision grounding as the architecture evolves.

### `planning/`

Task decomposition, task planning, action planning, reasoning interfaces, and replanning.

### `policy/`

VLA models and action-generation components, including future SmolVLA integration.

### `robotics/`

Robot interfaces, robot state, and integration with the underlying robotics framework.

### `execution/`

Execution of generated robot actions and safety-related checks.

### `verification/`

Goal verification, scene checking, and failure detection.

### `experiments/`

Experimental implementations and research code that may later be converted into reusable components.

### `tests/`

Unit and integration tests for the individual system components.

Current tests cover, among other things:

- SAM3 perception
- World-state construction
- Goal parsing
- Task context
- Reasoning input
- Mock AI reasoning
- SmolVLM2 model loading and inference

### `models/`

Local model weights, checkpoints, and model-cache configuration.

Large model files should not be committed to Git.

The project's Hugging Face cache is configured on the Z: drive:

```text
Z:\Robotics-AI-Agent\models\hf_cache
```

This keeps large model artifacts off the system C: drive.

### `data/`

Datasets, demonstrations, processed data, and experimental data.

Large datasets should generally remain outside Git and be referenced through appropriate dataset/configuration mechanisms.

### `external/`

Third-party source repositories used by the project.

For example:

```text
external/
└── sam3/
```

The SAM3 source repository is kept separately from its downloaded model checkpoint/cache.

---

## Development Environment

The primary Vortiqo development environment is:

```text
Z:\Robotics-AI-Agent\.venv
```

Current validated environment:

```text
Python:       3.12.10
PyTorch:      2.10.0+cu128
Torchvision:  0.25.0+cu128
LeRobot:      0.6.1
Transformers: 5.17.0
NumPy:        2.2.6
GPU:          NVIDIA GeForce RTX 4060 Laptop GPU
CUDA:         Available
```

SAM3 is maintained in an isolated environment:

```text
Z:\Robotics-AI-Agent\.venvs\sam3
```

The SAM3 environment uses a compatible dependency configuration that is kept separate from the main Vortiqo environment.

The project deliberately allows model-specific environments where dependency conflicts make isolation preferable.

---

## Model and Storage Management

Large model artifacts are not stored directly in the Git repository.

Hugging Face model caching is configured to use:

```text
HF_HOME=Z:\Robotics-AI-Agent\models\hf_cache
```

Currently downloaded model artifacts include:

```text
SAM3
SmolVLM2-500M-Video-Instruct
```

The project therefore separates:

```text
Third-party source code
        ↓
external/

Downloaded model artifacts
        ↓
models/hf_cache/
```

This distinction should be maintained as additional models are introduced.

---

## Development Roadmap

The project is intended to progress through the following stages.

### Stage 1 — Environment Setup

Completed/validated areas include:

- Python environment
- PyTorch
- CUDA GPU inference
- Hugging Face ecosystem
- LeRobot
- SAM3
- SmolVLM2

SmolVLA remains under evaluation and has not yet been integrated into the active execution pipeline.

The objective is to maintain a functioning development environment for the robotics AI stack while isolating model-specific dependencies where necessary.

### Stage 2 — Perception

Develop the visual perception pipeline:

```text
Camera
   ↓
SAM3
   ↓
Grounded visual regions
   ↓
SmolVLM2
   ↓
Semantic interpretation
   ↓
Evidence Fusion
   ↓
World State
```

Current progress:

- SAM3 environment established
- SAM3 checkpoint downloaded and validated sufficiently for local testing
- SAM3 multi-object perception tested
- Structured perception objects implemented
- World-state representation implemented
- SmolVLM2 model downloaded and loaded successfully
- SmolVLM2 controlled inference tested
- SmolVLM2 hallucination behavior identified and is being investigated

Next perception work:

- Evaluate SmolVLM2 on natural scenes
- Evaluate semantic attributes and relationships
- Test SAM3-region/crop → SmolVLM2 inference
- Define semantic evidence normalization
- Fuse SAM3 and SmolVLM2 observations into the world state

### Stage 3 — Language Understanding

Convert natural-language instructions into structured goals:

```text
Human instruction
       ↓
Language / VLM
       ↓
Goal representation
```

Current baseline:

```text
Goal
 ├── action
 └── target
```

A temporary deterministic parser validates the interface. More capable language understanding will be introduced after the perception/reasoning interfaces are stable.

### Stage 4 — Task Reasoning and Planning

Combine the goal with the perceived environment:

```text
Goal
  +
Environment State
  ↓
Task Decomposition
  ↓
Task Plan
```

Current progress:

- `TaskContext`
- `TaskReasoner`
- `AIReasoner`
- `ReasoningInput`
- `PlanStep`
- `TaskPlan`
- Baseline reasoner
- Mock AI reasoner

The mock/baseline implementations exist for architectural validation and will eventually be replaced or supplemented by the actual reasoning system.

### Stage 5 — Robot Policy

Use visual observations, task information, and robot state to generate robot actions through the VLA policy.

```text
Instruction
    +
Visual observations
    +
Robot state
    ↓
  SmolVLA
    ↓
Robot actions
```

This stage has not yet been integrated into the complete Vortiqo loop.

### Stage 6 — Execution

Execute generated actions through the robotics stack and observe the resulting environment.

### Stage 7 — Verification and Replanning

Determine whether the requested goal has been achieved.

```text
Goal
 ↓
Execute
 ↓
Observe
 ↓
Verify
 ├── Goal achieved → Finish
 └── Goal not achieved → Replan
```

The final verification mechanism must evaluate the **requested goal**, rather than merely checking whether a predefined list of objects has been processed.

---

## Example Task

### Input

```text
"Clean the table."
```

### Agent process

```text
1. Understand the goal
2. Inspect the table
3. Identify objects
4. Determine which objects are clutter
5. Determine suitable destinations
6. Generate a task plan
7. Execute manipulation actions
8. Observe the new scene
9. Check whether the table is clean
10. Replan if necessary
11. Report the result
```

### Successful completion

```text
"The table has been cleaned."
```

### Failure

```text
"I could not complete the task because the remaining object
could not be safely grasped."
```

The reporting layer should be capable of communicating completion, failure, uncertainty, and the reason for stopping.

---

## Difference From the WILP Robotics Project

Vortiqo intentionally differs from the separate industrial robotics project.

### Industrial Robotics Project

The industrial system focuses on:

```text
Object classification
        ↓
Object localization
        ↓
Coordinate transformation
        ↓
Robot motion
        ↓
Pick and place
```

The handling policy is largely defined in advance.

### Vortiqo

Vortiqo focuses on:

```text
Natural-language goal
        ↓
Language understanding
        ↓
Visual understanding
        ↓
Reasoning
        ↓
Task decomposition
        ↓
Planning
        ↓
VLA action generation
        ↓
Robot execution
        ↓
Feedback
        ↓
Goal verification
```

The defining distinction is that:

> **The human provides the goal while the AI determines the procedure.**

---

## Current Development Status

The project is currently in the **architecture, perception, and model-evaluation phase**.

### Implemented and validated

- Repository architecture
- Python package structure
- Main development environment
- CUDA-enabled PyTorch inference
- LeRobot installation
- Isolated SAM3 environment
- SAM3 model/source setup
- SAM3 multi-object perception tests
- Structured perception output
- World-state data structures
- Scene → world-state adapter
- Baseline natural-language goal parser
- Task context
- Task planning data structures
- Abstract task-reasoning interface
- AI reasoning interface
- Mock AI reasoner
- SmolVLM2 model setup
- SmolVLM2 GPU inference
- Structured SmolVLM2 scene extraction test
- Controlled SmolVLM2 hallucination experiment

### Current findings

SAM3 is currently functioning as the project's grounded visual perception component.

SmolVLM2 has demonstrated useful constrained visual understanding on controlled scenes, including object counting and structured color/shape/position extraction. It has also demonstrated significant hallucination under unconstrained scene-description prompts.

The current design therefore treats SmolVLM2 as a **semantic evidence source**, not an unquestioned source of world-state truth.

### Current work

- SmolVLM2 natural-scene evaluation
- SmolVLM2 prompt/grounding evaluation
- SAM3 + SmolVLM2 evidence fusion design
- World-state semantic normalization
- Task reasoning integration
- Evaluation of planning strategies
- Future SmolVLA integration

The exact division of responsibility between individual models and system components will continue to be finalized as implementation and evaluation progress.

---

## Project Philosophy

The core principle of Vortiqo is:

```text
HUMAN PROVIDES THE GOAL.

AI OBSERVES THE ENVIRONMENT.

AI FIGURES OUT THE PROCEDURE.

ROBOT EXECUTES THE PROCEDURE.

AI OBSERVES THE RESULT.

AI DECIDES WHETHER THE GOAL IS ACHIEVED.
```

The project therefore focuses on **agentic AI for robotics**, rather than simply automating a fixed sequence of robot movements.

---

## Research Areas

The project brings together concepts from:

- Natural Language Processing
- Multimodal AI
- Computer Vision
- Vision-Language Models
- Vision-Language-Action Models
- Scene Understanding
- Visual Grounding
- Task Planning
- Task Decomposition
- Imitation Learning
- Robot Learning
- Agentic AI
- World-State Representation
- Evidence Fusion
- Feedback and Replanning
- Autonomous Manipulation

---

## Status

**Project:** Vortiqo Robotics AI Agent

**Type:** Robotics AI / Agentic AI / VLA

**Development Status:** Active Development

The architecture and model stack are under active development and may change as individual components are evaluated.

---

## License

This project is currently under development. Licensing information will be added as the project matures.
