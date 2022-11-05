.. _usage-docs:

Primena / Inferenca
======================

Tranksripcija zvuka primenom treniranog modela se u ovom dokumentu naziva inferenca. 


Uvod
^^^^^^^^^^^^

Inferenca je proces unosa zvuka (govora) u trenirani Daktilograf STT model i primanja teksta (transkripcije) kao izlaza.
U praksi će biti potrebno da koristite dva modela za primenu: audio model i tekstualni model.
Audio model (ili akustični model) je duboka neuronska mreža koja pretvara zvuk u tekst.
Model teksta (tzv. jezički model / scorer) vraća niz teksta po parametru verovatnoće.
Ako akustički model pravi pravopisne ili gramatičke greške, jezički model može pomoći da se isprave.

Možete da primenite Daktilograf STT modele bilo preko klijenta komandne linije ili language bindings.
* :ref:`The Python package + language binding <py-usage>`
* :ref:`The Node.JS package + language binding <nodejs-usage>`
* :ref:`The Android libstt AAR package <android-usage>`
* :ref:`The command-line client <cli-usage>`
* :ref:`The C API <c-usage>`
* :ref:`Using the WebAssembly package <wasm-usage>`

U nekim use case-ovima ćete želeti da koristite mogućnosti inference ugrađene u kod treninga, kao na primer za brže prototipovanje novih funkcija. 
Ove funkcije nisu spremne za produkciju, ali pošto je sve Pzthon kod nećete morati da rekompajlujete kod kako biste testirali promene. 
Za više detalja, vidite :ref:`checkpoint-inference`

.. _download-models:

Download Daktilograf STT modela
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Već istrenirani model Daktilograf STT možete naći u <https://github.com/OM3GA-SOLUTIONS-d-o-o/daktilograf-STT/tree/main/models>`_. 
Možete i koristiti i Coqui STT Model Manager da snimite i probate neke od novijih modela za druge jezike:

.. code-block:: bash

   # Kreiraj virtuelno okruženje
   $ python3 -m venv venv-stt
   $ source venv-stt/bin/activate

   # Instaliraj model menadžer
   $ python -m pip install -U pip
   $ python -m pip install coqui-stt-model-manager

   # Pokreni model menadžer i testiraj modele
   $ stt-model-manager

U svakom xaktilograf STT release-u će biti objavljeni drugi modeli.
Akustični model ima ``.tflite`` ekstenziju. Jezički model koristi ekstenziju ``.scorer``. 

Možete pročitati više o jezičkim modelima u vezi sa :ref:`the decoding process <decoder-docs>` i :ref:`how scorers are generated <language-model>`.
.. _model-data-match:

Kako će se model ponašati na mom data setu?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Koliko dobro Daktilograf STT model transkribuje vaš zvuk zavisiće od mnogo stvari.
Opšte pravilo je sledeće: što su vaši podaci sličniji podacima koji se koriste za trening modela, to će model bolje transkribovati vaše podatke.
Što se vaši podaci više razlikuju od podataka koji se koriste za obuku modela, to će model biti lošiji na vašim podacima.
Ovo opšte pravilo važi i za akustični model i za jezički model.
Postoje mnogi faktori po kojima se podaci mogu razlikovati, ali evo najvažnijih:

* Jezik
* Akcenat
* Stil govora
* Govorna tema
* Demografija govornika


Ako uzmete Daktilograf STT model obučen na engleskom jeziku i ubacite španski u njega, očekujte da će model biti loš.
Zamislite da su modeli Daktilograf STT kao ljudi koji govore određeni jezik sa određenim akcentom, a zatim razmislite o tome šta bi se dogodilo kada biste zamolili tu osobu da transkribuje vaš audio zapis.

Akustični model (tj. datoteka ``.tflite``) je "naučio" kako da transkribuje određeni jezik, a model verovatno neke akcente razume bolje od drugih.
Pored jezika i akcenta, akustični modeli su osetljivi na stil govora, temu govora i demografiju osobe koja govori.
Jezički model (``.scorer``) je obučen samo za tekst.
Kao takav, jezički model je osetljiv na to koliko se tema i stil govora podudaraju sa tekstom koji se koristi u treningu.
Ako podaci koji se koriste za trening gotovih modela nisu u skladu sa vašim predviđenim slučajem upotrebe, možda će biti potrebno prilagoditi ili istrenirati nove modele kako biste poboljšali transkripciju vaših podataka.

Trening sopstvenog jezičkog modela je često dobar način da poboljšate transkripciju vašeg zvuka.
Proces i alati koji se koriste za generisanje jezičkog modela su opisani u :ref:`language-model`, a opšte informacije se mogu naći u :ref:`decoder-docs`.
Generisanje scorera iz skupa podataka ograničene teme je brz proces i može doneti značajna poboljšanja tačnosti ako je vaš zvuk iz te iste teme.

Trening akustičnog modela je opisan u :ref:`intro-training-docs`.
Fino podešavanje standardnog akustičnog modela prema vašim podacima može biti dobar način za poboljšanje performansi.
Pogledajte odeljke :ref:``fine tuning i transfer učenja <training-fine-tuning>` za više informacija.


Kompatibilnost modela
^^^^^^^^^^^^^^^^^^^^^

Daktilograf STT modeli su verzionisani da bi se ublažile nekompatibilnosti sa klijentima.
Ako dobijete grešku koja kaže da je verzija datoteke modela prestara za klijenta, trebalo bi ili (1) da klijenta nadogradite na noviji model, (2) da ponovo izvezete svoj model sa kontrolne tačke koristeći noviju verziju koda, ili (3) vratite klijenta na prethodnu verziju i stariji model.

.. _py-usage:

Korišćenje Python paketa
^^^^^^^^^^^^^^^^^^^^^^^^

Unapred napravljene binarne datoteke za primenu treniranog modela mogu se instalirati sa ``pip``. 
Preporučuje se da koristite Python 3.6 ili višu verziju u virtuelnom okruženju.
I  `pip <https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#installing-pip>`_  i `venv <https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment>`_  su uključeni u sve Python 3 instalacije.
Kada kreirate novo Python virtuelno okruženje, kreirate direktorijum koji sadrži ``python`` binarni fajl i sve što je potrebno za pokretanje Daktilografa STT.
Za potrebe ove dokumentacije, koristićemo na ``$HOME/coqui-stt-venv``, ali možete koristiti bilo koji direktorijum koji želite.

Da napravimo virtuelno okruženje:

.. code-block::

   $ python3 -m venv $HOME/coqui-stt-venv/

Nakon što se ova komanda završi, vaše novo okruženje je spremno za aktivaciju.
Svaki put kada radite sa Daktilograf STT, potrebno je da *aktivirate* svoje virtuelno okruženje:

.. code-block::

   $ source $HOME/coqui-stt-venv/bin/activate

Nakon što je vaše okruženje aktivirano, možete koristiti ``pip`` da instalirate ``stt``:

.. code-block::

   (coqui-stt-venv)$ python -m pip install -U pip && python -m pip install stt

Nakon što se instalacija završi, možete pozvati ``stt`` iz komandne linije.

Sledeća komanda pretpostavlja da ste :ref:`downloaded the pre-trained models <download-models>`.

.. code-block:: bash

   (coqui-stt-venv)$ stt --model model.tflite --scorer huge-vocabulary.scorer --audio my_audio_file.wav

Vidite :ref:`the Python client <py-api-example>` za primer kako se programski koristi paket.

.. _nodejs-usage:

Korišćenje Node.JS / Electron.JS paketa
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Imajte na umu da Daktilograf STT trenutno nudi samo pakete za primenu CPU-a sa Python-om 3.5 ili novijim na Linux-u.

Možete snimiti JS bindings koristeći ``npm``\ :

.. code-block:: bash

   npm install stt


Imajte na umu da od sada podržavamo:
 - Node.JS verzije 4 to 13
 - Electron.JS verzije 1.6 to 7.1

TypeScript podrška je dostupna takođe.

Vidi :ref:`TypeScript client <js-api-example>` za primer kako da programski koristite bindingse.

.. _android-usage:

Korišćenje Android AAR libstt paketa
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unapred izgrađen ``libstt`` Android AAR paket se može preuzeti sa GitHub Releases, za Android verzije 7.0+.
Da biste ga koristili u svojoj Android aplikaciji, prvo izmenite datoteku ``build.gradle`` svoje aplikacije da biste dodali lokalni direktorijum kao repozitorijum.
U odeljku ``repozitorijum`` dodajte sledeću definiciju:

.. code-block:: groovy

   repositories {
       flatDir {
           dirs 'libs'
       }
   }

Zatim napravite direktorijum libs u folder vaše aplikacije i tamo postavite libstt AAR datoteku.
Na kraju, dodajte sledeću dependencu u datoteku ``build.gradle`` vaše aplikacije:

.. code-block:: groovy

   dependencies {
       implementation fileTree(dir: 'libs', include: ['*.aar'])
   }

Ovo će povezati sve .aar datoteke u direktorijumu ``libs`` koji ste upravo kreirali, uključujući libstt.

.. _cli-usage:

Korišćenje klijenta komandne linije
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unapred izgrađeni binarni fajlovi za klijent komandne linije ``stt`` (preveden C++) dostupni su u arhivi ``native_client.*.tar.kz`` za vašu
željenu platformu (gde je * odgovarajući identifikator za platformu na kojoj želite da pokrenete).
Arhivu možete preuzeti sa stranice `releases page <https://github.com/coqui-ai/STT/releases>`_.

Pretpostavljajući da ste već skinuli :ref:`downloaded the pre-trained models <download-models>`, možete koristiti klijent ovako:

.. code-block:: bash

   ./stt --model model.tflite --scorer huge-vocabulary.scorer --audio audio_input.wav

Pogledajte pomoć ya više detalja ``./stt -h`` 

.. _c-usage:

Korišćenje C API-ja
^^^^^^^^^^^^^^^

Pored unapred izgrađenih binarnih datoteka za klijent komandne linije ``stt`` opisan :ref:`iznad <cli-usage>`,
u istoj ``native_client.*.tar.kz`` arhivi specifičnoj za platformu, naći ćete datoteku ``coqui-stt.h`` kao i
unapred izgrađene deljene biblioteke potrebne za korišćenje Daktilograf STT C API-ja.

Arhivu možete preuzeti sa stranice `releases page <https://github.com/coqui-ai/STT/releases>`_.

Zatim jednostavno uključite datoteku zaglavlja i vezu sa deljenim bibliotekama u svoj projekat i trebalo bi da budete u mogućnosti da koristite C API.
Referentna dokumentacija je dostupna u :ref:`c-api`.

.. _wasm-usage:

Korišćenje WebAssembly paketa
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Već napravljen ES5 libstt WebAssembly paket može biti skinut sa Git Hub releases:`<https://github.com/coqui-ai/STT/releases/latest/download/libstt.tflite.wasm.zip>`_ .
Vidi`wasm` doirektorijum u `STT-examples <https://github.com/coqui-ai/STT-examples/>_` za primer kako programski koristiti paket na veb stranici.

Već napravljen ES6 libstt WebAssembly paket se može preuzeti pomoću `npm`:


.. code-block:: bash

   npm install stt-wasm


Instaliranje bindings-a iz source-a
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ako unapred napravljene binarne datoteke nisu dostupni za vaš sistem, moraćete da ih instalirate od nule.
Pratite :ref:`native client build and installation instructions <build-native-client>`.


Dockerfile za bild is source-a
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Obezbeđujemo ``Dockerfile.build`` za automatsku izradu ``libstt.so``, C++ izvornog klijenta, Python bindings i KenLM.

Pre bilda, uverite se da su git podmoduli pokrenuti:

.. code-block:: bash

   git submodule sync
   git submodule update --init

zatim pokrenite bild sa:

.. code-block:: bash

   docker build . -f Dockerfile.build -t stt-image

Zatim možete koristiti stt unutar Docker-a:

.. code-block:: bash

   docker run -it stt-image bash


Runtime Dependencies
^^^^^^^^^^^^^^^^^^^^

Pokretanje ``stt`` može zahtevati runtime dependence. Za instalaciju porverite dokumentaciju vašeg sistema.

* ``sox`` - Python i Node.JS klijenti koriste SoX da risempluju fajlove na 16kHz
* ``libgomp1`` - libsox (statično povezan sa klijentom) zavisi od OpenMP
* ``libstdc++`` - Standard C++ Library implementacija
* ``libpthread`` -Dependenca na Linux-u. Na Ubuntu, ``libpthread`` je deoe ``libpthread-stubs0-dev`` paketa
* ``Redistribuable Visual C++ 2015 Update 3 (64-bits)`` - Depeendeca na Windows-u. 
Vidi `download from Microsoft <https://www.microsoft.com/download/details.aspx?id=53587>`_

.. toctree::
   :maxdepth: 1

   SUPPORTED_PLATFORMS

.. Third party bindings
   ^^^^^^^^^^^^^^^^^^^^

 Pored zvaničnih Daktilograf STT bindings-a i klijenata, i drugi programeri su obezbedili veze za druge jezike:

   * `Asticode <https://github.com/asticode>`_ provides `Golang <https://golang.org>`_ bindings in its `go-astideepspeech <https://github.com/asticode/go-astideepspeech>`_ repo.
   * `RustAudio <https://github.com/RustAudio>`_ provide a `Rust <https://www.rust-lang.org>`_ binding, the installation and use of which is described in their `deepspeech-rs <https://github.com/RustAudio/deepspeech-rs>`_ repo.
   * `stes <https://github.com/stes>`_ provides preliminary `PKGBUILDs <https://wiki.archlinux.org/index.php/PKGBUILD>`_ to install the client and python bindings on `Arch Linux <https://www.archlinux.org/>`_ in the `arch-deepspeech <https://github.com/stes/arch-deepspeech>`_ repo.
   * `gst-deepspeech <https://github.com/Elleo/gst-deepspeech>`_ provides a `GStreamer <https://gstreamer.freedesktop.org/>`_ plugin which can be used from any language with GStreamer bindings.
   * `thecodrr <https://github.com/thecodrr>`_ provides `Vlang <https://vlang.io>`_ bindings. The installation and use of which is described in their `vspeech <https://github.com/thecodrr/vspeech>`_ repo.
   * `eagledot <https://gitlab.com/eagledot>`_ provides `NIM-lang <https://nim-lang.org/>`_ bindings. The installation and use of which is described in their `nim-deepspeech <https://gitlab.com/eagledot/nim-deepspeech>`_ repo.
