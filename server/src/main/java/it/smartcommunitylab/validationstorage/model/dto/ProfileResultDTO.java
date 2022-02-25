package it.smartcommunitylab.validationstorage.model.dto;

import java.util.List;

public class ProfileResultDTO {
    private String result;
    
    private List<RunDataProfileDTO> reports;

    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }

    public List<RunDataProfileDTO> getReports() {
        return reports;
    }

    public void setReports(List<RunDataProfileDTO> reports) {
        this.reports = reports;
    }
    
}
