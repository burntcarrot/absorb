absorb
==============================

.. toctree::
   :hidden:
   :maxdepth: 1

   reference

The extensible, feature-rich CLI workspace.

Installation
------------

To install absorb,
run this command in your terminal:

.. code-block:: console

   $ pip install absorb


Usage
-----

absorb's usage looks like:

.. code-block:: console

   $ absorb [OPTIONS]

absorb provides 3 commands: `tasks`, `kanban`, `idea`

``tasks`` is the command used for using dealing with tasks. ``tasks`` has multiple subcommands for adding, deleting and editing a task.

``kanban`` is the command used for using dealing with kanban boards. ``kanban`` has multiple subcommands for adding, deleting and editing a card in the kanban board.

``idea`` is the command used for using dealing with ideas. ``idea`` has multiple subcommands for adding, deleting and editing an idea.


tasks
-----

.. code-block:: console

   $ absorb tasks [OPTIONS]

``tasks`` provides multiple subcommands, like:

add:
   Adds a new task.

   **Example:**

   ``absorb tasks add "A new task." "+7d" "low" "@new"``

   The above command adds a task with the name ``"A new task."``, with the due date being after a week (``+7d``). The priority of the added task is set to ``low`` and the group of the task is ``@new``.

   **Arguments:**

   **name**
      The name of the task, for example: ``"New task."``

   **date**
      A dot(``.``) can be used to add the current time as the due date of the task.

      A plus sign suffixed with ``d`` sets the due date by the specified number of days ahead of the current date. Example: ``+5d`` should set the due date as 5 days ahead of the current time.

   **priority**
      The priority of the task, for example: ``"low"``

   **group**
      The group in which the task should belong, for example: ``"@new"``

      The groups should be prefixed with ``@``. Adding a group without the ``@`` will result in no groups being added to the task.

      Multiple groups can be added to a task. The groups should be spaced, in order to add the groups to the tasks. For example, ``@new @tutorial``, should add ``new`` and ``tutorial``, to the task's groups.

      In order to avoid assigning a group to the task, we can use a dot/period(``.``). For example, ``absorb tasks add "A new task." "+4d" "medium" "."``, adds a task with no groups.

edit:
   Edits an existing task.

   **Example:**

   ``absorb tasks edit "#1" "Renamed task." "." "." "."``

   The above command edits a task with ID ``#1``, and renames it to ``Renamed task.``. Since we don't want to edit the task's other fields, we can add a dot/period(``.``) to the other arguments.

   **Arguments:**

   **id**
      The ID of the task. Multiple tasks can have the same name, but with different due dates or groups. Hence, to avoid confusion the ID of the task is required.

   **name**
      The name of the task, for example: ``"New task."``

      If you want the name of the task to be the same as the previous, we can use a dot/period(``.``). For example, ``absorb tasks add "." "+4d" "." "."``, edits the task's date only.

   **date**
      A dot/period(``.``) can be used to add the current time as the due date of the task.

      A plus sign suffixed with ``d`` sets the due date by the specified number of days ahead of the current date. Example: ``+5d`` should set the due date as 5 days ahead of the current time.

   **priority**
      The priority of the task, for example: ``"low"``

   **group**
      The group in which the task should belong, for example: ``"@new"``

      The groups should be prefixed with ``@``. Adding a group without the ``@`` will result in no groups being added to the task.

      Multiple groups can be added to a task. The groups should be spaced, in order to add the groups to the tasks. For example, ``@new @tutorial``, should add ``new`` and ``tutorial``, to the task's groups.

      In order to avoid assigning a group to the task, we can use a dot/period(``.``). For example, ``absorb tasks edit "A new task." "+4d" "medium" "."``, edits the task with no changes on the groups.

delete:
   Deletes an existing task.

   **Example:**

   ``absorb tasks delete "#1"``

   The above command deletes a task with ID ``#1``.

   **Arguments:**

   **id**
      The ID of the task.

show:
   Shows all existing tasks.

   **Example:**

   ``absorb tasks show``

show_group:
   Shows all existing tasks where the group is equal to the ``group_name``.

   **Example:**

   ``absorb tasks show_group "@new"``

   The above command shows all tasks where the group of the task is ``@new``.

   **Arguments:**

   **group_name**
      The name of the group of the task.


kanban
------

.. code-block:: console

   $ absorb kanban [OPTIONS]

``kanban`` provides multiple subcommands, like:

add:
   Adds a new card to the kanban board.

   **Example:**

   ``absorb kanban add "Finish project." "planned" "Send a mail to Alice with the reports attached." "@work @project"``

   The above command adds a card to the kanban board with the name ``Finish project.``, and is added to the ``planned`` section of the board. The card has also a description attached to it, in this case, we have added the description as ``Send a mail to Alice with the reports attached.``. The card is tagged with the tags ``work`` and ``project``.

   **Arguments:**

   **name**
      The name of the card, for example: ``"Finish project."``

   **status**
      The status of the card, i.e, in which column the card has to be added to. Currently, ``absorb`` supports three values for ``status``: ``completed``, ``doing`` and ``planned``.

   **description**
      The description for the card. Can be added as plain text or can be imported from a file.

      Plain text, example: ``absorb kanban add "Finish project." "planned" "Send a mail to Alice with the reports attached." "@work @project"``

      ``absorb`` supports importing card description as a file. The description should be ``+file``, for example, ``absorb kanban add "Finish project." "planned" "+file" "@work @project"``.

      This would then prompt the user to enter the path for the file.

   **tags**
      The tags for the card, for example: ``"@project"``

      The tags should be prefixed with ``@``. Adding a tag without the ``@`` will result in no tags being added to the card.

      Multiple tags can be added to a card. The tags should be spaced, in order to add the tags to the card. For example, ``@tutorial @project``, should add ``tutorial`` and ``project``, to the card's tags.

      In order to avoid assigning a tag to the card, we can use a dot/period(``.``). For example, ``absorb kanban add "Finish project." "planned" "Small description." "."``, adds a card with no tags.

edit:
   Edits an existing card in the kanban board.

   **Example:**

   ``absorb kanban edit "#1" "Finish project." "doing" "Send a mail to Alice and Bob with the reports attached." "@work @project"``

   The above command edits an existing card with ID ``#1`` in the kanban board. It changes the card's status from ``planned`` to ``doing``. The card's description has also been changed.

   **Arguments:**

   **id**
      The ID of the card, for example, ``#1``.

   **name**
      The name of the card, for example: ``"Finish project."``

      In order to avoid editing the name of the card, we can use a dot/period(``.``). For example, ``absorb kanban edit "#1" "." "Description." "@work @project"``, edits the card with the name being ignored, i.e, the name would be the same.

   **description**
      The description for the card. Can be added as plain text or can be imported from a file.

      Plain text, example: ``absorb kanban add "Finish project." "planned" "Send a mail to Alice with the reports attached." "@work @project"``

      ``absorb`` supports importing card description as a file. The description should be ``+file``, for example, ``absorb kanban edit "#1" "Finish project." "+file" "@work @project"``.

      This would then prompt the user to enter the path for the file.

      In order to avoid editing the description for the card, we can use a dot/period(``.``). For example, ``absorb kanban edit "Finish project." "." "@work @project"``, edits the card with the description being ignored, i.e, the description would be the same.

   **tags**
      The tags for the card, for example: ``"@project"``

      The tags should be prefixed with ``@``. Adding a tag without the ``@`` will result in no tags being added to the card.

      Multiple tags can be added to a card. The tags should be spaced, in order to add the tags to the tasks. For example, ``@tutorial @project``, should add ``tutorial`` and ``project``, to the card's tags.

      In order to avoid assigning a tag to the card, we can use a dot/period(``.``). For example, ``absorb kanban edit "#1" "Finish project." "Small description." "."``, edits the card with no tags.

delete:
   Deletes an existing card from the kanban board.

   **Example:**

   ``absorb kanban delete "#1"``

   The above command deletes a card with ID ``#1``.

   **Arguments:**

   **id**
      The ID of the card.

show:
   Shows the kanban board.

   **Example:**

   ``absorb kanban show``

move-card:
   Moves a card from one column to another, i.e., changes its status.

   **Example:**

   ``absorb kanban move-card "#1" "planned"``

   The above command moves the card with ID ``#1`` to the ``planned`` column.

   **Arguments:**

   **id**
      The ID of the card.

   **new_status**
      The new status to which the card should belong to.

      For example, "absorb kanban move-card "#1" "completed"``, moves the card with ID ``#1`` to the ``completed`` column.


idea
----

.. code-block:: console

   $ absorb idea [OPTIONS]

``idea`` provides multiple subcommands, like:

new:
   Adds a new idea.

   **Example:**

   ``absorb idea new "Make a cool machine." "Get inspiration for making this machine!" "@machine"``

   The above command adds an idea with the name as ``Make a cool machine``, and commits the idea to the local git repository.

   **Arguments:**

   **name**
      The name of the idea, for example: ``Make a cool machine.``

   **description**
      The description for the idea. Can be added as plain text or can be imported from a file.

      Plain text, example: ``absorb idea new "Make a cool machine!" "Some description." "@machine"``

      ``absorb`` supports importing idea description as a file. The description should be ``+file``, for example, ``absorb idea new "Make a cool machine!" "+file" "@machine"``.

      This would then prompt the user to enter the path for the file.

   **tags**
      The tags for the idea, for example: ``"@machine"``

      The tags should be prefixed with ``@``. Adding a tag without the ``@`` will result in no tags being added to the idea.

      Multiple tags can be added to an idea. The tags should be spaced, in order to add the tags to the ideas. For example, ``@machine @cool``, should add ``machine`` and ``cool``, to the idea's tags.

      In order to avoid assigning a tag to the idea, we can use a dot/period(``.``). For example, ``absorb idea new "Make a cool machine." "Small description." "."``, adds an idea with no tags.

edit:
   Edits an existing idea.

   **Example:**

   ``absorb idea edit "#1" "Make a super cool machine!" "Check out some existing work." "@machine"``

   The above command edits an existing idea with ID ``#1`` and changes its name and description. The changes are then committed in the local git repository.

   **Arguments:**

   **id**
      The ID of the idea, for example, ``#1``.

   **name**
      The name of the idea, for example: ``Make a super cool machine!``

      In order to avoid editing the name of the idea, we can use a dot/period(``.``). For example, ``absorb idea edit "#1" "." "Check out some existing work." "@machine"``, edits the idea with the name being ignored, i.e, the name would be the same.

   **description**
      The description for the idea. Can be added as plain text or can be imported from a file.

      Plain text, example: ``absorb idea edit "#1" "Make a super cool machine!" "Check out some existing work and make a prototype." "@machine"``

      ``absorb`` supports importing idea description as a file. The description should be ``+file``, for example, ``absorb idea edit "#1" "Make a super cool machine!" "+file" "@machine"``.

      This would then prompt the user to enter the path for the file.

      In order to avoid editing the description for the idea, we can use a dot/period(``.``). For example, ``absorb idea edit "#1" "Make a super cool machine!" "." "@machine"``, edits the idea with the description being ignored, i.e, the description would be the same.

   **tags**
      The tags for the idea, for example: ``"@machine"``

      The tags should be prefixed with ``@``. Adding a tag without the ``@`` will result in no tags being added to the idea.

      Multiple tags can be added to an idea. The tags should be spaced, in order to add the tags to the ideas. For example, ``@tutorial @machine``, should add ``tutorial`` and ``machine``, to the idea's tags.

      In order to avoid assigning a tag to the idea, we can use a dot/period(``.``). For example, ``absorb idea edit "#1" "Make a super cool machine!" "Some description." "."``, edits the idea with no tags.

open:
   Opens an idea.

   **Example:**

   ``absorb idea open "#1"``

   The above command opens the idea with ID ``#1``. Opening an idea refers to displaying the idea's content in the terminal.

   **Arguments:**

   **id**
      The ID of the idea.

show:
   Shows all ideas.

   **Example:**

   ``absorb idea show``
