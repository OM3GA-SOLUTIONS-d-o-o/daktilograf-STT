.. _exporting-checkpoints:

Izvoz modela
================================

Nakon što obučite STT model, vaš model će biti sačuvan na disku kao :ref:`checkpoint file <checkpointing>`. 
Kontrolne tačke modela su korisne za nastavak obuke kasnije, ali nisu pravi format za primenu modela u proizvodnji.
Format modela za primenu je TFLite datoteka.

Ovaj dokument objašnjava kako da izvezete kontrolne tačke modela kao TFLite datoteku.

Kako izvesti model
---------------------

Možete da izvezete kontrolne tačke STT modela za primenu pomoću skripte za izvoz  ``--export_dir`` oznake.

.. code-block:: bash

   $ python3 -m coqui_stt_training.export \
         --checkpoint_dir path/to/existing/model/checkpoints \
         --export_dir where/to/export/model
