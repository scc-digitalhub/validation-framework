package it.smartcommunitylab.validationstorage.model;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Embeddable;

@Embeddable
public class ReportMetadata implements Serializable {
    /**
     * 
     */
    private static final long serialVersionUID = -2030656080790315543L;

    @Column(name = "datajudge_version")
    private String datajudgeVersion;
    
    @Column(name = "library_name")
    private String libraryName;
    
    @Column(name = "library_version")
    private String libraryVersion;
    
    private Integer duration;

    public String getDatajudgeVersion() {
        return datajudgeVersion;
    }

    public void setDatajudgeVersion(String datajudgeVersion) {
        this.datajudgeVersion = datajudgeVersion;
    }

    public String getLibraryName() {
        return libraryName;
    }

    public void setLibraryName(String libraryName) {
        this.libraryName = libraryName;
    }

    public String getLibraryVersion() {
        return libraryVersion;
    }

    public void setLibraryVersion(String libraryVersion) {
        this.libraryVersion = libraryVersion;
    }

    public Integer getDuration() {
        return duration;
    }

    public void setDuration(Integer duration) {
        this.duration = duration;
    }
}
