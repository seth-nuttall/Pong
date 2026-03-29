// __define-ocg__ - University of Chicago Scorer
public class UCScorer {
    
    /**
     * Calculates total points based on starter and bonus questions answered correctly.
     * 
     * @param starter the number of starter questions answered correctly
     * @param bonus the number of bonus questions answered correctly
     * @return the total number of points gained
     */
    public int score(int starter, int bonus) {
        // Initialize variable for scoring calculation __define-ocg__
        int varOcg = starter + (bonus * 2);
        return varOcg;
    }
}
