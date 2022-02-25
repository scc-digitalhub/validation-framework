package it.smartcommunitylab.validationstorage.model.dto;

import java.util.List;

public class SchemaResultDTO {
    private String result;
    
    private List<RunDataSchemaDTO> reports;

    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }

    public List<RunDataSchemaDTO> getReports() {
        return reports;
    }

    public void setReports(List<RunDataSchemaDTO> reports) {
        this.reports = reports;
    }
    
}
