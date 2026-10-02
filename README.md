# Vortiqo

**Company:** Vortiqo.

This project is being developed for the company named **Vortiqo**. The project itself is a goal-driven robotics agent: a person will type an instruction into a web interface, and a robot arm in Gazebo will interpret the intended outcome, inspect the scene, plan and perform actions, then check whether the outcome was achieved.

The demonstration domain is a tabletop workspace. For example, given **“tidy the table”**, the agent should identify loose objects, decide where each belongs under the workspace's stated conventions, move them with a simulated gripper, and inspect the table again. It should also handle direct requests such as **“put the red cup in the tray.”** If a request is genuinely ambiguous or outside the robot's capabilities, it should explain the uncertainty or ask for clarification.

## Intended system

```text
Written goal in browser
    → goal interpretation
    → Gazebo camera observation
    → SAM3 object regions + SmolVLM2 semantic evidence
    → grounded world state and task plan
    → ROS 2 / MoveIt robot actions in Gazebo
    → new observation and goal verification
    → replan or report the result
```

SAM3 is intended to locate and segment objects; SmolVLM2 is intended to help identify and describe them. A separate goal interpreter and planner will turn the user's words and the observed scene into validated robot skills. The first version will use conventional motion planning for arm movement; a learned action policy is a possible later experiment.

## Project outcome

The target is a reproducible end-to-end simulation, launched with documented commands, that accepts written goals through the frontend and completes direct and reasonably vague tabletop tasks. Evaluation will use varied object arrangements and prompt wording, and will report task success, perception errors, grasp failures, and replanning behavior. Gazebo's true object state may score runs but will not be the agent's runtime perception source.

**Status:** The repository has an organized scaffold and an [implementation plan](PROJECT_PLAN.md). SAM3's source, Python environment, Hugging Face cache, and downloaded checkpoint are stored locally on the Z drive. The environment detects the CUDA GPU. ROS 2, Gazebo, robot control, the agent, and frontend are still to be set up or built.

## Why `vortiqo` appears in folder names

The folder `src/vortiqo/` is the planned Python import package for the agent's code. The ROS folders `vortiqo_description` and `vortiqo_gazebo` are separate ROS packages with a shared project prefix. These names identify software namespaces and packages; they are not extra copies of the company folder. The repository root is the project workspace, while **Vortiqo** is the company the project is for.
