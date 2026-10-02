# Vortiqo project plan

This is the build and learning sequence for a portfolio-ready robotics AI agent. Work through the milestones in order. Each milestone ends with a visible result and a check that must pass before moving on.

## 1. Define the finish line

The final demonstration starts from a web page. A user enters a natural-language goal such as “put the red cup in the tray,” “move the cup away from the plate,” or “tidy the table.” A simulated arm in Gazebo observes a tabletop scene, chooses actions, moves objects with a gripper, observes the result, and reports whether the goal was achieved. If a grasp fails or the scene changes, it tries a bounded recovery. If the goal cannot be grounded in the scene, it requests clarification or reports why it cannot proceed.

The first domain is deliberately limited to tabletop manipulation: one arm, one gripper, a fixed camera, a table, a few object types, and two or three destination regions. “Vague” means the agent can infer a sensible outcome **within that domain** from scene evidence and documented conventions. It does not mean unrestricted household competence.

### Completion criteria

- One documented startup procedure launches Gazebo, robot control, agent service, and frontend.
- A browser user can submit a goal, see the camera feed and agent progress, answer a clarification, stop a run, and read the verified outcome.
- The robot physically picks and places objects with simulated joint/gripper motion; it never teleports an object to claim success.
- The agent estimates objects and locations from camera/depth and robot observations. Gazebo ground truth is reserved for tests and scoring.
- The agent handles direct placement, relational placement, and vague tidying tasks in varied scenes, including an already-satisfied goal and a failed grasp.
- A held-out evaluation contains at least 20 randomized episodes per task family. Report success rate, object detection/label errors, grasp/place failures, replans, clarification requests, and average run time. Aim for at least 80% task success, but publish the measured result.
- The repository includes setup instructions, architecture notes, evaluation results, and a short demo video when implementation is complete.

## 2. Architecture and responsibilities

```text
Frontend ── written goal ──> Agent API
                              │
                              ▼
                    Goal interpreter ──> desired-state predicates
                                                │
Gazebo RGB/depth ──> SAM3 ──> SmolVLM2 ──> world state
                                                │
                                                ▼
                                      grounded task planner
                                                │
                                                ▼
                               validated pick/place skill calls
                                                │
                                                ▼
                             MoveIt / ROS 2 control / Gazebo
                                                │
                                                ▼
                                observe → verify → replan/report
```

| Component | Owns | Must not do |
| --- | --- | --- |
| Goal interpreter | Convert written input into a desired final state, assumptions, and clarification needs | Invent scene objects or directly command joints |
| SAM3 | Image regions, boxes, masks, detection scores | Decide the task goal |
| SmolVLM2 | Constrained semantic descriptions of a scene or object crop | Override visible geometry without evidence |
| World state | Stable object IDs, 3D estimates, attributes, relationships, and evidence provenance | Treat a model guess as certain fact |
| Task planner | Choose grounded actions that can satisfy the desired state | Output unsupported skills or unvalidated targets |
| Robot skills | Move, grasp, place, retreat, and report execution status | Decide what the human meant |
| Verifier | Compare a fresh observation with the requested final state | Declare success just because a plan ran |

Define typed contracts early: `Observation`, `WorldObject`, `GoalSpec`, `PlanStep`, `SkillResult`, and `RunStatus`. Give every pose a coordinate frame and timestamp. Validate model output against known objects, supported skills, and reachable destinations before execution.

## 3. Platform decision and setup

Start with **Ubuntu 24.04, ROS 2 Jazzy, and Gazebo Harmonic**, the documented supported pairing. On a Windows workstation, test WSL2 graphics, GPU inference, ROS networking, camera topics, and the Gazebo GUI immediately. If that stack is unreliable, use native Ubuntu for Gazebo and ROS. Keep the ROS environment separate from model-specific Python environments when dependencies conflict, and communicate through explicit topics/services rather than a shared global Python environment.

Use `ros_gz_bridge` for simulated sensor topics and `gz_ros2_control` for joint control. Select a robot/gripper only after confirming that its description, controllers, and MoveIt 2 configuration work with the chosen ROS/Gazebo versions. A Franka Panda is a candidate, but a maintained working integration is more valuable than a particular robot model.

**Learning focus:** ROS 2 topics, services, actions, TF frames, camera calibration, controllers, motion planning, and Gazebo worlds.

**Gate:** Launch a tiny world; read RGB/depth and joint states from ROS; command one safe joint movement; record exact versions and commands.

Official references: [ROS/Gazebo pairing](https://gazebosim.org/docs/jetty/ros_installation/), [Gazebo ROS integration](https://gazebosim.org/docs/harmonic/ros2_integration/), [`gz_ros2_control`](https://control.ros.org/jazzy/doc/gz_ros2_control/doc/index.html), and [MoveIt Task Constructor](https://moveit.picknik.ai/main/doc/tutorials/pick_and_place_with_moveit_task_constructor/pick_and_place_with_moveit_task_constructor.html).

## 4. Milestones

### M0 — Write down the tabletop domain

Define a small scene: table, robot, camera, 3–5 movable object types, 2–3 destinations, fixed obstacles, and a home pose. Write conventions for vague instructions. For example, “tidy” may mean cups in a cup tray, dishes in a dish area, and nonclutter objects left in place. Define what should trigger clarification. Create a small set of target prompts and scene sketches.

**Deliverable:** A domain specification and scenario list. **Gate:** A human can judge from the specification whether each example scene satisfies each goal.

### M1 — Make the simulated robot manipulate objects

Build the Gazebo world and robot description. Configure the gripper, controllers, TF tree, collision geometry, camera, and MoveIt. Implement `move_home`, `pick(pose)`, and `place(pose)` with approach, grasp, lift, transfer, release, and retreat. At this stage, scripted target poses may be supplied by the scenario so robot control can be debugged independently of AI.

**Learning focus:** robot kinematics, planning scenes, grasp geometry, contacts, and trajectory execution.

**Deliverable:** A recorded scripted pick-and-place run. **Gate:** At least 20 randomized reachable pick/place trials with measured success and failure reasons. Fix the largest control failure before progressing.

### M2 — Recover object locations from sensors

Publish aligned RGB and depth, camera intrinsics, and transforms. Implement pixel/depth-to-3D conversion, object pose estimates, candidate grasp poses, and object identity across observations. Add basic spatial relationships such as `on_table`, `inside_tray`, and `near`.

**Learning focus:** camera geometry, coordinate frames, tracking, uncertainty, and sensor timing.

**Deliverable:** Visual overlays and logged 3D object positions. **Gate:** Sensor-derived target positions support the M1 grasp skill in varied scenes. The runtime agent no longer reads simulator truth to locate objects.

### M3 — Integrate SAM3 and SmolVLM2

Use SAM3 to segment objects from camera images and produce boxes, masks, and detection scores. Use SmolVLM2 for narrowly worded questions about visible objects and object crops: likely category, color, or relevant attributes. Fuse those outputs with depth-derived geometry, keep source and confidence for each claim, merge duplicates, and reject malformed model output. Load each model once in a long-lived worker. Retest model inference on actual Gazebo images, not only synthetic shapes.

**Learning focus:** open-vocabulary detection, segmentation, VLM prompting, hallucination analysis, structured outputs, and model evaluation.

**Deliverable:** An annotated scene dataset and perception report. **Gate:** On at least 30 varied labeled images, measure detection recall, false positives, semantic label accuracy, and 3D localization error. Inspect failure examples and make the output usable by M1 skills.

References: [SAM3 project](https://github.com/facebookresearch/sam3) and [SmolVLM documentation](https://huggingface.co/docs/transformers/model_doc/smolvlm).

### M4 — Interpret direct and vague goals

Implement a goal interpreter behind a model-neutral interface. Supply the user text, current scene summary, supported skills, and domain conventions. Require a typed `GoalSpec` containing desired-state predicates, assumptions, confidence, and any clarification question. Validate that referenced objects and destinations exist or can be discovered. Start with direct instructions; then add paraphrases, relational goals, vague tidying, already-satisfied goals, and unsupported requests.

Examples: `in(red_cup, cup_tray)` for a direct instruction; `clear(table, clutter)` for “tidy the table,” with the destination convention expanded into per-object goals. Keep the original wording in the run log so the interpretation is inspectable.

**Learning focus:** grounding language in perception, prompting versus rules, ambiguity handling, and output validation.

**Deliverable:** A labeled prompt set with expected interpretations. **Gate:** The interpreter either returns a defensible validated goal or asks a specific clarification; it does not silently invent an action.

### M5 — Plan, act, observe, and verify

Build a task planner over supported skills and their preconditions/effects. A model may propose high-level steps, but a validator checks object IDs, destinations, reachability, and allowed skills. Execute one step, read the resulting observation, update world state, and check the requested final-state predicates. Replan after a failed grasp, missing object, or scene change. Limit retries and total run time.

**Learning focus:** task planning, state machines, feedback control, failure recovery, and goal verification.

**Deliverable:** A terminal-driven end-to-end run before adding the frontend. **Gate:** The agent solves a direct task, avoids action when the goal is already satisfied, and recovers from one induced failure or reports a justified partial result.

### M6 — Build the service and frontend

Expose a small API: start a run with a written goal, retrieve status, send a clarification reply, and request a stop. Stream camera frames and events by WebSocket or server-sent events. Permit one active robot run initially. The frontend shows goal entry, live scene, interpreted goal and assumptions, current action, event timeline, clarification prompt, and final report. A stop request must halt further action safely.

**Learning focus:** API design, asynchronous robot runs, frontend state, and useful observability.

**Deliverable:** A browser-only demo after startup. **Gate:** A user can submit and complete a task, answer a clarification, refresh to recover run status, and understand failures from the displayed result.

### M7 — Evaluate, improve, and present

Generate repeatable held-out scenes with randomized placement, object count, colors, distractors, and prompt paraphrases. Score final state with Gazebo truth **only in the evaluator**. Save input images, masks, goal interpretation, plans, skill results, final state, and video for each run. Separate failures by perception, language, planning, grasp/control, and verification. Improve the largest measured failure category, then rerun the same benchmark.

**Learning focus:** experimental design, ablation studies, error analysis, reproducibility, and honest reporting.

**Deliverable:** Results table, architecture diagram, setup guide, demo video, and a concise account of limitations. **Gate:** Run the held-out evaluation specified in section 1 and publish its actual metrics.

### M8 — Optional research extensions

Only after M7: compare a stronger VLM or text reasoner, try active camera views, add a second task domain, or collect demonstrations and fine-tune a learned action policy such as SmolVLA. Keep the M7 system as a working baseline to compare against. The [SmolVLA guide](https://huggingface.co/docs/lerobot/smolvla) describes task-specific data collection and fine-tuning.

## 5. Recommended repository layout as code is added

The empty directories below are tracked with `.gitkeep` files. Add implementation files as each milestone begins; remove a `.gitkeep` when the directory contains real files.

```text
README.md
PROJECT_PLAN.md
frontend/
  public/                  # Static browser assets
  src/                     # UI components and API client, M6
ros2_ws/src/
  vortiqo_description/
    urdf/                  # Robot description and sensor mounting
    meshes/                # Project-owned geometry, if needed
  vortiqo_gazebo/
    worlds/                # Tabletop simulation scenes
    models/                # Project-owned objects and fixtures
    config/                # Controllers and bridge settings
    launch/                # Gazebo/ROS startup files
src/vortiqo/
  api/                     # Run endpoints and event stream
  agent/                   # Orchestration and world state
  execution/               # Action loop, retries, and skill results
  interfaces/              # Shared typed contracts
  language/                # Goal interpretation and clarification
  perception/              # SAM3, SmolVLM2, fusion, 3D localization
  planning/                # Goal-grounded plans and validation
  robotics/                # ROS client and robot skills
  verification/            # Desired-state checks
configs/scenarios/         # Domain conventions and seeded scenarios
tests/
  unit/                    # Schemas, validation, and pure logic
  integration/             # Component and ROS interface checks
  e2e/                     # Gazebo task runs and scoring
docs/                      # Setup, architecture, and evaluation notes
```

The two ROS package directories are organizational placeholders, not buildable packages yet. Select and verify a robot before adding package manifests or a MoveIt configuration. Keep model weights, datasets, virtual environments, ROS build output, frontend dependencies, and run logs out of Git. Add dependency locks and setup instructions when each working environment exists.

## Local storage policy

Keep all large local assets on the Z drive under this workspace:

```text
.venvs/<component>/          # Component-specific Python environments
external/<repository>/       # Third-party source checkouts
models/hf_cache/             # Hugging Face tokens and model checkpoints
models/pip_cache/            # Temporary pip download cache
models/tmp/                  # Temporary package and model files
data/                         # Datasets and generated evaluation data
logs/                         # Local execution and installation logs
```

Install packages into a component-specific virtual environment rather than the global Python installation. Set `HF_HOME`, `HUGGINGFACE_HUB_CACHE`, `PIP_CACHE_DIR`, `TEMP`, and `TMP` to Z-drive paths before large downloads. If a required tool cannot avoid writing large data to C, request approval before installing it.

## 6. Order of work for the first session

1. Select the Ubuntu environment and confirm Jazzy/Harmonic launch and graphics.
2. Choose a robot with a working Jazzy controller and MoveIt example.
3. Create a minimal table world with one camera and two movable objects.
4. Prove one commanded joint movement and read RGB/depth, joint states, and TF.
5. Record the exact setup commands and the first blocker or passing result before adding AI dependencies.

The main rule for the project is to keep a working, measured baseline at each milestone. AI components should improve a complete physical loop, not substitute for one.

## Current local baseline

- Workspace: `Z:\Robotics-AI-Agent`.
- Local policy: keep environments, third-party checkouts, model weights and caches, temporary downloads, datasets, and logs on the Z drive. These paths are excluded from Git by `.gitignore`.
- SAM3: source checkout at `external/sam3`; Python environment at `.venvs/sam3`; Hugging Face cache and checkpoint at `models/hf_cache`. The installed environment reports PyTorch `2.10.0+cu128`, imports SAM3 from the Z drive, and detects CUDA. The earlier setup session also completed a SAM3 image prompt and mask inference check on the GPU.
- Simulator: ROS 2 and Gazebo are not configured yet. Choose and verify the Linux/WSL/native setup as the next milestone; do not install simulator dependencies until that setup step is approved.
- Git: local SAM3 and model files are ignored. The README and this plan are the tracked project guide; review local changes before committing or pushing.
