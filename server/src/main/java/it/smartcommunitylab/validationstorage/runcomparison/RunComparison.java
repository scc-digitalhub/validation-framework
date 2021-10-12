package it.smartcommunitylab.validationstorage.runcomparison;

import java.util.List;

import lombok.Getter;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class RunComparison {
    @NonNull
    private String id;
    
    @NonNull
    private String projectId;
    
    @NonNull
    private String experimentId;
    
    @NonNull
    private String[] comparedRunMetadataIds;
    
    @NonNull
    private List<RunSummary> runs;
    
}