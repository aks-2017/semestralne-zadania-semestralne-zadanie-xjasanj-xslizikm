Semestrálne zadanie z predmetu distrubúcia obsahu v internete

Vypracovali: Jakub Jasaň, Miloslav Slížik

Štruktúra repozitáru:

/docs - obsahuje dokument s analýzou článku a návrhom spôsobu, akým chceme zopakovať výsledky z článku\
/prototyp/host - obsahuje súbory, ktoré je potrebné mať na Host PC\
/prototyp/mininetVM - obsahuje súbory, ktoré je potrebné mať vo VM, kde beží mininet\
D-ITG - program na generovanie network traffic, nakoniec sme miesto neho použili iperf, ktorý je integrovaný v mininete,\
        pretože D-ITG nevedelo poslať presne taký traffic ako sme chceli.

Dependencies projektu:\
Program bol pisaný na Linuxe a jeho jediná externá závislosť okrem Mininetu a SDN controlleru je python.\
Na linuxových distribúciach s aptitutde package managerom sa inštaluje commandom : $ sudo apt install python-minimal\
Ako SDN controller je použitý floodlight, ktorý je dostupný cez github : https://github.com/floodlight/floodlight \
konkrétne pre tento projekt sme použili master branch.\
Návod na inštaláciu a spustenie floodlightu môžte nájsť na: https://floodlight.atlassian.net/wiki/spaces/floodlightcontroller/pages/1343544/Installation+Guide \

Floodlight je potrebné nainštalovať na host PC. \

Testovacia topologia z článku je pripravená v /prototyp/mininetVM/topo-2sw-2host.py \

mininet je potrebné spustiť príkazom: $ sudo mn --controller remote,ip="ip stroja kde bezi floodlight",port=6653 --custom  "/path/to/topology" --topo mytopo --link tc --mac \

Následne je možné spustiť na host stroji python skript ABW.py s vybranými prepínačmi a začne merať available bandwidth v sieti.

