Daktilograf STT dokumentacija glavni fajl.

 Možete da prilagodite ovu datoteku u potpunosti, ali bi trebalo da sadrži direktivu `toctree` 

.. image:: https://github.com/OM3GA-SOLUTIONS-d-o-o/daktilograf-V3-client/raw/main/images/dakt-stt-gh.png
  :alt: Daktilograf STT logo and wordmark

**STT** (Daktilograf STT) je komplet open source deep learning alata za trening i primenu modela transkripcije govora u tekst.

Daktilograf STT je testiran i u proizvodnji i u istraživanju.


.. toctree::
   :maxdepth: 1
   :caption: Quick Reference

  RAZVOJ

 TRENING_UVOD

 TRENING_NAPREDNI

 BILD

Najbrži način da koristite unapred obučeni Daktilograf STT model je pomoću Daktilograf STT modela menadžera, alata koji vam omogućava da brzo lokalno testirate demo modele. Trebaće vam Python 3.6, 3.7, 3.8 ili 3.9:

.. code-block:: bash

   # Napravi virtuelno okruženje
   $ python3 -m venv venv-stt
   $ source venv-stt/bin/activate

   # Instaliraj Daktilograf STT model menadžer
   $ python -m pip install -U pip
   $ python -m pip install coqui-stt-model-manager

   # Pokrenite menadžer modela. Otvoriće se kartica pretraživača i tada možete preuzeti i testirati modele iz Model Zoo-a.
   $ stt-model-manager

.. toctree::
   :maxdepth: 1
   :caption: API Reference

   Error-Codes

   C-API

   DotNet-API

   Java-API

   NodeJS-API

   Python-API

.. toctree::
   :maxdepth: 1
   :caption: Primeri

   Python-Primeri

   NodeJS-Primeri

   C-Primeri

   DotNet-Primeri

   Java-Primeri

   HotWordBoosting-Primeri

   Contributed-Primeri

.. toctree::
   :maxdepth: 1
   :caption: Language Model

   LANGUAGE_MODEL

.. include:: SUPPORT.rst

.. toctree::
   :maxdepth: 1
   :caption: STT Playbook

   playbook/README

.. toctree::
   :maxdepth: 1
   :caption: Advanced topics

   DECODER

   Decoder-API

   PARALLEL_OPTIMIZATION


Indeksi i tabele
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
