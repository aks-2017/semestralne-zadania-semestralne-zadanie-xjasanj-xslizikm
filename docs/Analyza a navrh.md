# 1. Analýza

V dnešnej dobe, keď sú architektúry sietí masívne je vytvorenie IP siete príliš komplexné na
vytvorenie a udržiavanie. Software Defined Networking (SDN) ponúka riešenie pomocou
následovných vlastností:

- Dátová časť je oddelená od kontrolnej
- Kontrolná logika je presnutá zo sieťových zariadení do NOS (Network Operating
    System)
- Vonkajšie aplikácie dokážu programovať sieť pomocou abstraktných mechanizmov
    ktoré ponúka SDN controller
Tento koncept sa rýchlo rozšíril a v posledných rokoch boli návrhy pre monitorovanie kvalít služieb
(QoS) pomocou SDN, no žiadny z nich sa priamo nezaoberal dostupnou priepustnosťou v sieti. Avšak
tento atribút je dôležitý pri spravovaní siete. Napríklad pri video streamingu sa generuje veľká zátaž na
sieť a je potrebné ju prispôsobiť dostupnej priepustnosti v sieti.

V tomto testovaní sa zameriame na problém, kde budeme hladať najviac priepustné cesty medzi
dvoma bodmi v kontrolovanej sieti. Na to použijeme Mininet na emuláciu siete a Floodlight ako SDN
controller.

# 2. Návrh

Pre uvedený problém, budeme postupovať pri implementácií následovne:

- Pomocou python api si vyvtoríme topológiu (viď odkaz na obrázok nižšie)
- Priamo na host server nainštalujeme Floodlight, nakoľko priamo na VM spôsoboval problémy
    pri načítaní a pre zopakovanie podmienok sme sa rozhodli spraviť to isté, ktorý bude slúžiť
    ako SDN controller pre sieť vytvorenú v mininete
- Naimplementujeme Ford-Fulkersonov algoritmus, ktorý bude riešiť problém maximálneho
    toku v našom grafe topológie siete
- V intervale 300 sekúnd budeme posielať dáta medzi hostami periodicky si budeme pýtať
    hodnotu countrov na SDN switchoch pomocou FlowStatsReq OpenFlow správ.
- Následne si vypočítame aktuálnu záťaž na hranách bi(t) v čase t pomocou vzorca:
    bi(t) = (ni(t) – ni(t – T))/T kde ni(t) je hodnota countra v čase t a T je dopytovacia perióda.
- Z predchádzajúceho vzorca si zistíme dostupnú kapacitu na hranách ai a potom si vypočítame
    dostupnú priestupnosť na cestách pomocou Ford-Fulkersonovho algoritmu


Pre toto meranie použijeme následovný hardware:

- Host CPU: Intel Core i5 3360M
- Host Memory: 16GB
- Virtualization: VirtualBox 5.1.
- Guest OS: Ubuntu 16.04 64-bit
- VM configuration: 2 CPU cores, 2GB memory
- Mininet version: 2.2.
- Floodlight version: 1.

Následovné merania budeme testovať na následujúcej [topológií](https://imgur.com/Cn3DBIb) vytvorenej v mininete.



