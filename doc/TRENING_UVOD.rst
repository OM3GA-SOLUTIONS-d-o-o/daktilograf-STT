.. _intro-training-docs:

Trening
=====================

Uvod
------------

Ovaj dokument je vodič za trening Daktilograf STT modela koristeći vaš sopstveni audio data set.
Za detaljniju dokumentaciju o treningu, trebalo bi da pogledate:ref:`Advanced Training Topics <advanced-training-docs>`.

Ako želite da prođete kroz Python notebook (radi u Google Colab), vidite: `official STT Python notebooks <https://github.com/coqui-ai/STT/tree/main/notebooks>`_.

Trening modela pomoću sopstvenog dataseta može dovesti do boljeg kvaliteta transkripcije  u poređenju sa standardnim Daktilograf STT modelom..
Ako se vaš data set značajno razlikuje od podataka koje smo koristili u našem treningu; ako obučite svoj model (ili fino podesite neki od naših)
to može dovesti do velikih poboljšanja u kvalitetu transkripcije. 
Možete pročitati o tome kako karakteristike govora utiču na transkripciju na :ref:`here <model-data-match>`.

Dockerfile Setup
----------------

Predlažemo da koristite našu Docker image kao bazu za trening. Možete skinuti i pokrenuti image sa: 

.. code-block:: bash

   $ docker pull ghcr.io/coqui-ai/stt-train
   $ docker run -it ghcr.io/coqui-ai/stt-train:latest

Ili možete ildovati iz source-a ``Dockerfile.train``, i pokrenuti trening lokalno u:

.. code-block:: bash

   $ git clone --recurse-submodules https://github.com/coqui-ai/STT
   $ cd STT
   $ docker build -f Dockerfile.train . -t stt-train:latest
   $ docker run -it stt-train:latest

Više o Dockerfiles možete pročitati na: <https://docs.docker.com/engine/reference/builder/>`_.

Ručno pokretanje
------------

Ukoliko ne želite da koristite naš Dockerfile template, moraćete ručno instalirati STT kako biste trenirali model.

.. _training-deps:

Preduslovi
^^^^^^^^^^^^^

* `Python 3.6, 3.7 ili 3.8 <https://www.python.org/>`_
* Mac ili Linux okruženje (trening na Windows-u trenutno *NIJE* podržan)
* CUDA 10.0 i CuDNN v7.6

Download
^^^^^^^^

Klonirajte Daktilograf STT repozitorijum sa GitHub-a:

.. code-block:: bash

   $ git clone https://github.com/OM3GA-SOLUTIONS-d-o-o/daktilograf-STT

Instalacija
^^^^^^^^^^^^

Instalacija STT-a i dependenci je lakše sa virtuelnim okruženjem. 

Postavke virtuelnog okruženja
""""""""""""""""""""""""""

Preporučujemo Python's već ugrađeni modul `venv <https://docs.python.org/3/library/venv.html>`_ kako biste upravljali svojim Python okruženjem.

Postavite Python viirtuelno okruženje i nazovite ga ``coqui-stt-train-venv``:

.. code-block::

   $ python3 -m venv coqui-stt-train-venv

Aktivirajte virtuelno okruženje:

.. code-block::

   $ source coqui-stt-train-venv/bin/activate

Setup sa ``conda`` virtuelnim okruženjem (Anaconda, Miniconda, or Mamba) nije garantovano da će raditi. 
Ipak, rado ćemo pregledati sve pull requests koji popravljaju sve nekompatibilnosti na koje naiđete.

Instalacija dependenci i STT-a
""""""""""""""""""""""""""""""

Sada kada smo klonirali STT repo sa Github-a i podesili virtuelno okruženje sa ``venv``, možemo da instaliramo STT i njegove dependence.
Preporučujemo već ugrađeni modul za instalaciju `pip <https://pip.pypa.io/en/stable/quickstart/>`_ :

.. code-block:: bash

   $ cd STT
   $ python -m pip install --upgrade pip wheel setuptools
   $ python -m pip install --upgrade -e .

Ako imate NVIDIA GPU, preporučuje se da instalirate TensorFlow sa podrškom za GPU. Obuka će biti znatno brža nego kad bi se za trening koristio CPU.

.. code-block:: bash

   $ python -m pip uninstall tensorflow
   $ python -m pip install 'tensorflow-gpu==1.15.4'

Pobrinite se da imate :ref:`prerequisites <training-deps>` i  CUDA instalaciju koja radi sa verzijama izlistanim ispod.

Verifikacija instalacije 
""""""""""""""""""""""""

Da potvrdite da je instalacija uspešna, pokrenite:

.. code-block:: bash

   $ ./bin/run-ldc93s1.sh

Ova skripta će trenirati model na jednom audio fajlu. 
Ako se skripta uspešno izvrši, vaš STT trening je spreman za pokretanje. 


Trening sa sopstvenim data setom
--------------------------------

Bez obzira da li ste koristili Dockerfile template ili ste napravili sopstveno okruženje,
centralni STT trening modul je ``python -m coqui_stt_training.train``. 
Za listu opcija komandi koristite ``--help`` flag:

.. code-block:: bash

   $ cd STT
   $ python -m coqui_stt_training.train --help

Trening podaci
^^^^^^^^^^^^^

za trening su vam potrebne dve vrste podataka:
1. audio fajlovi
2. tekstualni transkripti

Format podataka
"""""""""""""""

Audio podaci treba da budu u WAV formatu, frekvencije 16kHz, na MONO kanalu.
Nema striktnih pravila za dužinu podataka, ali iz našeg iskustva trening je najuspešniji kada su WAV datoteke trajanja između 5 i 20 sekundi.
Dataset po kvalitetu treba da odgovara kvalitetu zvuka koji očekujete pri korišćenju rešenja.
O karakteristikama zvuka u STT-u možete više pročitati na :ref:`here <model-data-match>`.

Tekstualni input treba da budu onakav kakav očekujete kasnije prilikom korišćenja rešenja - ukoliko želite da vaš model piše velika slova, vaš tekstualni input treba da sadrži velika slova.
Isto važi i za interpunkciju. Imajte u vidu da što više karaktera uključite u trening proces, to proces učenja postaje teži za model. 
STT modeli uče iz "iskustva", i ako imate malo primera datih karaktera u data setu, model će teško naučiti retke karaktere. 


CSV format dokumenta
""""""""""""""""""""

TAudio i transkripti koričćeni u treningu treba da se nalaze u CSV dokumentu. 
za trening treba da dostavite tri CSV dokumenta: (``train.csv``), validaciju (``dev.csv``), i testiranje (``test.csv``). 
CSV dokumenta treba da sadrže tri kolone:

1. ``wav_filename`` - putanja do WAV fajla na vašem uređaju
2. ``wav_filesize`` - broj bajtova u WAV fajlu
3. ``transcript`` - tekstualni transkript WAV fajla

Ukoliko nemate predefinisanu podelu za dokumenata za trening validaciju i testiranje, možete koristiti ``--auto_input_dataset`` 
da automatski podelite jedan CSV dokument na subsetove i generišete alfabet:

.. code-block:: bash

   $ python -m coqui_stt_training.train --auto_input_dataset samples.csv

Pokretanje treninga
^^^^^^^^^^^^^^^^^^^

Nakon što ste uspešno instalirali STT i imate pristup podacima, možete pokrenuti trening proces:

.. code-block:: bash

   $ cd STT
   $ python -m coqui_stt_training.train --train_files train.csv --dev_files dev.csv --test_files test.csv

Naredni koraci
--------------

Ukoliko želite da podesite trening tako da odgovara vašim podacima i hardveru treba da pogledate
 :ref:`command-line training flags <training-flags>`, i eksperimentšete sa različitim podešavanjima.

Za detaljniju dokumentaciju o treningu pogledajte :ref:`Advanced Training Topics <advanced-training-docs>` sekciju.
