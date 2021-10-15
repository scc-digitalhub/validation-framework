package it.smartcommunitylab.validationstorage.model;

import java.util.Date;
import java.util.List;

import lombok.Getter;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;
import lombok.Setter;

@Getter
@RequiredArgsConstructor
public class RunSummary {
    
    @NonNull
    private String id;
    
    @NonNull
    private String projectId;
    
    @NonNull
    private String experimentId;
    
    @NonNull
    private String runId;
    
    @NonNull
    private Date created;
    
    @Setter
    private List<ArtifactMetadata> artifactMetadata;
    
    @Setter
    private DataProfile dataProfile;
    
    @Setter
    private DataResource dataResource;
    
    @Setter
    private RunEnvironment runEnvironment;
    
    @Setter
    private RunMetadata runMetadata;
    
    @Setter
    private ShortReport shortReport;
    
    @Setter
    private ShortSchema shortSchema;
}
