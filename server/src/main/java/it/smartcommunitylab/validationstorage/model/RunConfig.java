package it.smartcommunitylab.validationstorage.model;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Entity
public class RunConfig {
    @Id
    @GeneratedValue
    private long id;
    
    private Project project;
    
    private Experiment experiment;
    
    private Run run;
    
    private RunConfigImpl snapshot;
    
    private RunConfigImpl profiling;
    
    private RunConfigImpl schemaInference;
    
    private RunConfigImpl validation;

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public Project getProject() {
        return project;
    }

    public void setProject(Project project) {
        this.project = project;
    }

    public Experiment getExperiment() {
        return experiment;
    }

    public void setExperiment(Experiment experiment) {
        this.experiment = experiment;
    }

    public Run getRun() {
        return run;
    }

    public void setRun(Run run) {
        this.run = run;
    }

    public RunConfigImpl getSnapshot() {
        return snapshot;
    }

    public void setSnapshot(RunConfigImpl snapshot) {
        this.snapshot = snapshot;
    }

    public RunConfigImpl getProfiling() {
        return profiling;
    }

    public void setProfiling(RunConfigImpl profiling) {
        this.profiling = profiling;
    }

    public RunConfigImpl getSchemaInference() {
        return schemaInference;
    }

    public void setSchemaInference(RunConfigImpl schemaInference) {
        this.schemaInference = schemaInference;
    }

    public RunConfigImpl getValidation() {
        return validation;
    }

    public void setValidation(RunConfigImpl validation) {
        this.validation = validation;
    }
}
