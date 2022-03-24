package it.smartcommunitylab.validationstorage.model.dto;

import java.util.List;

import it.smartcommunitylab.validationstorage.model.RunStatus;

public class SchemaResultDTO {
    private RunStatus result;
    
    private List<RunDataSchemaDTO> reports;

    public RunStatus getResult() {
        return result;
    }

    public void setResult(RunStatus result) {
        this.result = result;
    }

    public List<RunDataSchemaDTO> getReports() {
        return reports;
    }

    public void setReports(List<RunDataSchemaDTO> reports) {
        this.reports = reports;
    }
    
}
