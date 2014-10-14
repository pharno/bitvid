.. _conventions

Conventions
===========

Intro
-----



RESTful
-------

The API is developed in a RESTful way. In short, it means that the tools of
the HTTP standard are used instead of creating our own standards.

To implement :abbr:`CRUD (create, read, update, delete)` functionality in
a RESTful way, we make use of different HTTP methods for each action::

    Create = POST
    Read   = GET
    Update = PUT
    Delete = DELETE

Code Style
----------

This is a Python project, so we apply Python conventions. All we need for
code styling is :pep:`8`. It's important to follow this guide consistently.

PEP 8 in a nutshell:

    | *Everything is lowercase*
    | *except for constants and classnames.*

Documentation
-------------

Sphinx is used to generate the documentation.

Computers only need code, humans require context. Documentation is very
helpful and can prevent countless hours of decrypting code structures. Creating
good documentation can be hard though. Usually, it's helpful to answer
these questions:

    - *Why did I implement it this way?*
    - *What should other developers be cautious about?*
    - *What is the relation of this thing to this other thing?*
    - *In what unit is this number measured?*

Really, answering that last question `can save alot of money
<http://lamar.colostate.edu/~hillger/unit-mixups.html>`_.

And here are a couple of questions you should not answer:

    - *Is this method gluten-free?*

It's also *very useful* to provide examples in these comments. For example::

    def bunny_hop(bunny, height):
        """Let a bunny hop the specified amount in the air.

        Example::

            bunny_hop(newly_acquired_bunny, 4)

        .. note:: It's discouraged to provide a negative jump height,
                  because the bunny might die.

        :param height: The height to jump to in :dfn:`*chains* (The distance
                       between the two wickets on a cricket pitch)`.
        """
        bunny.z += height

This is probably a bad example for it could be done object oriented and the
example is pretty self explanatory. However, this piece does answer:

    - *What should other developers be cautious about?*

Yeah, you get the idea.

Testing
-------

