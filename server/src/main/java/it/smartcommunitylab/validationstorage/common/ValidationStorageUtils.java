package it.smartcommunitylab.validationstorage.common;

import java.text.Normalizer;

/**
 * Various constants and utility methods used throughout the application are grouped here.
 */
public class ValidationStorageUtils {
    /**
     * Converts string to lower case, removes accents and other diacritics.
     * 
     * @param input String to normalize.
     * @return Result of input normalization.
     */
    public static String normalizeString(String input) {
        return Normalizer.normalize(input.toLowerCase(), Normalizer.Form.NFKD).replaceAll("\\p{InCombiningDiacriticalMarks}+", "");
    }
    
    public static void checkIdMatch(String id1, String id2) {
        if (!id1.equals(id2))
            throw new IdMismatchException("The project/experiment ID specified in the path does not match the equivalent field in the document.");
    }
}