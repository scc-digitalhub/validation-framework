package it.smartcommunitylab.validationstorage.model;

public class DuckDBConstraint extends TypedConstraint {
    private String query;
    
    private Expect expect;
    
    private String value;
    
    enum Expect {
        empty,
        nonEmpty,
        exact,
        range
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
