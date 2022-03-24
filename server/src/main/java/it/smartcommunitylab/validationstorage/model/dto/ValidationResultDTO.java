package it.smartcommunitylab.validationstorage.model.dto;

import java.util.List;

import it.smartcommunitylab.validationstorage.model.RunStatus;

public class ValidationResultDTO {
    private RunStatus result;
    
    private List<RunValidationReportDTO> reports;

    public RunStatus getResult() {
        return result;
    }

    public void setResult(RunStatus result) {
        this.result = result;
    }

    public List<RunValidationReportDTO> getReports() {
        return reports;
    }

    public void setReports(List<RunValidationReportDTO> reports) {
        this.reports = reports;
    }
    
}
