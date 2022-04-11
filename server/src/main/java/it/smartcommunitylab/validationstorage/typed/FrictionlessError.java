package it.smartcommunitylab.validationstorage.typed;

public class FrictionlessError extends TypedError {
    
    /**
     * 
     */
    private static final long serialVersionUID = 642218210469996635L;

    private String fieldName;
    
    private int rowNumber;
    
    private String description;

    public String getFieldName() {
        return fieldName;
    }

    public void setFieldName(String fieldName) {
        this.fieldName = fieldName;
    }

    public int getRowNumber() {
        return rowNumber;
    }

    public void setRowNumber(int rowNumber) {
        this.rowNumber = rowNumber;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

}
