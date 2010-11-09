Introduction
============

This package provides infrastructure to extend Archetypes content types with
set of fields defined in PloneFormGen forms.

It is the result of the collaboration of a ``archetypes.schemaextender``, a
CMF Factory Type information (FTI) and a CMF tool that holds the PloneFormGen
forms.

When a form is added in the ``portal_pfgextender`` tool, it is marked as a
``IPFGExtenderForm`` and registered (by id) as a named utility.

The FTI holds a ``pfgform_id`` property that refers to one of the forms in the
tool. When the FTI creates a content instance, it sets the
``archetypes.pfgextender.interfaces.IPFGExtensible`` interface and stores the
``pfgform_id`` on the instance.

The ``archetypes.pfgextender.extender.Extender`` is registered for
``IPFGExtensible``. It queries the ``pfgform_id`` on the instance. 
It looks up the corresponding form utility. It computes the additional
fields for the schema by turning PloneFormGen fields to Archetypes fields.
