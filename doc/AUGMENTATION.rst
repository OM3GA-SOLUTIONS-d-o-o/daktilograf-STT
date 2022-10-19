.. _training-data-augmentation:

Trening augmentacije podataka
==========================

Ovaj dokument je pregled tehnika povećanja količine podataka dostupnih za trening STT-a.

Augmentacija data seta može pomoći STT modelima da bolje transkribuju nepoznat govor. 
Osnovna ideja koja stoji iza augmentacije podataka je sledeća: izobličenjem, modifikovanjem ili dodavanjem postojećih audio podataka, možete kreirati data set za trening mnogo puta veći od onoga koji ste imali na početku.
Ako koristite veći data set za trening da biste trenirali STT model, prisiljavate model da nauči karakteristike govora koje se mogu generalizovati, što otežava `prekomerno prilagođavanje. 
Ukoliko ne možete naći veći dataset, možete ga kreirati augmentacijom.

Implementirali smo unapred procesuirani pipeline sa različitim tehnikama augmentacije na audio fajlovima. (t.j. raw ``PCM`` i spektrograme).

Augmentacija koju odredite će potencijalno imati uticaj na svaki fajl u vašem dta setu. 
Da li će augmentacija zapravo biti primenjena na svaki audio fajl zavisi od njene vrednosti povećanja verovatnoće. 
Naprimer, vrednost verovatnoće od``p=0.1`` znači da postoji 10% šanse da se augmentacija primeni na dati audio fajl. 
Ovo takođe znači da se augmentacije ne isključuju međusobno na datom fajlu. 

Oznaka``--augment`` koristi zajedničku sintaksu za sve tipove povećanja:

.. code-block::

  --augment "augmentation_type1[param1=value1,param2=value2,...]" "augmentation_type2[param1=value1,param2=value2,...]" ...

Na rimer, za ``overlay`` augmentaciju:

.. code-block::

  python -m coqui_stt_training.train --augment "overlay[p=0.1,source=/path/to/audio.sdb,snr=20.0]" ...

U dokumentaciji ispod, kad god je vrednost navedena kao ``<float-range>`` ili ``<int-range>``, podržava jedan od sledećih formata:

  * ``<value>``: Konstantna (int or float) vrednost

  * ``<value>~<r>``: Centralna vrednost sa radijusom randomizacije oko nje. Na primer.. ``1.2~0.4`` će rezultirati odabirom ujednačeno nasumične vrednosti između 0.8 and 1.6 na svakom povećanju augmentacije.

  * ``<start>:<end>``: Vrednost će se kretati od `<start>`na početku treninga do `<end>` na kraju treninga. Na primer ``-0.2:1.2`` (float) ili ``2000:4000`` (int)

  * ``<start>:<end>~<r>``: Kombinacija prethodna dva slučaja sa centralnom vrednošću raspona. Na primer ``4-6~2`` bi na početku treninga biralo vrednosti između 2 i 6 a na kraju treninga između 4 i 8.

Opsezi navedeni sa ograničenjima celog broja pretpostavljaju samo celobrojne (zaokružene) vrednosti.
.. warning::
    Kada je keširanje funkcija omogućeno, keš po podrazumevanoj vrednosti nema ograničenje roka trajanja i koristiće se za ceo trening proces.
	Ovo će dovesti do toga da se ove augmentacije vrše samo jednom tokom prve epohe, a rezultat će se ponovo koristiti za sledeće epohe.
	Ovo ne samo da bi omelo opsege vrednosti od dostizanja predviđenih konačnih vrednosti, već bi takođe moglo dovesti do nenamernog overfittinga.
	U ovom slučaju, oznaku``--cache_for_epochs N`` (with N > 1) treba koristiti za periodično poništavanje keša nakon svakih N epoha i na taj način omogućiti da se uzorci ponovo augmentuju na nove načine i sa trenutnim vrednostima opsega.

Svaka augmentacija targetira određenu reprezentaciju uzorka - u ovoj dokumentaciji te se reprezentacije nazivaju *domeni*.
Augmentacije se primenjuju sledećim redosledom:

1. **sample** domen: Uzorak je upravo učitan i njegov talasni oblik je predstavljen kao NumPy niz. Zbog implementacije, ove augmentacije su jedine koje se mogu "simulirati" preko``bin/play.py``.

2. **signal** domen: Talasni oblik uzorka je predstavljen kao tenzor.

3. **spectrogram** domen: Spektrogram uzorka je predstavljen kao tenzor.

4. **features** domen: Karakteristike mel spektrograma uzorka su predstavljene kao tenzor.

U okviru jednog domena, proširenja se primenjuju istim redosledom kako se pojavljuju u komandnoj liniji.


Primer augmentacije domena
---------------------------

**Overlay augmentation** ``"overlay[p=<float>,source=<str>,snr=<float-range>,layers=<int-range>]"``
  Dodaje se sloj drugog audio fajla na već augmentirane uzorke. 

  * **p**: vrednost verovatnoće je 0.0 (nikad) i 1.0 (uvek) ako se dati uzorak augmentira ovom metodom.

  * **source**: putanja za kolekciju uzoraka kojom se vrši augmentacija (\*.sdb or \*.csv file). Ponoviće se ako nema dovoljno uzoraka.

  * **snr**: odnos signal/šum u dB - pozitivne vrednosti za smanjenje jačine preklapanja u odnosu na uzorak

  * **layers**: broj slojeva koji su dodati uzorku (npr. 10 slojeva govora da bi se dobio „efekat koktela“). Sloj je samo uzorak istog trajanja kao i uzorak za povećanje. Sastavlja se iz onoliko izvornih uzoraka koliko je potrebno.

**Reverb augmentation** ``"reverb[p=<float>,delay=<float-range>,decay=<float-range>]"``
  Dodaje pojednostavljene(no all-pass filters) `Schroeder reverberation <https://ccrma.stanford.edu/~jos/pasp/Schroeder_Reverberators.html>`_za augmentovane uzorke.

  * **p**: vrednost verovatnoće 0.0 (nikad) i 1.0 (uvek) ako se dati uzorak augmentuje ovom metodom

  * **delay**: vremensko kašnjenje u milisekundama za prvu refleksiju signala -e veće vrednosti proširuju "sobu".
 
  * **decay**: opadanje zvuka u dB po refleksiji - veće vrednosti će rezultirati sa manje povratnog signala


**Resample augmentation** ``"resample[p=<float>,rate=<int-range>]"``
  Resample-uje augmentovane uzorke na rugi sample rate, a yatim ga vra'a na originalni sample rate. 

  * **p**: vrednost verovatnoće 0.0 (nikad) i 1.0 (uvek) ako se dati uzorak augmentuje ovim metodom.

  * **rate**: sample-rate to re-sample to


**Codec augmentation** ``"codec[p=<float>,bitrate=<int-range>]"``
  Kompersuje, zatim dekompresuje augmentovane uzorke koriteći lossy Opus audio kodek.

  * **p**: vrednost verovatnoće između 0.0 (nikad) i  1.0 (uvek)  ako se dati uzorak augmentuje ovim metodom.

  * **bitrate**: bitrate korišćen tokom kompresovanja.


**Volume augmentation** ``"volume[p=<float>,dbfs=<float-range>]"``
  Meri date uzorke da bi odredili dBFS vrednost.

  * **p**: vrednost između 0.0 (nikad) i 1.0 (uvek) ako se dati uzorak augmentuje ovim metodom.

  * **dbfs** : ciljna jačina u dBFS (default vrednost od 3.0103 će normalizovati minimalne i maksimalne amplitude u rasponu od -1.0/1.0)

Augmentacija spektrogram domena
--------------------------------

**Pitch augmentation** ``"pitch[p=<float>,pitch=<float-range>]"``
  Skalira spektrogram na osi frekvencije i tako menja visinu.

  * **p**: vrednost između 0.0 (nikad) i 1.0 (uvek) ako se dati uzorak augmentuje ovim metodom.

  * **pitch**: Faktor visine tona sa frekvencijskom osom je skaliran (npr. vrednost od 2,0 će povećati audio frekvenciju za jednu oktavu)


**Tempo augmentation** ``"tempo[p=<float>,factor=<float-range>]"``
 Skalira spektrogram na vremenskoj osi i tako menja tempo reprodukcije.

  * **p**: vrednost između 0.0 (nikad) i 1.0 (uvek) ako se dati uzorak augmentuje ovim metodom.

  
  * **factor**: faktor brzine za koji se vremenska osa rasteže ili skuplja (npr. vrednost od 2,0 će udvostručiti tempo reprodukcije)


**Warp augmentation** ``"warp[p=<float>,nt=<int-range>,nf=<int-range>,wt=<float-range>,wf=<float-range>]"``
  Primenjuje nelinearnu deformaciju slike na spektrogram. Ovo se postiže nasumičnim pomeranjem mreže jednako raspoređenih tačaka osnove duž vremenske i frekvencijske ose.

  * **p**:vrednost između 0.0 (nikad) i 1.0 (uvek) ako se dati uzorak augmentuje ovim metodom.

  * **nt**: broj jednako raspoređenih linija osnove mreže duž vremenske ose spektrograma (isključujući ivice)

  * **nf**: broj jednako raspoređenih linija iskrivljene mreže duž ose frekvencije spektrograma (isključujući ivice)

  * **wt**: standardna devijacija nasumičnog pomeranja primenjenog na tačke osnove duž vremenske ose (0.0 = no warp, 1.0 = half the distance to the neighbour point)

  * **wf**: standardna devijacija nasumičnog pomeranja primenjenog na tačke osnove duž ose frekvencije (0.0 = no warp, 1.0 = half the distance to the neighbour point)


**Frequency mask augmentation** ``"frequency_mask[p=<float>,n=<int-range>,size=<int-range>]"``
  Postavlja frekvencijske intervale unutar proširenih uzoraka na nulu (tišina) na nasumičnim frekvencijama. Pogledajte SpecAugment dokument za više detalja- https://arxiv.org/abs/1904.08779

  * **p**: vrednost između 0.0 (nikad) i 1.0 (uvek) ako se dati uzorak augmentuje ovim metodom.

  * **n**: broj intervala za maskiranje

  * **size**: broj frekventnih opsega za maskiranje po intervalu

Više domenska augmentacija
--------------------------

**Time mask augmentation** ``"time_mask[p=<float>,n=<int-range>,size=<float-range>,domain=<domain>]"``
  Postavlja vremenske intervale unutar proširenih uzoraka na nulu (tišina) na nasumičnim pozicijama

  * **p**: vrednost između 0.0 (nikad) i 1.0 (uvek) ako se dati uzorak augmentuje ovim metodom.

  * **n**: broj intervala je podešen na nulu

  * **size**: dužina intervala u milisekundama

  * **domain**: predstavljanje podataka za primenu augmentacije - "signal", "features" ili "spectrogram" (default)


**Dropout augmentation** ``"dropout[p=<float>,rate=<float-range>,domain=<domain>]"``
  Nule slučajne tačke podataka ciljanog prikaza podataka.

  * **p**: vrednost između 0.0 (nikad) i 1.0 (uvek) ako se dati uzorak augmentuje ovim metodom.

  * **rate**: stopa dropout-a u opsegu od 0.0 do 1.0 za 100% dropout-a

  * **domain**: predstavljanje podataka za primenu augmentacije - "signal", "features" ili "spectrogram" (default)


**Add augmentation** ``"add[p=<float>,stddev=<float-range>,domain=<domain>]"``
 Dodaje nasumične vrednosti izabrane iz normalne distribucije (sa srednjom vrednošću 0,0) svim tačkama podataka ciljanog prikaza podataka.

  * **p**: vrednost između 0.0 (nikad) i 1.0 (uvek) ako se dati uzorak augmentuje ovim metodom.

  * **stddev**:standardna devijacija normalne distribucije za odabir vrednosti

  * **domain**: predstavljanje podataka za primenu augmentacije  - "signal", "features" (default) ili "spectrogram"


**Multiply augmentation** ``"multiply[p=<float>,stddev=<float-range>,domain=<domain>]"``
  Množi sve tačke podataka ciljane reprezentacije podataka sa slučajnim vrednostima izabranim iz normalne distribucije (sa srednjom vrednošću 1,0).

  * **p**: vrednost između 0.0 (nikad) i 1.0 (uvek) ako se dati uzorak augmentuje ovim metodom.

  * **stddev**: standardna devijacija normalne distribucije za odabir vrednosti

  * **domain**: predstavljanje podataka za primenu augmentacije  - "signal", "features" (default) ili "spectrogram"
  

Primer treninga sa primenom svih augmentacija

.. code-block:: bash

        python -m coqui_stt_training.train \
          --train_files "train.sdb" \
          --epochs 100 \
          --augment \
              "overlay[p=0.5,source=noise.sdb,layers=1,snr=50:20~10]" \
              "reverb[p=0.1,delay=50.0~30.0,decay=10.0:2.0~1.0]" \
              "resample[p=0.1,rate=12000:8000~4000]" \
              "codec[p=0.1,bitrate=48000:16000]" \
              "volume[p=0.1,dbfs=-10:-40]" \
              "pitch[p=0.1,pitch=1~0.2]" \
              "tempo[p=0.1,factor=1~0.5]" \
              "warp[p=0.1,nt=4,nf=1,wt=0.5:1.0,wf=0.1:0.2]" \
              "frequency_mask[p=0.1,n=1:3,size=1:5]" \
              "time_mask[p=0.1,domain=signal,n=3:10~2,size=50:100~40]" \
              "dropout[p=0.1,rate=0.05]" \
              "add[p=0.1,domain=signal,stddev=0~0.5]" \
              "multiply[p=0.1,domain=features,stddev=0~0.5]" \
          [...]


The ``bin/play.py`` and ``bin/data_set_tool.py`` alati takođe podržavaju ``--augment`` parametre (za uzorke domenskih augmentacija) i može se koristiti za eksperimentisanje sa različitim konfiguracijama ili kreiranje proširenih data setova.
Primer svih semplova sa reverberacijom i maksimalnom jačinom zvuka:

.. code-block:: bash

        bin/play.py --augment "reverb[p=0.1,delay=50.0,decay=2.0]" --augment volume --random true --source test.sdb

Primer simulacije augmentacije kodeka.wav datoteke na početku i na kraju epohe: 

.. code-block:: bash

        bin/play.py --augment "codec[p=0.1,bitrate=48000:16000]" --clock 0.0 --source test.wav
        bin/play.py --augment "codec[p=0.1,bitrate=48000:16000]" --clock 1.0 --source test.wav

Primer kreiranja test seta pre augmentacije:

.. code-block:: bash

        bin/data_set_tool.py \
          --augment "overlay[source=noise.sdb,layers=1,snr=20~10]" \
          --augment "resample[rate=12000:8000~4000]" \
          --sources test.sdb --target test-augmented.sdb
