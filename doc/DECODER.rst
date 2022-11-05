.. _decoder-docs:

Beam search deKoder
===================

Uvod
------------

Daktilograf STT koristi funkciju loss-a: `Connectionist Temporal Classification <http://www.cs.toronto.edu/~graves/icml_2006.pdf>`
Za odlično objašnjenje CTC-a i njegove upotrebe, pogledajte ovaj Distill članak: `Sequence Modeling with CTC <https://distill.pub/2017/ctc/>`_. 
Ovaj dokument pretpostavlja da je čitalac upoznat sa konceptima opisanim u tom članku i opisuje specifično ponašanje Daktilografa STT koje
programeri koji grade sisteme sa Daktilograf STT treba da znaju da bi izbegli probleme.

Napomena: Dokumentacija za alate za kreiranje prilagođenih paketa scorer fajla dostupna je u :ref:`language-model`. 
Dokumentacija za coqui_stt_ctcdecoder Python paket koji koristi kod treninga za dekodiranje dostupna je u :ref:`decoder-api`.

Ključne reči „MORA“, „NE SME“, „NEOPHODNO“, „ĆE“, „NEĆE“, „BI TREBALO“, „NE BI TREBALO“, „PREPORUČUJE SE“, „MOŽE“ i „OPCIONALNO“
u ovom dokumentu treba tumačiti kako je opisano u`BCP 14 <https://tools.ietf.org/html/bcp14>`_ kada, i samo kada se pojave sa sve velikim slovima, kao što je prikazano iznad. 


Eksterni scorer
---------------

Daktilograf STT  klijenti podržavaju OPCIONALNO korišćenje eksternog jezičkog modela da povećaju preciznost transkripta.
U kodu, parametrima komandne linije i dokumentaciji, ovo se naziva "scorer".
Scorer se koristi za izračunavanje verovatnoće (koja se takođe naziva rezultatom, otuda i naziv „scorer“) sekvenci reči ili znakova u output-u, da bi vodio dekoder ka verovatnijim rezultatima.
Ovo značajno poboljšava preciznost.

Korišćenje eksternog scorera je potpuno opciono.
Kada eksterni scorer nije prisutan, Daktilograf STT i dalje koristi algoritam za dekodiranje beam search, ali bez spoljnog bodovanja.

Trenutno je spoljni zapisivač Daktilograf STT implementiran sa `KenLM <https://kheafield.com/code/kenlm/>`_, i sa nekim alatkama za pakovanje potrebnih datoteka i metapodataka u jedan ``.scorer`` paket. Alat se nalazi u``data/lm/``. 
Skripte navedene u ``data/lm/`` mogu se koristiti i modifikovati za izgradnju sopstvenog jezičkog modela na osnovu vašeg konkretnog use case-a ili jezika. 
Vidi :ref:`language-model` za više detalja o tome kako da reprodukujete našu datoteku zapisničara kao i da kreirate sopstvenu.

Skripte su usmerene ka repliciranju datoteka jezičkog modela koje izdajemo kao deo `STT model releases <https://github.com/coqui-ai/STT/releases/latest>`_, 
ali njihovo modifikovanje da koriste različite data setove ili parametre konstrukcije specifičnog jezičkog modela trebalo bi da bude jednostavno.


Režimi dekodiranja
--------------

Daktilograf STT trenutno podržava dva režima rada sa značajnim razlikama u vremenu obuke i dekodiranja.
Imajte na umu da je režim ``bytes output`` eksperimentalan i nije testiran za druge jezike osim kineskog mandarinskog.


Podrazumevani režim (zasnovan na abecedi)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Podrazumevani režim, koji koristi datoteku abecede (specified with ``--alphabet_config_path`` at training and export time)  
da bi odredio koje oznake (znakove) i koliko ih treba predvideti u izlaznom sloju. U vreme dekodiranja, ako koristite eksterni scorer,
on MORA biti baziran na rečima i MORA da bude napravljen korišćenjem iste abecedne datoteke koja se koristi za trening.

Zasnovan na rečima znači da korpus teksta koji se koristi za pravljenje scorer fajla treba da sadrži reči razdvojene razmakom.
Za većinu svetskih jezika, ovo je podrazumevani režim i ne zahteva posebne korake od programera prilikom kreiranja scorera.



Implementacija
^^^^^^^^^^^^^^

Izvorni kod dekodera se može naći u ``native_client/ctcdecode``.
Dekoder je uključen u language bindings i klijente.
Pored toga, postoji poseban Python modul koji uključuje samo dekoder i potreban je za procenu.
Unapred napravljena verzija ovog paketa se automatski preuzima i instalira prilikom instaliranja koda za trening.
Ako želite da ga ručno napravite i instalirate iz izvora, pogledajte:ref:`decoder build and installation instructions <build-ctcdecoder-package>`.
