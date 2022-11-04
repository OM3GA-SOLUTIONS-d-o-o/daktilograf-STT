.. _build-native-client:

Bild binarnih datoteka
=================

Ovaj odeljak opisuje kako da napravite Daktilograf STT binarne datoteke.

Izričito se preporučuje da uvek koristite naše unapred izgrađene Daktilograf STT binarne datoteke (dostupne sa svakim `izdanjem
<https://github.com/coqui-ai/STT/releases>`_) osim ako nemate razloga da ih napravite sami.
Ako i dalje želite da sami napravite binarne datoteke Daktilograf STT, biće vam potrebni sledeći preduslovi preuzeti i instalirani:

* `Bazel 5.0.0 <https://bazel.build/install/bazelisk>`_ (ili `Bazelisk <https://github.com/bazelbuild/bazelisk>`__)
* `General TensorFlow r2.3 requirements <https://www.tensorflow.org/install/source#tested_build_configurations>`_
* `libsox <https://sourceforge.net/projects/sox/>`_

Neophodno je da se koristi naš TensorFlow fork jer uključuje ispravke za uobičajene probleme na koje se susreću prilikom pravljenja izvornih klijentskih datoteka.

Ako želite da napravite language bindings ili paket dekodera, takođe će vam trebati:

* `SWIG master <https://github.com/swig/swig>`_.
  Nažalost, NodeJS / ElectronJS nakon 10.x podrška na SWIG malo zaostaje, iako postoje popravke spojene na masteru, one nisu puštene.
  Unapred izgrađene patcho-vane verzije( Linux, Windows i macOS) SWIG-a treba da se instaliraju pod `native_client/ <native_client/>`_ automatski čim bildujete bilo koji binding koji ga zahteva.
  
* `node-pre-gyp <https://github.com/mapbox/node-pre-gyp>`_ (for Node.JS bindings only)

Za informacije o bildu na Windows-u, pogledajte: :ref:`Windows Building <build-native-client-dotnet>`.

Dependence
------------

Ukoliko sledite ova uputstva, trebalo bi da sastavite sopstvene binarne datoteke Daktilografa STT (napravljenog na TensorFlow-u koristeći Bazel).

Za više informacija o konfigurisanju TensorFlov-a, pročitajte dokumente do kraja: `"Configure the Build" <https://www.tensorflow.org/install/source#configure_the_build>`_.

Checkout source code
^^^^^^^^^^^^^^^^^^^^

Klon izvornog koda Daktilograf STT (TensorFlow je submodul):

.. code-block::

   git clone https://github.com/coqui-ai/STT.git STT
   cd STT
   git submodule sync tensorflow/
   git submodule update --init tensorflow/

Bazel: Download i Instalacija
^^^^^^^^^^^^^^^^^^^^^^^^^

Prvo instalirajte Bazel 5.0.0 prateći `Bazel instalacijsku dokumentaciju <https://docs.bazel.build/versions/5.0.0/install.html>`_
ili `Bazelisk <https://docs.bazel.build/versions/main/install-bazelisk.html>`_.

TensorFlow: Konfiguracija sa Bazel-om 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nakon što instalirate ispravnu verziju Bazel-a, konfigurišite TensorFlow:

.. code-block::

   cd tensorflow
   ./configure

Kompajling  STT-a
-----------------

Compile ``libstt.so``
^^^^^^^^^^^^^^^^^^^^^

Unutar vašeg TensorFloq direktorijuma, trebalo bi da postoji veza ka direktorijumu Daktilograf STT ``native_client``. 
Ako nije prisutna, kreirajte ga sledećom komandom:


.. code-block::

   cd tensorflow
   ln -s ../native_client

Sada možete da koristite Bazel da napravite glavnu Daktilograf STT biblioteku, ``libstt.so``. Dodajte ``--config=cuda`` ako želite CUDA bild.

.. code-block::

   bazel build --workspace_status_command="bash native_client/bazel_workspace_status_cmd.sh" -c opt --copt="-D_GLIBCXX_USE_CXX11_ABI=0" //native_client:libstt.so

Generisane binarne datoteke će biti sačuvane u ``bazel-bin/native_client/``.

.. _build-generate-scorer-package:

Kompajling ``generate_scorer_package``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prateći isto podešavanje kao za ``libstt.so`` iznad, možete ponovo da bildujete ``generate_scorer_package`` 
binarnu datoteku dodajući komandu: ``//native_client:generate_scorer_package``.
Koristeći primer odozgo možete da napravite biblioteku i binarnu datoteku u isto vreme:

.. code-block::

   bazel build --workspace_status_command="bash native_client/bazel_workspace_status_cmd.sh" -c opt --copt="-D_GLIBCXX_USE_CXX11_ABI=0" //native_client:libstt.so //native_client:generate_scorer_package

Generisane binarne datoteke će biti sačuvane u ``bazel-bin/native_client/``.

Kompajling Language Bindings
^^^^^^^^^^^^^^^^^^^^^^^^^

Sada, ``cd`` u ``STT/native_client`` direktorijum i koristite ``Makefile`` da izgradi sve language bindings (C++ client, Python package, Nodejs package, etc.).

.. code-block::

   cd ../STT/native_client
   make stt

Instaliranje sopstvenih binarnih datoteka
----------------------------

Nakon bilda, biblioteka i binarni fajlovi mogu opciono da se instaliraju na sistemsku putanju radi lakšeg razvoja. Ovo je takođe obavezan korak za generisanje veza.
.. code-block::

   PREFIX=/usr/local sudo make install

Pretpostavlja se da: ``$PREFIX/lib`` je važeća putanja biblioteke, inače ćete možda morati da promenite svoje okruženje.

Instaliranje Python veza
^^^^^^^^^^^^^^^^^^^^^^^

Uključen je set generisanih Python veza. Nakon uputstava odozgo za bild i instalaciju, dalja instalacija se sprovodi izvršavanjem sledećih komandi (ili ekvivalenta na vašem sistemu):
.. code-block::

   cd native_client/python
   make bindings
   pip install dist/stt-*

`Reference documentation <python-api>`_ je dostupna za Python veze, kao i primeri u `STT-examples repository <https://github.com/coqui-ai/STT-examples>`_ i `izvorni kod za CLI alat instaliran uz Python veze <py-api-example>`_.

Instaliranje NodeJS / ElectronJS veza
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nakon što ste sledili gorenavedena uputstva za bild i instalaciju, Node.JS veze mogu da se bilduju:

.. code-block::

   cd native_client/javascript
   make build
   make npm-pack

Kreirati paket ``stt-VERSION.tgz`` u ``native_client/javascript``.

.. _build-ctcdecoder-package:

Instaliranje CTC decoder paketa
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Za bild ``coqui_stt_ctcdecoder`` paketa, biće potrebno je da ispunite zahteve (posebno SWIG-a). Komanda u nasvku gradi veze koristeći osam (8) procesa za kompajling. Podesite parametre za više ili manje korelacije.

.. code-block::

   cd native_client/ctcdecode
   make bindings NUM_PROCESSES=8
   pip install dist/*.whl


Podržavamo samo bild CTC dekodera na x86-64 arhitekturi.
Međutim, nudimo neke savete o bildu CTC dekodera na drugim arhitekturama, a možda ćete pronaći pomoć u `GitHub diskusijama <https://github.com/coqui-ai/STT/discussions>`_.

Prvo morate bildovati SWIG od nule od master branch-a. >Naše binarne datoteke su bildovane iz `90cdbee6a69d13b39d734083b9f91069533b0d7b <https://github.com/swig/swig/tree/90cdbee6a69d13b39d734083b9f91069533b0d7b>`_.

Možete da isporučite svoj unapred bildovan SWIG koristeći``SWIG_DIST_URL``

Možda ćete morati da promenite``PYTHON_PLATFORM_NAME`` u skladu sa platformom koju koristite.

.. code-block::

    # PowerPC (ppc64le)
    PYTHON_PLATFORM_NAME="--plat-name linux_ppc64le"

Kompletna bild komanda:

.. code-block::

    SWIG_DIST_URL=[...] PYTHON_PLATFORM_NAME=[...] make bindings
    pip install dist/*.whl

Cross-building
--------------

RPi3 ARMv7 and LePotato ARM64
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

podržavamo unakrsnu kompilaciju sa Linuk hostova. Sledeće``--config`` flags mogu biti navedene kada se bilduje sa bazel-om:

* ``--config=elinux_armhf`` for Raspbian / ARMv7
* ``--config=elinux_aarch64`` for ARMBian / ARM64

Dakle, vaša komandna linija za ``RPi3`` i ``ARMv7`` treba da izgleda ovako:

.. code-block::

   bazel build --workspace_status_command="bash native_client/bazel_workspace_status_cmd.sh" -c opt --config=elinux_armhf //native_client:libstt.so

A vaša komandna linija za``LePotato`` i  ``ARM64`` treba da izgleda ovako:

.. code-block::

   bazel build --workspace_status_command="bash native_client/bazel_workspace_status_cmd.sh" -c opt --config=elinux_aarch64 //native_client:libstt.so

Iako testiramo samo na RPi3 Raspbian Buster i LePotato ARMBian Bullseye, sve što je kompatibilno sa ``armv7-a cortex-a53`` ili ``armv8-a cortex-a53`` bi trebalo da odgovara.

``stt`` binarna datoteka takođe može biti bildovana, sa ``TARGET=rpi3`` ili ``TARGET=rpi3-armv8``. 
Ovo može zahtevati da podesite sistemsko stablo koristeći alatku ``multistrap`` i multitrap konfiguracione datoteke: ``native_client/multistrap_armbian64_buster.conf`` and ``native_client/multistrap_raspbian_buster.conf``.
Putanja sistemskog stabla se može zameniti od podrazumevanih vrednosti definisanih u ``definitions.mk`` kroz ``RASPBIAN`` ``make`` varijablu.

.. code-block::

   cd ../STT/native_client
   make TARGET=<system> stt

Bild ``libstt.so`` za Android
----------------------------------

Preduslovi
^^^^^^^^^^^^^

Osim generalnih preduslova navedenih iznad , biće vam potrebne i specifične dependence za Android za TensorFlow, 
Naime, moraćete da instalirate `Android SDK <https://developer.android.com>`_ 
i `Android NDK version r18b <https://github.com/android/ndk/wiki/Unsupported-Downloads#r18b>`_. 
Nakon što to završite, izvezite varijable okruženja ``ANDROID_SDK_HOME`` i ``ANDROID_NDK_HOME`` 
u odgovarajuće fascikle u koje su instalirani SDK i NDK.
Konačno, konfigurišite TensorFlov verziju i uverite se da ste odgovorili sa "da" kada skripta pita da li želite da podesite Android verziju.

Tada možete bildovati ``libstt.so`` koristeći (ARMv7):

.. code-block::

   bazel build --workspace_status_command="bash native_client/bazel_workspace_status_cmd.sh" --config=android_arm --action_env ANDROID_NDK_API_LEVEL=21 //native_client:libstt.so

ili (ARM64):

.. code-block::

   bazel build --workspace_status_command="bash native_client/bazel_workspace_status_cmd.sh" --config=android_arm64 --action_env ANDROID_NDK_API_LEVEL=21 //native_client:libstt.so

Bild``libstt.aar``
^^^^^^^^^^^^^^^^^^^^^^^

Da bi se izgradile JNI bindings, izvorni kod je dostupan u direktorijumu``native_client/java/libstt``. 
Bild AAR paketa zahteva  prethodno napravljen ``libstt.so``za sve željene arhitekture 
i  odgovarajuće binarne datoteke u subdirektorijumima``native_client/java/libstt/libs/{arm64-v8a,armeabi-v7a,x86_64}/`` . 
Ako ne želite da bildujete AAR paket za sve ARM64, ARMv7 and x86_64, možete izmeniti fajl
``native_client/java/libstt/gradle.properties`` da izbacite sve neželjene arhitekture.

Bild bindings-a kontroliše ``gradle`` i možete se napraviti pozivanjem ``./gradlew libstt:build`` unutar ``native_client/java`` foldera, praveći ``AAR`` paket u
``native_client/java/libstt/build/outputs/aar/``.

Imajte na umu da ćete možda morati da kopirate datoteku u lokalni Maven repozitorijum
i prilagodite imenovanje datoteka (kada nedostaje, poruka o grešci treba da navede koje ime datoteke se očekuje i gde).

Bild C++ ``stt`` binarne datoteke za Android
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bild ``stt`` binarne datoteke se dešava kroz ``ndk-build`` (ARMv7):

.. code-block::

   cd ../STT/native_client
   $ANDROID_NDK_HOME/ndk-build APP_PLATFORM=android-21 APP_BUILD_SCRIPT=$(pwd)/Android.mk NDK_PROJECT_PATH=$(pwd) APP_STL=c++_shared TFDIR=$(pwd)/../tensorflow/ TARGET_ARCH_ABI=armeabi-v7a

I (ARM64):

.. code-block::

   cd ../STT/native_client
   $ANDROID_NDK_HOME/ndk-build APP_PLATFORM=android-21 APP_BUILD_SCRIPT=$(pwd)/Android.mk NDK_PROJECT_PATH=$(pwd) APP_STL=c++_shared TFDIR=$(pwd)/../tensorflow/ TARGET_ARCH_ABI=arm64-v8a

Android demo APK
^^^^^^^^^^^^^^^^

Obezbeđena je veoma jednostavna Android demo aplikacija koja vam omogućava da testirate biblioteku.
Možete bildovati sa ``make apk`` i instalirati rezultujući APK fajl. Pogledajte Gradle dokumentaciju 
za više detalja.

``APK`` treba da se nađe u ``/app/build/outputs/apk/``. Ova demo aplikacija bi mogla
zahtevaju spoljne dozvole za skladištenje. 
Zatim možete eksportovati fajlove modela na svoj uređaj, postavite putanju do datoteke u 
korisničkom interfejsu i pokušate da pokrenete audio datoteku. 
Prilikom pokretanja, prvo bi trebalo da reprodukuje audio datoteku, a zatim da pokrene dekodiranje.
na kraju dekodiranja, trebalo bi da vam se prikaže i dekodirani tekst i koliko je vremena proteklo u milisekundama.

This application is very limited on purpose, and is only here as a very basic
demo of one usage of the application. For example, it's only able to read PCM
mono 16kHz 16-bits file and it might fail on some WAVE file that are not
following exactly the specification.

Ova aplikacija je namerno veoma ograničena i ovde je samo kao osnovna
demonstracija jedne upotrebe aplikacije. Na primer, može samo da čita PCM
mono 16kHz 16-bitnu datoteku i možda neće uspeti na nekoj WAV datoteci koja nije u potpunosti
u skladu sa specifikacijom.


Pokretanje ``stt`` kroz adb
^^^^^^^^^^^^^^^^^^^^^^^

Treba da koristite ``adb push`` da pošaljete datoteke na uređa. 
Molimo pogledajte Android dokumentaciju za više detalja.

Push Daktilograf STT fajlove na ``/sdcard/STT/``\ , uključujući:


* ``output_graph.tflite`` što je TF lifte model
* Eksterni scorer fajl (dostupan na jednom od naših release-ova), ako želite da koristite skorer; 
Imajte na umu da preveliki scorer fajl može uzrokovati preopterećenje memorije uređaja-

Zatim, push binarne datoteke iz ``native_client.tar.xz`` u ``/data/local/tmp/ds``\ :

* ``stt``
* ``libstt.so``
* ``libc++_shared.so``

Tada bi trebalo da pokrenete run kao i obično koristeći shell ``adb shell``\ :

.. code-block::

   user@device$ cd /data/local/tmp/ds/
   user@device$ LD_LIBRARY_PATH=$(pwd)/ ./stt [...]

Imajte na umu da Android linker ne podržava ``rpath`` pa morate podesiti
``LD_LIBRARY_PATH``. 
Pravilno upakovani bindings  ugrađuju biblioteku
na mestu gde linker zna gde da traži, te će ovo odgovarati za Android aplikacije.

Delegacija API'ja
^^^^^^^^^^^^^^^^^

TensorFlow Lite podržava Delegate API za oslobađanje CPU-a od nekih komputacija. 
Za više detalja pogledajte `TensorFlow's dokumentaciju:
<https://www.tensorflow.org/lite/performance/delegates>`_.

Da bismo olakšali eksperimentisanje, omogućili smo neke od tih delegacija na našoj
Android verziji * GPU, da bi se iskoristile mogućnosti * NNAPI,  Android API
da bi se iskoristile mogućnosti GPU / DSP / NPU * Hexagon,  Qualcomm-specific DSP

Ovo je veoma eksperimentalno:

* Zahteva prosleđivanje promenljive okruženja ``STT_TFLITE_DELEGATE`` sa vrednostima od
 ``gpu``, ``nnapi`` ili ``hexagon`` (samo jedan po jedan)
* Možda će biti potrebne promene izvezenog modela (neke operacije možda nisu podržane)
* Ne možemo da garantujemo da će raditi, niti će biti brži od podrazumevane
 implementacije

Povratne informacije o poboljšanju ovoga su dobrodošle: kako ovo može biti izloženo u API-ju, koliko
 poboljšanja performansi dobijate u svojim aplikacijama, kako ste morali da promenite
model da radi sa delegatom itd.

Vidi :ref:`the support / contact details <support>`
