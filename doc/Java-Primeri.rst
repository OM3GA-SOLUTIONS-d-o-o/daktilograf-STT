Primer upotrebe Java API-ja
======================

Primeri su od `native_client/java/app/src/main/java/ai/coqui/sttexampleapp/STTActivity.java`.

Kreiranje instance modela i učitavanje modela
-------------------------------------------

.. literalinclude:: ../native_client/java/app/src/main/java/ai/coqui/sttexampleapp/STTActivity.java
   :language: java
   :linenos:
   :lineno-match:
   :start-after: sphinx-doc: java_ref_model_start
   :end-before: sphinx-doc: java_ref_model_stop

Transkripcija zvuka sa učitanim modelom
----------------------------------------

.. literalinclude:: ../native_client/java/app/src/main/java/ai/coqui/sttexampleapp/STTActivity.java
   :language: java
   :linenos:
   :lineno-match:
   :start-after: sphinx-doc: java_ref_inference_start
   :end-before: sphinx-doc: java_ref_inference_stop

Potpuni izvorni kod
----------------

See :download:`Full source code<../native_client/java/app/src/main/java/ai/coqui/sttexampleapp/STTActivity.java>`.
