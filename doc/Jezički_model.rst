.. _language-model:

Kako trenirati jezički model
==============================

Uvod
------------

Ovaj dokument objašnjava kako da trenirate i pripremite jezički model za primenu.

Primena jezičkog modela je u proizvodnji.
Dobar jezički model će poboljšati tačnost transkripcije ispravljajući predvidive pravopisne i gramatičke greške.
Ako možete da predvidite sa kakvom vrstom govora će se susresti vaš STT, možete postići veliki napredak u preciznosti pomoću prilagođenog jezičkog modela.

Na primer, ako želite da transkribujete univerzitetska predavanja o biologiji, trebalo bi da obučite jezički model na tekstu koji se odnosi na biologiju.
Sa ovim jezičkim modelom specifičnim za biologiju, Daktilograf STT će moći bolje da prepozna retke reči koje je teško napisati kao što je "citokineza".

Kako trenirati model
--------------------

Postoje tri koraka za primenu novog jezičkog modela za Daktilograf STT:

1. Identifikujte i formatirajte tekstualne podatke za obuku
2. Trenirajte  `KenLM <https://github.com/kpu/kenlm>`_ jezički model koristeći ``data/lm/generate_lm.py``
3. Spakujte model za primenu sa ``generate_scorer_package``

Pronađite podatke za trening
^^^^^^^^^^^^^^^^^^

Jezički modeli se treniraju iz teksta, i što je taj tekst sličniji govoru sa kojim će se vaš Daktilograf STT sistem susresti tokom rada, to će Daktilograf STT bolje raditi.

Na primer, ako želite da transkribujete vesti, onda će transkripti vesti biti vaš najbolji podaci za trening.
Ako želite da transkribujete audio knjigu, tačan tekst te knjige će napraviti najbolji mogući jezički model.
Ako želite da Daktilograf STT postavite na pametni zvučnik, vaš korpus teksta za trening treba da sadrži sve komande koje stavljate na raspolaganje korisniku,
kao što je "isključi muziku" ili "postavi alarm na 5 minuta".
Ako ne možete da predvidite vrstu govora koji će Daktilograf STT čuti tokom rada, pokušajte da prikupite što je više moguće teksta na vašem ciljanom jeziku.

Kada identifikujete tekst koji je prikladan za primenu, trebalo bi da sačuvate tekst u jednoj datoteci gde će jedna rečenica biti u jednom redu.



Treniranje jezičkog modela
^^^^^^^^^^^^^^^^^^^^^^^^

Pod pretpostavkom da ste pronašli i formatirali korpus teksta, sledeći korak je da koristite taj tekst za obuku KenLM jezičkog modela sa``data/lm/generate_lm.py``.

Za slučajeve prilagođene upotrebe, možete se upoznati sa KenLM kompletom alata <https://kheafield.com/code/kenlm/>`_. 
Većina opcija izloženih ``generate_lm.py`` se jednostavno prosleđuje na KenLM opcije istog imena, tako da bi trebalo da pročitate
`KenLM documentation <https://kheafield.com/code/kenlm/estimation/>`_ kako biste u potpunosti razumeli njihovo ponašanje.

.. code-block:: bash

    python generate_lm.py \
      --input_txt mls_lm_english/data.txt \
      --output_dir . \
      --top_k 500000 \
      --kenlm_bins path/to/kenlm/build/bin/ \
      --arpa_order 5 \
      --max_arpa_memory "85%" \
      --arpa_prune "0|0|1" \
      --binary_a_bits 255 \
      --binary_q_bits 8 \
      --binary_type trie

``generate_lm.py`` će sačuvati novi jezički model kao dve datoteke na disku: ``lm.binary`` i ``vocab-500000.txt``.

Generisanje jezičkog modela za primenu
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Konačno, generišemo obučeni KenLM model za primenu sa ``generate_scorer_package``. 
Možete pronaći unapred napravljene binarne datoteke za ``generate_scorer_package`` na zvaničnoj stranici izdanja STT-a <https://github.com/coqui-ai/STT/releases>`_ (unutar ``native_client.*.tar. kz``). 
Ako iz nekog razloga morate sami da kompajlirate ``generate_scorer_package``, pogledajte :ref:`build-generate-scorer-package`.

Generišite jezički model za primenu sa ``generate_scorer_package``:

.. code-block:: bash

    ./generate_scorer_package \
      --checkpoint path/to/your/checkpoint \
      --lm lm.binary \
      --vocab vocab-500000.txt \
      --package kenlm.scorer \
      --default_alpha 0.931289039105002 \
      --default_beta 1.1834137581510284

``--checkpoint`` treba da ukazuje na kontrolnu tačku akustičnog modela sa kojom ćete koristiti generisani scorer fajl.

Alfabet će biti učitana sa kontrolne tačke. Eksterni scorer fajlovi moraju biti kreirani sa istim alfabetom kao i akustični modeli sa kojima će se koristiti.
Parametri ``--default_alpha`` i ``--default_beta`` prikazani iznad su pronađeni sa ``lm_optimizer.py`` Python skriptom.