package it.smartcommunitylab.validationstorage.typed;

import com.fasterxml.jackson.annotation.JsonValue;

public class DuckDBConstraint extends TypedConstraint {
    /**
     * 
     */
    private static final long serialVersionUID = -2736975852137187090L;

    private String query;
    
    private Expect expect;
    
    private String value;
    
    private Check check;
    
    enum Expect {
        EMPTY("empty"),
        NON_EMPTY("non-empty"),
        EXACT("exact"),
        RANGE("range"),
        MINIMUM("minimum"),
        MAXIMUM("maximum");
        
        public final String label;
        
        private Expect(String label) {
            this.label = label;
        }
        
        @JsonValue
        public String getLabel() {
            return label;
        }
        
    }
    
    enum Check {
        VALUE("value"),
        ROWS("rows");
        
        public final String label;
        
        private Check(String label) {
            this.label = label;
        }
        
        @JsonValue
        public String getLabel() {
            return label;
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

    public Check getCheck() {
        return check;
    }

    public void setCheck(Check check) {
        this.check = check;
    }
    
}
