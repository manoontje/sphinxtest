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

Objects
=======

Classes
-------

.. toctree::
   :maxdepth: 2
   :hidden:

.. autosummary::
   :toctree: _generated_autodoc

    matrxs.objects.advanced_objects.Battery
    matrxs.objects.agent_body.AgentBody
    matrxs.objects.env_object.EnvObject
    matrxs.objects.simple_objects.SquareBlock
    matrxs.objects.simple_objects.Door
    matrxs.objects.simple_objects.Wall
    matrxs.objects.simple_objects.AreaTile
    matrxs.objects.simple_objects.SmokeTile

Functions
---------

.. toctree::
   :maxdepth: 2
   :hidden:

.. autosummary::
   :toctree: _generated_autodoc

    matrxs.objects.advanced_objects.Battery.update
    matrxs.objects.agent_body.AgentBody._set_agent_busy
    matrxs.objects.agent_body.AgentBody._check_agent_busy
    matrxs.objects.agent_body.AgentBody._set_agent_changed_properties
    matrxs.objects.agent_body.AgentBody.change_property
    matrxs.objects.agent_body.AgentBody.location
    matrxs.objects.agent_body.AgentBody.properties

