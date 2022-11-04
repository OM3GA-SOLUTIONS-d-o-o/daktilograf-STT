.. _checkpointing:

Kontrolne tačke
===============

Kontrolne tačke su prikazi parametara neuronske mreže.
Tokom treninga, parametri modela se stalno ažuriraju, a kontrolne tačke omogućavaju prekid treninga bez gubitka podataka.
Ako iz bilo kog razloga prekinete trening, možete da nastavite gde ste stali koristeći kontrolne tačke kao početno mesto.
Potpuno ista logika vaći i za :ref:`model fine-tuning <transfer-learning>`.

Kontrolna tačka se dešava u vremenskom intervalu koji se može konfigurisati.
Nastavak sa kontrolnih tačaka se dešava automatski ponovnim pokretanjem treninga sa istim``--checkpoint_dir`` prethodnog treninga. 
Alternativno, možete da odredite detaljnije opcije sa ``--load_checkpoint_dir`` and ``--save_checkpoint_dir``, koji određuju odvojene lokacije koje će se koristiti za učitavanje i čuvanje kontrolnih tačaka.

Imajte na umu da kontrolne tačke važe samo za istu geometriju modela iz koje su generisane.
Ako imate poruke o grešci da određeni ``Tenzori`` imaju nekompatibilne dimenzije, možda pokušavate da koristite kontrolne tačke sa nekompatibilnom arhitekturom.
