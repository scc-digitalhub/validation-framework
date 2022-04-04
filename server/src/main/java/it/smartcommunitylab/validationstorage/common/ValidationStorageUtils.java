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
        if (id1 != null && id2 != null && !id1.equals(id2))
            throw new IdMismatchException("There is a mismatch between project/experiment/run indicated in the document and the equivalent value specified in the path or parent document.");
    }
}