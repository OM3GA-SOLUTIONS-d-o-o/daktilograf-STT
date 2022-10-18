Daktilograf STT Model
=========

Cilj ovog projekta je kreiranje jednostavnog, otvorenog i sveprisutnog engine-a za prepoznavanje govora u tekst.
Jednostavnog u smislu da engine ne zahteva serversku strukturu za rad.
Otvorenog u smislu da su kod i modeli objavljeni pod Mozilla Public Licencom. 
Svobuhvatnog , u smslsu da engine može da radi na svim platformama i da se razvoja na brojnim jezicima. 

Arhitektura engine-ea je originalno zamišljena  i predstavljena u publikaciji 
`Deep Speech: Scaling up end-to-end speech recognition <http://arxiv.org/abs/1412.5567>`_.
Međutim, engine se trenutno u mnogo čemu razlikuje od prvobitno koncipiranog engine-a.
Kor engine-a je rekurentna neuronska mreža (RNN) trenirana za unos govornih spektrograma i generisanje transkripcija teksta.

Ako je iskaz :math:`x` and label :math:`y` semplovan kao trening set

onda je
.. math::
    S = \{(x^{(1)}, y^{(1)}), (x^{(2)}, y^{(2)}), . . .\}.

Svaki iskaz, :math:`x^{(i)}` je vremenska sekvenca dužine :math:`T^{(i)}`
gde je svaka sekvenca vektor sa zvučnim karakteristikama,
:math:`x^{(i)}_t` where :math:`t=1,\ldots,T^{(i)}`.

Koristimo MFCC kao naše karakteristike; so :math:`x^{(i)}_{t,p}` označava :math:`p`-th MFCC funkciju
u audio frejmu u vreme :math:`t`. Cilj našeg RNN-a je da konvertuje ulaznu
sekvencu :math:`x` u niz karaktera po verovatnoći za transkripciju 
:math:`y`, with :math:`\hat{y}_t =\mathbb{P}(c_t \mid x)`,
gde je za engleski :math:`c_t \in \{a,b,c, . . . , z, space, apostrophe, blank\}`.
(Značenje :math:`blank`će biti objašnjeno ispod.)

Naš RNN  model se satoji iz :math:`5` slojeva skrivenih jedinica.
Za ulaz :math:`x`, skrivene jedinice na sloju :math:`l` su označene sa :math:`h^{(l)}` sa
konvolucijom da je :math:`h^{(0)}` ulaz. Prva tri sloja se ne ponavljaju.
Za prvi sloj u svakom trenutku :math:`t`, izlaz zavisi of MFCC frejma
:math:`x_t` sa kontekstom :math:`C` ima okvir sa obe strane.
(Koristimo :math:`C = 9` za eksperimente.)
Preostali slojevi koji se ne ponavljaju rade sa nezavisnim podacima za svaku vremensku sekvencu.
Dakle, za svako vreme :math:`t`, prvih :math:`3` sloja se izračunavaju sa:

.. math::
    h^{(l)}_t = g(W^{(l)} h^{(l-1)}_t + b^{(l)})

gde je :math:`g(z) = \min\{\max\{0, z\}, 20\}` je isečena ispravljačka aktivaciona funkcija (ReLu)
i :math:`W^{(l)}`, :math:`b^{(l)}` su matrica težine i parametar biasa za sloj  :math:`l`. Četvrti sloj je ponavljajući
 `[1] <https://en.wikipedia.org/wiki/Recurrent_neural_network>`_.
Ovaj sloj uključuje skup skrivenih jedinica sa ponavljanjem unapred,
:math:`h^{(f)}`:

.. math::
    h^{(f)}_t = g(W^{(4)} h^{(3)}_t + W^{(f)}_r h^{(f)}_{t-1} + b^{(4)})

Imajte na umu da :math:`h^{(f)}` mora da se izračuna uzastopno od :math:`t = 1` to :math:`t = T^{(i)}`
za :math:`i`-th iskaz.

Peti (neponavljajući) sloj uzima napredne jedinice kao ulaze

.. math::
    h^{(5)} = g(W^{(5)} h^{(f)} + b^{(5)}).

Izlazni sloj su standardni logiti koji odgovaraju predviđenim verovatnoćama karaktera
za svaki vremenski isečak :math:`t` i znak :math:`k` u alfabetu:

.. math::
    h^{(6)}_{t,k} = \hat{y}_{t,k} = (W^{(6)} h^{(5)}_t)_k + b^{(6)}_k

Ovde :math:`b^{(6)}_k` označava :math:`k`-th bias i :math:`(W^{(6)} h^{(5)}_t)_k`  :math:`k`-th
element matričnog rezultata.

Kada smo izračunali predviđanje za :math:`\hat{y}_{t,k}`, izračunavamo loss (gubitak) CTC-a
`[2] <http://www.cs.toronto.edu/~graves/preprint.pdf>`_ :math:`\cal{L}(\hat{y}, y)`
da bismo izračunali procenat greške u predikciji. (CTC loss zahteva :math:`blank` iznad
da ukaže na prelaze između znakova.) Tokom treninga možemo proceniti i gradijent
:math:`\nabla \cal{L}(\hat{y}, y)` u odnosu na mrežne izlaze imajući u vidu stvarne vrednosti 
sekvenci karaktera :math:`y`. Od ove tačke, proračun gradijenta
u odnosu na sve parametre modela može da se uradi putem propagacije unazad
preko ostatka mreže. Za obuku koristimo Adamov metod
`[3] <http://arxiv.org/abs/1412.6980>`_.

Kompletan RNN model je ilustrovan na slici ispod.

.. image:: ../images/rnn_fig-624x598.png
    :alt: DeepSpeech BRNN
