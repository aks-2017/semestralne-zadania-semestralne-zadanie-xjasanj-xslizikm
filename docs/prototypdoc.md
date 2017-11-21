# Druhý kontrolný bod - Implementácia prototypu

Cieľom vytvorenia nášho prototypu bolo vytvorenie siete, v ktorej sme simulovali tok dát medzi hostmi a následne sme zistovali dostupnú kapacitu. 

## Nastavenie mininetu
Na vytvorenie topologie v mininete sme pouzili skript topo-4sw-5host.py. Topológia bola vytvorená podla obrázku (Obr. 1), ktorá bola použitá aj
v článku.

![topo](https://github.com/aks-2017/semestralne-zadania-semestralne-zadanie-xjasanj-xslizikm/blob/master/docs/topo.png)

Obr. 1 Topológia siete

Na vytvorenie premávky v sieti sme použili D-ITG (Distributed Internet Traffic Generator), ktorý nám umožnil vytvoriť kotrolovanú premávku v sieti,
ktorá zodpovedala tej v článku. Ako controler siete sme použili Floodlight, ktorý sa postaral o routing v sieti.

## Využitie Floodlight REST API

Našim cieľom je zmerať maximálny dostupný bandwith na ceste medzi dvoma hostami. Na tento účel využívame REST API, ktorú Floodlight poskytuje. 
Najskôr cez $ curl -X GET \<controller ip:8080\>/wm/topology/links/json/ získame informáciu o , ktoré v sieti existujú potom pomocou $ curl -X GET \<controller ip:8080\>/wm/device/ zistíme konkretny port a switch ku ktorému je každý host pripojený.
Následne cez $ curl -X GET \<controller ip:8080\>/wm/core/switch/all/flow/json/ zistíme informácie o aktuálnych tokoch v sieti. Príkaz vracia informáciu o premávke medzi hostami, konkrétne cez ktoré switche ide. 
Následne zistíme routy týchto tokov cez $ curl -X GET \<controller ip:8080\>/wm/routing/path/\<src-dpid\>/\<src-port\>/\<dst-dpid\>/\<dst-port\>/json/, kde použijeme vyššie zistené porty a switche ku ktorým su hosty pripojené.

## Výpočet Availiable Bandwith

Výpočet availiable bandwith prebieha dopytovaním countru na switchi, taktiež cez REST API $ curl -X GET \<controller ip:8080\>/wm/statistics/bandwidth/\<switch-dpid\>/\<port-number\>/json/ konkrétne dopytujeme jeden switch z každej linky a na ňom hodnoty rx-bits-per-second a tx-bits-per-second, čo nam v našom prípade, keď sú linky obojsmerné zabezpečí informáciu o aktuálnom loade. A tú len odpočítame od max bandwithu definovaného v mininete a dostaneme availible bandwith
