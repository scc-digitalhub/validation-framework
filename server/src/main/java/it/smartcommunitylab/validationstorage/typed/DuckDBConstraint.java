package it.smartcommunitylab.validationstorage.typed;

import com.fasterxml.jackson.annotation.JsonValue;

public class DuckDBConstraint extends TypedConstraint {
    private String query;
    
    private Expect expect;
    
    private String value;
    
    enum Expect {
        EMPTY("empty"),
        NON_EMPTY("nonEmpty"),
        EXACT("exact"),
        RANGE("range");
        
        public final String label;
        
        private Expect(String label) {
            this.label = label;
        }
        
        @JsonValue
        public String getLabel() {
            return label;
        }
        
        public static Expect fromString(String s) {
            for (Expect e : Expect.values()) {
                if (e.label.equalsIgnoreCase(s)) {
                    return e;
                }
            }
            
            throw new IllegalArgumentException("Expect: '" + s + "' is not supported.");
        }
        
    }
    
    public String getQuery() {
        return query;
    }

    public void setQuery(String query) {
        this.query = query;
    }

    public Expect getExpect() {
        return expect;
    }

    public void setExpect(Expect expect) {
        this.expect = expect;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }
    
}
