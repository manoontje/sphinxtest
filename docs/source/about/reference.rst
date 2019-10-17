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

   matrxs.world_builder
   matrxs.grid_world

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

   matrxs.agents.agent_brain
   matrxs.agents.human_agent_brain
   matrxs.agents.patrolling_agent
   matrxs.agents.capabilities.capability

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
