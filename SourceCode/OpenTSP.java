// Umgesetzt in Java

// imports für benötigte externe Pakete
import java.io.File;
import java.util.Scanner;
import java.util.Random;

// Definierung der Hauptprogrammklasse
public class OpenTSP {

    // Definierung (+Initialisierung) wichtiger Konstanten und Variablen
    static final int RUNS = 100;

    static double tourLength, bestTourLength = Double.MAX_VALUE;
    static int bestAcuteAngles = Integer.MAX_VALUE;
    static int n;
    static double[] x, y;
    static double dist[][];
    static int[] tour, bestTour, index;
    static boolean[] dontLook;
    static Random rand = new Random();

    // Funktion zur Berechnung der Entfernung zweier Punkte
    static double edgeLength(double x1, double y1, double x2, double y2) {
        return Math.hypot(x1 - x2, y1 - y2);
    }

    // Funktion, die die Entfernung zweier Punkte wiedergibt, entweder aus der abgespeicherten Matrix oder neu berechnet
    static double length(int i, int j) {
        if (dist != null)
            return dist[i][j];
        if (i == n - 1 || j == n - 1)
            return 0.0;
        return edgeLength(x[i], y[i], x[j], y[j]);
    }

    // Funktion, die die Gesamtlänge einer Tour berechnet und wiedergibt
    static double tourLength() {
        double sum = length(tour[n - 1], tour[0]);
        for (int i = 1; i < n; i++)
            sum += length(tour[i - 1], tour[i]);
        return sum;
    }

    // Funktion, die die Anzahl an invaliden Innenwinkel zählt
    static int acuteAngles() {
        int acuteAngles = 0;
        for (int i = 0; i < n; i++)
            if (isAcute(prev(i), i, next(i)))
                acuteAngles++;
        return acuteAngles;
    }

    // Funktion, die zufällig einen Rundweg erzeugt
    static void createRandomTour() {
        for (int i = 0; i < n; i++)
            index[tour[i] = i] = i;
        for (int i = 1; i < n; i++)
            swap(i, rand.nextInt(i));
    }

    // Funktion, die den Vorgänger eines Punktes in dem Rundweg wiedergibt
    static int prev(int v) {
        return tour[index[v] > 0 ? index[v] - 1 : n - 1];
    }

    // Funktion, die den Nachfolger eines Punktes in dem Rundweg wiedergibt
    static int next(int v) {
        return tour[index[v] < n - 1 ? index[v] + 1 : 0];
    }

    // Funktion, die zwei Punkte des Rundwegs vertauscht
    static void swap(int i, int j) {
        int temp = tour[i];
        index[tour[i] = tour[j]] = i;
        index[tour[j] = temp] = j;
    }

    // Funktion, die einen Abschnitt des Rundwegs dreht
    static void flip(int b, int d) {
        int i = index[b], j = index[d];
        while (i != j) {
            swap(i, j);
            if (++i == n) i = 0;
            if (i != j && --j < 0)
                j = n - 1;
        }
    }

    // Funktion, die prüft, ob ein Innenwinkel valide ist
    static boolean isAcute(int a, int b, int c) {
        // falls der Dummy Node dabei ist, ist der Winkel immer valide
        if (a == n - 1 || b == n - 1 || c == n - 1)
            return false;
        // prüft, ob das Dotproduct positiv ist
        return (x[a] - x[b]) * (x[c] - x[b]) +
               (y[a] - y[b]) * (y[c] - y[b]) > 0;
    }

    // Lösungsfunktion, die den 2h-opt Algorithmus implementiert
    static void twohOpt() {
        tourLength = tourLength();
        int failures = 0, b = -1;
        int bestAcuteAngles = Integer.MAX_VALUE;

        // Schleife solange es Verbesserungsmöglichkeiten gibt
        while (failures++ < n) {
            if (++b == n)
                b = 0;
            // Initialisierung der Don't Look Bits
            if (dontLook[b])
                continue;
            dontLook[b] = true;
            // Initlialisierung der beteiligten Punkte für eine Bewegung
            int a = prev(b), c = next(b), d;
            while ((d = c) != prev(a)) {
                c = next(d);

                // erste Möglichkeit die Knoten wiederzuverbinden
                // Berechnung der invaliden Winkel vor der Bewegung
                int acuteBeforeA =
                    (isAcute(prev(a), a, b) ? 1 : 0) +
                    (isAcute(a, b, next(b)) ? 1 : 0) +
                    (isAcute(d, c, next(c)) ? 1 : 0) +
                    (isAcute(prev(d), d, c) ? 1 : 0);
                // Berechnung der invaliden Winkel nach der Bewegung
                int acuteAfter =
                    (isAcute(d, a, prev(a)) ? 1 : 0) +
                    (isAcute(c, b, next(b)) ? 1 : 0) +
                    (isAcute(b, c, next(c)) ? 1 : 0) +
                    (isAcute(a, d, prev(d)) ? 1 : 0);
                // Bedingung, ob der Rundweg aktualisiert werden soll
                if (acuteAfter <= acuteBeforeA) {
                    // hierfür Berechnung des Gain in Bezug auf die Weglänge
                    double gain = length(a, b) + length(c, d) -
                                  length(a, d) - length(b, c);
                    if (acuteAfter < acuteBeforeA ||
                            (acuteAfter == acuteBeforeA &&
                             tourLength - gain < tourLength)) {
                        flip(b, d); // Ausführen der Bewegung
                        tourLength -= gain;
                        dontLook[a] = dontLook[b] = dontLook[c] =
                                                        dontLook[d] = false;
                        failures = 0; // Zurücksetzen von failures
                        if (false)
                            System.out.printf("A: %d %1.2f\n",
                                              acuteAngles(), tourLength);
                        break;
                    }
                }
                // Weiterverschieben der Variablen zu den nächsten Punkten
                int e = next(c);
                if (e == a)
                    continue;

                // zweite Möglichkeit die Knoten wiederzuverbinden - analog zur ersten
                int acuteBeforeB = acuteBeforeA +
                                   (isAcute(c, e, next(e)) ? 1 : 0);
                acuteAfter =
                    (isAcute(prev(a), a, c) ? 1 : 0) +
                    (isAcute(c, b, next(b)) ? 1 : 0) +
                    (isAcute(b, c, a) ? 1 : 0) +
                    (isAcute(prev(d), d, e) ? 1 : 0) +
                    (isAcute(d, e, next(e)) ? 1 : 0);
                if (acuteAfter <= acuteBeforeB) {
                    double gain = length(a, b) + length(d, c) + length(c, e) -
                                  length(a, c) - length(b, c) - length(d, e);
                    if (acuteAfter < acuteBeforeB ||
                            (acuteAfter == acuteBeforeB &&
                             tourLength - gain < tourLength)) {
                        flip(b, d);
                        flip(e, a);
                        tourLength -= gain;
                        dontLook[a] = dontLook[b] = dontLook[c] =
                                                        dontLook[d] = dontLook[e] = false;
                        failures = 0;
                        if (false)
                            System.out.printf("B: %d %1.2f\n",
                                              acuteAngles(), tourLength);
                        break;
                    }
                }

                // zweite Möglichkeit die Knoten wiederzuverbinden - analog zur ersten
                e = prev(a);
                if (e == next(c))
                    continue;
                int acuteBeforeC = acuteBeforeA +
                                   (isAcute(prev(e), e, a) ? 1 : 0);
                acuteAfter =
                    (isAcute(d, a, c) ? 1 : 0) +
                    (isAcute(e, b, next(b)) ? 1 : 0) +
                    (isAcute(a, c, next(c)) ? 1 : 0) +
                    (isAcute(a, d, prev(d)) ? 1 : 0) +
                    (isAcute(prev(e), e, b) ? 1 : 0);
                if (acuteAfter <= acuteBeforeC) {
                    double gain = length(a, b) + length(d, c) + length(e, a) -
                                  length(d, a) - length(a, c) - length(e, b);
                    if (acuteAfter < acuteBeforeC ||
                            (acuteAfter == acuteBeforeC &&
                             tourLength - gain < tourLength)) {
                        flip(b, d);
                        flip(c, e);
                        tourLength -= gain;
                        dontLook[a] = dontLook[b] = dontLook[c] =
                                                        dontLook[d] = dontLook[e] = false;
                        failures = 0;
                        if (false)
                            System.out.printf("C: %d %1.2f\n",
                                              acuteAngles(), tourLength);

                        break;
                    }
                }
            }
        }
    }

    // Lösungsfunktion, die den 2-opt Algorithmus implementiert - analog zu 2h-opt nur, dass auschließlich eine Möglichkeit zur Wiederverbindung vorliegt
    static void twoOpt() {
        tourLength = tourLength();
        int failures = 0, b = -1;
        while (failures++ < n) {
            if (++b == n)
                b = 0;
            if (dontLook[b])
                continue;
            dontLook[b] = true;
            int a = prev(b), c = next(b), d;
            while ((d = c) != prev(a)) {
                c = next(d);
                int acuteBefore =
                    (isAcute(prev(a), a, b) ? 1 : 0) +
                    (isAcute(a, b, next(b)) ? 1 : 0) +
                    (isAcute(d, c, next(c)) ? 1 : 0) +
                    (isAcute(prev(d), d, c) ? 1 : 0);
                int acuteAfter =
                    (isAcute(d, a, prev(a)) ? 1 : 0) +
                    (isAcute(c, b, next(b)) ? 1 : 0) +
                    (isAcute(b, c, next(c)) ? 1 : 0) +
                    (isAcute(a, d, prev(d)) ? 1 : 0);
                if (acuteAfter > acuteBefore)
                    continue;
                double gain = length(a, b) + length(c, d) -
                              length(a, d) - length(b, c);
                if (acuteAfter < acuteBefore ||
                        (acuteAfter == acuteBefore &&
                         tourLength - gain < tourLength)) {
                    flip(b, d);
                    tourLength -= gain;
                    dontLook[a] = dontLook[b] = false;
                    dontLook[c] = dontLook[d] = false;
                    failures = 0;
                    if (false)
                        System.out.printf("%d %1.2f\n", acuteAngles(), tourLength);
                    break;
                }
            }
        }
    }

    // Funktion zum Einlesen der Daten
    static void readInstance(String fileName) throws Exception {
        Scanner scan = new Scanner(new File(fileName));
        n = scan.nextInt();
        x = new double[n];
        y = new double[n];
        for (int i = 0; i < n; i++) {
            x[i] = scan.nextDouble();
            y[i] = scan.nextDouble();
        }
    }

    // main-Funktion
    public static void main(String[] args) throws Exception {
        long startTime = System.currentTimeMillis();
        readInstance(args[0]);
        // Berechnung der Kostenmatrix
        if (n <= 20000) {
            dist = new double[n][n];
            for (int i = 0; i < n - 1; i++)
                for (int j = i + 1; j < n - 1; j++)
                    dist[i][j] = dist[j][i] =
                                     edgeLength(x[i], y[i], x[j], y[j]);
        }
        tour = new int[n];
        bestTour = new int[n];
        index = new int[n];
        for (int run = 1; run <= RUNS; run++) { // Schleife, die die Anzahl an Durchläufen mit neuen Starttouren angibt
            createRandomTour();
            dontLook = new boolean[n];

            twohOpt(); // Aufrufen der Lösungsfunktion

            // Aktualisierung des besten rundwegs falls notwendig
            int acuteAngles = acuteAngles();
            if (acuteAngles < bestAcuteAngles ||
                    (acuteAngles == bestAcuteAngles &&
                     tourLength < bestTourLength)) {
                bestAcuteAngles = acuteAngles;
                bestTourLength = tourLength;
                System.arraycopy(tour, 0, bestTour, 0, n);
                System.out.printf("%d: Acute angles = %d, Length = %1.2f\n",
                                  run, bestAcuteAngles, bestTourLength);
            }
        }
        // Ausgabe der besten Lösung ohne den Dummy Node
        System.out.print("Path: ");
        int dummyIndex;
        for (dummyIndex = 0;  dummyIndex < n; dummyIndex++)
            if (bestTour[dummyIndex] == n - 1)
                break;
        for (int i = dummyIndex + 1; i < n; i++)
            System.out.print(bestTour[i] + 1 + " ");
        for (int i = 0; i < dummyIndex; i++)
            System.out.print(bestTour[i] + 1 + " ");
        System.out.println();

        System.out.printf("Length = %1.2f\n", bestTourLength);
        System.out.printf("Acute angles = %d\n", bestAcuteAngles);
        System.out.printf("Time used = %1.2f seconds\n",
                          (System.currentTimeMillis() - startTime) / 1000.0);
    }
}

