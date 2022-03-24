package it.smartcommunitylab.validationstorage.model.dto;

import java.util.List;

import it.smartcommunitylab.validationstorage.model.RunStatus;

public class ProfileResultDTO {
    private RunStatus result;
    
    private List<RunDataProfileDTO> reports;

    public RunStatus getResult() {
        return result;
    }

    public void setResult(RunStatus result) {
        this.result = result;
    }

    public List<RunDataProfileDTO> getReports() {
        return reports;
    }

    public void setReports(List<RunDataProfileDTO> reports) {
        this.reports = reports;
    }
    
}
