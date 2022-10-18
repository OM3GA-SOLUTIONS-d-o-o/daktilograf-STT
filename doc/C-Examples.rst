C API primer korišćenja
===================

Primeri su preuzeti sa `native_client/client.cc`.

Kreiranje instance modela i učitavanje modela
-------------------------------------------

.. literalinclude:: ../native_client/client.cc
   :language: c
   :start-after: sphinx-doc: c_ref_model_1_start
   :end-before: sphinx-doc: c_ref_model_1_stop

.. literalinclude:: ../native_client/client.cc
   :language: c
   :start-after: sphinx-doc: c_ref_model_2_start
   :end-before: sphinx-doc: c_ref_model_2_stop

Transkripcija zvuka sa učitanim modelom
----------------------------------------

.. literalinclude:: ../native_client/client.cc
   :language: c
   :linenos:
   :lineno-match:
   :start-after: sphinx-doc: c_ref_inference_start
   :end-before: sphinx-doc: c_ref_inference_stop

Pun izvorni kod
----------------

Vidi :download:`Full source code<../native_client/client.cc>`.
