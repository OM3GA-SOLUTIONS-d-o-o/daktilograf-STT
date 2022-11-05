.. _parallel-training-optimization:

Paralena optimizacija treninga
==============================

Koristimo hibridnu optimizaciju za trening modela Daktilograf STT na više GPU-a na jednom hostu.
Paralelna optimizacija može imati različite oblike. Na primer, može se koristiti asinhrona optimizacija modela, sinhrona optimizacija modela, ili kombinacija ova dva.

Asinhrona paralelna optimizacija
----------------------------------

U asinhronoj paralelnoj optimizaciji, na primer, model se prvobitno smešta u memoriju procesora.
Zatim svaki od :math:`G` GPU-a dobija mini-seriju podataka zajedno sa parametrima trenutnog modela.
Koristeći ovaj mini-batch, svaki GPU zatim izračunava gradijente za sve parametre modela i šalje te gradijente nazad u CPU kada GPU završi sa svojom mini-serijom.
CPU zatim asinhrono optimizuje parametre modela kad god od GPU-a primi skup gradijenta.

Asinhrona paralelna optimizacija ima nekoliko prednosti i nekoliko nedostataka.
Jedna velika prednost je propusnost. Nijedan GPU nikada neće biti u stanju mirovanja.
Kada GPU završi obradu mini-serije, može odmah da dobije sledeću mini-seriju za obradu i nikada ne mora da čeka da drugi GPU završe svoju mini-seriju. 
Međutim, to znači da će optimizacija modela takođe biti asinhrona, što može imati svojih nedostataka.

Na primer, neko može imati parametre modela :math:`W` na CPU-u i poslati mini-batch :math:`n` na GPU 1 i poslati mini-batch :math:`n+1` na GPU 2.
Pošto je obrada asinhrona, GPU 2 može završiti pre GPU 1 i tako ažurira parametre modela CPU-a :math:`W` with its gradients :math:`\Delta W_{n+1}(W)`, 
gde indeks :math:`n+1` identifikuje mini-serija, a argument :math:`V` lokaciju na kojoj je procenjen gradijent.

Ovo rezultira novim parametrima modela:

.. math::
    W + \Delta W_{n+1}(W).

Sledeći GPU 1 bi mogao da završi sa svojom mini serijom i ažurira parametre na

.. math::
    W + \Delta W_{n+1}(W) + \Delta W_{n}(W).

Problem sa ovim je da je :math:`\Delta W_{n}(W)` procenjen na :math:`W` a ne na :math:`W + \Delta W_{n+1}(W)`. 
Dakle, smer gradijenta :math:`\Delta W_{n}(W)` nije u potpunosti tačan i procenjen je na pogrešnoj lokaciji. 
Ovo se može suprotstaviti sinhronim ažuriranjima modela, ali to je takođe problematično.

Sinhrona optimizacija
-------------------------

Sinhrona optimizacija rešava problem iznad.
U sinhronoj optimizaciji, prvo se model smešta u memoriju procesora.
Zatim se jednom od `G` GPU-ova daje mini serija podataka zajedno sa parametrima trenutnog modela.
Koristeći mini-batch, GPU izračunava gradijente za sve parametre modela i šalje gradijente nazad u CPU.
CPU zatim ažurira parametre modela i započinje proces slanja sledeće mini serije.

Kao što se lako može videti, sinhrona optimizacija nema problem sa netačnim gradijentima.
Međutim, sinhrona optimizacija može istovremeno koristiti samo jedan GPU.
Dakle, kada imamo više GPU podešavanja, :math:`G > 1`, svi GPU-ovi osim jednog će ostati neaktivni, što je neprihvatljivo.
Međutim, postoji i treća alternativa koja kombinuje prednosti asinhrone i sinhrone optimizacije.

Hibridna paralelna optimizacija
----------------------------

Hibridna paralelna optimizacija kombinuje većinu prednosti asinhrone i sinhrone optimizacije.
Omogućava korišćenje više GPU-a, ali nema problem sa netačnim gradijentom koji pokazuje asinhrona optimizacija.

U hibridnoj paralelnoj optimizaciji model se prvobitno smešta u CPU memoriju.
Zatim, kao u asinhronoj optimizaciji, svaki od :math:`G` GPU-ova dobija mini-seriju podataka zajedno sa trenutnim parametrima modela.
Koristeći mini-batch svaki od GPU-a zatim izračunava gradijente za sve parametre modela i šalje te gradijente nazad u CPU.
Sada, za razliku od asinhrone optimizacije, CPU čeka dok svaki GPU ne završi sa svojom mini-serijom, a zatim uzima srednju vrednost svih gradijenta iz
:math:`G` GPU-a i ažurira model sa srednjim gradijentom.

.. image:: ../images/Parallelism.png
    :alt: Slika prikazuje dijagram sa strelicama koje prikazuju tok informacija između uređaja tokom treninga. CPU uređaj šalje gradijente na jedan ili više GPU uređaja, koji pokreću optimizaciju, a zatim vraćaju nove parametre u CPU, koji ih usredsređuje i započinje novu iteraciju treninga.

Hibridna paralelna optimizacija ima nekoliko prednosti i nekoliko nedostataka.
Kao i u asinhronoj paralelnoj optimizaciji, hibridna paralelna optimizacija omogućava da se paralelno koristi više GPU-ova.
Štaviše, za razliku od asinhrone paralelne optimizacije, problem pogrešnog gradijenta ovde nije prisutan.
U stvari, hibridna paralelna optimizacija radi kao da se radi sa jednom mini-serijom koja je :math:`G` puta veća od veličine mini-serije kojom upravlja jedan GPU.
Međutim, hibridna paralelna optimizacija nije savršena.
Ako je jedan GPU sporiji od svih ostalih u dovršavanju svoje mini serije, svi ostali GPU-ovi će morati da miruju dok zaostali GPU ne završi sa svojom mini-serijom.
Ovo šteti propusnosti. Ali, ako su svi GPU-ovi iste marke i modela, ovaj problem je na minimumu.

Dakle, relativno govoreći, čini se da hibridna paralelna optimizacija ima više prednosti i manje nedostataka u poređenju sa asinhronom i sinhronom
optimizacijom i mi ćemo za rad koristiti ovaj hibridni model.

Adam Optimizacija
-----------------

Nasuprot `Deep Speech: Scaling up end-to-end speech recognition <http://arxiv.org/abs/1412.5567>`_,u kome je korišćen `Nesterov’s Accelerated Gradient Descent <www.cs.toronto.edu/~fritz/absps/momentum.pdf>`_ 
mi koristimo `Adam <http://arxiv.org/abs/1412.6980>`_ metod optimizacije, jer iz iskustva znamo da taj pristup zahteva manje fine tuning-a.
