package it.smartcommunitylab.validationstorage.model;

import java.util.List;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;

import org.springframework.data.annotation.Id;

@Entity
public class Run {
    @Id
    @GeneratedValue
    private long id;
    
    private String name;
    
    private String title;
    
    private Project project;
    
    private Experiment experiment;
    
    private DataPackage dataPackage;
    
    private RunConfig runConfig;
    
    private List<Constraint> constraints;
    
    private List<ArtifactMetadata> artifactMetadata;
    
    private DataProfile dataProfile;
    
    private DataResource dataResource;
    
    private RunEnvironment runEnvironment;
    
    private RunMetadata runMetadata;
    
    private ShortReport shortReport;
    
    private ShortSchema shortSchema;

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
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

    public DataPackage getDataPackage() {
        return dataPackage;
    }

    public void setDataPackage(DataPackage dataPackage) {
        this.dataPackage = dataPackage;
    }

    public RunConfig getRunConfig() {
        return runConfig;
    }

    public void setRunConfig(RunConfig runConfig) {
        this.runConfig = runConfig;
    }

    public List<Constraint> getConstraints() {
        return constraints;
    }

    public void setConstraints(List<Constraint> constraints) {
        this.constraints = constraints;
    }

    public List<ArtifactMetadata> getArtifactMetadata() {
        return artifactMetadata;
    }

    public void setArtifactMetadata(List<ArtifactMetadata> artifactMetadata) {
        this.artifactMetadata = artifactMetadata;
    }

    public DataProfile getDataProfile() {
        return dataProfile;
    }

    public void setDataProfile(DataProfile dataProfile) {
        this.dataProfile = dataProfile;
    }

    public DataResource getDataResource() {
        return dataResource;
    }

    public void setDataResource(DataResource dataResource) {
        this.dataResource = dataResource;
    }

    public RunEnvironment getRunEnvironment() {
        return runEnvironment;
    }

    public void setRunEnvironment(RunEnvironment runEnvironment) {
        this.runEnvironment = runEnvironment;
    }

    public RunMetadata getRunMetadata() {
        return runMetadata;
    }

    public void setRunMetadata(RunMetadata runMetadata) {
        this.runMetadata = runMetadata;
    }

    public ShortReport getShortReport() {
        return shortReport;
    }

    public void setShortReport(ShortReport shortReport) {
        this.shortReport = shortReport;
    }

    public ShortSchema getShortSchema() {
        return shortSchema;
    }

    public void setShortSchema(ShortSchema shortSchema) {
        this.shortSchema = shortSchema;
    }
}
