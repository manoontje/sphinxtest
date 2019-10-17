.. _Reference

=========
Reference
=========

This is the class and function reference of MATRXS. Please refer to the tutorials for further details, as the
class and function raw specifications may not be enough to give full guidelines on their uses.

World classes
=============

Classes
-------

.. toctree::
   :maxdepth: 2
   :hidden:

.. autosummary::
   :toctree: _generated_autodoc

   matrxs.world_builder.WorldBuilder
   matrxs.grid_world.GridWorld

Functions
---------

.. toctree::
   :maxdepth: 2
   :hidden:

.. autosummary::
   :toctree: _generated_autodoc

   matrxs.world_builder.WorldBuilder.worlds

Agent brains
============

Classes
-------
.. toctree::
   :maxdepth: 2
   :hidden:

.. autosummary::
   :toctree: _generated_autodoc

   matrxs.agents.agent_brain.AgentBrain
   matrxs.agents.human_agent_brain.HumanAgentBrain
   matrxs.agents.patrolling_agent.PatrollingAgentBrain
   matrxs.agents.capabilities.capability.SenseCapability

Functions
---------

.. toctree::
   :maxdepth: 2
   :hidden:

.. autosummary::
   :toctree: _generated_autodoc

   matrxs.agents.agent_brain.AgentBrain.initialize
   matrxs.agents.agent_brain.AgentBrain.filter_observations
   matrxs.agents.agent_brain.AgentBrain.decide_on_action
   matrxs.agents.agent_brain.AgentBrain.send_message
   matrxs.agents.agent_brain.AgentBrain.is_action_possible
