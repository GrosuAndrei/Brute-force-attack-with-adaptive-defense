Pentru rularea proiectului

1) Să se descarce fișierele authentication.py config.py defense.py main.py passwords.txt și storage.py în același director
2) Se deschide un command prompt în directorul unde au fost descărcate fișierele
3) Se rulează din terminal comanda: python main.py

Se va afișa următoarea secvență

**** MENIU ****
1. Login (cu aparare)
2. Login (fara aparare)
3. Brute force (cu aparare)
4. Brute force (fara aparare)
5. Wordlist (cu aparare)
6. Wordlist (fara aparare)
7. Reset logs
0. Exit
Alege:

după selectarea opțiunilor 1-6 se va cere introducerea unui nume de utilizator

În baza de date există 2 utilizatori andrei și admin

parole setate: 

andrei - daniel1

admin - mic

opțiunile
1 și 2 simulează autentificarea clasică a unui utilizator, parola se introduce manual

********************************** IMPORTANT ****************************************

*** 3 și 4 simulează atacul Brute force clasic, pentru aceste variante selectați utilizatorul admin 

*** 5 și 6 simulează atacul Brute force după o listă de parole aflat în passwords.txt,  pentru aceste variante selectați utilizatorul andrei

*************************************************************************************

7 Șterge conținutul tabelei logs și permite deblocarea unui IP blocat deja de mecanismul de apărare.

0 Finalizează execuția prograului


Pentru schimbarea adresei IP utilizate în simulare se modifică DEFAULT_ATTACKER_IP din config.py
Dacă este selectat IP-ul 10.0.0.66 - acesta va fi restricționat regional

Pentru vizualizarea tabelei logs poate fi utilizat DB browser for SQLite.

Rezultatele obținute în cadrul testării funcționalităților sunt prezentate în documentul rezultate.docx
