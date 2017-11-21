# Druhý kontrolný bod - Implementácia prototypu

Cieľom vytvorenia nášho prototypu bolo vytvorenie siete, v ktorej sme simulovali tok dát medzi hostmi a následne sme zistovali dostupnú kapacitu. 

## Nastavenie mininetu
Na vytvorenie topologie v mininete sme pouzili skript topo-4sw-5host.py. Topológia bola vytvorená podla obrázku (Obr. 1), ktorá bola použitá aj
v článku.

[!topo](https://github.com/aks-2017/semestralne-zadania-semestralne-zadanie-xjasanj-xslizikm/blob/master/docs/topo.png)

Na vytvorenie premávky v sieti sme použili D-ITG (Distributed Internet Traffic Generator), ktorý nám umožnil vytvoriť kotrolovanú premávku v sieti,
ktorá zodpovedala tej v článku. Ako controler siete sme použili Floodlight, ktorý sa postaral o routing v sieti.

## Využitie Floodlight REST API

Pomocou REST API, ktorú nám ponúka floodlight, sme sa dopytovali na switch a vyberali Rx hodnotu, ktorá nám udávala počet prijatých bitov za sekundu.
Nakoľko priepustnosť sme mali dopredu danú, vedeli sme si z tejto informácie vypočítať ešte dostupnú kapacitu na hrane medzi switchmi.
