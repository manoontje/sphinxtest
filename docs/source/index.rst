.. MATRXS documentation master file, created by
   sphinx-quickstart on Fri Jul 26 09:03:28 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
   https://raw.githubusercontent.com/tobiasHeinke/Blender-Manual/master/blender_docs/resources/theme/css/theme_overrides.css

.. figure:: /_static/images/tno_banner.png
   :width: 145%

MATRXS's documentation
======================

Welcome! This is the documentation for Man-Agent Teaming; Rapid Experimentation Software (MATRXS).

MATRXS a 2D-discrete testbed to facilitate Human Agent Teaming (HAT) research. The original use case in MATRXS is an urban search and rescue operation in which pairs of a human and an autonomous system have to locate and rescue victims. However, MATRXS is very versatile and can, therefore, also be used in many other cases.


Getting started
===============

.. toctree::
   :maxdepth: 2

   about/aboutmatrxs.rst
   installation/installing.rst
   about/tutorials.rst
   about/FAQ.rst


Sections
========
.. The image ratio is: width: 350px; height: 350/4 + (2x5) ~= 98px

.. only:: builder_html and (not singlehtml)

   .. container:: tocdescr

      .. container:: descr

         .. figure:: /_static/images/contents_animation.jpg
            :target: html/_generated_autodoc/matrxs.world_builder.WorldBuilder.html

         :doc:`WorldBuilder`
            Learn MATRXS' way of creating worlds.

      .. container:: descr

         .. figure:: /_static/images/contents_animation.jpg
            :target: html/_generated_autodoc/matrxs.grid_world.GridWorld.html

         :doc:`GridWorld`
            MATRXS' worlds are based on grids.

      .. container:: descr

         .. figure:: /_static/images/contents_animation.jpg
            :target: html/_generated_autodoc/matrxs.agents.agent_brain.AgentBrain.html

         :doc:`AgentBrain`
            The agents in MATRXS have brains. Check this section for a piece of their minds.

      .. container:: descr

         .. figure:: /_static/images/contents_animation.jpg
            :target: html/_generated_autodoc/matrxs.objects.simple_objects.Wall.html

         :doc:`Objects`
            Make the world more worldlike by placing objects in it.


Resources
=========
* `TNO <https://tno.nl>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`















