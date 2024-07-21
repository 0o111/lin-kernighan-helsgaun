// Umgesetzt in C

// includes für die Einbindung in LKH-3
#include "LKH.h"
#include "Segment.h"

// Funktion zur Prüfung, ob ein geformter Innenwinkel valide ist
static int IsAcute(Node * a, Node * b, Node * c) {
    // schaut, ob es sich um den Dummy Node handelt
    if (a->Id == Dimension || b->Id == Dimension || c->Id == Dimension)
        return 0;
    // schaut, ob das Dotproduct positiv ist
    return (a->X - b->X) * (c->X - b->X) +
           (a->Y - b->Y) * (c->Y - b->Y) > 0;
}

// Funktion, um die Anzahl an invaliden Punkte zu berechnen, die bei einer Bewegung entstehen
GainType Penalty_OpenTSP()
{
    int i, j, AcuteBefore = 0, AcuteAfter = 0;
    for (i = 0; i < Swaps; i++) {
        for (j = 1; j <= 4; j++) {
            // Auswahl der beteiligten Nodes an dem Winkel
            Node *N = j == 1 ? SwapStack[i].t1 :
                      j == 2 ? SwapStack[i].t2 :
                      j == 3 ? SwapStack[i].t3 :
                      j == 4 ? SwapStack[i].t4 : 0;
            // Prüfen, ob die Winkel valide sind
            AcuteBefore += IsAcute(N->OldPred, N, N->OldSuc);
            AcuteAfter  += IsAcute(PREDD(N), N, SUCC(N));
        }
    }
    // Rückgabe entweder der Anzahl der dazugekommenen invaliden Winkel oder 0
    return AcuteAfter > AcuteBefore ? AcuteAfter - AcuteBefore : 0;
}
