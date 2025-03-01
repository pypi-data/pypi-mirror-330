Informatics Matters cross-product protocol buffers
==================================================

.. image:: https://badge.fury.io/py/im-protobuf.svg
   :target: https://badge.fury.io/py/im-protobuf
   :alt: PyPI package (latest)

.. image:: https://github.com/InformaticsMatters/squonk2-protobuf/actions/workflows/build.yaml/badge.svg
   :target: https://github.com/InformaticsMatters/squonk2-protobuf/actions/workflows/build.yaml
   :alt: Build

.. image:: https://github.com/InformaticsMatters/squonk2-protobuf/actions/workflows/publish.yaml/badge.svg
   :target: https://github.com/InformaticsMatters/squonk2-protobuf/actions/workflows/publish.yaml
   :alt: Publish

A library of python bindings for `protocol buffer`_ definitions used by one or
more products in the Informatics Matters product suite.

The protocol buffers are used across multiple components and languages.
At the outset we anticipate supporting Python, and Java. The root
of all packages is ``src/main`` as required by build tools like ``Gradle``.
From there the directory is ``proto/informaticsmatters`` followed by component
directories or a ``common`` directory. An example protocol message
file might be::

    src/main/proto/informaticsmatters/protobuf/datamanager/pod_message.proto

When transmitted on a topic-based messaging service the topic is
the lower-case dot-separated message name relative to ``informaticsmatters``
(excluding the ``Message`` suffix), e.g. ``datamanager.pod``.

.. _Protocol Buffer: https://developers.google.com/protocol-buffers/docs/proto3

Installation (Python)
=====================

The protocol buffers are published on `PyPI`_ and can be installed from
there::

    pip install im-protobuf

.. _PyPI: https://pypi.org/project/im-protobuf

Once installed you can access the protocol buffers with::

    >>> from informaticsmatters.protobuf.datamanager.pod_message_pb2 import PodMessage
    >>> pm: PodMessage = PodMessage()

Get in touch
============

- Report bugs, suggest features or view the source code `on GitHub`_.

.. _on GitHub: https://github.com/informaticsmatters/squonk2-protobuf
