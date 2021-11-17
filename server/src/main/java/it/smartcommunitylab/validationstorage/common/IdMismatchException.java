package it.smartcommunitylab.validationstorage.common;

public class IdMismatchException extends RuntimeException{

    /**
     * Auto-generated ID.
     */
    private static final long serialVersionUID = 1L;
    
    public IdMismatchException() {
        this("Specified project ID does not match the value contained in the document.");
    }

    public IdMismatchException(String message) {
        super(message);
    }
}
