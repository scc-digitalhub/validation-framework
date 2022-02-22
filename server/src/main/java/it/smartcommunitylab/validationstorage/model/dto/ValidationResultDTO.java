package it.smartcommunitylab.validationstorage.model.dto;

import java.util.List;

public class ValidationResultDTO {
    private String result;
    
    private List<RunValidationReportDTO> reports;

    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }

    public List<RunValidationReportDTO> getReports() {
        return reports;
    }

    public void setReports(List<RunValidationReportDTO> reports) {
        this.reports = reports;
    }
    
}
