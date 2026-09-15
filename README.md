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

* Understanding natural-language instructions
* Extracting high-level task goals
* Connecting language to objects and locations in the physical environment
* Perceiving and understanding the surrounding scene
* Maintaining a representation of the current world state
* Decomposing high-level goals into actionable subtasks
* Generating task plans dynamically
* Generating robot actions using Vision-Language-Action models
* Executing actions through a robotics software stack
* Observing the environment after actions
* Detecting whether the goal has been achieved
* Replanning when the current plan is insufficient
* Reporting task completion, failure, or uncertainty to the human

---

## Core Architecture

The intended architecture consists of several interacting layers:

```text
                        HUMAN
                          │
                          │ Natural-language goal
                          ▼
                ┌─────────────────────┐
                │  LANGUAGE / VLM     │
                │      SmolVLM        │
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
                │ Camera + SAM3 + VLM │
                └──────────┬──────────┘
                           │
                           ▼
                      WORLD STATE
                           │
                           ▼
                    Task Planning
                           │
                           ▼
                ┌─────────────────────┐
                │        VLA          │
                │      SmolVLA        │
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
                  ┌────────┴────────┐
                  │                 │
                 NO                YES
                  │                 │
                  ▼                 ▼
               Replan             Finish
```

The exact division of responsibility between the language model, perception models, reasoning/planning layer, and VLA policy will be refined during implementation.

---

## Technology Stack

The project is being developed around the Hugging Face robotics ecosystem and related vision-language models.

### LeRobot

[LeRobot](https://github.com/huggingface/lerobot) provides the primary robotics software foundation for the project.

It is being explored for:

* Robot interfaces
* Robot policies
* Vision-Language-Action models
* Robot datasets
* Imitation learning
* Training and evaluation
* Hardware integration

### SmolVLM

SmolVLM is being explored as a compact **Vision-Language Model** component.

Potential responsibilities include:

* Multimodal understanding
* Visual scene interpretation
* Connecting language to visual information
* Understanding objects and their relationships
* Supporting language grounding and reasoning

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

### SAM3

[Meta's SAM3](https://github.com/facebookresearch/sam3) is being explored for visual perception and segmentation.

Potential responsibilities include:

* Object segmentation
* Region identification
* Object localization
* Visual scene information extraction

SAM3 is primarily considered a **perception component** rather than the task-planning or action-generation component.

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

## World State

The agent requires a representation of the environment that can be used for planning.

A conceptual world state may contain:

```text
Object
 ├── Identity
 ├── Location
 ├── Properties
 ├── Relationships
 └── Task relevance
```

For example:

```text
Cup
 ├── Location: Table
 ├── Destination: Storage
 └── Relevant to current goal: Yes

Bottle
 ├── Location: Table
 ├── Destination: Recycling
 └── Relevant to current goal: Yes
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

---

## Repository Structure

The repository is organized to keep the major components of the agent separate:

```text
Vortiqo-Robotics-Agent/
│
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── requirements.txt
├── pyproject.toml
│
├── configs/
│   ├── default.yaml
│   ├── models.yaml
│   ├── robot.yaml
│   ├── camera.yaml
│   └── environments.yaml
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

Camera processing, SAM3 integration, segmentation, object localization, scene understanding, and visual grounding.

### `language/`

Natural-language processing, SmolVLM integration, goal extraction, and language grounding.

### `planning/`

Task decomposition, task planning, action planning, and replanning.

### `policy/`

VLA models and action-generation components, including SmolVLA.

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

### `models/`

Local model weights and checkpoints.

Large model files should not be committed to Git.

### `data/`

Datasets, demonstrations, processed data, and experimental data.

Large datasets should generally remain outside Git and be referenced through appropriate dataset/configuration mechanisms.

---

## Development Roadmap

The project is intended to progress through the following stages.

### Stage 1 — Environment Setup

Set up:

* Python environment
* PyTorch
* Hugging Face ecosystem
* LeRobot
* SAM3
* SmolVLM
* SmolVLA

The objective is to establish a functioning development environment for the robotics AI stack.

### Stage 2 — Perception

Develop the visual perception pipeline:

```text
Camera
  ↓
Vision Models / SAM3
  ↓
Objects + Scene Information
  ↓
World State
```

### Stage 3 — Language Understanding

Convert natural-language instructions into structured goals:

```text
Human instruction
       ↓
Language / VLM
       ↓
Goal representation
```

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

Vortiqo intentionally differs from the industrial robotics project being developed separately.

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

The defining distinction is that **the human provides the goal while the AI determines the procedure**.

---

## Current Development Status

The project is currently in the development and integration phase.

Current areas of work include:

* Robotics AI environment setup
* LeRobot exploration
* SmolVLM exploration
* SmolVLA exploration
* SAM3 environment setup
* Vision/perception experiments
* Defining the agent architecture
* Designing the world-state representation
* Planning the perception → reasoning → action → verification loop

The exact division of responsibility between individual models and system components will be finalized as implementation and evaluation progress.

---

## Project Philosophy

The core principle of Vortiqo is:

```text
HUMAN PROVIDES THE GOAL.
AI FIGURES OUT THE PROCEDURE.
ROBOT EXECUTES THE PROCEDURE.
AI OBSERVES THE RESULT.
AI DECIDES WHETHER THE GOAL IS ACHIEVED.
```

The project therefore focuses on **agentic AI for robotics**, rather than simply automating a fixed sequence of robot movements.

---

## Research Areas

The project brings together concepts from:

* Natural Language Processing
* Multimodal AI
* Computer Vision
* Vision-Language Models
* Vision-Language-Action Models
* Scene Understanding
* Visual Grounding
* Task Planning
* Task Decomposition
* Imitation Learning
* Robot Learning
* Agentic AI
* World-State Representation
* Feedback and Replanning
* Autonomous Manipulation

---

## Status

**Project:** Vortiqo Robotics AI Agent
**Type:** Robotics AI / Agentic AI / VLA
**Development Status:** Active Development

The architecture and model stack are under active development and may change as individual components are evaluated.

---

## License

This project is currently under development. Licensing information will be added as the project matures.
