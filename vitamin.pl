:- dynamic(tanya/1).

% Gejala untuk Vitamin A
gejala(vitamin_a, 'penglihatan malam terganggu').
gejala(vitamin_a, 'kulit kering').
gejala(vitamin_a, 'mata kering').

% Gejala untuk Vitamin B
gejala(vitamin_b, 'mudah lelah').
gejala(vitamin_b, 'sariawan').
gejala(vitamin_b, 'kesemutan').

% Gejala untuk Vitamin C
gejala(vitamin_c, 'gusi berdarah').
gejala(vitamin_c, 'luka lama sembuh').
gejala(vitamin_c, 'mudah memar').

% Diagnosis unik jika minimal 2 gejala cocok
diagnosa_unik(Vitamin) :-
    setof(V, (
        gejala(V, G1), tanya(G1),
        gejala(V, G2), tanya(G2),
        G1 \= G2
    ), List),
    member(Vitamin, List).
